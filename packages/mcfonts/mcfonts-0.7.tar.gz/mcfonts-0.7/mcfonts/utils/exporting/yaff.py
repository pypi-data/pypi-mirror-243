#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""
Functions for exporting into the text-only human-readable
`YAFF format <https://github.com/robhagemans/monobit/blob/master/YAFF.md>`_.
"""
from __future__ import annotations

import mcfonts.glyphs
import mcfonts.utils.unihex

YAFF_STORE_GLYPH_MAGIC = "__glyph__"
"""The magic constant that is used as a key for glyph data to be stored under."""


def set_space_to_character(
    yaff_store: dict[str, str | int | dict[str, list[str]]],
    character: str,
    width: int,
    replace: bool = True,
) -> None:
    """
    Set a simple blank space width to a character.

    :param yaff_store: The YAFF font, represented as a dictionary.
    :param character: The character to set a space to.
    :param width: The width.
    :param replace: Whether the width should overwrite pre-existing glyph data for `character`.
    """
    local_name = f"u+{ord(character):04X}"
    if local_name in yaff_store and not replace:
        return
    if local_name not in yaff_store:
        yaff_store[local_name] = {YAFF_STORE_GLYPH_MAGIC: []}
    yaff_store[local_name][YAFF_STORE_GLYPH_MAGIC] = ["." * width] * 8


def set_yaff_to_character(
    yaff_store: dict[str, str | int | dict[str, list[str] | str | int]],
    yaff_glyph: dict[str, list[str] | str | int],
    character: str,
    replace: bool = True,
) -> None:
    """
    Set YAFF glyph data to a character.

    :param yaff_store: The YAFF font, represented as a dictionary.
    :param yaff_glyph: A dictionary of the YAFF data. Glyph data is stored under :data:`YAFF_STORE_GLYPH_MAGIC`.
    :param character: The character to set a glyph to.
    :param replace: Whether the width should overwrite pre-existing glyph data for `character`.
    """
    if (local_name := f"u+{ord(character):04X}") in yaff_store and not replace:
        return
    yaff_store[local_name] = yaff_glyph


def include_glyph(
    yaff_store: dict[str, str | int | dict[str, list[str]]],
    glyph: mcfonts.glyphs.Glyph,
    character: str,
) -> None:
    """
    Include `glyph` into the YAFF font, represented as a dictionary.

    Different Glyph subtypes have different methods of being imported;
    this function centralizes those varying methods.

    :param yaff_store: The YAFF font, represented as a dictionary.
    :param glyph: An instance of :class:`mcfont.glyphs.Glyph`.
    :param character: The character to assign this glyph to.
    """
    if isinstance(glyph, mcfonts.glyphs.SpaceGlyph):
        set_space_to_character(yaff_store, character, min(glyph.get_width(), 512))
    elif isinstance(glyph, mcfonts.glyphs.BitmapGlyph):
        set_yaff_to_character(yaff_store, generate_bitmap_yaff(glyph), character, False)
    elif isinstance(glyph, mcfonts.glyphs.UnihexGlyph):
        set_yaff_to_character(yaff_store, generate_unihex_yaff(glyph), character, False)


def generate_bitmap_yaff(glyph: mcfonts.glyphs.BitmapGlyph) -> dict[str, list[str] | str | int]:
    """
    Generate a YAFF glyph out of a :class:`~mcfonts.glyphs.BitmapGlyph`.

    :param glyph: A :class:`~mcfonts.glyphs.BitmapGlyph`.
    :returns: A dictionary of the YAFF data. Glyph data is stored under :data:`YAFF_STORE_GLYPH_MAGIC`.
    """

    image = glyph.get_image()
    pixel_values = [pixel >= mcfonts.glyphs.BITMAP_EXPORT_PIXEL_THRESHOLD for pixel in image.convert("LA").getdata(1)]

    glyph_store = []

    for row in [pixel_values[i : i + image.width] for i in range(0, len(pixel_values), image.width)]:
        # Trim the excess to the real width.
        # There'll never be data there anyway.
        glyph_store.append(
            "".join("@" if pixel_value else "." for pixel_value in row)[
                : mcfonts.utils.image.get_image_bearings(image)[1]
            ]
            + "."  # Single padding
        )

    return {
        YAFF_STORE_GLYPH_MAGIC: glyph_store,
        "ascent": glyph.get_ascent(),
        "descent": glyph.get_height() - glyph.get_ascent(),
        "pixel-size": glyph.get_height() + glyph.get_ascent(),
    }


def generate_unihex_yaff(glyph: mcfonts.glyphs.UnihexGlyph) -> dict[str, list[str] | str | int]:
    """
    Generate a YAFF glyph out of a :class:`~mcfonts.glyphs.UnihexGlyph`.

    :param glyph: A :class:`~mcfonts.glyphs.UnihexGlyph`.
    :returns: A dictionary of the YAFF data. Glyph data is stored under :data:`YAFF_STORE_GLYPH_MAGIC`.
    """
    return {
        YAFF_STORE_GLYPH_MAGIC: [
            row.replace("0", ".").replace("1", "@")
            for row in mcfonts.utils.unihex.bit_string_to_rows(glyph.get_bit_string(), False)
        ],
        "ascent": 7,
        "descent": 1,
    }
