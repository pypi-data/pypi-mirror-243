#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""A unihex provider, handling .hex glyphs."""
import collections.abc
import os
import typing

import jsonschema
import unirange

import mcfonts.glyphs
import mcfonts.providers.base
import mcfonts.utils.schemas
import mcfonts.utils.unihex


class UnihexProvider(mcfonts.providers.base.Provider):
    """
    The ``unihex`` provider loads glyphs from text files in the ".hex" format.

    It has two required fields, ``hex_file`` and ``size_overrides``.

    * ``hex_file`` is a resource location to a .ZIP file containing any number of ".hex" files at its root.
    * ``size_overrides`` is a list of maps stating the beginning and end of a character range, and the starting and
      ending columns of the glyphs that match that range.

    Each ".hex" file is a text document with each line containing a hex glyph.
    A hex glyph is a string of text in the format of ``<codepoint>:<bit string>``.
    The bit string is a string of hexadecimal numbers.
    The numbers, when converted to binary, describe the glyph's pixels.
    A 1 bit is an "on" pixel, and a 0 bit is an "off" pixel.
    When exporting, the empty left and right columns are trimmed unless ``size_overrides`` explicitly overrides this.
    """

    def __init__(
        self,
        provider: mcfonts.utils.types.TypedProviderUnihex,
        origin: os.PathLike[str] | str,
        resources: dict[str, str] | None,
    ) -> None:
        self.contents = provider
        self.resources = resources
        self.size_overrides = dict(self.yield_size_overrides())
        self.glyphs = dict(self.construct_glyphs())
        super().__init__("unihex", origin, set(self.glyphs.keys()))
        self.validate()

    def construct_glyphs(self) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.UnihexGlyph]]:
        if not self.resources:
            return
        for name, hex_contents in self.resources.items():
            for hex_glyph in hex_contents.splitlines():
                yield mcfonts.utils.unihex.get_codepoint(hex_glyph), mcfonts.glyphs.UnihexGlyph(
                    mcfonts.utils.unihex.get_bit_string(hex_glyph), None, None, None, None
                )

    def yield_size_overrides(self) -> collections.abc.Iterable[tuple[str, tuple[int, int]]]:
        """
        Yield all the size overrides for every character.

        Overrides are given as ``tuple[int, int]``.

        :returns: A yield of ``(character: str, (left: int, right: int))``.
        """
        for override in self.get_contents().get("size_overrides", {}):
            left = override.get("left", -1)
            right = override.get("right", -1)
            for codepoint in range(ord(override.get("from", "\0")), ord(override.get("to", "\0"))):
                yield chr(codepoint), (left, right)

    def get_size_override(self, character: str) -> tuple[int, int] | None:
        """
        Return the size overrides of a character, if they exist.

        Size overrides is a tuple of two integers of the starting and ending columns to cut off when exporting.
        If there are no size overrides for a character, None is returned.

        :returns: A tuple of two integers, or None.
        """
        return self.size_overrides.get(character)

    def validate(self) -> None:
        jsonschema.validate(self.contents, mcfonts.utils.schemas.SCHEMA_PROVIDER_UNIHEX)

    def pretty_print(self) -> str:
        return (
            f"{self.get_icon()} unihex: {len(self.resources or []):,} .hex files, "
            f"{len(self.size_overrides):,} size overrides"
        )

    def print_info(self) -> None:
        pass

    def yield_glyphs(self) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.UnihexGlyph]]:
        yield from self.glyphs.items()

    def yield_characters(self) -> collections.abc.Iterable[str]:
        yield from self.glyphs.keys()

    def get_icon(self) -> str:
        return "⬣"

    def get_pack_versions(self) -> tuple[int, None]:
        return 15, None

    def yield_glyphs_in_unirange(
        self, unirange_notation: str
    ) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.UnihexGlyph]]:
        for character in unirange.unirange_to_characters(unirange_notation):
            yield character, self.glyphs[character]  # Guaranteed to succeed, no need to dict.get().

    def get_contents(self) -> mcfonts.utils.types.TypedProviderUnihex:
        return self.contents
