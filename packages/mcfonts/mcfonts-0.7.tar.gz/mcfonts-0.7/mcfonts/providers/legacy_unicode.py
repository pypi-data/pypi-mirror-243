#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""A legacy unicode provider, handling bitmap glyphs in a 16px x 16px grid."""
import collections.abc
import os
import re
import unicodedata

import PIL.Image
import unirange

import mcfonts.constants
import mcfonts.glyphs
import mcfonts.providers.base
import mcfonts.utils.resources
import mcfonts.utils.schemas

TEMPLATE_CHARS = {
    0: PIL.Image.frombytes("1", (3, 5), b"\xe0\xa0\xa0\xa0\xe0"),
    1: PIL.Image.frombytes("1", (3, 5), b"@\xc0@@\xe0"),
    2: PIL.Image.frombytes("1", (3, 5), b"\xe0 \xe0\x80\xe0"),
    3: PIL.Image.frombytes("1", (3, 5), b"\xe0 \xe0 \xe0"),
    4: PIL.Image.frombytes("1", (3, 5), b"\xa0\xa0\xe0  "),
    5: PIL.Image.frombytes("1", (3, 5), b"\xe0\x80\xe0 \xe0"),
    6: PIL.Image.frombytes("1", (3, 5), b"\xe0\x80\xe0\xa0\xe0"),
    7: PIL.Image.frombytes("1", (3, 5), b"\xe0    "),
    8: PIL.Image.frombytes("1", (3, 5), b"\xe0\xa0\xe0\xa0\xe0"),
    9: PIL.Image.frombytes("1", (3, 5), b"\xe0\xa0\xe0 \xe0"),
    10: PIL.Image.frombytes("1", (3, 5), b"\xe0\xa0\xe0\xa0\xa0"),
    11: PIL.Image.frombytes("1", (3, 5), b"\xc0\xa0\xc0\xa0\xc0"),
    12: PIL.Image.frombytes("1", (3, 5), b"\xe0\x80\x80\x80\xe0"),
    13: PIL.Image.frombytes("1", (3, 5), b"\xc0\xa0\xa0\xa0\xc0"),
    14: PIL.Image.frombytes("1", (3, 5), b"\xe0\x80\xe0\x80\xe0"),
    15: PIL.Image.frombytes("1", (3, 5), b"\xe0\x80\xe0\x80\x80"),
    -4: PIL.Image.frombytes(
        "1", (11, 16), b"\xff\xe0\x80 \x80 \x80 \x80 \x80 \x80 \x80 \x80 \x80 \x80 \x80 \x80 \x80 \x80 \xff\xe0"
    ),
    -6: PIL.Image.frombytes(
        "1",
        (15, 16),
        b"\xff\xfe\x80\x02\x80\x02\x80\x02\x80\x02\x80\x02\x80\x02\x80\x02\x80\x02\x80\x02\x80\x02\x80\x02\x80\x02\x80"
        b"\x02\x80\x02\xff\xfe",
    ),
}


class LegacyUnicodeProvider(mcfonts.providers.base.Provider):
    """
    The ``legacy_unicode`` provider is a "fallback" provider intended to be used as a last-resort.

    It is similar to the :class:`bitmap provider<mcfonts.providers.bitmap.BitmapProvider>`
    in that its glyphs are bitmaps.

    It uses a system of templates to create and add 16px x 16px tables of "fallback" characters.
    Each glyph is 16px x 16px pixels wide, so each page is 256px x 256px;
    16 characters on each line, 16 lines, 16 length for each glyph.

    .. warning::
        This provider is deprecated and should not be used when possible.
        Use the "unihex" provider instead.

    .. important::
        Characters above the `BMP <https://en.wikipedia.org/wiki/Plane_(Unicode)#Basic_Multilingual_Plane>`_ (U+FFFF)
        are not handled.
    """

    def __init__(
        self,
        provider: mcfonts.utils.types.TypedProviderLegacyUnicode,
        origin: os.PathLike[str] | str,
        resources: dict[str, PIL.Image.Image | bytes],
    ) -> None:
        self.contents = provider
        self.resources = resources
        self.codepages_covered: list[int] = []
        self.glyphs = dict(self.construct_glyphs())
        super().__init__(
            "legacy_unicode",
            origin,
            set(self.yield_characters()),
        )
        self.validate()

    def pretty_print(self) -> str:
        return f"{self.get_icon()} legacy_unicode: {self.get_contents().get('template', 'no template')}"

    def validate(self) -> None:
        return None  # No specific validation checks yet.

    def print_info(self) -> None:
        super().print_info()
        print(f"Template: {self.contents['template'] or mcfonts.constants.UNKNOWN_FIELD}")
        print(f"Sizes: {self.contents['sizes'] or mcfonts.constants.UNKNOWN_FIELD}")

    def construct_glyphs(self) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.BitmapGlyph]]:
        for codepage, content in self.resources.items():
            if not re.match(
                self.contents["template"].replace("\\", "\\\\").replace("(", "\\(").replace("%s", r"(\d\d)"), codepage
            ) or not isinstance(content, PIL.Image.Image):
                continue  # If template_\d\d\.png doesn't match codepage name, skip.
            if not (codepage_num := re.match(codepage, r"\d\d")):
                continue  # If template doesn't have \d\d, skip.
            for index, glyph in enumerate(mcfonts.utils.resources.divide_resource_by_grid(content, (16, 16))):
                if glyph is None:
                    continue
                yield chr((int(codepage_num.group(1), 16) << 8) + index), mcfonts.glyphs.BitmapGlyph(glyph, 1)

    def yield_glyphs(self) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.BitmapGlyph]]:
        yield from self.glyphs.items()

    def yield_characters(self) -> collections.abc.Iterable[str]:
        for key in self.glyphs.keys():
            yield str(key)

    def get_icon(self) -> str:
        return "🖳"

    def get_pack_versions(self) -> tuple[int, int]:
        return 4, 19

    def yield_glyphs_in_unirange(
        self, unirange_notation: str
    ) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.BitmapGlyph | None]]:
        for character in unirange.unirange_to_characters(unirange_notation):
            yield character, self.glyphs.get(character)

    def get_contents(self) -> mcfonts.utils.types.TypedProviderLegacyUnicode:
        return self.contents


