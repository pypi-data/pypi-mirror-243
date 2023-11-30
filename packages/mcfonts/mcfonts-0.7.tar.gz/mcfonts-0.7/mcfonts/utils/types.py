#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""Typed dictionaries for providers in JSON form. See :func:`typing.TypedDict`."""

import typing

TypedProviderBitmap = typing.TypedDict(
    "TypedProviderBitmap",
    {"type": str, "file": str, "height": typing.NotRequired[int], "ascent": int, "chars": list[str]},
)

TypedProviderSpace = typing.TypedDict("TypedProviderSpace", {"type": str, "advances": dict[str, float | int]})

TypedProviderLegacyUnicode = typing.TypedDict(
    "TypedProviderLegacyUnicode", {"type": str, "template": str, "sizes": str}
)

TypedProviderReference = typing.TypedDict("TypedProviderReference", {"type": str, "id": str})

TypedProviderTTF = typing.TypedDict(
    "TypedProviderTTF",
    {
        "type": str,
        "file": str,
        "shift": list[float | int],
        "size": float | int,
        "oversample": float | int,
        "skip": str | list[str],
    },
)

TypedProviderUnihexSizeOverride = typing.TypedDict(
    "TypedProviderUnihexSizeOverride", {"from": str, "to": str, "left": int, "right": int}
)

TypedProviderUnihex = typing.TypedDict(
    "TypedProviderUnihex",
    {"type": str, "hex_file": str, "size_overrides": list[TypedProviderUnihexSizeOverride]},
)

TypedProviderDict = typing.Union[
    TypedProviderUnihex,
    TypedProviderTTF,
    TypedProviderSpace,
    TypedProviderBitmap,
    TypedProviderLegacyUnicode,
    TypedProviderReference,
]

TypedProvidersDict = typing.TypedDict("TypedProvidersDict", {"providers": list[TypedProviderDict]})
