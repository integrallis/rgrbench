"""Code Breaker kata.

A Mastermind-style feedback engine. The secret code is supplied to the constructor
(no randomness anywhere in this module); guesses are scored against it.

Rules:

- A code is a string of digits drawn from the alphabet "123456" by default; the
  core game uses 4 digits, and the bonus allows lengths of 4, 5 or 6 plus a custom
  alphabet.
- Feedback: one ``+`` per digit that is correct and in the correct position, then
  one ``-`` per digit that occurs in the secret but sits in the wrong position.
  All ``+`` symbols precede all ``-`` symbols.
- Exact matches are consumed first: a secret digit used by an exact match cannot
  also count as a partial match, and repeated guess digits only earn as many marks
  as the secret has unconsumed copies.
- Validation (ValueError): a secret outside 4-6 characters raises
  "code must be 4 to 6 characters long"; a secret with characters outside the
  alphabet raises "code may only contain characters from '<alphabet>'"; a guess
  whose length differs from the secret's raises "guess must be the same length as
  the secret". Guesses themselves are not alphabet-checked - the kata's own
  examples score guesses such as "5678" against a 1-6 secret, where out-of-range
  digits simply never match.

Kata catalogued at tddbuddy.com/katas/code-breaker; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from __future__ import annotations

from collections import Counter

_DEFAULT_ALPHABET = "123456"
_MIN_LENGTH = 4
_MAX_LENGTH = 6


class CodeBreaker:
    """Scores guesses against a fixed secret code."""

    def __init__(self, secret: str, alphabet: str = _DEFAULT_ALPHABET) -> None:
        self._alphabet = alphabet
        if not _MIN_LENGTH <= len(secret) <= _MAX_LENGTH:
            raise ValueError("code must be 4 to 6 characters long")
        self._require_in_alphabet(secret)
        self._secret = secret

    def guess(self, attempt: str) -> str:
        """Return feedback for ``attempt``: '+' per exact match, '-' per digit
        present in the secret but in the wrong position."""
        if len(attempt) != len(self._secret):
            raise ValueError("guess must be the same length as the secret")

        unmatched_pairs = [
            (secret_digit, guess_digit)
            for secret_digit, guess_digit in zip(self._secret, attempt)
            if secret_digit != guess_digit
        ]
        exact = len(self._secret) - len(unmatched_pairs)
        secret_rest = Counter(secret_digit for secret_digit, _ in unmatched_pairs)
        guess_rest = Counter(guess_digit for _, guess_digit in unmatched_pairs)
        partial = sum((secret_rest & guess_rest).values())
        return "+" * exact + "-" * partial

    def _require_in_alphabet(self, code: str) -> None:
        if any(char not in self._alphabet for char in code):
            raise ValueError(
                f"code may only contain characters from '{self._alphabet}'"
            )
