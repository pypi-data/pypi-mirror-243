#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""Command-line tool front-end for mcfonts."""
from __future__ import annotations

import argparse
import inspect
import os.path
import sys

import PIL.Image

import mcfonts.utils.resources

if __name__ == "__main__":

    def __check_dir(path: str) -> str:
        if os.path.exists(path):
            return path
        raise FileNotFoundError(path)

    INPUT_HELP = (
        "Path to folder, JSON, or ZIP file of font. "
        "If folder, this folder must be a resource pack. "
        "If JSON, this file must be a font JSON file. "
        "If ZIP, this file must be a resource pack archive. "
        "If -, stdin is used."
    )

    parser = argparse.ArgumentParser(
        description="""
        mcfonts is a versatile, fast, and extensible package for working with Minecraft fonts.
        
        The CLI front-end does not expose every possible option.
        For more in-depth usage, import the mcfonts module in Python.
        """
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="mcfonts " + ".".join(str(x) for x in mcfonts.__version__),
    )

    subparsers = parser.add_subparsers(title="Functions")

    export_parser = subparsers.add_parser("export", help="export to another font format")
    export_parser.add_argument(
        "input",
        type=__check_dir,
        default=(None if sys.stdin.isatty() else sys.stdin),
        help=INPUT_HELP,
    )
    export_parser.add_argument(
        "outfile", type=argparse.FileType("wb"), default=sys.stdout, help="Where to write the file to."
    )
    export_parser.add_argument("-n", "--name", help="Name of the font.", default=mcfonts.constants.UNKNOWN_FIELD)
    export_parser.add_argument("-c", "--credits", type=bool, help="Whether to embed the mcfonts credits.", default=True)
    export_parser.add_argument(
        "-a",
        "--author",
        help="Author of the font.",
    )
    export_parser.add_argument("-l", "--license", type=bool, help="License of the font.", required=False)
    export_parser.add_argument(
        "format",
        help="What format to export to.",
        default="opentype",
        # Dynamically get all functions in mcfonts.export_formats
        choices={x[0] for x in inspect.getmembers(mcfonts.export_formats, inspect.isfunction)},
        nargs="?",
    )
    export_parser.set_defaults(export=True)

    info_parser = subparsers.add_parser("info", help="print information about a font file")
    info_parser.add_argument(
        "input",
        type=argparse.FileType(),
        default=(None if sys.stdin.isatty() else sys.stdin),
        help=INPUT_HELP,
    )
    info_parser.add_argument(
        "-t",
        "--table-chars",
        action="store_true",
        default=False,
        help="to put characters into a formatter table or put in single list",
    )
    info_parser.add_argument(
        "-s",
        "--summary-only",
        action="store_true",
        default=False,
        help="to print only a small summary",
    )
    info_parser.set_defaults(info=True)

    compact_parser = subparsers.add_parser("compact", help="fit the glyphs in the minimum amount of space needed")
    compact_parser.add_argument(
        "input",
        type=argparse.FileType("rb"),
        default=(None if sys.stdin.isatty() else sys.stdin),
        help="Path to PNG file.",
    )
    compact_parser.add_argument(
        "char-counts",
        nargs=2,
        type=int,
        default=(16, 16),
        help="Two numbers of the characters in each row and column of the input file.",
    )
    compact_parser.add_argument(
        "-c",
        "--chars-in-row",
        type=int,
        default=16,
        help="The desired number of glyphs to put in one row, set to 0 for square. Default is 16.",
    )
    compact_parser.add_argument("outfile", type=argparse.FileType("wb"), default=sys.stdout)
    compact_parser.set_defaults(compact=True)

    compare_parser = subparsers.add_parser("compare", help="compare two fonts")
    compare_parser.add_argument(
        "input1",
        type=argparse.FileType("rb"),
        default=(None if sys.stdin.isatty() else sys.stdin),
        help=INPUT_HELP,
    )
    compare_parser.add_argument(
        "input2",
        type=argparse.FileType("rb"),
        default=(None if sys.stdin.isatty() else sys.stdin),
        help=INPUT_HELP,
    )
    compare_parser.add_argument(
        "-s",
        "--swap",
        action="store_true",
        default=(None if sys.stdin.isatty() else sys.stdin),
        help="swap the order of fonts compared",
    )
    compare_parser.set_defaults(compare=True)

    vargs = vars(parser.parse_args(args=None if sys.argv[1:] else ["--help"]))

    if vargs.get("export"):
        to_write = mcfonts.from_java_ambiguous(vargs["input"]).export(
            getattr(mcfonts.export_formats, vargs["format"]) or mcfonts.export_formats.opentype,
            {
                "name": vargs["name"],
                "include_credits": vargs["include_credits"],
                "author": vargs["author"],
                "license": vargs["license"],
            },
        )
        vargs["outfile"].write(to_write)
    elif vargs.get("info"):
        mcfonts.from_java_ambiguous(vargs["input"].name).print_info(
            vargs.get("table_chars", False), vargs.get("summary_only", False)
        )
    elif vargs.get("compact"):
        resource = PIL.Image.open(vargs["input"])
        cell_size = tuple(vargs["char_counts"])
        compacted = mcfonts.compacting.compact_images(
            list(mcfonts.utils.resources.divide_resource_by_grid(resource, cell_size)),
            vargs["chars_in_row"](resource.width // cell_size[0], resource.height // cell_size[1]),
        )
        compacted[0].save(vargs["outfile"])
        print(compacted[1])
    elif vargs.get("compare"):
        font1 = mcfonts.from_java_ambiguous(vargs["input1"].name)
        font2 = mcfonts.from_java_ambiguous(vargs["input2"].name)
        if vargs.get("swap", False):
            font2.compare(font1)
        else:
            font1.compare(font2)
