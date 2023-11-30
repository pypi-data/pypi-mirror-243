#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""Contains the basic parent provider that all functional providers subclass and inherit from."""
from __future__ import annotations

import abc
import collections.abc
import os
import typing

import mcfonts.constants
import mcfonts.glyphs


class Provider(abc.ABC):
    """The base provider class. All providers subclass this."""

    def __init__(
        self,
        provider_type: str,
        origin: os.PathLike[str] | str,
        chars_covered: set[str] | None = None,
    ):
        """
        Construct a Provider base class.

        :param provider_type: A string of the value in the JSON "type" field.
        :param origin: The absolute path to the provider's JSON file.
        :param chars_covered: A set of the individual characters covered by this provider.
        """

        if chars_covered is None:
            chars_covered = set()
        self.provider_type = provider_type
        self.chars_covered = chars_covered
        self.origin = origin

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}("{self.provider_type}", {self.get_contents()}, '
            f"{self.get_pack_versions()[0]},"
            f" {self.chars_covered})"
        )

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({len(self.chars_covered):,} chars)"

    def validate(self) -> None:
        """
        Specific tests for validating a provider.

        This function checks values to ensure that they're correct and in an acceptable range.

        If applicable, textures are checked to ensure all characters have a defined glyph,
        and that the dimensions are correct.

        Warnings are printed through :func:`mcfonts.logger.warning`.

        :returns: Nothing; problems are either raised or warned.
        """

    def print_info(self) -> None:
        """Print information about this provider."""
        print(f"Provider type: {mcfonts.constants.UNKNOWN_FIELD}")
        print(f"Characters covered: {len(self.chars_covered):,}")

    @abc.abstractmethod
    def pretty_print(self) -> str:
        """
        Return a short one line description of the provider.

        :returns: A string of the provider's info, normally ``<icon> <type>: <info,...>``.
        """
        return f"{self.get_icon()} {self.provider_type}"

    @abc.abstractmethod
    def construct_glyphs(self) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.Glyph]]:
        """
        Yield a tuple of (character, glyph) for every glyph available in the provider's resource.

        Some glyphs may be empty or have no content.

        :returns: A yield of ``(character, Glyph)``, or None if there are no glyphs.
        """

    @abc.abstractmethod
    def yield_characters(self) -> collections.abc.Iterable[str]:
        """
        Yield strings of the individual characters this provider supports.

        :returns: A yield of strings of length 1, or None if no characters are present.
        """

    @abc.abstractmethod
    def yield_glyphs(self) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.Glyph | None]]:
        """
        Yield a tuple of (character, glyph) for every glyph available in the provider's resource.

        This is different from :meth:`construct_glyphs`
        because it yields glyphs that have already been constructed and stored.

        :returns: A yield of ``(character, Glyph)``.
        """

    @abc.abstractmethod
    def get_icon(self) -> str:
        """
        Return a Unicode character that can be used to represent this provider in shorthand descriptions.

        :returns: A 1-character string.
        """
        return "?"

    @abc.abstractmethod
    def get_pack_versions(self) -> tuple[int, int | None]:
        """
        Return a tuple of the minimum and maximum pack versions for which this provider is valid.

        The first element is guaranteed to be an integer. There will always be a minimum version, even if it's 0.
        The second element may be an integer, or None. If it is None, there is no maximum version bound.

        :returns: A 2-element tuple of the minimum and maximum valid pack versions.
        """
        return 0, None

    @abc.abstractmethod
    def yield_glyphs_in_unirange(
        self, unirange_notation: str
    ) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.Glyph | None]]:
        """
        Given `unirange_notation`, return a dictionary of the requested characters to their glyphs.

        :param unirange_notation:
            A string representing the requested range of chars.
            See https://pypi.org/project/unirange/.
        :returns:
            A yield of the requested glyphs that match `unirange_notation`.
        """

    @abc.abstractmethod
    def get_contents(self) -> mcfonts.utils.types.TypedProviderDict:
        """
        Return the contents of the provider.

        :returns: Dictionary of the provider.
        """


def format_provider_message(provider: mcfonts.providers.base.Provider | dict[str, typing.Any], message: str) -> str:
    """
    Format a provider warning message properly, following Provider <type>: <message>.

    Calls :func:`mcfonts.utils.pretty_print_provider()`.

    :param provider:
        The provider, either as a dictionary or instance of :data:`mcfonts.providers.base.Provider`.
    :param message: The message to append at the end.
    :returns: The formatted warning message.
    """
    if isinstance(provider, dict):
        return f"Provider {pretty_print_provider_dictionary(provider)} {message}"
    return f"Provider {provider.pretty_print()} {message}"


def pretty_print_provider_dictionary(provider: dict[str, typing.Any]) -> str:
    """
    Format a provider information message properly, following ``<type><provider specific>``.

    Provider specific info:

     * ``bitmap``: ``<file> h <height> a <ascent>``
     * ``space``: nothing
     * ``legacy_unicode``: ``<template>``
     * ``ttf``: ``<file> s <shift0, 1>, sz <size>, o <oversample>, sk <skip>``

    :param provider:
        The provider as a dictionary, **not** an instance of :data:`mcfonts.providers.base.Provider`.
    :returns: The pretty provider information.
    """
    if (provider_type := provider.get("type", "")).lower() == "bitmap":
        return f'"bitmap": {provider.get("file", "no resource")}'
    if provider_type == "space":
        return '"space"'
    if provider_type == "legacy_unicode":
        return f'"legacy_unicode": {provider.get("template", "no template")}'
    if provider_type == "ttf":
        return (
            f'"ttf": {provider.get("file", "no file")}, s '
            f'{provider.get("shift", "[?, ?]")}, sz '
            f'{provider.get("size", "?")}, o '
            f'{provider.get("oversample", "?")}, sk '
            f'{provider.get("skip", "none")}'
        )
    if provider_type == "reference":
        return f'"reference": to {provider.get("id"), "nothing"}'
    if provider_type == "unihex":
        return f'"unihex": {provider.get("hex_file")}, so {len(provider.get("size_overrides", []))}'
    return f'"{provider_type}": ?'
