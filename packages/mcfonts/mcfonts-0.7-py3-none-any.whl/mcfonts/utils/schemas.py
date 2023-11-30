#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""JSON schemas for providers. Dynamically loaded from ``mcfonts/schemas/``."""
from __future__ import annotations

import json
import pathlib

with pathlib.Path(__file__).parent.parent.joinpath("schemas/provider.bitmap.schema.json").open() as __x:
    SCHEMA_PROVIDER_BITMAP = json.load(__x)
    """A schema to validate "bitmap" providers against."""

with pathlib.Path(__file__).parent.parent.joinpath("schemas/provider.space.schema.json").open() as __x:
    SCHEMA_PROVIDER_SPACE = json.load(__x)
    """A schema to validate "space" providers against."""

with pathlib.Path(__file__).parent.parent.joinpath("schemas/provider.legacy_unicode.schema.json").open() as __x:
    SCHEMA_PROVIDER_LEGACY_UNICODE = json.load(__x)
    """A schema to validate "legacy_unicode" providers against."""

with pathlib.Path(__file__).parent.parent.joinpath("schemas/provider.ttf.schema.json").open() as __x:
    SCHEMA_PROVIDER_TTF = json.load(__x)
    """A schema to validate "ttf" providers against."""

with pathlib.Path(__file__).parent.parent.joinpath("schemas/provider.unihex.schema.json").open() as __x:
    SCHEMA_PROVIDER_UNIHEX = json.load(__x)
    """A schema to validate "unihex" providers against."""

with pathlib.Path(__file__).parent.parent.joinpath("schemas/provider.reference.schema.json").open() as __x:
    SCHEMA_PROVIDER_REFERENCE = json.load(__x)
    """A schema to validate "reference" providers against."""

with pathlib.Path(__file__).parent.parent.joinpath("schemas/providers.schema.json").open() as __x:
    SCHEMA_PROVIDERS = json.load(__x)
    """A schema to validate the base font providers dictionary against."""
