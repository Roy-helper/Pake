"""Example formatting rules.
This module defines a `format_text` function used by text_formatter.py.
"""


def format_text(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return '\n'.join(f"* {line}" for line in lines)
