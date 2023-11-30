#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""
**mcfonts** is a versatile, fast, and extensible package for working with Minecraft fonts.

mcfonts works with any valid font JSON and can export every kind of texture and sizing.

| For more information, see `<https://gitlab.com/whoatemybutter/mcfonts/>`_.
| Read the documentation online at `<https://mcfonts.rtfd.io>`_.

----

| Licensed under the MIT license, see https://choosealicense.com/licenses/mit/ for details.
| Formatted with Black, see https://github.com/psf/black.
| Checked with Pylint, see https://pylint.org/.
"""
from __future__ import annotations

import collections.abc
import json
import logging
import math
import os
import os.path
import pathlib
import shutil
import sys
import tempfile
import typing
import warnings
import zipfile

import PIL.Image
import tinyunicodeblock
import unirange

import mcfonts.compacting
import mcfonts.constants
import mcfonts.coverage_reports
import mcfonts.exceptions
import mcfonts.export_formats
import mcfonts.filters
import mcfonts.glyphs
import mcfonts.providers.base
import mcfonts.providers.bitmap
import mcfonts.providers.legacy_unicode
import mcfonts.providers.reference
import mcfonts.providers.space
import mcfonts.providers.ttf
import mcfonts.providers.unihex
import mcfonts.utils
import mcfonts.utils.importing
import mcfonts.utils.resources

__author__ = mcfonts.constants.AUTHOR
__version__ = mcfonts.constants.VERSION
__license__ = mcfonts.constants.LICENSE

if sys.version_info < (3, 11, 0):
    raise RuntimeError(f"minimum Python version is 3.11.0, you are running {sys.version.split(' ', 1)[0]}")

# Decompression bombs will error, as they should
warnings.simplefilter("error", PIL.Image.DecompressionBombWarning)

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="[%(relativeCreated)d] [%(name)s/%(levelname)s]: (at %(funcName)s()) %(message)s",
)


class MinecraftFont:
    """
    The MinecraftFont class.

    Requires the providers of a provider file, and the associated resources mapping.

    You should never instantiate this class directly.
    Use :mod:`mcfonts.importing`.

    If you need to add, modify, or remove providers, do it through :attr:`self.providers`;
    it's a list of Provider classes, each containing relevant fields and methods.

    Be sure to run :meth:`mcfonts.MinecraftFont.validate` after making any changes;
    it won't be done automatically.

    .. warning::
        If more than one :class:`mcfonts.providers.OptionsProvider` is present in `provider_list`,
        only the **last** one will be used.

    :param provider_list:
        A list of providers, all of which are instances of :data:`mcfonts.providers.base.Provider`.
    :param is_monochrome:
        Whether font resources are loaded in grayscale or not.
        Default is True.
    """

    def __init__(
        self,
        provider_list: list[mcfonts.providers.base.Provider],
        is_monochrome: bool = True,
    ):
        self.providers = provider_list
        """Do not iterate over this! Use :meth:`yield_providers` instead."""
        self.is_monochrome = is_monochrome

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.providers}, {self.is_monochrome})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __hash__(self) -> int:
        return hash((self.providers, self.is_monochrome))

    def __add__(self, other: MinecraftFont) -> MinecraftFont:
        return MinecraftFont(self.providers, self.is_monochrome) + other

    def __iadd__(self, other: MinecraftFont) -> MinecraftFont:
        self.providers += other.providers
        if other.is_monochrome is False:
            self.is_monochrome = False
        self.validate()
        return self

    def __len__(self) -> int:
        return len(list(self.yield_characters()))

    def export(
        self,
        export_format: collections.abc.Callable[
            [dict[str, mcfonts.glyphs.Glyph], mcfonts.export_formats.ExportSettings], bytes
        ],
        settings: mcfonts.export_formats.ExportSettings | None = None,
        filter_instance: mcfonts.filters.Filter | None = None,
    ) -> bytes:
        """
        Export this Minecraft font to another format.
        See available formats at :const:`mcfonts.export_formats.EXPORT_FORMATS_MAP`.

        :param export_format:
            The function to pass glyphs and settings to.
            Look in :mod:`mcfonts.export_formats` for a list of the functions you can pass.
            Also accepts a string of the format name (see :const:`mcfonts.export_formats.EXPORT_FORMATS_MAP`).
        :param settings:
            A dictionary of the needed parameters to attach to the exported font.
            See :class:`mcfonts.export_formats.ExportSettings`.
        :param filter_instance:
            An optional instance of :class:`mcfonts.filters.Filter`.
            If supplied, filter rules will be obeyed.
        :returns: The exported data in the specified format that can be written to a file and saved.
        """
        cached_glyphs: dict[str, mcfonts.glyphs.Glyph] = {}
        num_providers = 0
        for provider in self.yield_providers():
            if filter_instance and filter_instance.check_provider(provider.__class__):
                logger.info(f"Skipping provider {num_providers + 1:,} {provider.pretty_print()} (filtered)")
                continue
            for character, glyph in provider.yield_glyphs():
                if mcfonts.utils.unicode.is_codepoint_surrogate(ord(character)) or (
                    filter_instance and filter_instance.check_character(character)
                ):  # Don't include surrogates or filtered characters.
                    continue
                if glyph:
                    cached_glyphs[character] = glyph
            num_providers += 1
        return export_format(
            cached_glyphs,
            settings
            or {
                "name": None,
                "author": None,
                "license": None,
                "include_credits": None,
            },
        )

    def yield_providers(
        self, unwind_reference_children: bool = True
    ) -> collections.abc.Iterable[mcfonts.providers.base.Provider]:
        """
        Yield the providers in this font.

        By default, this will unpack reference providers and yield its children instead.
        Reference providers will never yield the same referenced font twice if `unwind_reference_children` is True.

        :param unwind_reference_children:
            Whether to yield a reference provider's children instead of the reference provider plainly.
            Usually, this is a good idea.
            This also prevents the same font from being yielded twice.
        :returns: A yield of Provider.
        """
        referenced_providers: list[str] = []
        for provider in self.providers:
            if isinstance(provider, mcfonts.providers.reference.ReferenceProvider) and unwind_reference_children:
                assert isinstance(provider, mcfonts.providers.reference.ReferenceProvider)
                # Reference providers require no duplication, so store each font ID and check it.
                if (referenced := provider.contents["id"]) in referenced_providers:
                    # It's already been yielded, ignore it now.
                    continue
                # Not yielded yet.
                referenced_providers.append(referenced)
                yield from provider.yield_children()
            else:
                yield provider

    def yield_characters(self) -> collections.abc.Iterable[str]:
        """
        Yield all the characters this font covers and has a definition for.

        .. note:: Any character in :const:`mcfonts.constants.PADDING_CHARS` isn't counted.

        :returns: A yield of strings of individual characters.
        """
        for provider in self.yield_providers():
            yield from provider.yield_characters()

    def save(self, indent: int | str | None = "\t") -> None:
        """
        Recursively write all providers to their original file locations.

        This is different from exporting.
        The file is indented by default.

        .. warning:: Not to be confused with :meth:`MinecraftFont.export`.

        .. warning:: Doesn't save resources.

        :param indent:
            The indentation level, refer to :func:`json.dump()` for possible values.
        """
        origin_cache: dict[str, list[mcfonts.utils.types.TypedProviderDict]] = {}
        providers_total: list[mcfonts.providers.base.Provider] = []
        for wound_provider in self.yield_providers(False):
            providers_total.append(wound_provider)
            if isinstance(wound_provider, mcfonts.providers.reference.ReferenceProvider):
                providers_total.extend(wound_provider.yield_children())

        for provider in providers_total:
            if (origin_str := str(provider.origin)) not in origin_cache:
                origin_cache[origin_str] = []
            origin_cache[origin_str].append(provider.get_contents())

        for path, contents in origin_cache.items():
            with open(path, "w+", encoding="utf-8") as open_path:
                json.dump({"providers": contents}, open_path, ensure_ascii=False, indent=indent)

    def count_providers(self) -> dict[str, int]:
        """
        Return a counted summary of the providers this font contains.

        This is future-proof, and will work with any provider as long as it has a "type" key.

        :returns: A summary of font's providers.
        """
        result = {}
        for provider in self.yield_providers():
            if (provider_type := provider.provider_type) not in result:
                result[provider_type] = 1
            else:
                result[provider_type] += 1
        return result

    def count_providers_total(self) -> int:
        """
        Count the number of providers in the font.

        :returns: Number of providers.
        """
        return len(self.count_providers())

    def print_info(self, table_chars: bool = True, summary_only: bool = False) -> None:
        """
        Print basic information about the font.

        :param table_chars:
            Whether to print a 'chars' list as a square table, or as a simple string.
            This only applies to :class:`mcfonts.providers.BitmapProvider`.
        :param summary_only:
            If True, will only print the number of characters and providers.
        """
        if not summary_only:
            for provider in self.yield_providers():
                if isinstance(provider, mcfonts.providers.bitmap.BitmapProvider):
                    assert isinstance(provider, mcfonts.providers.bitmap.BitmapProvider)
                    provider.print_info(table_chars)
                else:
                    provider.print_info()
            print("\n")
        print(f"Characters: {len(list(self.yield_characters())):,}")
        print(f"Providers: {self.count_providers_total():,}")

    def validate(self) -> None:
        """Run basic structure checks on the providers of the font JSON."""
        if len(self.providers) < 1:
            logger.warning("There are no providers.")
        for provider in self.yield_providers():
            if isinstance(provider, mcfonts.providers.base.Provider):
                provider.validate()
            else:
                raise mcfonts.exceptions.ProviderError(
                    mcfonts.providers.base.format_provider_message(provider, "is not a valid provider.")
                )

    def compact(
        self,
        chars_in_row: int = 0,
        cell_size: tuple[int, int] = (0, 0),
        square_cells: bool = True,
        output_file: str | None = None,
    ) -> tuple[list[str], PIL.Image.Image, tuple[int, int]]:
        """
        Take all "bitmap" providers and export every character sheet into a single sheet.

        Characters are scaled according to the largest effective bounding box in all providers.

        :param chars_in_row:
            How many characters to fit inside each row of the resulting sheet.
            If this is 0, this will be set to the length of the first string in the
            "charlist" list. If this is negative, this will be set so that the resulting sheet is
            square. By default, this is 0 (auto first string).
        :param cell_size:
            What size to make each glyph cell.
            If this is (0, 0), this will be set to the largest dimensions of every glyph in `glyphs`.
        :param square_cells:
            If True, each glyph's width will equal its height.
            This is based on whichever number is largest.
            If False, each glyph's width will be unrelated to its height.
        :param output_file: Where to write the sheet to. If this is None, nothing will be
            written.
        :returns: A list of the new characters, and the new file as a :class:`PIL.Image.Image`.
        """
        extracted: dict[str, mcfonts.glyphs.BitmapGlyph | mcfonts.glyphs.UnihexGlyph] = {}
        for provider in self.yield_providers():
            if isinstance(provider, (mcfonts.providers.bitmap.BitmapProvider, mcfonts.providers.unihex.UnihexProvider)):
                yields = provider.yield_glyphs()
                for character, glyph in yields:
                    if glyph:
                        extracted[character] = glyph

        if chars_in_row == 0:
            bitmap_providers = [
                provider
                for provider in self.yield_providers()
                if isinstance(provider, mcfonts.providers.bitmap.BitmapProvider)
            ]

            chars_in_row = max(len(provider.contents["chars"][0] or "") for provider in bitmap_providers)
        elif chars_in_row < 0:
            chars_in_row = math.ceil(math.sqrt(len(extracted)))

        compacted = mcfonts.compacting.compact_glyphs(list(extracted.values()), chars_in_row, cell_size, square_cells)
        sheet = (
            list(mcfonts.providers.bitmap.fit_chars_into_charlist(list(extracted.keys()), chars_in_row)),
            compacted[0],
            compacted[1],
        )
        if output_file:
            with open(mcfonts.utils.resources.expand_path(output_file), "wb") as open_output_file:
                sheet[1].save(open_output_file)
        return sheet

    def coverage_report(self) -> mcfonts.coverage_reports.CoverageReport:
        """
        Build a report of what characters this font contains.

        This includes information like how many characters are in the font,
        and what Unicode blocks are covered.

        :returns: A dictionary of ``{"chars": int, "blocks": {str: int}}``.
        """
        characters: list[str] = []
        blocks: dict[str, int] = {}
        for character in self.yield_characters():
            characters.append(character)
            if (block := tinyunicodeblock.block(character, include_csur=True)) in blocks:
                blocks[block] += 1
            else:
                blocks[block] = 1
        return mcfonts.coverage_reports.CoverageReport(set(characters), blocks)

    def yield_glyphs_in_unirange(
        self, unirange_notation: str
    ) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.Glyph | None]]:
        """
        Given a `unirange_notation`, yield a tuple of the requested character to their glyph.

        :param unirange_notation:
            A string representing the requested range of chars.
            See https://pypi.org/project/unirange/.
        :returns: A yield of the requested characters and associated glyphs that match `unirange_notation`.
        """
        for provider in self.yield_providers():
            yield from provider.yield_glyphs_in_unirange(unirange_notation)

    def get_covering_providers(self, unirange_notation: str) -> list[mcfonts.providers.base.Provider]:
        """
        Given a codepoint range, return a list of providers that cover these characters.

        :param unirange_notation:
            A string representing the requested range of chars.
            See https://pypi.org/project/unirange/.
        :returns: A list of the providers that cover codeopints defined in `unirange_notation`.
        """
        result = []
        covers = unirange.unirange_to_characters(unirange_notation)
        for provider in self.yield_providers():
            if not isinstance(provider, mcfonts.providers.space.SpaceProvider):
                # Ignore padding chars
                covers.difference_update(mcfonts.constants.PADDING_CHARS)
            if provider.chars_covered.intersection(covers):
                result.append(provider)
        return result

    def reload_to_monochrome(self) -> None:
        """
        Replace the resources used in the providers with a grayscale version.

        If the resource is already grayscale, this will have no effect.
        This modifies the resource of this provider in place, and **can't be undone**.
        """
        if self.is_monochrome:
            mcfonts.logger.info("Font is already in monochrome; can't reload")
            return
        for provider in self.yield_providers():
            if isinstance(provider, mcfonts.providers.bitmap.BitmapProvider):
                provider.reload_to_monochrome()
        self.is_monochrome = True

    def compare(self, other: typing.Self) -> None:
        """
        Given `other`, compare the two, using `self` as a baseline.

        The information compared is:

        * Character count
        * Blocks covered
        * Providers included

        :param other: A second instance of :class:`mcfonts.MinecraftFont` to compare to.
        """
        self.coverage_report().compare(other.coverage_report())
        if mcfonts.utils.colors.USE_COLORS:
            print(f"\n{mcfonts.utils.colors.BRIGHT}PROVIDERS{mcfonts.utils.colors.RESET_ALL}")
        else:
            print("\nPROVIDERS")
        print(":: type: this | other (delta)")
        providers_this = {"bitmap": 0, "space": 0, "ttf": 0, "legacy_unicode": 0}
        providers_other = providers_this.copy()
        for provider in self.yield_providers():
            providers_this[provider.provider_type] += 1
        for provider in other.yield_providers():
            providers_other[provider.provider_type] += 1
        for provider_type in ("bitmap", "space", "ttf", "legacy_unicode"):
            amount_this = providers_this[provider_type]
            amount_other = providers_other[provider_type]
            print(
                f"\t{provider_type}: "
                f"{amount_this} | {amount_other} "
                f"({mcfonts.utils.colors.color_number(amount_other - amount_this)})"
            )

    def regenerate_charlists(self) -> mcfonts.utils.types.TypedProvidersDict:
        """
        Iterate through each resource and analyse it.

        For each resource, an entry will be made in a dictionary that contains the same height and ascent fields as
        the original, except the "chars" list will be updated to reflect the glyphs in the associated resource.

        .. warning::
            This only works if the first character in the original charlist is present,
            **and** if the order is incremental (U+0100, then U+0101, then U+0102, so on).

            If this condition isn't true, this function **will** fail.
            There are **no** checks for this rule.

        :returns: A dictionary matching a normal font JSON, with each "chars" list updated.
        """
        result: list[mcfonts.utils.types.TypedProviderDict] = []
        for provider in self.yield_providers():
            if isinstance(provider, mcfonts.providers.bitmap.BitmapProvider) and provider.resource:
                old_contents = provider.get_contents().copy()
                old_contents["chars"] = mcfonts.providers.bitmap.resource_to_charlist(
                    provider.resource,
                    chr(int(os.path.basename(provider.contents["file"]).split("-", 1)[0].split(".", 1)[0], 16)),
                    provider.glyph_cell,
                )
                result.append(old_contents)
            else:
                result.append(provider.get_contents())
        return {"providers": result}


def from_java_font_file(
    file_path: pathlib.Path,
    read_colors: bool = False,
    strict: bool = True,
) -> mcfonts.MinecraftFont:
    """
    Load a Java Edition font JSON into a :class:`mcfonts.MinecraftFont`.

    Requires a "providers" list, and missing files will raise an error.

    :param file_path:
        The real path to the font JSON.
    :param read_colors:
        If True, glyph will be loaded in RGBA.
        If false, loaded in LA.

        RGBA images incur **heavy** time cost.
        Be careful.
    :param strict:
        If True:

        * Bad providers will raise an error.
        * Missing files will raise an error.

        If False:

        * Bad providers will be ignored.
        * Missing files will be skipped.

    :returns: A :class:`mcfonts.MinecraftFont` instance.
    :raises FileNotFoundError: If a referenced file is not found and `strict` is True.
    """
    with open(file_path, encoding="utf-8") as datafp:
        file_contents: dict[str, typing.Any] = json.load(datafp, strict=False)
    return from_java_font_contents(file_contents, file_path, read_colors, strict)


def from_java_font_contents(
    file_contents: dict[str, typing.Any],
    file_path: pathlib.Path,
    read_colors: bool = False,
    strict: bool = True,
) -> mcfonts.MinecraftFont:
    """
    Load a Java Edition font JSON into a :class:`mcfonts.MinecraftFont`.

    Requires a "providers" list, and missing files will raise an error.

    :param file_contents:
        The contents of the font JSON file, loaded as a dictionary.
        This dictionary should include the base "providers" key.
    :param file_path:
        The path to the font JSON.
        This is needed for loading resources.
    :param read_colors:
        If True, glyph will be loaded in RGBA (Red, Green, Blue, Alpha). If false, loaded in LA.
        RGBA images incur **heavy** time cost. Be careful.
    :param strict:
        If True:

        * Bad providers will raise an error.
        * Missing files will raise an error.
        If False:

        * Bad providers will be ignored.
        * Missing files will be skipped.

    :returns: A :class:`mcfonts.MinecraftFont` instance.
    :raises FileNotFoundError: If a referenced file isn't found and `strict` is True.
    """
    provider_content = file_contents.get("providers", [])
    if read_colors:
        mode = "RGBA"
    else:
        mode = "LA"
    return mcfonts.MinecraftFont(
        list(
            mcfonts.utils.importing.load_all(
                provider_content, mcfonts.utils.resources.expand_path(file_path), strict, mode
            )
        ),
        not read_colors,
    )


def from_java_pack_folder(
    folder_path: pathlib.Path,
    font_file_name: str = "default.json",
    namespace: str = "minecraft",
    read_colors: bool = False,
    strict: bool = True,
) -> mcfonts.MinecraftFont:
    """
    Load a Java Edition resource pack into a :class:`mcfonts.MinecraftFont`.

    The font must be in the path ``assets/<namespace>/font/<fontfile>``.

    :param folder_path:
        The real path to the folder that contains a resource pack.
        This isn't the ``/assets/`` folder, nor is it a ZIP file.
        The files inside this folder should be ``assets/``, and ``pack.mcmeta``.
    :param font_file_name:
        The name of the font file.
        By default, this is "default.json".
    :param namespace:
        The namespace to find assets in.
        By default, this is "minecraft".
    :param read_colors:
        If True, glyph will be loaded in 'RGBA'.
        If False, loaded in 'LA'.

        RGBA images incur **heavy** time cost.
        Be careful.
    :param strict:
        If True:

        * Bad providers will raise an error.
        * Missing files will raise an error.

        If False:

        * Bad providers will be ignored.
        * Missing files will be skipped.

    :returns: A :class:`mcfonts.MinecraftFont` instance.
    :raises FileNotFoundError: If a referenced file isn't found and `strict` is True.
    """

    return from_java_font_file(
        mcfonts.utils.resources.expand_path(folder_path).joinpath(
            f"assets/{namespace}/font/{font_file_name}",
        ),
        read_colors,
        strict,
    )


def from_java_pack_zip(
    file_path: pathlib.Path, password: bytes | None = None, read_colors: bool = False, strict: bool = True
) -> mcfonts.MinecraftFont:
    """
    Load a Java Edition resource pack ZIP into a :class:`mcfonts.MinecraftFont`.

    The font must be in the path ``assets/<namespace>/font/<fontfile>``.

    :param file_path:
        The real path to the ZIP file.
    :param password:
        Password to use when reading the ZIP file.
        Set to ``None`` if there is no password.
    :param read_colors:
        If True, glyph will be loaded in 'RGBA'.
        If False, loaded in 'LA'.

        RGBA images incur **heavy** time cost.
        Be careful.
    :param strict:
        If True:

        * Bad providers will raise an error.
        * Missing files will raise an error.

        If False:

        * Bad providers will be ignored.
        * Missing files will be skipped.

    :returns: A :class:`mcfonts.MinecraftFont` instance.
    :raises FileNotFoundError: If a referenced file isn't found and `strict` is True.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        real_temp_dir = pathlib.Path(temp_dir).absolute()
        with zipfile.ZipFile(mcfonts.utils.resources.expand_path(file_path)) as zip_file:
            zip_file.extractall(real_temp_dir, pwd=password)
        return from_java_pack_folder(real_temp_dir, read_colors=read_colors, strict=strict)


