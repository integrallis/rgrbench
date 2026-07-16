# In-memory cache with recency eviction and expiry

## Overview
An in-memory key-value cache with a bounded capacity and a time-to-live for its entries. When the cache is full, the least-recently-used entry makes way for new ones; entries go stale once their time-to-live elapses, and stale entries are invisible to reads, counts and membership checks. The cache observes the passage of time through a caller-supplied clock reporting seconds.

## User Stories

### US-1: Configuration
As a service developer, I want capacity and expiry to be configurable with safe defaults, so that the cache fits its workload.

- AC-1.1: By default the cache holds a maximum of 100 entries and entries live for 60 seconds.
- AC-1.2: Capacity and time-to-live can both be configured when the cache is created.
- AC-1.3: A capacity below one is rejected with the exact message "capacity must be at least 1, got [value]", where value is the offending number (for example "capacity must be at least 1, got [0]").
- AC-1.4: A zero or negative time-to-live is rejected with the exact message "ttl must be positive, got [value]", where value is the offending number (for example "ttl must be positive, got [-1.5]").
- AC-1.5: Any positive time-to-live is accepted, including values of one second or less.

### US-2: Store and retrieve
As a service developer, I want to store values by key and read them back, so that expensive results are reused.

- AC-2.1: A stored value is retrieved by its key.
- AC-2.2: Reading an absent key yields nothing by default, or a caller-supplied fallback value when one is given.
- AC-2.3: Writing to an existing key replaces its value without growing the entry count.

### US-3: Least-recently-used eviction
As a service developer, I want the least useful entry evicted when the cache is full, so that hot entries stay cached.

- AC-3.1: Inserting a new key into a full cache displaces exactly one entry: the least recently used one.
- AC-3.2: Reading a key refreshes its recency, so a different, less recently used entry is evicted instead.
- AC-3.3: Rewriting an existing key also refreshes its recency.
- AC-3.4: With a capacity of one, each insert of a new key replaces the previous entry.

### US-4: Expiry
As a service developer, I want entries to expire after their time-to-live, so that stale data is never served.

- AC-4.1: An entry is stale from the instant its time-to-live has fully elapsed: exactly at the boundary it is already gone.
- AC-4.2: Immediately before the boundary the entry is still served.
- AC-4.3: Rewriting a key restarts its time-to-live from the moment of the rewrite.
- AC-4.4: A key whose entry went stale accepts a fresh value.

### US-5: Housekeeping
As a service developer, I want counting, membership, removal and cleanup to respect staleness, so that the cache's bookkeeping can be trusted.

- AC-5.1: The entry count and membership checks treat stale entries as absent, including entries exactly at their expiry boundary.
- AC-5.2: An explicit sweep removes every stale entry — including entries exactly at their expiry boundary — and reports how many were removed.
- AC-5.3: When a full cache takes a new entry, stale slots are reclaimed first, sparing live entries from eviction.
- AC-5.4: Removing a live key reports success and the key becomes absent.
- AC-5.5: Removing an absent key reports failure; so does removing a key exactly at its expiry boundary, since that entry is already stale.
- AC-5.6: Clearing the cache leaves it with no entries.

## Traceability
```json
{
  "test_default_capacity_is_100_and_default_ttl_is_60_seconds": ["AC-1.1"],
  "test_capacity_and_ttl_are_configurable": ["AC-1.2"],
  "test_non_positive_capacity_is_rejected": ["AC-1.3"],
  "test_non_positive_ttl_is_rejected": ["AC-1.4"],
  "test_put_then_get_returns_the_stored_value": ["AC-2.1"],
  "test_get_missing_key_returns_none_or_supplied_default": ["AC-2.2"],
  "test_put_overwrites_existing_value_for_same_key": ["AC-2.3"],
  "test_least_recently_used_entry_is_evicted_when_capacity_is_reached": ["AC-3.1"],
  "test_get_refreshes_recency_and_protects_entry_from_eviction": ["AC-3.2"],
  "test_put_refreshes_recency_of_an_existing_key": ["AC-3.3"],
  "test_only_one_entry_is_evicted_per_overflowing_insert": ["AC-3.1"],
  "test_entry_expires_once_its_ttl_has_elapsed": ["AC-4.1"],
  "test_entry_is_still_live_just_before_its_ttl_elapses": ["AC-4.2"],
  "test_rewriting_a_key_resets_its_ttl": ["AC-4.3"],
  "test_expired_key_can_be_stored_again": ["AC-4.4"],
  "test_len_and_contains_ignore_stale_entries": ["AC-5.1"],
  "test_sweep_purges_stale_entries_and_reports_the_count": ["AC-5.2"],
  "test_stale_entries_are_dropped_before_lru_eviction_on_insert": ["AC-5.3"],
  "test_remove_deletes_a_live_entry_and_reports_success": ["AC-5.4"],
  "test_remove_of_missing_key_reports_failure": ["AC-5.5"],
  "test_clear_empties_the_cache": ["AC-5.6"],
  "test_cache_of_capacity_one_keeps_only_the_latest_entry": ["AC-3.4"],
  "test_ttl_of_one_second_or_less_is_accepted": ["AC-1.5"],
  "test_len_and_contains_treat_entry_at_exact_ttl_boundary_as_stale": ["AC-5.1"],
  "test_sweep_purges_an_entry_exactly_at_its_ttl_boundary": ["AC-5.2"],
  "test_remove_of_entry_exactly_at_its_ttl_boundary_reports_failure": ["AC-5.5"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
