"""Diamond kata.

Given a target letter, build a text diamond that begins with 'A', widens one
letter per row until the target letter is reached, then narrows back down to
'A'. The first and last rows hold a single 'A'; every other row holds exactly
two copies of its letter. Leading spaces align the rows so the figure is
symmetric both vertically and horizontally, the inner gap between the letter
pair grows by two spaces per row, and the widest row is as wide as the diamond
is tall. Lowercase input is normalised to uppercase; anything other than a
single letter A-Z is rejected with a ValueError.

Kata catalogued at tddbuddy.com/katas/diamond; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""


def diamond(letter: str) -> str:
    """Return the diamond figure for ``letter`` as a newline-joined string."""
    normalized = letter.upper()
    if len(letter) != 1 or len(normalized) != 1 or not ("A" <= normalized <= "Z"):
        raise ValueError("Input must be a single letter A-Z")

    size = ord(normalized) - ord("A")
    top_half: list[str] = []
    for offset in range(size + 1):
        row_letter = chr(ord("A") + offset)
        leading = " " * (size - offset)
        if offset == 0:
            top_half.append(leading + row_letter)
        else:
            inner = " " * (2 * offset - 1)
            top_half.append(leading + row_letter + inner + row_letter)

    return "\n".join(top_half + top_half[-2::-1])
