#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""Functions for working with Unicode characters, codepoints, and surrogate pairs."""

from __future__ import annotations

import unicodedata

INVISIBLE_CHARACTERS = {
    "\u034F",
    "\u115F",
    "\u1160",
    "\u17B4",
    "\u17B5",
    "\u2800",
    "\u3164",
    "\uFFA0",
    "\U0001D159",
    "\U0001d173",
    "\U0001d174",
    "\U0001d175",
    "\U0001d176",
    "\U0001d177",
    "\U0001d178",
    "\U0001d179",
    "\U0001d17a",
}
"""A set of characters that do not have a visual representation under most fonts."""


def character_to_surrogates(character: str) -> tuple[int, int]:
    r"""
    Convert one character into 2 integers of its UTF-16 surrogate codepoints.

    A surrogate pair are two characters that represent another character.
    Since UTF-16 only stores characters from 0 to 0xFFFF,
    chars past 0xFFFF need to be split into two codepoints below 0xFFFF.

    This is useful even in plaintext Unicode notation, because ``\u1D105`` is not a single
    character, it's two (``ᴐ5``, not ``𝄅``).

    :param character:
        A single character.
    :returns:
        A surrogate pair, in codepoints of the surrogates.
    """
    codepoint = ord(character)
    codepoint -= 0x10000
    return 0xD800 + (codepoint >> 10), 0xDC00 + (codepoint & 0x3FF)


def surrogates_to_character(surrogates: tuple[int, int]) -> str:
    """
    Given a tuple of surrogate chars, return the single codepoint they combine to.

    :param surrogates:
        A tuple of two surrogate codepoints.
    :returns:
        A single character of the resulting surrogates.
    """
    return chr((surrogates[0] - 0xD800) * 0x400 + (surrogates[1] - 0xDC00) + 0x10000)


def is_character_invisible(character: str) -> bool:
    """
    Return if `character` would be invisible (might not have glyph info).

    A character is "invisible" if it:

    * Is in these categories: ``Cf, Cc, Zl, Zs, Zp``.
    * Is equal to these codepoints:
      ``2800, 034F, 115F, 1160, 17B4, 17B5, 3164, FFA0, 1D159, 1D174, 1D176, 1D177, 1D178, 1D17A``.
    * Is private use.

    You can visit `<https://invisible-characters.com/>`_ if you would like to see the list.

    .. warning::

        "Invisibility" is not a valid Unicode standard property.
        For standardization purposes, do use utilize this outside of this library.

    :param character:
        A single character.
    :returns:
        If `char` is a spacing character.
    """
    return (
        unicodedata.category(character) in ("Cf", "Cc", "Zl", "Zs", "Zp")
        or character in INVISIBLE_CHARACTERS
        or is_character_private_use(character)
    )


def is_character_private_use(character: str) -> bool:
    """
    Return if `character` is in a Private Use Area (PUA).

    A PUA is one of these codepoint ranges:

    * U+E000 to U+F8FF
    * U+F0000 to U+FFFFD
    * U+100000 to U+10FFFD

    :param character:
        A single character.
    :returns:
        If `character` is in a Private Use Area.
    """
    codepoint = ord(character)
    return (0xE000 <= codepoint <= 0xF8FF) or (0xF0000 <= codepoint <= 0xFFFFD) or (0x100000 <= codepoint <= 0x10FFFD)


def str_to_tags(string: str) -> str:
    """
    Return a version of `string` with all alphanumeric characters changed into Tags.

    Given `string`, which should have only ASCII characters, turn it into that same string but every character is a\
    Tag of itself, instead.

    See https://en.wikipedia.org/wiki/Tags_(Unicode_block).

    :param string: Any string; it should have ASCII characters.
    :returns: `string` but with ASCII characters replaced with their Tag equivalents.
    """
    return "".join(chr(ord(ch) + 0xE0000) for ch in string if ord(ch) < 0x7F)


def pretty_print_character(character: str) -> str:
    r"""
    Return relevant info about a character into a string, following ``U+<codepoint> <name> <character>``.

    >>> pretty_print_character('\u2601')
    'U+2601: CLOUD ☁'
    >>> pretty_print_character('\ue000')
    'U+E000: <PRIVATE USE> \ue000'
    >>> pretty_print_character('\U0001f400')
    'U+1F400: RAT 🐀'
    >>> pretty_print_character('\b')
    'U+0008: BACKSPACE ␈'
    >>> pretty_print_character('\b')
    'U+0008: BACKSPACE ␈'

    :param character: A single character.
    :returns: The pretty character string.
    """
    codepoint = ord(character)
    try:
        if unicodedata.category(character) == "Cc":
            return (
                f"U+{codepoint:04X}: "
                f"{unicodedata.name(chr(ord(character) + 0x2400)).split('SYMBOL FOR ')[1]} "
                f"{chr(ord(character) + 0x2400)}"
            )
        return f"U+{codepoint:04X}: {unicodedata.name(character)} {character}"
    except (ValueError, IndexError):
        if is_character_private_use(character):
            return f"U+{codepoint:04X}: <PRIVATE USE> {character}"
        return f"U+{codepoint:04X}: {character}"


def is_codepoint_surrogate(codepoint: int) -> bool:
    """
    Return if a codepoint is part of a high or low surrogate pair.

    :param codepoint: An integer of the character's codepoint.
    :return: If it's within ``0xD800..=0xDC00``.
    """
    return 0xD800 <= codepoint <= 0xDC00
