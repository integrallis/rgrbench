"""Text Justification kata - fully justify text to a fixed column width.

``justify(text, width)`` breaks text into lines of the given width and
returns them as a list of strings. Words are delimited by any run of
whitespace (spaces, tabs, or line breaks). Lines are filled greedily;
on every line except the last, the padding spaces are distributed as
evenly as possible across the gaps between words, with the leftmost
gaps receiving the remainder (the LeetCode-68 convention). A line that
holds a single word and is not the last line is padded on the right to
the full width. The last line is left-aligned with single spaces and no
right padding. A word longer than the width overflows on its own line
rather than being split. Empty or whitespace-only text justifies to an
empty list; a None text or a width below one is an error.

Kata catalogued at tddbuddy.com/katas/text-justification; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""


def justify(text: str | None, width: int) -> list[str]:
    """Return ``text`` fully justified to ``width`` as a list of lines."""
    if text is None:
        raise ValueError("text must not be None")
    if width < 1:
        raise ValueError("width must be a positive integer")
    words = text.split()
    if not words:
        return []
    lines = _pack_greedily(words, width)
    justified = [_justify_line(line, width) for line in lines[:-1]]
    justified.append(" ".join(lines[-1]))
    return justified


def _pack_greedily(words: list[str], width: int) -> list[list[str]]:
    lines: list[list[str]] = []
    current: list[str] = []
    current_length = 0
    for word in words:
        needed = current_length + bool(current) + len(word)
        if current and needed > width:
            lines.append(current)
            current = []
            current_length = 0
        current_length += bool(current) + len(word)
        current.append(word)
    lines.append(current)
    return lines


def _justify_line(words: list[str], width: int) -> str:
    if len(words) == 1:
        return words[0].ljust(width)
    gaps = len(words) - 1
    total_spaces = width - sum(len(word) for word in words)
    base, extra = divmod(total_spaces, gaps)
    pieces: list[str] = []
    for index, word in enumerate(words[:-1]):
        pieces.append(word)
        pieces.append(" " * (base + (1 if index < extra else 0)))
    pieces.append(words[-1])
    return "".join(pieces)
