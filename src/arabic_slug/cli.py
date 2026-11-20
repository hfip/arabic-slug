"""Command line interface for arabic-slug."""

from __future__ import annotations

import argparse
import sys
from typing import Iterable, Optional

from . import __version__
from .slugify import slugify

MODES = ("translit", "keep")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="arabic-slug",
        description="Make URL slugs out of Arabic text, either transliterated or kept in Arabic.",
    )
    parser.add_argument("text", nargs="*", help="text to slugify")
    parser.add_argument(
        "--mode",
        choices=MODES,
        default="translit",
        help="translit (default) gives ASCII, keep leaves Arabic letters in place",
    )
    parser.add_argument("--separator", default="-", help="separator between words (default: -)")
    parser.add_argument("--max-length", type=int, default=80, help="truncate at a word boundary")
    parser.add_argument("--keep-case", action="store_true", help="do not lowercase")
    parser.add_argument("--stdin", action="store_true", help="read lines from stdin")
    parser.add_argument("-V", "--version", action="version", version="arabic-slug " + __version__)
    return parser


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.stdin:
        values = [line.strip() for line in sys.stdin if line.strip()]
    else:
        values = args.text

    if not values:
        parser.print_usage()
        return 2

    for value in values:
        print(
            slugify(
                value,
                mode=args.mode,
                separator=args.separator,
                max_length=args.max_length,
                lowercase=not args.keep_case,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
