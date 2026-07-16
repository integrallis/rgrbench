"""Character Copy kata.

A ``Copier`` collaborates with a character source and a character destination. The
source and destination are the kata's own abstractions, supplied by the caller (in
tests, as small in-memory fakes); only the ``Copier`` is concrete here.

Rules:

- ``copy`` reads characters from the source one at a time with ``read_char`` and
  writes each to the destination with ``write_char``. Copying stops when a newline
  (``"\\n"``) is read; the newline itself is not written. Copying also stops if the
  source is exhausted and returns the empty string.
- Bonus batch operations: ``copy_multiple(count)`` reads chunks of ``count``
  characters with ``read_chars`` and writes them with ``write_chars``, never writing
  the newline or anything after it. It stops after a chunk containing a newline,
  after a short chunk (source exhausted), or after an empty chunk. Only non-empty
  chunks are written. ``count`` must be at least 1, otherwise
  ValueError("count must be at least 1") is raised.

Kata catalogued at tddbuddy.com/katas/character-copy; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from __future__ import annotations

from typing import Protocol

_NEWLINE = "\n"


class Source(Protocol):
    """Character source: ``read_char`` for single reads, ``read_chars`` for batch."""

    def read_char(self) -> str: ...

    def read_chars(self, count: int) -> str: ...


class Destination(Protocol):
    """Character sink: ``write_char`` for single writes, ``write_chars`` for batch."""

    def write_char(self, char: str) -> None: ...

    def write_chars(self, chars: str) -> None: ...


class Copier:
    """Copies characters from a source to a destination until a newline."""

    def __init__(self, source: Source, destination: Destination) -> None:
        self._source = source
        self._destination = destination

    def copy(self) -> None:
        """Copy characters one at a time, stopping at (and not writing) a newline.

        Only ``read_char``/``write_char`` are used. Stops as well if the source
        returns the empty string.
        """
        while True:
            char = self._source.read_char()
            if char == _NEWLINE or char == "":
                return
            self._destination.write_char(char)

    def copy_multiple(self, count: int) -> None:
        """Copy in chunks of ``count`` characters, never past the newline.

        Only ``read_chars``/``write_chars`` are used. A chunk containing a newline
        is written only up to the newline; a short or empty chunk ends copying.
        """
        if count < 1:
            raise ValueError("count must be at least 1")
        while True:
            chunk = self._source.read_chars(count)
            newline_index = chunk.find(_NEWLINE)
            if newline_index != -1:
                chunk = chunk[:newline_index]
                if chunk:
                    self._destination.write_chars(chunk)
                return
            if chunk:
                self._destination.write_chars(chunk)
            if len(chunk) < count:
                return
