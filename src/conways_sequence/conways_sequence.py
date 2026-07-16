"""Conway's Sequence kata (look-and-say).

Each term of the sequence describes the previous term: scan it left to
right, collapse every run of identical digits into the run length followed
by the digit, and concatenate the results. Starting from "1" the sequence
runs 1, 11, 21, 1211, 111221, 312211, ... A run of ten or more identical
digits produces a multi-digit count, so ten 1s become "101".

next_term produces the single following term; look_and_say applies the
transformation a given number of times, with zero iterations returning the
seed unchanged. Terms must be non-empty strings of digits and the iteration
count must not be negative; violations raise ValueError.

Kata catalogued at tddbuddy.com/katas/conways-sequence; implementation and
tests original (MIT), machine-authored from the specification, 2026.
"""


def next_term(term: str) -> str:
    """Return the look-and-say reading of the given term."""
    _validate_term(term)
    pieces: list[str] = []
    run_digit = term[0]
    run_length = 0
    for digit in term:
        if digit == run_digit:
            run_length += 1
        else:
            pieces.append(f"{run_length}{run_digit}")
            run_digit = digit
            run_length = 1
    pieces.append(f"{run_length}{run_digit}")
    return "".join(pieces)


def look_and_say(seed: str, iterations: int) -> str:
    """Apply the look-and-say transformation to the seed the given number of times."""
    _validate_term(seed)
    if iterations < 0:
        raise ValueError("iterations must be non-negative")
    term = seed
    for _ in range(iterations):
        term = next_term(term)
    return term


def _validate_term(term: str) -> None:
    if not term or any(not "0" <= ch <= "9" for ch in term):
        raise ValueError("term must be a non-empty string of digits")
