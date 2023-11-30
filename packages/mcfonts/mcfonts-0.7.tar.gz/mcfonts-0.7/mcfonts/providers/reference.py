#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""A reference provider, including other fonts."""
import collections.abc
import os
import typing

import jsonschema
import unirange

import mcfonts.exceptions
import mcfonts.glyphs
import mcfonts.providers.base
import mcfonts.providers.bitmap
import mcfonts.providers.legacy_unicode
import mcfonts.providers.space
import mcfonts.providers.ttf
import mcfonts.providers.unihex
import mcfonts.utils.schemas

AnyProviderNotReference = (
    mcfonts.providers.bitmap.BitmapProvider
    | mcfonts.providers.space.SpaceProvider
    | mcfonts.providers.legacy_unicode.LegacyUnicodeProvider
    | mcfonts.providers.ttf.TTFProvider
    | mcfonts.providers.unihex.UnihexProvider
)
"""
A UnionType that does not include :class:`ReferenceProvider`.
"""

PROVIDER_SHORTCUT_MAP: dict[typing.Type[AnyProviderNotReference], str] = {
    mcfonts.providers.bitmap.BitmapProvider: "bt",
    mcfonts.providers.space.SpaceProvider: "sp",
    mcfonts.providers.legacy_unicode.LegacyUnicodeProvider: "lu",
    mcfonts.providers.ttf.TTFProvider: "ttf",
    mcfonts.providers.unihex.UnihexProvider: "uh",
}


class ReferenceProvider(mcfonts.providers.base.Provider):
    """
    The ``reference`` provider is used to include and load another font only once.

    It has one field, ``id``, which points to a font JSON to include.
    If more than 1 reference provider points to the same font JSON, it will be ignored.
    """

    def __init__(
        self,
        provider: mcfonts.utils.types.TypedProviderReference,
        origin: os.PathLike[str] | str,
        children: list[AnyProviderNotReference],
    ) -> None:
        if isinstance(children, self.__class__):
            raise mcfonts.exceptions.ReferenceChildError("a child provider cannot be another reference provider")
        self.contents = provider
        self.children = children

        super().__init__("reference", origin, set(self.yield_characters()))
        self.validate()

    def validate(self) -> None:
        jsonschema.validate(self.contents, mcfonts.utils.schemas.SCHEMA_PROVIDER_REFERENCE)

    def print_info(self) -> None:
        super().print_info()
        children = list(self.yield_children())
        print(f"Children: ({len(children)})")
        for child in children:
            print(f"\t- {str(child.__class__)}, {len(child.chars_covered):,} chars")

    def construct_glyphs(self) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.Glyph]]:
        for provider in self.yield_children():
            yield from provider.construct_glyphs()

    def yield_children(self) -> collections.abc.Iterable[AnyProviderNotReference]:
        """
        Yield all the providers that this reference provider is referring to.

        :returns: A yield of the contained providers.
        """
        yield from self.children

    def pretty_print(self) -> str:
        children_formatted = [
            PROVIDER_SHORTCUT_MAP.get(child.__class__, mcfonts.constants.UNKNOWN_FIELD) for child in self.children
        ]
        return f"{self.get_icon()} reference: {len(self.children):,} children: [{', '.join(children_formatted)}]"

    def yield_glyphs(self) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.Glyph | None]]:
        for child in self.yield_children():
            yield from child.yield_glyphs()

    def yield_characters(self) -> collections.abc.Iterable[str]:
        for child in self.children:
            yield from child.yield_characters()

    def get_icon(self) -> str:
        return "↩"

    def get_pack_versions(self) -> tuple[int, None]:
        return 15, None

    def yield_glyphs_in_unirange(
        self, unirange_notation: str
    ) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.Glyph | None]]:
        for child in self.yield_children():
            for character, glyph in zip(unirange.unirange_to_characters(unirange_notation), child.yield_glyphs()):
                assert isinstance(character, str) and isinstance(glyph, mcfonts.glyphs.Glyph)
                yield character, glyph

    def get_contents(self) -> mcfonts.utils.types.TypedProviderReference:
        return self.contents
