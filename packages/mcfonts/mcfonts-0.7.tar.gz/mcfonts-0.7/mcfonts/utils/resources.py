#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""Utilities for working with paths, resources, and loading resources."""
from __future__ import annotations

import collections.abc
import itertools
import os
import pathlib
import re
import zipfile

import PIL.Image
import PIL.ImageChops

import mcfonts.utils.image


def resolve_path(resource: str, base: pathlib.Path, subpath: str | None = None) -> pathlib.Path:
    """
    Resolve the correct path to the resource indicated by `path`, using `origin` as the base path to follow from.

    `origin` is where the original calling resource is;
    ``path`` is the requested resource path from the requesting resource.

    .. warning::

        This function doesn't return extensions.
        You must add those later.

    >>> resolve_path("mypath", pathlib.Path("~/mcfonts"), "textures")
    '~/mcfonts/textures/mypath'

    :param resource: An unresolved path to the resource.
    :param base: A real path to the central ``/assets/`` directory.
    :param subpath: Under what subdirectory in `base` to start looking for a resource. Optional.
    :returns: An absolute path of the requested resource.
    """
    temppath = str(resource).split(":", 1)
    if len(temppath) > 1:
        path_suffix = f"{temppath[0]}/{subpath}/{temppath[1]}" if subpath else f"{temppath[0]}/{temppath[1]}"
    else:
        path_suffix = f"minecraft/{subpath}/{temppath[0]}" if subpath else f"minecraft/{temppath[0]}"
    return expand_path(base.joinpath(path_suffix))


def expand_path(path: os.PathLike[str] | str) -> pathlib.Path:
    """
    Expand `path` with any variables or shortcuts, such as ``~``, ``$HOME``, etc.

    >>> expand_path("~/Documents")
    '/home/me/Documents'

    :param path: The unexpanded path.
    :returns: The expanded absolute path.
    """
    return pathlib.Path(path).expanduser()


def expand_resource_location(file_path: pathlib.Path) -> str:
    """
    Take any path to a texture file and return the Minecraft file string for it.

    :param file_path: A real path to any file.
    :returns: A string in the format of "<namespace>?:<dir/>?<file>".
    """
    splitted = re.split(f"[{os.path.sep}:]", str(file_path))
    try:
        assets = splitted.index("assets")
    except ValueError:
        assets = -1
    if (namespace := splitted[0]) == "minecraft":
        return f"{splitted[assets + 3]}/{'/'.join(splitted[assets + 4:])}"
    return f"{namespace}/{splitted[assets + 3]}/{'/'.join(splitted[assets + 4:])}"


def traverse_to_assets(path: pathlib.Path) -> pathlib.Path:
    """
    Traverse up the path until the ``/assets/`` directory is found, and then cut off the path there.

    :param path: The path to the file.
    :returns:
        The cut-off path up to the ``/assets/`` directory if found.
    :raises FileNotFoundError: If the ``/assets/`` directory could not be found.
    """
    current_path = path.absolute()

    n = 500
    while n > 0:
        if current_path.name == "assets":
            return current_path
        current_path = current_path.parent
        n -= 1
    raise FileNotFoundError


def divide_resource_by_grid(
    resource: PIL.Image.Image, row_column_count: tuple[int, int]
) -> collections.abc.Iterable[PIL.Image.Image | None]:
    """
    Yield images of the sections of a divided resource.

    Given a resource and number of characters in each row and column of that resource, yield every
    :class:`PIL.Image.Image` in that resource.

    If no data exists in a cell, yield None.

    :param resource: A :class:`PIL.Image.Image` of the font resource.
    :param row_column_count: A tuple of the number of characters in each row and column of `resource`.
    :returns: A yield of :class:`PIL.Image.Image` glyphs, or None.
    """
    height = resource.height // row_column_count[1]
    width = resource.width // row_column_count[0]
    for y_index in range(row_column_count[1]):
        for x_index in range(row_column_count[0]):
            if not mcfonts.utils.image.is_image_empty(
                glyph := resource.crop(
                    (
                        x_index * width,
                        y_index * height,
                        (x_index + 1) * width,
                        (y_index + 1) * height,
                    )
                )
            ):
                yield glyph
            else:
                yield None


