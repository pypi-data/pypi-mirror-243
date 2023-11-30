#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""
Functions for exporting into the GNU Unifont HEX format.

Contains functions for transforming and handling Unifont HEX data.
"""
from __future__ import annotations

import PIL.Image

import mcfonts.glyphs


def set_space_to_character(hex_store: dict[str, str], character: str, width: int, replace: bool = True) -> None:
    """
    Set a simple blank space width to a character.

    :param hex_store: The .hex font, represented as a dictionary.
    :param character: The character to set a space to.
    :param width: The width.
    :param replace: Whether the width should overwrite pre-existing glyph data for `character`.
    """
    local_name = f"{ord(character):04X}"
    if local_name in hex_store and not replace:
        return
    hex_store[local_name] = "0" * (width * 4)


def set_hex_to_character(hex_store: dict[str, str], hex_glyph: str, character: str, replace: bool = True) -> None:
    """
    Set .hex glyph data to a character.

    :param hex_store: The .hex font, represented as a dictionary.
    :param hex_glyph: A string of the glyph data.
    :param character: The character to set a glyph to.
    :param replace: Whether the width should overwrite pre-existing glyph data for `character`.
    """
    local_name = f"{ord(character):04X}"
    if local_name in hex_store and not replace:
        return
    hex_store[local_name] = hex_glyph


def generate_bitmap_hex(glyph: mcfonts.glyphs.BitmapGlyph) -> str:
    """
    Generate a .hex glyph out of a :class:`~mcfonts.glyphs.BitmapGlyph`.

    :param glyph: A :class:`~mcfonts.glyphs.BitmapGlyph`.
    :returns: A string of the .hex glyph data. In hexadecimal, used as-is for exporting.
    """
    if glyph.get_bearings() == (0, 0):
        return "0000"

    image = glyph.get_image()
    glyph_width = image.width

    newsize_image = image.copy()
    # Image must be 16 pixels tall and 2**n height to be encoded as unihex
    if image.height > 16 or image.width > 16:  # We can just resize image down to force it to fit
        newsize_image = image.resize((16, 2 ** (glyph_width - 1).bit_length()), PIL.Image.Resampling.NEAREST)
    elif image.height != 16 or (glyph_width & (glyph_width - 1) != 0):
        newsize_image = PIL.Image.new("LA", (16, 2 ** (glyph_width - 1).bit_length()))
        newsize_image.paste(image, (16 + (glyph.get_height() - glyph.get_ascent()), 0))

    data = newsize_image.convert("LA").getdata(1)

    bit_string = []
    row = 0
    for index, pixel in enumerate(data):
        if pixel >= mcfonts.glyphs.BITMAP_EXPORT_PIXEL_THRESHOLD:
            # Set the bit in `row` at position equal to the X position in the current bitmap image row
            row |= 1 << (glyph_width - (index % glyph_width))
        if index % (glyph_width - 1) == 0:
            # Index position is at the end of glyph X boundary, start new row
            # Index starts at 0, and width starts at 1
            # Pad "byte" with 0 to match the number of bytes it would be, equal to width // 4 (16 width,
            bit_string.append(hex(row)[2:].rjust(glyph_width // 4, "0"))
            row = 0

    return "".join(bit_string)


def include_glyph(hex_store: dict[str, str], glyph: mcfonts.glyphs.Glyph, character: str) -> None:
    """
    Include `glyph` into the .hex font, represented as a dictionary.

    Different Glyph subtypes have different methods of being imported;
    this function centralizes those varying methods.

    :param hex_store: The .hex font, represented as a dictionary.
    :param glyph: An instance of :class:`mcfont.glyphs.Glyph`.
    :param character: The character to assign this glyph to.
    """
    if isinstance(glyph, mcfonts.glyphs.SpaceGlyph):
        set_space_to_character(hex_store, character, min(glyph.get_width(), 512))
    elif isinstance(glyph, mcfonts.glyphs.BitmapGlyph):
        set_hex_to_character(hex_store, generate_bitmap_hex(glyph), character, False)
    elif isinstance(glyph, mcfonts.glyphs.UnihexGlyph):
        set_hex_to_character(hex_store, glyph.get_bit_string(), character, False)
