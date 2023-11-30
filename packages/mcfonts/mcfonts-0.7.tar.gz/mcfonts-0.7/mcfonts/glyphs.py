#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""
Various glyph formats that can be present in a font.

Each vary in their storage formats and methods of manipulating contained data.
"""
from __future__ import annotations

import abc
import dataclasses

import fontTools.pens.t2CharStringPen
import PIL.Image

import mcfonts.constants
import mcfonts.exceptions
import mcfonts.utils.image
import mcfonts.utils.unihex

BITMAP_EXPORT_PIXEL_THRESHOLD = 180
UNIHEX_EXPORT_PIXEL_ON = "1"
SPACE_EXPORT_MAX_ADVANCE = 12500


class Glyph(abc.ABC):
    """The base Glyph class. Should never be called or instantiated."""

    @abc.abstractmethod
    def get_width(self) -> int:
        """Width of the glyph."""

    @abc.abstractmethod
    def get_ascent(self) -> int:
        """Ascent of the glyph."""

    @abc.abstractmethod
    def get_height(self) -> int:
        """Height of the glyph. This is not always equal to the glyph's image, if applicable."""

    @abc.abstractmethod
    def get_program(self) -> list[str | int] | None:
        """A Type 2 charstring program. This is used in exporting and can be cached for better performance."""

    @abc.abstractmethod
    def construct_program(self, pixel_size: int) -> list[str | int] | None:
        """
        Create a Type 2 charstring program.

        If the glyph is empty or has no white pixels, None will be returned.
        Otherwise, a list *(the program)* will be returned.

        .. warning::

            These charstrings are **not** optimized or checked for overlaps.
            In FontForge, use :menuselection:`E&lement -> O&verlap -> &Remove Overlap` manually afterward.

        :param pixel_size:
            How big each pixel should be.
        :returns:
            A list of strings of the glyph's program, or None if there was no pixel data in ``glyph``.
        """


