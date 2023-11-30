#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""A space provider, defining simple widths for characters."""
import collections.abc
import os
import typing

import unirange

import mcfonts.constants
import mcfonts.glyphs
import mcfonts.providers
import mcfonts.utils


class SpaceProvider(mcfonts.providers.base.Provider):
    """
    The ``space`` provider defines only the width of a character.

    It's the simplest provider: it only contains the ``"advances"`` map.

    The keys of the advances are the characters as 1-length strings, and the values are the widths as integers.
    In mcfonts only, uniranges can also be used as the keys.

    The default width for ``U+0020 SPACE`` is 4.
    """

    def __init__(self, provider: mcfonts.utils.types.TypedProviderSpace, origin: os.PathLike[str] | str) -> None:
        self.contents = provider
        self.glyphs: dict[str, mcfonts.glyphs.SpaceGlyph] = dict(self.construct_glyphs())
        for key, value in provider.get("advances", {}).items():
            for new_character in unirange.unirange_to_characters(key):
                # Expand the uniranges and copy over fields.
                self.contents["advances"][new_character] = value
        super().__init__("space", origin, set(provider["advances"].keys()))
        self.validate()

    def pretty_print(self) -> str:
        return f"{self.get_icon()} space: {len(self.get_contents().get('advances', [])):,} widths"

    def validate(self) -> None:
        return None  # No specific validation checks yet.

    def print_info(self) -> None:
        super().print_info()

        if len(self.contents["advances"]) < 1:
            # There's no "advances" dictionary.
            print("No advances.")
        else:
            advances = self.contents["advances"]
            print(f"Advances: ({len(advances):,})")
            for space_character, width in advances.items():
                print(f"\tCharacter {mcfonts.utils.unicode.pretty_print_character(space_character)}: {width}")

    def construct_glyphs(self) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.SpaceGlyph]]:
        for character, width in self.contents["advances"].items():
            yield character, mcfonts.glyphs.SpaceGlyph(int(width))

    def yield_characters(self) -> collections.abc.Iterable[str]:
        yield from self.contents["advances"]

    def yield_glyphs(self) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.SpaceGlyph]]:
        yield from self.glyphs.items()

    def get_icon(self) -> str:
        return "␣"

    def get_pack_versions(self) -> tuple[int, None]:
        return 9, None

    def yield_glyphs_in_unirange(
        self, unirange_notation: str
    ) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.SpaceGlyph | None]]:
        for character in unirange.unirange_to_characters(unirange_notation):
            yield character, self.glyphs.get(character)

    def get_contents(self) -> mcfonts.utils.types.TypedProviderSpace:
        return self.contents


def to_glyph_sizes(advances: dict[str, int], default_width: tuple[int, int] = (0, 14)) -> bytearray:
    r"""
    Create a glyph_sizes.bin bytearray from a template of characters and their starting and ending positions.

    >>> to_glyph_sizes({"\0": 15}, (0, 0))
    bytearray(b'\x0e\x00\x00\x00...')

    :param advances: A dictionary of ``{character: width}``.
    :param default_width:
        The width to fall back to if `advances` doesn't define one for a character.
    :returns: Bytearray of glyph_sizes.bin.
    """
    glyphsizes = bytearray((default_width[0] * 16 + default_width[1]).to_bytes(1, "big") * 65536)
    for character, width in advances.items():
        if (codepoint := ord(character)) > 0xFFFF:
            # Can't pack characters higher than the BMP.
            mcfonts.logger.warning(f"Cannot include character {character} in glyph_sizes; codepoint is above U+FFFF.")
            continue
        # Ensure the high and low bits are in the correct 0-F range.
        if 0 > width < 15:
            raise ValueError("Width must be within 0 to 15")
        glyphsizes[codepoint] = width
    return glyphsizes
