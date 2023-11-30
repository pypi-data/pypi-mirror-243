#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""A filter is a class used to control what characters and providers are included or not included when exporting."""
from __future__ import annotations

import enum

import unirange

import mcfonts.providers.base


@enum.unique
class Policy(enum.IntEnum):
    """How to handle filtered characters or providers."""

    INCLUDE = 0
    """Include **only** the predicate matches."""
    EXCLUDE = 1
    """Include **none** of the predicate matches."""


class Filter:
    """
    A filter used in exporting; this controls which glyphs are exported and under which conditions.

    Can either act as either an excluding filter, or an inclusive filter.
    """

    def __init__(
        self,
        filtered_characters: set[str] | str | None = None,
        filtered_providers: set[type[mcfonts.providers.base.Provider]] | None = None,
        character_policy: Policy = Policy.EXCLUDE,
        provider_policy: Policy = Policy.EXCLUDE,
    ):
        """
        Construct a filter.

        :param filtered_characters: An optional string or set of strings of the character to add to the filter.
        :param filtered_providers: An optional list of the types of providers to add to the filter.
        :param character_policy: The policy to use with regards to the character filter. Can also be an integer.
        :param provider_policy: The policy to use with regards to the provider filter. Can also be an integer.
        """
        if filtered_characters is None:
            filtered_characters = set()
        if isinstance(filtered_characters, str):
            filtered_characters = unirange.unirange_to_characters(filtered_characters)
        if filtered_providers is None:
            filtered_providers = set()

        assert filtered_characters is not None and not isinstance(filtered_characters, str)  # Mypy
        self.filtered_chars = filtered_characters
        self.char_policy: Policy = character_policy
        self.filtered_providers: set[type[mcfonts.providers.base.Provider]] = filtered_providers
        self.provider_policy: Policy = provider_policy

    def filter_character(self, character: str) -> bool:
        """
        Add `character` to the character filter.

        :param character: A string of 1 character.
        :returns: Boolean of success; True if character was added, False if it was already present.
        """
        if character in self.filtered_chars:
            return False
        self.filtered_chars.add(character)
        return True

    def unfilter_character(self, character: str) -> bool:
        """
        Remove `character` from the character filter.

        :param character: A string of 1 character.
        :returns: Boolean of success; True if character was removed, False if it wasn't present.
        """
        if character not in self.filtered_chars:
            return False
        self.filtered_chars.remove(character)
        return True

    def filter_provider(self, provider: type[mcfonts.providers.base.Provider]) -> bool:
        """
        Add `provider` to the provider filter.

        :param provider: A type of :data:`~mcfonts.providers.base.Provider`.
        :returns: Boolean of success; True if the provider was added, False if it was already present.
        """
        if provider in self.filtered_providers:
            return False
        self.filtered_providers.add(provider)
        return True

    def unfilter_provider(self, provider: type[mcfonts.providers.base.Provider]) -> bool:
        """
        Remove `provider` from the provider filter.

        :param provider: A type of :data:`~mcfonts.providers.base.Provider`.
        :returns: Boolean of success; True if provider was removed, False if it was never present.
        """
        if provider not in self.filtered_providers:
            return False
        self.filtered_providers.remove(provider)
        return True

    def set_character_policy(self, new_char_policy: Policy) -> None:
        """
        Set the character policy for how to handle filtering characters.

        :param new_char_policy: A value from the :class:`Policy` enum.
        """
        self.char_policy = new_char_policy

    def set_provider_policy(self, new_provider_policy: Policy) -> None:
        """
        Set the provider policy for how to handle filtering providers.

        :param new_provider_policy: A value from the :class:`Policy` enum.
        """
        self.provider_policy = new_provider_policy

    def check_character(self, character: str) -> bool:
        """
        Determine how `character` should be handled.

        - If character is **in** filtered characters **and** character policy is EXCLUDE, or
        - If character is **not in** filtered characters **and** character policy is INCLUDE:
            - *Skip character*

        :param character: A string of a character to determine filtering for.
        :returns: A boolean; True to skip, False to include normally.
        """

        return bool(
            self.filtered_chars
            and (
                (self.char_policy == Policy.EXCLUDE and character in self.filtered_chars)
                or (self.char_policy == Policy.INCLUDE and character not in self.filtered_chars)
            )
        )

    def check_provider(self, provider: type[mcfonts.providers.base.Provider]) -> bool:
        """
        Determine how `provider` should be handled.

        - If provider is **in** filtered providers **and** provider policy is EXCLUDE, or
        - If provider is **not in** filtered providers **and** provider policy is INCLUDE:
            - *Skip provider*

        :param provider: The type of the provider to determine filtering for; this is not an instance.
        :returns: A boolean; True to skip, False to include normally.
        """
        return bool(
            self.filtered_providers
            and (
                (provider in self.filtered_providers and self.provider_policy == Policy.EXCLUDE)
                or (provider not in self.filtered_providers and self.provider_policy == Policy.INCLUDE)
            )
        )
