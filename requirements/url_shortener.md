# URL shortening service

## Overview
A link-sharing service turns long web addresses into short, predictable ones and back
again. Each new long URL receives the next identifier in a deterministic base-36
sequence appended to a base address, the same long URL always maps to the same short
URL, and the service keeps per-link usage statistics: how many times a short link was
followed and, when a clock is supplied, exactly when.

## User Stories

### US-1: Issue deterministic short URLs
As a link sharer, I want each long URL turned into a compact, predictable short URL, so that links are easy to pass around and their identifiers never collide.

- AC-1.1: Identifiers are issued sequentially starting at base-36 "0": the first shortened URL gets identifier "0", the second distinct URL gets "1".
- AC-1.2: Identifiers count in base 36: the eleventh distinct URL gets identifier "a" and the thirty-seventh gets "10".
- AC-1.3: A short URL is the base address followed by the identifier; the default base address is "https://short.url/", so the first short URL is "https://short.url/0".
- AC-1.4: The base address is configurable; short URLs are built on whatever base is configured.
- AC-1.5: An identifier source can be supplied instead of the built-in sequence, in which case its identifiers are used one per shortened URL, in order.

### US-2: Translate in both directions and never duplicate
As a link sharer, I want to look up either form of a link and get the other, so that one mapping serves both redirection and reverse lookup.

- AC-2.1: Translating a short URL returns the original long URL.
- AC-2.2: Translating a known long URL returns its short URL.
- AC-2.3: Shortening the same long URL again returns the existing short URL rather than creating a new one.
- AC-2.4: A duplicate does not advance the identifier sequence; the next distinct URL still receives the next identifier.

### US-3: Track usage statistics per link
As a service operator, I want per-link visit counts and timestamps, so that I can see how much and when each short link is used.

- AC-3.1: A freshly shortened URL has zero visits.
- AC-3.2: Each translation of a short URL counts as one visit.
- AC-3.3: Translating the long URL does not count as a visit; visits track short-URL accesses only.
- AC-3.4: The statistics record for a link — retrievable by either its short or its long URL — reports the short URL, the long URL, and the visit count.
- AC-3.5: When a clock is supplied to the service, every visit's timestamp is recorded in the link's history, in visit order.
- AC-3.6: Without a supplied clock, visits are still counted but the history stays empty.
- AC-3.7: A link's log is a four-part text summary — short URL, long URL, visit count, then one line per access timestamp — exactly of the form:
  "short_url: https://short.url/0", then "long_url: https://example.com/page", then "visits: 1", then "2026-01-01 12:00:00", each on its own line.

### US-4: Refuse invalid or unknown URLs
As a service operator, I want malformed input and unknown links refused with a clear message, so that the mapping stays trustworthy.

- AC-4.1: Only web URLs are accepted for shortening: a value without an http or https scheme is rejected with the message "Invalid URL: '<the given value>'".
- AC-4.2: A bare scheme with nothing after it is rejected as an invalid URL.
- AC-4.3: Translating a URL the service has never seen is rejected with the message "Unknown URL: '<the given value>'".
- AC-4.4: Requesting statistics for a URL the service has never seen is rejected with the same "Unknown URL" message form.

## Traceability
```json
{
  "test_first_short_url_uses_identifier_zero": ["AC-1.1", "AC-1.3"],
  "test_identifiers_are_sequential": ["AC-1.1"],
  "test_eleventh_identifier_is_a": ["AC-1.2"],
  "test_thirty_seventh_identifier_is_10": ["AC-1.2"],
  "test_custom_base_url": ["AC-1.4"],
  "test_injected_identifier_generator_is_used": ["AC-1.5"],
  "test_translate_short_url_returns_long_url": ["AC-2.1"],
  "test_translate_long_url_returns_short_url": ["AC-2.2"],
  "test_duplicate_long_url_returns_existing_short_url": ["AC-2.3"],
  "test_duplicate_long_url_does_not_consume_an_identifier": ["AC-2.4"],
  "test_visits_start_at_zero": ["AC-3.1"],
  "test_translating_short_url_counts_visits": ["AC-3.2"],
  "test_translating_long_url_does_not_count_visits": ["AC-3.3"],
  "test_stats_accepts_short_url": ["AC-3.4"],
  "test_stats_accepts_long_url": ["AC-3.4"],
  "test_url_without_scheme_is_rejected": ["AC-4.1"],
  "test_scheme_only_url_is_rejected": ["AC-4.2"],
  "test_translate_unknown_url_raises": ["AC-4.3"],
  "test_stats_for_unknown_url_raises": ["AC-4.4"],
  "test_history_records_injected_clock_timestamps_in_order": ["AC-3.5"],
  "test_history_is_empty_without_a_clock": ["AC-3.6"],
  "test_log_lists_urls_visits_and_history": ["AC-3.7"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
