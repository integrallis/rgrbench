"""String Transformer kata - chainable text transformation pipeline.

A ``StringTransformer`` wraps an initial string and offers chainable
operations that are applied in the order they are invoked; ``result()``
returns the transformed text. Operations: ``capitalise`` uppercases the
first letter of every word (other characters untouched); ``reverse``
reverses the whole string; ``remove_whitespace`` deletes all whitespace;
``snake_case`` lowercases the text and joins words with underscores;
``camel_case`` lowercases the first word and capitalises the following
words with separators removed; ``truncate(n)`` cuts the text to n
characters and appends an ellipsis only when something was cut;
``repeat(n)`` repeats the text n times joined by single spaces; and
``replace(target, replacement)`` replaces every occurrence. Words are
delimited by whitespace, hyphens, or underscores. Negative counts for
``truncate`` and ``repeat`` are rejected.

Kata catalogued at tddbuddy.com/katas/string-transformer; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

import re

_WORD_SPLIT = re.compile(r"[\s_-]+")


class StringTransformer:
    """Chainable string transformation pipeline applied in invocation order."""

    def __init__(self, text: str) -> None:
        self._text = text

    def result(self) -> str:
        """Return the text after all operations applied so far."""
        return self._text

    def capitalise(self) -> "StringTransformer":
        """Uppercase the first letter of each word, leaving the rest unchanged."""
        chars: list[str] = []
        at_word_start = True
        for char in self._text:
            chars.append(char.upper() if at_word_start else char)
            at_word_start = char.isspace() or char in "_-"
        self._text = "".join(chars)
        return self

    def reverse(self) -> "StringTransformer":
        """Reverse the entire string."""
        self._text = self._text[::-1]
        return self

    def remove_whitespace(self) -> "StringTransformer":
        """Remove all whitespace characters."""
        self._text = "".join(self._text.split())
        return self

    def snake_case(self) -> "StringTransformer":
        """Lowercase the text and join its words with underscores."""
        words = self._words()
        self._text = "_".join(word.lower() for word in words)
        return self

    def camel_case(self) -> "StringTransformer":
        """Lowercase the first word, capitalise later words, drop separators."""
        words = self._words()
        if not words:
            self._text = ""
            return self
        head = words[0].lower()
        tail = (word[0].upper() + word[1:].lower() for word in words[1:])
        self._text = head + "".join(tail)
        return self

    def truncate(self, length: int) -> "StringTransformer":
        """Cut the text to ``length`` characters, appending an ellipsis if cut."""
        if length < 0:
            raise ValueError("length must not be negative")
        if len(self._text) > length:
            self._text = self._text[:length] + "…"
        return self

    def repeat(self, times: int) -> "StringTransformer":
        """Repeat the text ``times`` times, joined by single spaces."""
        if times < 0:
            raise ValueError("times must not be negative")
        self._text = " ".join([self._text] * times)
        return self

    def replace(self, target: str, replacement: str) -> "StringTransformer":
        """Replace every occurrence of ``target`` with ``replacement``."""
        self._text = self._text.replace(target, replacement)
        return self

    def _words(self) -> list[str]:
        return [word for word in _WORD_SPLIT.split(self._text) if word]
