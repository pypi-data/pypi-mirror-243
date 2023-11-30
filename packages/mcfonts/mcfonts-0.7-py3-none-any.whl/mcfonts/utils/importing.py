#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""Utilities for importing provider dictionaries."""
from __future__ import annotations

import collections.abc
import copy
import json
import pathlib
import typing

import jsonschema
import PIL

import mcfonts.exceptions
import mcfonts.providers
import mcfonts.providers.reference
import mcfonts.utils


def load_all(
    providers: list[dict[str, typing.Any]],
    json_path: pathlib.Path,
    strict: bool = False,
    mode: str = "LA",
) -> collections.abc.Iterable[mcfonts.providers.base.Provider]:
    """
    Load every provider in the list `providers`.

    :param providers:
        A list of dictionaries of providers.
        This should be the value of the "providers" key in the JSON file.
    :param json_path: The path to the JSON file at which this provider JSON is from.
    :param strict: Whether to raise or warn (and continue) on exceptions.
    :param mode:
        What "mode" to load bitmap resources in.

        * ``"LA"`` - Grayscale
        * ``"RGBA"`` - Color

    :returns: A yield of Providers.
    """
    for provider in copy.deepcopy(providers):
        yield load_provider(provider, json_path, strict, mode)


def load_provider(
    provider: dict[str, typing.Any],
    json_path: pathlib.Path,
    strict: bool = False,
    mode: str = "LA",
) -> mcfonts.providers.base.Provider:
    """
    Load a specific provider dictionary and return the equivalent Provider class.
    Performs JSON schema validation.

    :param provider: A dictionary of a provider.
    :param json_path: The real path to the JSON file at which this provider JSON is from.
    :param strict: Whether to raise or warn (and continue) on exceptions.
    :param mode:
        What "mode" to load bitmap resources in.

        * ``"LA"`` - Grayscale
        * ``"RGBA"`` - Color

    :returns: A Provider instance.
    """
    provider_type = provider.get("type", "")
    try:
        if provider_type == "bitmap":
            jsonschema.validate(provider, mcfonts.utils.schemas.SCHEMA_PROVIDER_BITMAP)
            typed_bitmap_provider: mcfonts.utils.types.TypedProviderBitmap = {
                "type": "bitmap",
                "file": provider["file"],
                "height": provider.get("height", 8),
                "ascent": provider["ascent"],
                "chars": provider["chars"],
            }
            return mcfonts.providers.bitmap.BitmapProvider(
                typed_bitmap_provider,
                json_path,
                mcfonts.utils.resources.load_bitmap(
                    typed_bitmap_provider["file"], mcfonts.utils.resources.traverse_to_assets(json_path)
                ),
            )
        elif provider_type == "legacy_unicode":
            jsonschema.validate(provider, mcfonts.utils.schemas.SCHEMA_PROVIDER_LEGACY_UNICODE)
            typed_legacy_unicode_provider: mcfonts.utils.types.TypedProviderLegacyUnicode = {
                "type": "legacy_unicode",
                "template": provider["template"],
                "sizes": provider["sizes"],
            }
            return mcfonts.providers.legacy_unicode.LegacyUnicodeProvider(
                typed_legacy_unicode_provider,
                json_path,
                dict(
                    mcfonts.utils.resources.load_resources_legacy_unicode(
                        typed_legacy_unicode_provider["template"],
                        typed_legacy_unicode_provider["sizes"],
                        mcfonts.utils.resources.traverse_to_assets(json_path),
                    )
                ),
            )
        elif provider_type == "space":
            jsonschema.validate(provider, mcfonts.utils.schemas.SCHEMA_PROVIDER_SPACE)
            typed_space_provider: mcfonts.utils.types.TypedProviderSpace = {
                "type": "space",
                "advances": provider["advances"],
            }
            return mcfonts.providers.space.SpaceProvider(typed_space_provider, json_path)
        elif provider_type == "ttf":
            jsonschema.validate(provider, mcfonts.utils.schemas.SCHEMA_PROVIDER_TTF)
            typed_ttf_provider: mcfonts.utils.types.TypedProviderTTF = {
                "type": "ttf",
                "file": provider["file"],
                "shift": provider["shift"],
                "size": provider["size"],
                "oversample": provider["oversample"],
                "skip": provider["skip"],
            }
            with open(
                mcfonts.utils.resources.resolve_path(
                    typed_ttf_provider["file"], mcfonts.utils.resources.traverse_to_assets(json_path), "font"
                ),
                "rb",
            ) as open_tempfile:
                ttf = open_tempfile.read()
            return mcfonts.providers.ttf.TTFProvider(typed_ttf_provider, json_path, ttf)
        elif provider_type == "unihex":
            jsonschema.validate(provider, mcfonts.utils.schemas.SCHEMA_PROVIDER_UNIHEX)
            typed_unihex_provider: mcfonts.utils.types.TypedProviderUnihex = {
                "type": "unihex",
                "hex_file": provider["hex_file"],
                "size_overrides": provider["size_overrides"],
            }
            return mcfonts.providers.unihex.UnihexProvider(
                typed_unihex_provider,
                json_path,
                dict(
                    mcfonts.utils.resources.load_resources_unihex(
                        typed_unihex_provider["hex_file"], mcfonts.utils.resources.traverse_to_assets(json_path)
                    )
                ),
            )
        elif provider_type == "reference":
            jsonschema.validate(provider, mcfonts.utils.schemas.SCHEMA_PROVIDER_REFERENCE)
            typed_reference_provider: mcfonts.utils.types.TypedProviderReference = {
                "type": "reference",
                "id": provider["id"],
            }
            # Create any child providers first
            with open(
                temp_recursive_path := mcfonts.utils.resources.resolve_path(
                    typed_reference_provider["id"] + ".json",
                    mcfonts.utils.resources.traverse_to_assets(json_path),
                    "font",
                ),
                encoding="utf-8",
            ) as temp_recursive_file:
                data = json.load(temp_recursive_file, strict=strict)
            children = list(
                load_all(data.get("providers", {}), temp_recursive_path, strict, mode)
            )  # This acts recursively.
            if any(isinstance(child, mcfonts.providers.reference.ReferenceProvider) for child in children):
                raise mcfonts.exceptions.ReferenceChildError()
            return mcfonts.providers.reference.ReferenceProvider(
                typed_reference_provider,
                json_path,
                children,  # type: ignore[arg-type] # children will never be list[Provider]
            )
        elif provider_type in {"mcfonts:options", "options"}:
            raise mcfonts.exceptions.ProviderError("Options providers are longer accepted and must be removed.")
    except PIL.UnidentifiedImageError as exception:
        if strict:
            raise exception
        mcfonts.logger.warning(
            mcfonts.providers.base.format_provider_message(provider, "has invalid file; must be PNG.")
        )

    except FileNotFoundError as exception:
        if strict:
            # Missing files not allowed, raising exception
            raise exception
            # Missing files are ignored
        mcfonts.logger.warning(
            mcfonts.providers.base.format_provider_message(
                provider, f'file "{exception.filename}" does not exist, skipping.'
            )
        )

    raise mcfonts.exceptions.ProviderError(f'Unknown provider "{provider_type}".')
