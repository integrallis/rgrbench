# Number list statistics

## Overview
A statistics reporter for lists of whole numbers. The caller picks one statistic from a fixed catalogue — minimum, maximum, element count, or average — and receives the answer as text.

## User Stories

### US-1: Compute a chosen statistic
As a data reviewer, I want to request a single statistic for a list of numbers, so that I can summarise the list without computing it by hand.

Canonical worked example — for the series 1, -1, 2, -2, 6, 9, 15, -2, 92, 11:

- AC-1.1: Requesting the minimum reports "-2".
- AC-1.2: Requesting the maximum reports "92".
- AC-1.3: Requesting the element count reports "10".
- AC-1.4: Requesting the average reports "13.1" — a decimal result, not truncated to a whole number.
- AC-1.5: Every statistic is delivered as text.

### US-2: Unrecognised statistic requests
As a maintainer, I want a request for a statistic outside the catalogue to yield empty text, so that unexpected selector values never produce a misleading number.

- AC-2.1: A statistic selector outside the supported catalogue yields an empty text result rather than an error.

## Traceability
```json
{
  "test_can_find_minimum_value": ["AC-1.1", "AC-1.5"],
  "test_can_find_maximum_value": ["AC-1.2", "AC-1.5"],
  "test_can_get_element_count": ["AC-1.3", "AC-1.5"],
  "test_can_get_average_of_series": ["AC-1.4", "AC-1.5"],
  "test_handles_invalid_stat_type": ["AC-2.1"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
