"""Bank OCR kata.

Machine-printed account numbers arrive as ASCII art: each entry is three lines of 27
characters, and each of the nine digits occupies a 3x3 cell drawn with pipes and
underscores::

     _     _  _     _  _  _  _  _
    | |  | _| _||_||_ |_   ||_||_|
    |_|  ||_  _|  | _||_|  ||_| _|

Requirements:

- Parse an entry into its 9-digit account number; cells that match no digit are
  reported as ``?``.
- Validate account numbers with the checksum
  ``(d1*9 + d2*8 + ... + d9*1) mod 11 == 0`` where d1 is the leftmost digit.
- Classify an entry for reporting: the number alone when valid, with `` ILL``
  appended when it contains unreadable cells, or with `` ERR`` appended when it is
  readable but fails the checksum.
- Error correction: for an illegible or checksum-failing entry, consider every
  variant in which exactly one cell differs by a single segment (one pipe or
  underscore added or removed) and forms a digit. If exactly one variant yields a
  valid account number, report that number; if several do, report the parsed number
  followed by `` AMB`` and the sorted list of candidates; if none do, fall back to
  the `` ILL``/`` ERR`` classification.

Kata catalogued at tddbuddy.com/katas/bank-ocr; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from __future__ import annotations

_CELL_WIDTH = 3
_DIGITS_PER_ENTRY = 9
_LINE_WIDTH = _CELL_WIDTH * _DIGITS_PER_ENTRY

_DIGIT_GLYPHS: dict[str, str] = {
    " _ | ||_|": "0",
    "     |  |": "1",
    " _  _||_ ": "2",
    " _  _| _|": "3",
    "   |_|  |": "4",
    " _ |_  _|": "5",
    " _ |_ |_|": "6",
    " _   |  |": "7",
    " _ |_||_|": "8",
    " _ |_| _|": "9",
}


def parse_entry(entry: str) -> str:
    """Return the 9-character account number for a three-line entry.

    Unreadable cells are rendered as ``?``. Lines shorter than 27 characters are
    padded with spaces; a trailing blank line is tolerated. Raises
    ValueError("entry must have exactly three lines") otherwise.
    """
    return "".join(_DIGIT_GLYPHS.get(glyph, "?") for glyph in _entry_glyphs(entry))


def checksum_valid(account_number: str) -> bool:
    """Return True when the 9-digit account number satisfies the mod-11 checksum."""
    if len(account_number) != _DIGITS_PER_ENTRY or not account_number.isdigit():
        return False
    total = sum(
        int(digit) * weight
        for digit, weight in zip(account_number, range(_DIGITS_PER_ENTRY, 0, -1))
    )
    return total % 11 == 0


def account_status(entry: str) -> str:
    """Classify an entry: the number, ``<number> ILL`` or ``<number> ERR``."""
    account_number = parse_entry(entry)
    if "?" in account_number:
        return f"{account_number} ILL"
    if not checksum_valid(account_number):
        return f"{account_number} ERR"
    return account_number


def fix_entry(entry: str) -> str:
    """Report an entry after attempting single-segment error correction.

    A valid entry is reported as its account number. Otherwise every one-segment
    variation of every cell is tried: a unique valid candidate is reported directly,
    several candidates as ``<number> AMB [<sorted candidates>]``, and none as the
    plain `` ILL``/`` ERR`` classification.
    """
    account_number = parse_entry(entry)
    if "?" not in account_number and checksum_valid(account_number):
        return account_number

    candidates: set[str] = set()
    for position, glyph in enumerate(_entry_glyphs(entry)):
        for digit in _one_segment_digits(glyph):
            candidate = (
                account_number[:position] + digit + account_number[position + 1 :]
            )
            if "?" not in candidate and checksum_valid(candidate):
                candidates.add(candidate)

    if len(candidates) == 1:
        return candidates.pop()
    if candidates:
        return f"{account_number} AMB {sorted(candidates)}"
    return account_status(entry)


def _entry_glyphs(entry: str) -> list[str]:
    """Split a three-line entry into nine 9-character cell glyphs."""
    lines = entry.split("\n")
    while lines and lines[-1] == "":
        lines.pop()
    if len(lines) != 3:
        raise ValueError("entry must have exactly three lines")
    rows = [line.ljust(_LINE_WIDTH) for line in lines]
    return [
        "".join(row[cell * _CELL_WIDTH : (cell + 1) * _CELL_WIDTH] for row in rows)
        for cell in range(_DIGITS_PER_ENTRY)
    ]


def _one_segment_digits(glyph: str) -> list[str]:
    """Digits whose glyph differs from ``glyph`` in exactly one character."""
    return [
        digit
        for candidate, digit in _DIGIT_GLYPHS.items()
        if sum(a != b for a, b in zip(candidate, glyph)) == 1
    ]
