#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""
Formats that can be passed into :meth:`mcfonts.MinecraftFont.export`.

All functions defined here must have a signature of::

   (glyphs: dict[str, mcfonts.glyphs.Glyph], settings: ExportSettings) -> bytes


"""
import io
import typing

import fontTools.ttLib
import lxml.etree

import mcfonts.glyphs
import mcfonts.utils.exporting.opentype
import mcfonts.utils.exporting.unihex
import mcfonts.utils.exporting.yaff
import mcfonts.utils.unihex


class ExportSettings(typing.TypedDict):
    """A TypedDict of the options that can be passed to any export format function."""

    name: str | None
    """The name of the resulting font, not what its filename is. Optional."""
    include_credits: bool | None
    """Whether to include basic copyright information and credits in the font file. Optional."""
    author: str | None
    """The author(s) of the font. Optional."""
    license: str | None
    """An instance of :class:`mcfonts.filters.Filter`. If supplied, filter rules will be obeyed. Optional."""


def opentype(glyphs: dict[str, mcfonts.glyphs.Glyph], settings: ExportSettings) -> bytes:
    """
    Export to an OpenType font with Type 2 Charstring outlines.

    The font is crafted through a TTX file (font XML), and characters are added in tables and
    given self-descriptive name mappings: ``("u0954", "u1fae4", "u2605")``.

    For some fields, the font's name will be "Minecraft <font name>".

    The font mustn't contain over 65,535 characters, or else any additional characters
    won't be added, and the font will be saved prematurely.

    :param glyphs: A dictionary of ``{character: glyph}``.
    :param settings: A dictionary conforming to :class:`ExportSettings`.
    :returns: An OpenType file binary.
    """
    font_xml = lxml.etree.XML(mcfonts.utils.exporting.opentype.XML_FONT_TEMPLATE)
    characters: set[str] = set()
    # Set the space character pre-emptively
    mcfonts.utils.exporting.opentype.set_space_to_character(font_xml, " ", 4)

    try:
        for character, glyph in glyphs.items():
            mcfonts.utils.exporting.opentype.include_glyph(font_xml, glyph, character, characters)
            characters.add(character)
    except mcfonts.exceptions.GlyphLimitError:
        pass

    if "name" in settings:
        font_name = settings["name"].encode("ascii", "ignore").decode("utf-8")  # Ignore anything not in ASCII.
    else:
        font_name = mcfonts.constants.UNKNOWN_FIELD
    mcfonts.utils.exporting.opentype.set_font_name(font_xml, font_name)

    if "author" in settings:
        mcfonts.utils.exporting.opentype.add_namerecord_to_font(font_xml, settings["author"], 9)

    if "include_credits" in settings:
        mcfonts.utils.exporting.opentype.add_namerecord_to_font(
            font_xml, f"mcfonts: {font_name} Regular: {hash(font_xml)}", 3
        )
        mcfonts.utils.exporting.opentype.add_namerecord_to_font(font_xml, "mcfonts", 8)
        mcfonts.utils.exporting.opentype.add_namerecord_to_font(
            font_xml, "https://gitlab.com/whoatemybutter/mcfonts", 11
        )
    if "license" in settings:
        mcfonts.utils.exporting.opentype.add_namerecord_to_font(font_xml, settings["license"], 0)
        mcfonts.utils.exporting.opentype.add_namerecord_to_font(font_xml, settings["license"], 7)
        mcfonts.utils.exporting.opentype.add_namerecord_to_font(font_xml, settings["license"], 13)
    else:
        mcfonts.utils.exporting.opentype.add_namerecord_to_font(font_xml, "Unknown license", 0)
        mcfonts.utils.exporting.opentype.add_namerecord_to_font(font_xml, "Unknown trademark.", 7)
        mcfonts.utils.exporting.opentype.add_namerecord_to_font(
            font_xml,
            (
                "This font is under no explicit licensing. "
                "This font's author may have additional licensing terms, contact them."
            ),
            13,
        )

    mcfonts.utils.exporting.opentype.set_ulunicoderange(font_xml, characters)
    mcfonts.utils.exporting.opentype.set_font_times(font_xml)

    sstr = io.BytesIO()
    with fontTools.ttLib.ttFont.TTFont(recalcTimestamp=False, recalcBBoxes=False, sfntVersion="OTTO") as font:
        font.importXML(io.StringIO(lxml.etree.tostring(font_xml, encoding=str)))
        font.save(sstr)
    return sstr.getvalue()


def yaff(glyphs: dict[str, mcfonts.glyphs.Glyph], settings: ExportSettings) -> bytes:
    """
    Export to a YAFF font file.

    For details on the YAFF format, see https://github.com/robhagemans/monobit/blob/master/YAFF.md.
    There is no limit to the number of characters.

    :param glyphs: A dictionary of ``{character: glyph}``.
    :param settings: A dictionary conforming to :class:`ExportSettings`.
    :returns: A YAFF file encoded in UTF-8 **bytes**.
    """
    store: dict[str, str | int | dict[str, list[str]]] = {
        "name": settings.get("name", mcfonts.constants.UNKNOWN_FIELD),
        "family": settings.get("name", mcfonts.constants.UNKNOWN_FIELD),
        "author": settings.get("author", "Unknown author"),
        "copyright": settings.get("license", "Unknown copyright"),
        "source-format": "minecraft-java-font",
        "encoding": "unicode",
        "default-char": "notdef",
        "word-boundary": "u+0020",
    }

    if not settings.get("license"):
        store["notice"] = (
            "This font is under no explicit licensing. "
            "This font's author may have additional licensing terms, contact them."
        )

    # Set the space character pre-emptively
    mcfonts.utils.exporting.yaff.set_space_to_character(store, " ", 4)
    for character, glyph in glyphs.items():
        mcfonts.utils.exporting.yaff.include_glyph(store, glyph, character)

    ret = []

    for key, value in store.items():
        if isinstance(value, str):
            ret.append(f"{key}: {value}")
        elif isinstance(value, dict):
            ret.append(f"{key}:")
            for subkey, subvalue in value.items():
                if subkey == mcfonts.utils.exporting.yaff.YAFF_STORE_GLYPH_MAGIC:
                    for line in value.get(mcfonts.utils.exporting.yaff.YAFF_STORE_GLYPH_MAGIC, []):
                        ret.append(f"\t{line}")
                else:
                    ret.append(f"\t{subkey}: {subvalue}")

    return "\n".join(ret).encode("utf-8")


def unihex(glyphs: dict[str, mcfonts.glyphs.Glyph], settings: ExportSettings) -> bytes:
    """
    Export to a GNU Unifont .hex format.

    For details on the Unifont .hex format, see https://en.wikipedia.org/wiki/GNU_Unifont#.hex_format.
    There is no limit to the number of characters.

    :param glyphs: A dictionary of ``{character: glyph}``.
    :param settings: A dictionary conforming to :class:`ExportSettings`. This is not used.
    :returns: A .hex file encoded in UTF-8 **bytes**.
    """
    store: dict[str, str] = {}
    mcfonts.utils.exporting.unihex.set_space_to_character(store, " ", 4)
    for character, glyph in glyphs.items():
        mcfonts.utils.exporting.unihex.include_glyph(store, glyph, character)
    ret = []
    meta = []
    if "name" in settings:
        meta.append(f"# Name: {settings['name']}")
    if "author" in settings:
        meta.append(f"# Author: {settings['author']}")
    if "license" in settings:
        meta.append(f"# License: {settings['license']}")
    if "include_credits" in settings:
        meta.append("# Generated by mcfonts: https://gitlab.com/whoatemybutter/mcfonts")

    for codepoint, data in store.items():
        ret.append(f"{codepoint}:{data}")

    return ("\n".join(meta) + "\n".join(sorted(ret, key=mcfonts.utils.unihex.get_codepoint))).encode("utf-8")
