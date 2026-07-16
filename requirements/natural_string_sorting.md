# Natural ordering of mixed text

## Overview
A sorting service arranges a collection of strings that mix digits, letters, and spaces
into the order a person would expect: numbers are compared by their numeric value rather
than character by character, and the whole ordering can be reversed on request.

## User Stories

### US-1: Sorting in natural ascending order
As a user browsing mixed labels, I want strings sorted in natural ascending order by default, so that numbered entries appear in numeric order instead of character order.

- AC-1.1: When no direction is requested, the collection is returned sorted in natural
  ascending order.
- AC-1.2: Numbers embedded in strings compare by numeric value rather than by character
  order, so "3" precedes "23".
- AC-1.3: Strings that begin with a digit precede strings that begin with a letter.
- AC-1.4: Canonical worked example (this ordering is the specification): the collection
  "a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0" sorts
  ascending to "0", "1", "1a", "2", "3", "23", "21 1", "a1", "b1", "b3", "z 21", "z22".

### US-2: Sorting in natural descending order
As a user browsing mixed labels, I want to request descending order, so that the same natural ordering can be viewed from largest to smallest.

- AC-2.1: When descending order is requested, the result is the exact reverse of the
  natural ascending order.
- AC-2.2: Canonical worked example: the collection from the ascending example sorts
  descending to "z22", "z 21", "b3", "b1", "a1", "21 1", "23", "3", "2", "1a", "1", "0".

## Traceability
```json
{
  "test_can_sort_string_default_order": ["AC-1.1", "AC-1.2", "AC-1.3", "AC-1.4"],
  "test_can_sort_string_des_order": ["AC-2.1", "AC-2.2"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
