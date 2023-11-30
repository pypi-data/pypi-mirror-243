#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""A ttf provider, including already-made TTF and OTF fonts."""
import collections.abc
import io
import os

import fontTools.ttLib

import mcfonts.providers.base
import mcfonts.utils.schemas


class TTFProvider(mcfonts.providers.base.Provider):
    """
    The ``ttf`` provider embeds already-compiled TrueType and OpenType fonts.

    mcfonts does not handle TTF providers by default, and they cannot be exported.
    """

    def __init__(
        self,
        provider: mcfonts.utils.types.TypedProviderTTF,
        origin: os.PathLike[str] | str,
        resource: bytes | None = None,
    ) -> None:
        self.contents = provider
        super().__init__("ttf", origin)
        if "skip" in self.contents:
            chars = []
            if isinstance(skip := self.get_contents().get("skip"), list):
                for line in skip:
                    chars.append(line)
            # Flatten into a string
            self.contents["skip"] = "".join(chars)
        self.validate()
        self.resource = resource
        if self.resource:
            self.font = fontTools.ttLib.TTFont(io.BytesIO(self.resource))
        else:
            self.font = None

    def pretty_print(self) -> str:
        return f"{self.get_icon()} ttf: {self.get_contents().get('file', 'no file')}"

    def print_info(self) -> None:
        super().print_info()
        if self.font:
            print(f"Characters: {self.font['maxp'].numGlyphs:,}")

    def construct_glyphs(self) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.Glyph]]:
        yield from []

    def yield_glyphs(self) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.Glyph]]:
        yield from []

    def yield_characters(self) -> collections.abc.Iterable[str]:
        yield from []

    def get_icon(self) -> str:
        return "𝐓"

    def get_pack_versions(self) -> tuple[int, None]:
        return 9, None

    def yield_glyphs_in_unirange(
        self, unirange_notation: str
    ) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.BitmapGlyph]]:
        yield from []

    def get_contents(self) -> mcfonts.utils.types.TypedProviderTTF:
        return self.contents
