"""URL shortener kata.

Requirements summary (paraphrased): a small in-memory library that turns long
URLs into short ones under a base such as ``https://short.url/``. Identifiers
are deterministic: by default they come from a sequential base-36 counter (the
first URL gets ``0``, the eleventh ``a``, the thirty-seventh ``10``), and a
custom identifier generator can be injected instead. ``translate`` converts in
both directions — a short URL yields its long URL and counts as a visit, a
long URL yields its short URL without counting. ``stats`` reports the short
URL, the long URL and the visit count for either form of a known URL. Bonus
behaviour included: invalid URLs (anything not ``http(s)://`` plus a
non-empty remainder) raise ``ValueError``; shortening the same long URL again
returns the existing short URL without consuming a new identifier; when a
clock is injected, each visit's timestamp is recorded and reported through
``stats`` and the ``log`` summary. No randomness and no wall-clock reads —
timestamps exist only when a clock is supplied.

Kata catalogued at tddbuddy.com/katas/url-shortener; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Iterator

_BASE36_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"
_VALID_SCHEMES = ("http://", "https://")


@dataclass(frozen=True)
class UrlStats:
    """Statistics for one shortened URL."""

    short_url: str
    long_url: str
    visits: int
    history: tuple[datetime, ...]


class UrlShortener:
    """In-memory URL shortener with deterministic identifiers."""

    def __init__(
        self,
        base_url: str = "https://short.url/",
        id_generator: Iterator[str] | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self._base_url = base_url
        self._ids = id_generator if id_generator is not None else _sequential_ids()
        self._clock = clock
        self._short_to_long: dict[str, str] = {}
        self._long_to_short: dict[str, str] = {}
        self._visits: dict[str, int] = {}
        self._history: dict[str, list[datetime]] = {}

    def shorten(self, long_url: str) -> str:
        """Return a short URL for ``long_url``, reusing any existing mapping."""
        _validate_url(long_url)
        existing = self._long_to_short.get(long_url)
        if existing is not None:
            return existing
        short_url = self._base_url + next(self._ids)
        self._short_to_long[short_url] = long_url
        self._long_to_short[long_url] = short_url
        self._visits[short_url] = 0
        self._history[short_url] = []
        return short_url

    def translate(self, url: str) -> str:
        """Convert between short and long URLs.

        A short URL returns its long URL and counts as a visit; a long URL
        returns its short URL without counting.
        """
        long_url = self._short_to_long.get(url)
        if long_url is not None:
            self._visits[url] += 1
            if self._clock is not None:
                self._history[url].append(self._clock())
            return long_url
        short_url = self._long_to_short.get(url)
        if short_url is not None:
            return short_url
        raise ValueError(f"Unknown URL: {url!r}")

    def stats(self, url: str) -> UrlStats:
        """Return the statistics for a known short or long URL."""
        short_url = self._resolve_short(url)
        return UrlStats(
            short_url=short_url,
            long_url=self._short_to_long[short_url],
            visits=self._visits[short_url],
            history=tuple(self._history[short_url]),
        )

    def log(self, url: str) -> str:
        """Return a text summary: short URL, long URL, visits and history."""
        record = self.stats(url)
        lines = [
            f"short_url: {record.short_url}",
            f"long_url: {record.long_url}",
            f"visits: {record.visits}",
        ]
        lines.extend(moment.isoformat(sep=" ") for moment in record.history)
        return "\n".join(lines)

    def _resolve_short(self, url: str) -> str:
        if url in self._short_to_long:
            return url
        short_url = self._long_to_short.get(url)
        if short_url is not None:
            return short_url
        raise ValueError(f"Unknown URL: {url!r}")


def _sequential_ids() -> Iterator[str]:
    counter = 0
    while True:
        yield _to_base36(counter)
        counter += 1


def _to_base36(number: int) -> str:
    if number == 0:
        return _BASE36_ALPHABET[0]
    digits: list[str] = []
    while number > 0:
        number, remainder = divmod(number, 36)
        digits.append(_BASE36_ALPHABET[remainder])
    return "".join(reversed(digits))


def _validate_url(url: str) -> None:
    for scheme in _VALID_SCHEMES:
        if url.startswith(scheme) and len(url) > len(scheme):
            return
    raise ValueError(f"Invalid URL: {url!r}")
