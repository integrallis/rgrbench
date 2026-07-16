# Odd/Even number announcer

## Overview
A number announcer calls out whole numbers one at a time or across a range. Positive
even numbers are called "Even", odd primes are called by their own value, other positive
odd numbers are called "Odd", and zero and negative numbers are called by their own
value. Range announcements join the individual calls with single spaces.

## User Stories

### US-1: Announcing a single number
As a player of the calling game, I want each number classified and announced by the game's rules, so that every number gets exactly one call.

- AC-1.1: A positive even number is announced as "Even"; this includes 2, whose evenness
  takes precedence over its primality.
- AC-1.2: An odd prime is announced as the number itself, so 3, 5, and 11 are announced
  as "3", "5", and "11".
- AC-1.3: A positive odd number that is not prime is announced as "Odd", so 1, 9, and
  25 are all announced as "Odd".
- AC-1.4: Zero is announced as "0".
- AC-1.5: A negative number is announced as itself even when it is even, so -4 is
  announced as "-4".

### US-2: Announcing a range of numbers
As a player, I want a whole span of numbers announced in one line, so that the game can be played over any range.

- AC-2.1: For a start and end number, the announcements for every number from start to
  end inclusive are joined with single spaces; the range 1 through 10 is announced as
  "Odd Even 3 Even 5 Even 7 Even Odd Even".
- AC-2.2: A negative start is raised so the range begins at 1; the range -5 through 3 is
  announced as "Odd Even 3".
- AC-2.3: A start of zero is kept, and the zero announces itself; the range 0 through 2
  is announced as "0 Odd Even".
- AC-2.4: When the start exceeds the end, the announcement is the empty string.
- AC-2.5: Range announcements always produce a result, including long spans such as 1
  through 100 or 5 through 150.

## Traceability
```json
{
  "test_can_print_odd_even_1_50": ["AC-2.5"],
  "test_can_print_odd_even_1_100": ["AC-2.5"],
  "test_can_print_odd_even_5_150": ["AC-2.5"],
  "test_can_print_odd_even_for_single_number_1": ["AC-1.3"],
  "test_can_print_odd_even_for_single_number_3": ["AC-1.2"],
  "test_can_print_odd_even_for_single_number_5": ["AC-1.2"],
  "test_can_print_odd_even_for_single_number_4": ["AC-1.1"],
  "test_can_print_odd_even_for_single_number_9": ["AC-1.3"],
  "test_can_print_odd_even_for_single_number_10": ["AC-1.1"],
  "test_print_odd_even_range_1_10": ["AC-2.1"],
  "test_print_odd_even_negative_start_begins_at_1": ["AC-2.2"],
  "test_print_odd_even_start_zero_includes_zero": ["AC-2.3"],
  "test_print_odd_even_empty_range_returns_empty_string": ["AC-2.4"],
  "test_can_print_odd_even_for_single_number_2": ["AC-1.1"],
  "test_can_print_odd_even_for_single_number_11": ["AC-1.2"],
  "test_can_print_odd_even_for_single_number_25": ["AC-1.3"],
  "test_can_print_odd_even_for_single_number_0": ["AC-1.4"],
  "test_can_print_odd_even_for_single_number_negative_4": ["AC-1.5"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