def to_advances(glyphsizes: bytes, match_unicode_category: list[str] | None = None) -> dict[str, int]:
    r"""
    Translate a glyphsizes.bin file into an "advances" mapping, which goes inside a "space" provider.

    .. note::

        This function does not return a new provider.

    >>> to_advances(b"\x00\x00\x00...")
    {
        "\x00": 0,
        "\x01": 0,
        "\x02": 0,
        "\uBEEF": 15
    }

    :param glyphsizes: The bytes of glyphsizes.bin.
    :param match_unicode_category:
        Only translate Unicode characters with these categories.
        By default, this is ``[Mc, Zp, Zs, Zl]``.
        This should cover most whitespace and marking characters.
    :returns: An "advances" dictionary.
    """
    if match_unicode_category is None:
        match_unicode_category = ["Mc", "Zp", "Zs", "Zl"]
    advances = {}
    for index, nibble in enumerate(glyphsizes):
        if unicodedata.category(character := chr(index)) in match_unicode_category:
            advances[character] = (nibble & 0xF) - (nibble >> 4 & 0xF)
    return advances


def build_template_for_character(
    character: str, template_storage: dict[int, PIL.Image.Image] | None = None
) -> PIL.Image.Image:
    """
    Build an image of a template :term:`codepoint`.

    Templates are simple white boxes with a codepoint :term:`texture` inside them.
    This is intended for use with a "legacy_unicode" :term:`provider`.

    :param character:
        A single character.
        This character's codepoint is what goes inside the box.
    :param template_storage:
        Dictionary of integers mapped to the template character PNG images.

        * `0-15` are images of hexadecimal digits.
        * `-4` and `-6` are "boxes" for 4 and 6 digit-long codepoints, respectively.

    :returns:
        A :class:`PIL.Image.Image` of the character template.
    """
    if template_storage is None:
        template_storage = TEMPLATE_CHARS
    codepoint = ord(character)
    if codepoint > 0xFFFF:
        box = template_storage[-6]
        # 0xABCDEF -> A
        box.paste(template_storage[(codepoint & 0xF00000) >> 20], (2, 2))
        # 0xABCDEF -> B
        box.paste(template_storage[(codepoint & 0xF0000) >> 16], (6, 2))
        # 0xABCDEF -> C
        box.paste(template_storage[(codepoint & 0xF000) >> 12], (10, 2))
        # 0xABCDEF -> D
        box.paste(template_storage[(codepoint & 0xF00) >> 8], (2, 9))
        # 0xABCDEF -> E
        box.paste(template_storage[(codepoint & 0xF0) >> 4], (6, 9))
        # 0xABCDEF -> F
        box.paste(template_storage[(codepoint & 0xF)], (10, 9))
    else:
        box = template_storage[-4]
        # 0xABCD -> A
        box.paste(template_storage[(codepoint & 0xF000) >> 12], (2, 2))
        # 0xABCD -> B
        box.paste(template_storage[(codepoint & 0xF00) >> 8], (6, 2))
        # 0xABCD -> C
        box.paste(template_storage[(codepoint & 0xF0) >> 4], (2, 9))
        # 0xABCD -> D
        box.paste(template_storage[codepoint & 0xF], (6, 9))
    return box


def align_unicode_page(sheet: PIL.Image.Image) -> PIL.Image.Image:
    """
    Align a Unicode page font sheet's characters to the left.

    This function is a shortcut for :func:`mcfonts.utils.resources.align_font_texture(sheet, (16, 16))`.

    :param sheet: The font sheet, not the individual character.
    :returns: The new font sheet.
    """
    return mcfonts.utils.resources.align_font_texture(sheet, (16, 16))