def from_java_resource_template(
    file_path: pathlib.Path,
    template_provider: dict[str, typing.Any],
    read_colors: bool = False,
    strict: bool = True,
) -> mcfonts.MinecraftFont:
    """
    | Given the path to a texture and the contents of an individual font provider,
    | return a :class:`mcfonts.MinecraftFont` instance with it, and the resource in `file_path`.

    ``template_provider["file"]`` can be any value; it will be overwritten anyway,
    although it must exist.

    :param file_path:
        The path to the PNG :term:`resource` that needs templating.
    :param template_provider:
        An individual provider dictionary.
        Not a list of providers.
    :param read_colors:
        If True, glyph will be loaded in 'RGBA'.
        If False, loaded in 'LA'.
        RGBA images incur **heavy** time cost. Be careful.
    :param strict:
        If a provider has bad data,
        an exception will be raised and no provider list will be returned if this is True.
        If this is False, it will be ignored.
    :returns:
        A :class:`mcfonts.MinecraftFont` instance.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        # Put the PNG file into the temp dir to later read all-together.
        file_path = mcfonts.utils.resources.expand_path(file_path)
        shutil.copy(file_path, temp_dir)
        # Make a temporary fake provider file
        with tempfile.NamedTemporaryFile("w+", dir=temp_dir) as temp_file:
            # Overwrite default file, use expanded argument with modifications
            try:
                template_provider["file"] = mcfonts.utils.resources.expand_resource_location(file_path)
            except KeyError as exception:
                if strict:
                    raise exception
            json.dump(template_provider, temp_file, ensure_ascii=False)
        return from_java_font_file(pathlib.Path(temp_file.name), read_colors, strict)


def from_java_ambiguous(path: pathlib.Path, read_colors: bool = False, strict: bool = True) -> mcfonts.MinecraftFont:
    """
    For file paths where the file pointed to is of an unknown type; it could be a JSON, ZIP, or directory.

    This function automatically figures out which function to use, and returns a MinecraftFont.

    :param path:
        The real path to either a file or a folder.
    :param read_colors:
        If True, glyph will be loaded in 'RGBA'.
        If False, loaded in 'LA'.

        RGBA images incur **heavy** time cost.
        Be careful.
    :param strict:
        If True:

        * Bad providers will raise an error.
        * Missing files will raise an error.

        If False:

        * Bad providers will be ignored.
        * Missing files will be skipped.

    :returns: A :class:`mcfonts.MinecraftFont` instance.
    """
    if str(path).endswith(".json"):
        return from_java_font_file(path, read_colors, strict)
    if os.path.isdir(path):
        return from_java_pack_folder(path, read_colors=read_colors, strict=strict)
    # Not a JSON, not a directory, must be a ZIP.
    return from_java_pack_zip(path, read_colors=read_colors, strict=strict)
