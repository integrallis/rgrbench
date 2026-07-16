"""End-of-Line Trim kata.

trim removes trailing spaces and tabs from the end of every line of the
input while leaving everything else untouched: leading whitespace is kept,
interior whitespace is kept, and each line keeps its original terminator,
whether Unix ("\\n") or Windows ("\\r\\n"), even when the two styles are
mixed within one input. A carriage return that is not immediately followed
by a line feed is ordinary line content, not a terminator. Lines consisting
solely of a terminator pass through unchanged, as does text with no
trailing whitespace at all.

Kata catalogued at tddbuddy.com/katas/end-of-line-trim; implementation and
tests original (MIT), machine-authored from the specification, 2026.
"""


def trim(text: str) -> str:
    """Strip trailing spaces and tabs from each line, preserving terminators."""
    segments = text.split("\n")
    last_index = len(segments) - 1
    trimmed: list[str] = []
    for index, segment in enumerate(segments):
        if index < last_index and segment.endswith("\r"):
            trimmed.append(segment[:-1].rstrip(" \t") + "\r\n")
        elif index < last_index:
            trimmed.append(segment.rstrip(" \t") + "\n")
        else:
            trimmed.append(segment.rstrip(" \t"))
    return "".join(trimmed)
