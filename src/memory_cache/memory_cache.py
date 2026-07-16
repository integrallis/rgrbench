"""In-memory key-value cache with LRU eviction and time-to-live expiry.

The cache stores string values under string keys, following the dictionary
storage paradigm. Every entry goes stale once its time-to-live (TTL) has
elapsed; stale entries behave as absent and can also be purged explicitly
with a sweep. The cache holds a bounded number of entries — 100 by default,
with a default TTL of 60 seconds; both are configurable, and non-positive
values are rejected. When an insert would exceed capacity, the
least-recently-used entry is evicted to make room for the incoming value.
Reading or writing a key counts as a use for recency purposes, and writing
a key refreshes its TTL. All timing is read from an injected clock callable
(returning seconds as a float), so behaviour is fully deterministic.

Kata catalogued at tddbuddy.com/katas/memory-cache; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from collections import OrderedDict
from collections.abc import Callable


class MemoryCache:
    """Bounded key-value cache with LRU eviction and per-entry TTL expiry."""

    DEFAULT_CAPACITY = 100
    DEFAULT_TTL = 60.0

    def __init__(
        self,
        clock: Callable[[], float],
        capacity: int = DEFAULT_CAPACITY,
        ttl: float = DEFAULT_TTL,
    ) -> None:
        if capacity < 1:
            raise ValueError(f"capacity must be at least 1, got [{capacity}]")
        if ttl <= 0:
            raise ValueError(f"ttl must be positive, got [{ttl}]")
        self._clock = clock
        self._capacity = capacity
        self._ttl = float(ttl)
        # key -> (value, expires_at); ordered from least- to most-recently used.
        self._entries: OrderedDict[str, tuple[str, float]] = OrderedDict()

    @property
    def capacity(self) -> int:
        """Maximum number of entries the cache can hold."""
        return self._capacity

    @property
    def ttl(self) -> float:
        """Time-to-live, in seconds, applied to every entry on write."""
        return self._ttl

    def put(self, key: str, value: str) -> None:
        """Store a value under a key, refreshing its TTL and recency.

        Inserting a new key into a full cache first drops stale entries and
        then, if still full, evicts the least-recently-used entry.
        """
        expires_at = self._clock() + self._ttl
        if key in self._entries:
            self._entries[key] = (value, expires_at)
            self._entries.move_to_end(key)
            return
        self.sweep()
        if len(self._entries) >= self._capacity:
            self._entries.popitem(last=False)
        self._entries[key] = (value, expires_at)

    def get(self, key: str, default: str | None = None) -> str | None:
        """Return the live value for a key, or the default if absent/stale.

        A successful read marks the entry as most recently used.
        """
        entry = self._entries.get(key)
        if entry is None:
            return default
        value, expires_at = entry
        if self._clock() >= expires_at:
            del self._entries[key]
            return default
        self._entries.move_to_end(key)
        return value

    def remove(self, key: str) -> bool:
        """Delete a key; return True if a live entry was removed."""
        entry = self._entries.pop(key, None)
        if entry is None:
            return False
        return self._clock() < entry[1]

    def sweep(self) -> int:
        """Purge every stale entry; return how many were removed."""
        now = self._clock()
        stale = [
            key for key, (_, expires_at) in self._entries.items() if now >= expires_at
        ]
        for key in stale:
            del self._entries[key]
        return len(stale)

    def clear(self) -> None:
        """Remove every entry from the cache."""
        self._entries.clear()

    def __contains__(self, key: str) -> bool:
        """Return whether a live entry exists, without touching recency."""
        entry = self._entries.get(key)
        return entry is not None and self._clock() < entry[1]

    def __len__(self) -> int:
        """Number of live entries currently stored."""
        now = self._clock()
        return sum(1 for _, expires_at in self._entries.values() if now < expires_at)
