# One hundred doors

## Overview
A corridor holds a row of doors, all starting closed, numbered from 1. The corridor is
walked once per door: on walk k, every k-th door is toggled (opened if closed, closed if
open). After all walks, the final state of the doors is reported — as a list of open/closed
indicators, as the positions of the open doors, or as a compact string of markers.

## User Stories

### US-1: Compute the final door states
As a puzzle solver, I want the doors toggled through every walk, so that I can see which doors end open.

- AC-1.1: For N doors, after walk k of N has toggled every k-th door for all k, exactly the doors at perfect-square positions end open (worked examples: 10 doors leave 1, 4, 9 open; 100 doors leave the ten squares 1, 4, 9, 16, 25, 36, 49, 64, 81, 100 open; 50 doors leave the squares up to 49 open).
- AC-1.2: A single door ends open: the only walk toggles it once.
- AC-1.3: Door 2 ends closed: it is toggled twice, by walks 1 and 2.

### US-2: Report the outcome in three forms
As a puzzle solver, I want the final state in several forms, so that I can inspect it however suits me.

- AC-2.1: The final state is available as a list of open/closed indicators with exactly one entry per door, in door order.
- AC-2.2: The final state is available as the list of open-door positions in ascending order.
- AC-2.3: The final state is available as a string with one character per door — "@" for an open door, "#" for a closed one, and no other characters (worked example: ten doors render as "@##@####@#").

### US-3: Handle edge counts
As a puzzle solver, I want degenerate door counts handled cleanly, so that the reports stay trustworthy.

- AC-3.1: Zero doors yield an empty state list, an empty list of open positions, and an empty string.
- AC-3.2: A negative door count is rejected as an error with exactly the message "door count must be non-negative".

## Traceability
```json
{
  "test_single_door_ends_open": ["AC-1.2", "AC-2.2"],
  "test_zero_doors_yield_empty_results": ["AC-3.1"],
  "test_ten_doors_leave_perfect_squares_open": ["AC-1.1", "AC-2.2"],
  "test_hundred_doors_leave_perfect_squares_open": ["AC-1.1", "AC-2.2"],
  "test_final_states_for_three_doors": ["AC-2.1"],
  "test_state_list_length_matches_door_count": ["AC-2.1"],
  "test_render_ten_doors": ["AC-2.3"],
  "test_render_single_door": ["AC-2.3"],
  "test_render_four_doors": ["AC-2.3"],
  "test_hundred_doors_have_exactly_ten_open": ["AC-1.1"],
  "test_door_two_ends_closed": ["AC-1.3"],
  "test_fifty_doors_leave_perfect_squares_open": ["AC-1.1", "AC-2.2"],
  "test_render_uses_only_open_and_closed_markers": ["AC-2.3"],
  "test_negative_door_count_is_rejected": ["AC-3.2"],
  "test_negative_door_count_error_names_the_rule": ["AC-3.2"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
