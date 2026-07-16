"""Tests for the Memory Cache kata.

The cache is driven by an injected clock so every TTL scenario is deterministic.
"""


class FakeClock:
    """Controllable clock: calling the instance returns the current time in seconds."""

    def __init__(self, start: float = 0.0) -> None:
        self.now = start

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


def test_default_capacity_is_100_and_default_ttl_is_60_seconds() -> None:
    """Test 1: The cache holds a maximum of 100 entries with a TTL of 60 seconds by default"""
    from memory_cache import MemoryCache

    cache = MemoryCache(FakeClock())

    assert cache.capacity == 100
    assert cache.ttl == 60.0


def test_capacity_and_ttl_are_configurable() -> None:
    """Test 2: Capacity and TTL can be configured at construction"""
    from memory_cache import MemoryCache

    cache = MemoryCache(FakeClock(), capacity=3, ttl=5.0)

    assert cache.capacity == 3
    assert cache.ttl == 5.0


def test_non_positive_capacity_is_rejected() -> None:
    """Test 3: Capacity below one raises ValueError with the offending value"""
    import pytest

    from memory_cache import MemoryCache

    with pytest.raises(ValueError) as excinfo:
        MemoryCache(FakeClock(), capacity=0)
    assert str(excinfo.value) == "capacity must be at least 1, got [0]"

    with pytest.raises(ValueError) as excinfo:
        MemoryCache(FakeClock(), capacity=-5)
    assert str(excinfo.value) == "capacity must be at least 1, got [-5]"


def test_non_positive_ttl_is_rejected() -> None:
    """Test 4: A zero or negative TTL raises ValueError with the offending value"""
    import pytest

    from memory_cache import MemoryCache

    with pytest.raises(ValueError) as excinfo:
        MemoryCache(FakeClock(), ttl=0)
    assert str(excinfo.value) == "ttl must be positive, got [0]"

    with pytest.raises(ValueError) as excinfo:
        MemoryCache(FakeClock(), ttl=-1.5)
    assert str(excinfo.value) == "ttl must be positive, got [-1.5]"


def test_put_then_get_returns_the_stored_value() -> None:
    """Test 5: A stored value is retrieved by its key"""
    from memory_cache import MemoryCache

    cache = MemoryCache(FakeClock())
    cache.put("greeting", "hello")

    assert cache.get("greeting") == "hello"


def test_get_missing_key_returns_none_or_supplied_default() -> None:
    """Test 6: Reading an absent key yields None, or the caller's default"""
    from memory_cache import MemoryCache

    cache = MemoryCache(FakeClock())

    assert cache.get("absent") is None
    assert cache.get("absent", "fallback") == "fallback"


def test_put_overwrites_existing_value_for_same_key() -> None:
    """Test 7: Writing an existing key replaces its value without growing the cache"""
    from memory_cache import MemoryCache

    cache = MemoryCache(FakeClock())
    cache.put("key", "first")
    cache.put("key", "second")

    assert cache.get("key") == "second"
    assert len(cache) == 1


def test_least_recently_used_entry_is_evicted_when_capacity_is_reached() -> None:
    """Test 8: Inserting into a full cache evicts the least-recently-used entry"""
    from memory_cache import MemoryCache

    cache = MemoryCache(FakeClock(), capacity=3)
    cache.put("a", "1")
    cache.put("b", "2")
    cache.put("c", "3")

    cache.put("d", "4")  # "a" is the least recently used

    assert cache.get("a") is None
    assert cache.get("b") == "2"
    assert cache.get("c") == "3"
    assert cache.get("d") == "4"


def test_get_refreshes_recency_and_protects_entry_from_eviction() -> None:
    """Test 9: Reading a key makes it most recently used, so another key is evicted"""
    from memory_cache import MemoryCache

    cache = MemoryCache(FakeClock(), capacity=3)
    cache.put("a", "1")
    cache.put("b", "2")
    cache.put("c", "3")

    cache.get("a")  # "a" becomes most recently used; "b" is now LRU
    cache.put("d", "4")

    assert cache.get("a") == "1"
    assert cache.get("b") is None
    assert cache.get("c") == "3"
    assert cache.get("d") == "4"


def test_put_refreshes_recency_of_an_existing_key() -> None:
    """Test 10: Rewriting a key makes it most recently used, so another key is evicted"""
    from memory_cache import MemoryCache

    cache = MemoryCache(FakeClock(), capacity=3)
    cache.put("a", "1")
    cache.put("b", "2")
    cache.put("c", "3")

    cache.put("a", "updated")  # "a" becomes most recently used; "b" is now LRU
    cache.put("d", "4")

    assert cache.get("a") == "updated"
    assert cache.get("b") is None


def test_only_one_entry_is_evicted_per_overflowing_insert() -> None:
    """Test 11: A single insert into a full cache displaces exactly one entry"""
    from memory_cache import MemoryCache

    cache = MemoryCache(FakeClock(), capacity=3)
    cache.put("a", "1")
    cache.put("b", "2")
    cache.put("c", "3")

    cache.put("d", "4")

    assert len(cache) == 3


def test_entry_expires_once_its_ttl_has_elapsed() -> None:
    """Test 12: After the TTL has fully elapsed the entry is gone"""
    from memory_cache import MemoryCache

    clock = FakeClock()
    cache = MemoryCache(clock, ttl=60.0)
    cache.put("key", "value")

    clock.advance(60.0)  # exactly at TTL: the entry is stale

    assert cache.get("key") is None


def test_entry_is_still_live_just_before_its_ttl_elapses() -> None:
    """Test 13: Immediately before the TTL boundary the entry is still served"""
    from memory_cache import MemoryCache

    clock = FakeClock()
    cache = MemoryCache(clock, ttl=60.0)
    cache.put("key", "value")

    clock.advance(59.999)

    assert cache.get("key") == "value"


