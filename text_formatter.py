#!/usr/bin/env python3
"""Apply text formatting rules to input text.

This script loads a user-provided Python module which must define a
`format_text(text: str) -> str` function. The input text is processed by
this function and the result is printed or written to an output file.
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import sys


def load_format_func(path: str):
    module_path = Path(path)
    if not module_path.exists():
        raise FileNotFoundError(f"Rules file not found: {path}")
    spec = importlib.util.spec_from_file_location("_rules_module", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore
    if not hasattr(module, "format_text"):
        raise AttributeError("Rules module must define a 'format_text' function")
    return getattr(module, "format_text")


def read_text(path: str | None) -> str:
    if path:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return sys.stdin.read()


def write_text(path: str | None, text: str) -> None:
    if path:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        print(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Format text using custom Python rules")
    parser.add_argument("-i", "--input", help="Input text file. Defaults to stdin.")
    parser.add_argument(
        "-r",
        "--rules",
        required=True,
        help="Python file containing a 'format_text(text)' function",
    )
    parser.add_argument("-o", "--output", help="Write result to a file instead of stdout")
    args = parser.parse_args()

    text = read_text(args.input)
    format_func = load_format_func(args.rules)
    result = format_func(text)
    write_text(args.output, result)


if __name__ == "__main__":
    main()