@dataclasses.dataclass
class BitmapGlyph(Glyph):
    """
    A bitmap glyph.

    Must contain an image and ascent.
    Height, ascent, and bearings are optional.
    Bearings and width are lazily-loaded.
    """

    image: PIL.Image.Image
    """Required image."""
    ascent: int
    """Required ascent."""
    height: int | None = None
    """Optional height. Lazy default is 8 if None."""
    width: int | None = None
    """Optional width. Lazy default is `self.image.width`."""
    bearings: tuple[int, int] | None = None
    """Optional padding from the edges of the canvas."""
    program: list[str | int] | None = None
    """Optional Type 2 charstring program of the glyph."""

    def get_bearings(self) -> tuple[int, int]:
        """
        From :func:`mcfonts.utils.resources.get_image_bearings`:

        | Bearings are a "padding" from the edge of the canvas to image pixels.
        | Left bearing is the distance from the left edge of the canvas to the most-left pixel data.
        | Right bearing is the distance from the right edge of the canvas to the most-right pixel data.

        This is lazily-loaded.
        """
        if self.bearings is None:
            self.bearings = mcfonts.utils.image.get_image_bearings(self.image)
        return self.bearings

    def get_width(self) -> int:
        """
        Width of the glyph's image.

        This is lazily-loaded.
        """
        if self.width is None:
            self.width = self.image.width
        return self.width

    def get_image(self) -> PIL.Image.Image:
        """The image of the glyph."""
        if self.image.mode not in {"RGBA", "LA"}:
            self.image = self.image.convert("RGBA")
        return self.image

    def get_height(self) -> int:
        """
        The height of the glyph; this is not necessarily the glyph's image width.

        This is lazily-loaded.
        """
        if self.height is None:
            self.height = 8
        return self.height

    def get_ascent(self) -> int:
        """The glyph's ascent."""
        return self.ascent

    def get_program(self) -> list[str | int] | None:
        if self.program is None:
            self.program = self.construct_program(
                # Em size (1000) divided by 8 (standard width) = 125,
                # divide this by scale (glyph height / JSON height) to get how big each "pixel" will translate to.
                125
                // self.image.height
                // self.get_height()
            )
        return self.program

    def construct_program(self, pixel_size: int) -> list[str | int] | None:
        if (bearings := self.get_bearings()) == (0, 0):
            return None

        pen = fontTools.pens.t2CharStringPen.T2CharStringPen(0, {})
        ascent = self.get_ascent()
        height = self.get_image().height
        glyph_width = self.get_image().width

        for index, pixel in enumerate(self.get_image().convert("LA").getdata(1)):
            if pixel >= BITMAP_EXPORT_PIXEL_THRESHOLD:
                x_real = index % glyph_width
                y_real = height - (index // glyph_width) + ascent
                pen.moveTo(
                    (
                        x_real * pixel_size,
                        y_real * pixel_size,
                    )
                )  # Left X, top right.

                pen.lineTo(
                    (
                        (x_real + 1) * pixel_size,
                        y_real * pixel_size,
                    )
                )  # Down Y, bottom left.

                pen.lineTo(
                    (
                        (x_real + 1) * pixel_size,
                        (y_real - 1) * pixel_size,
                    )
                )  # Right X, bottom right.

                pen.lineTo(
                    (
                        x_real * pixel_size,
                        (y_real - 1) * pixel_size,
                    )
                )  # Done with pixel.

                pen.closePath()
        program: list[int | str] = pen.getCharString().program
        program[0] = (bearings[1] + 1) * pixel_size  # Set the width correctly.
        return program


@dataclasses.dataclass
class SpaceGlyph(Glyph):
    """
    A space glyph.

    Contans one required field, the glyph's width.
    """

    width: int
    """The width of the glyph."""
    program: list[str | int] | None = None
    """Optional Type 2 charstring program of the glyph."""

    def get_width(self) -> int:
        return self.width

    def get_ascent(self) -> int:
        return 1

    def get_height(self) -> int:
        return 8

    def get_program(self) -> list[str | int] | None:
        if self.program is None:
            self.program = self.construct_program(125)
        return self.program

    def construct_program(self, pixel_size: float) -> list[str | int] | None:
        return [int(min(abs((self.get_width() * pixel_size)), SPACE_EXPORT_MAX_ADVANCE)), "endchar"]


@dataclasses.dataclass
class UnihexGlyph(Glyph):
    """
    A unihex glyph.

    Must contain a bit string.
    Width, image, and bearings are optional.
    Width, image, and bearings are lazily-loaded.

    Unihex glyphs are always 16 pixels tall.
    """

    bit_string: str
    """The bit string; does not include the `codepoint:` starting portion."""
    width: int | None
    """The width of the glyph. Equal to ``len(self.bit_string) // 4``."""
    image: PIL.Image.Image | None
    """
    An optional image of the glyph, comparable to a :class:`BitmapGlyph`.
    If possible, try not to use this.
    """
    bearings: tuple[int, int] | None
    """An optional tuple of the glyph's bearings, comparable to a :class:`BitmapGlyph`."""
    size_override: tuple[int, int] | None
    """
    An optional tuple of the glyph's size override.
    
    The first value is the starting column, and the second value is the ending column.
    When exporting, data outside of these columns will be discarded.
    If this is None, this is lazily-calculated to be ``(0, self.get_width())``.
    """
    program: list[str | int] | None = None
    """Optional Type 2 charstring program of the glyph."""

    def get_width(self) -> int:
        if self.width is None:
            self.width = len(self.bit_string) >> 2
        return self.width

    def get_image(self) -> PIL.Image.Image:
        """
        The image of the glyph.

        This is lazily-loaded.
        """
        if self.image is None:
            self.image = mcfonts.utils.unihex.bit_string_to_image(self.bit_string)
        return self.image

    def get_bit_string(self) -> str:
        """The bit string is the portion after the ``codepoint:``."""
        return self.bit_string

    def get_bearings(self) -> tuple[int, int]:
        """See :func:`mcfonts.utils.unihex.get_unihex_bearings`."""
        if self.bearings is None:
            self.bearings = mcfonts.utils.unihex.get_unihex_bearings(self.get_bit_string())
        return self.bearings

    def get_ascent(self) -> int:
        return 1

    def get_height(self) -> int:
        return 8

    def get_program(self) -> list[str | int] | None:
        if self.program is None:
            self.program = self.construct_program(
                # Em size (1000) divided by 10 = 100
                # divide this by scale (glyph height / JSON height) to get how big each "pixel" will translate to.
                125
            )
        return self.program

    def construct_program(self, pixel_size: int) -> list[str | int] | None:
        pen = fontTools.pens.t2CharStringPen.T2CharStringPen(0, {})
        glyph_width = self.get_width()
        size = self.get_size_override()
        index = 0
        bearings = self.get_bearings()
        for row in mcfonts.utils.unihex.bit_string_to_rows(self.get_bit_string()):
            for pixel in row:
                if pixel == UNIHEX_EXPORT_PIXEL_ON:
                    x_real = index % glyph_width
                    # - 1 to correct for baseline
                    y_real = (index // glyph_width) - 1
                    if x_real < min(size[0], 0) or x_real > min(size[1], glyph_width):
                        # Size overrides say to cut it off
                        continue
                    x_real -= bearings[0]
                    pen.moveTo(
                        (
                            x_real * pixel_size,
                            y_real * pixel_size,
                        )
                    )  # Left X, top right.

                    pen.lineTo(
                        (
                            (x_real + 1) * pixel_size,
                            y_real * pixel_size,
                        )
                    )  # Down Y, bottom left.

                    pen.lineTo(
                        (
                            (x_real + 1) * pixel_size,
                            (y_real - 1) * pixel_size,
                        )
                    )  # Right X, bottom right.

                    pen.lineTo(
                        (
                            x_real * pixel_size,
                            (y_real - 1) * pixel_size,
                        )
                    )  # Done with pixel.

                    pen.closePath()
                index += 1
        program: list[int | str] = pen.getCharString().program
        program[0] = (bearings[1] - bearings[0] + 1) * pixel_size  # Set the width correctly.
        return program

    def get_size_override(self) -> tuple[int, int]:
        """Size override is a tuple of 2 integers of the starting and ending columns for a glyph."""
        if self.size_override is None:
            self.size_override = (0, self.get_width())
        return self.size_override