def test_rewriting_a_key_resets_its_ttl() -> None:
    """Test 14: A rewrite extends the entry's life by a fresh TTL"""
    from memory_cache import MemoryCache

    clock = FakeClock()
    cache = MemoryCache(clock, ttl=60.0)
    cache.put("key", "old")

    clock.advance(50.0)
    cache.put("key", "new")  # TTL now runs until t=110
    clock.advance(50.0)  # t=100: within the refreshed TTL

    assert cache.get("key") == "new"


def test_expired_key_can_be_stored_again() -> None:
    """Test 15: A key whose entry went stale accepts a fresh value"""
    from memory_cache import MemoryCache

    clock = FakeClock()
    cache = MemoryCache(clock, ttl=10.0)
    cache.put("key", "old")
    clock.advance(10.0)

    cache.put("key", "new")

    assert cache.get("key") == "new"


def test_len_and_contains_ignore_stale_entries() -> None:
    """Test 16: Stale entries count as absent for len() and the in operator"""
    from memory_cache import MemoryCache

    clock = FakeClock()
    cache = MemoryCache(clock, ttl=10.0)
    cache.put("old", "1")
    clock.advance(6.0)
    cache.put("fresh", "2")
    clock.advance(5.0)  # t=11: "old" is stale, "fresh" lives until t=16

    assert len(cache) == 1
    assert "old" not in cache
    assert "fresh" in cache


def test_sweep_purges_stale_entries_and_reports_the_count() -> None:
    """Test 17: An explicit sweep removes every stale entry and returns how many"""
    from memory_cache import MemoryCache

    clock = FakeClock()
    cache = MemoryCache(clock, ttl=10.0)
    cache.put("a", "1")
    cache.put("b", "2")
    clock.advance(6.0)
    cache.put("c", "3")
    clock.advance(5.0)  # t=11: "a" and "b" stale, "c" live

    removed = cache.sweep()

    assert removed == 2
    assert len(cache) == 1
    assert cache.get("c") == "3"


def test_stale_entries_are_dropped_before_lru_eviction_on_insert() -> None:
    """Test 18: A full cache reclaims stale slots first, sparing live entries"""
    from memory_cache import MemoryCache

    clock = FakeClock()
    cache = MemoryCache(clock, capacity=2, ttl=10.0)
    cache.put("stale", "1")
    clock.advance(6.0)
    cache.put("live", "2")
    clock.advance(5.0)  # t=11: "stale" expired, "live" valid until t=16

    cache.put("new", "3")  # reuses the stale slot instead of evicting "live"

    assert cache.get("live") == "2"
    assert cache.get("new") == "3"


def test_remove_deletes_a_live_entry_and_reports_success() -> None:
    """Test 19: Removing a live key returns True and the key becomes absent"""
    from memory_cache import MemoryCache

    cache = MemoryCache(FakeClock())
    cache.put("key", "value")

    assert cache.remove("key") is True
    assert cache.get("key") is None


def test_remove_of_missing_key_reports_failure() -> None:
    """Test 20: Removing an absent key returns False"""
    from memory_cache import MemoryCache

    cache = MemoryCache(FakeClock())

    assert cache.remove("ghost") is False


def test_clear_empties_the_cache() -> None:
    """Test 21: clear() leaves the cache with no entries"""
    from memory_cache import MemoryCache

    cache = MemoryCache(FakeClock())
    cache.put("a", "1")
    cache.put("b", "2")

    cache.clear()

    assert len(cache) == 0
    assert cache.get("a") is None


def test_cache_of_capacity_one_keeps_only_the_latest_entry() -> None:
    """Test 22: With capacity one, each insert replaces the previous entry"""
    from memory_cache import MemoryCache

    cache = MemoryCache(FakeClock(), capacity=1)
    cache.put("a", "1")
    cache.put("b", "2")

    assert cache.get("a") is None
    assert cache.get("b") == "2"
    assert len(cache) == 1


def test_ttl_of_one_second_or_less_is_accepted() -> None:
    """Test 23: Any positive TTL is valid, including values of one second or less"""
    from memory_cache import MemoryCache

    clock = FakeClock()
    cache = MemoryCache(clock, ttl=0.5)
    cache.put("key", "value")

    assert cache.ttl == 0.5
    assert cache.get("key") == "value"


def test_len_and_contains_treat_entry_at_exact_ttl_boundary_as_stale() -> None:
    """Test 24: Exactly at its TTL an entry is stale for len() and the in operator"""
    from memory_cache import MemoryCache

    clock = FakeClock()
    cache = MemoryCache(clock, ttl=10.0)
    cache.put("key", "value")

    clock.advance(10.0)  # exactly at TTL: the entry is stale

    assert len(cache) == 0
    assert "key" not in cache


def test_sweep_purges_an_entry_exactly_at_its_ttl_boundary() -> None:
    """Test 25: A sweep at the exact TTL boundary removes the entry"""
    from memory_cache import MemoryCache

    clock = FakeClock()
    cache = MemoryCache(clock, ttl=10.0)
    cache.put("key", "value")

    clock.advance(10.0)  # exactly at TTL: the entry is stale

    assert cache.sweep() == 1
    assert len(cache) == 0


def test_remove_of_entry_exactly_at_its_ttl_boundary_reports_failure() -> None:
    """Test 26: Removing a key exactly at its TTL returns False, as the entry is stale"""
    from memory_cache import MemoryCache

    clock = FakeClock()
    cache = MemoryCache(clock, ttl=10.0)
    cache.put("key", "value")

    clock.advance(10.0)  # exactly at TTL: the entry is stale

    assert cache.remove("key") is False