def load_bitmap(file_name: str, base: pathlib.Path) -> PIL.Image.Image:
    """
    Companion function to :func:`load_resources` but specialized for bitmap provider resources.

    :param file_name: The name of the file to search for.
    :param base: The path to the base "assets" directory.
    :return: A :class:`PIL.Image.Image` instance.
    """
    with open(
        resolve_path(file_name, base, "textures"),
        "rb",
    ) as open_tempfile:
        image = PIL.Image.open(open_tempfile, formats=["png"])
        image.load()
    return image


def load_resources_legacy_unicode(
    template: str,
    sizes: str,
    base: pathlib.Path,
) -> collections.abc.Iterable[tuple[str, PIL.Image.Image | bytes]]:
    """
    Companion function to :func:`load_resources` but specialized for legacy_unicode provider resources.

    :param template: The template string, which must include "%s".
    :param sizes: The name of the "sizes" file.
    :param base: The real path to the base ``/assets/`` directory.
    :returns: A yield of {filename: image}.
    """
    template_parts: list[str] = template.split("%s", 1)
    # Skip surrogates
    for codepage in itertools.chain(range(0xD8), range(0xE0, 0x100)):
        template_name = f"{template_parts[0]}{codepage:02x}{template_parts[1]}"
        try:
            with open(
                resolve_path(template_name, base, "font"),
                "rb",
            ) as open_tempfile:
                image = PIL.Image.open(open_tempfile, formats=["png"])
                image.load()
                yield template_name, image
        except FileNotFoundError:
            # Page doesn't exist, acceptable error
            continue
    with open(
        resolve_path(sizes, base, "font"),
        "rb",
    ) as open_tempfile:
        yield sizes, open_tempfile.read()


def load_resources_unihex(file_name: str, base: pathlib.Path) -> collections.abc.Iterable[tuple[str, str]]:
    """
    Companion function to :func:`load_resources` but specialized for unihex provider resources.

    :param file_name: The path to the .zip file that contains the .hex files.
    :param base: The real path to the base ``/assets/`` directory.
    :returns: Yield of ``(filename, contents)``.
    """
    with open(resolve_path(file_name, base), "rb") as hex_zip:
        with zipfile.ZipFile(hex_zip) as memory_zip:
            for filename in memory_zip.namelist():
                if filename.lower().endswith(".hex"):  # Only care about .hex files.
                    yield filename, memory_zip.read(filename).decode("utf-8")


def align_font_texture(
    sheet: PIL.Image.Image, glyph_cell: tuple[int, int] = (8, 8), new_left_padding: int = 0
) -> PIL.Image.Image:
    """
    Align a font sheet's character's sheet to what `new_left_padding` is.

    This only shifts the character on the X axis (horizontally, left-right).

    :param sheet: The font sheet, not the individual glyph.
    :param glyph_cell: The dimensions of each individual character, their cell bounding box.
    :param new_left_padding: The distance away from the left edge the new character should be.
    :returns: The new font sheet.
    """
    height = sheet.height // glyph_cell[1]
    width = sheet.width // glyph_cell[0]
    for y_position in range(height):
        for x_position in range(width):
            # Glyph dimensions before alignment.
            dimensions = (
                x_position * glyph_cell[0],
                y_position * glyph_cell[1],
                (x_position + 1) * glyph_cell[0],
                (y_position + 1) * glyph_cell[1],
            )
            # Get the glyph itself.
            glyph = sheet.crop(dimensions)
            # If width is not the new padding, offset it by the difference.
            if (margin := mcfonts.utils.image.get_image_bearings(glyph)[0]) != new_left_padding:
                sheet.paste(PIL.ImageChops.offset(glyph, new_left_padding - margin, 0))
    return sheet
