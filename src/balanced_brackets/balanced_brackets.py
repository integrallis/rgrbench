"""Balanced Brackets kata.

Decide whether a string of square brackets is balanced: every opening "["
must be matched by a later closing "]", pairs must nest correctly, and a
closing bracket may never appear before its opener. The empty string counts
as balanced. Because only one bracket type is involved, a single-pass depth
counter suffices: the depth must never go negative and must end at zero.
Input is assumed to contain only brackets.

Kata catalogued at tddbuddy.com/katas/balanced-brackets; implementation and
tests original (MIT), machine-authored from the specification, 2026.
"""


def is_balanced(text: str) -> bool:
    """Return True when every bracket in the text is matched and well nested."""
    depth = 0
    for ch in text:
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0
