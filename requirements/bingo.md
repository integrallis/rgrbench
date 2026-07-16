# Bingo card play and win detection

## Overview
A bingo game helper covering the classic 75-ball game. Called numbers belong to lettered columns — B covers 1-15, I covers 16-30, N covers 31-45, G covers 46-60, O covers 61-75. A card is a five-by-five grid holding 24 unique numbers arranged column by column, with the centre space free and pre-marked. Players mark called numbers on the card, and the card reports a win when any row, column, or diagonal is completely marked.

## User Stories

### US-1: Announce the column letter for a call
As a bingo caller, I want each drawn number paired with its column letter, so that calls follow the traditional B-I-N-G-O announcement.

- AC-1.1: Numbers map to letters by range — 1-15 to B, 16-30 to I, 31-45 to N, 46-60 to G, 61-75 to O — including both ends of every range.
- AC-1.2: A number outside 1-75 is rejected with an error stating the number must be between 1 and 75.

### US-2: Lay out a card
As a player, I want my card's 24 numbers arranged in the standard grid, so that the card matches what is printed.

- AC-2.1: The 24 numbers fill the five-by-five grid column by column in B, I, N, G, O order, skipping the centre; the number at any position can be queried by row and column (zero-based).
- AC-2.2: The centre space holds no number and starts already marked (the free space).
- AC-2.3: Every space other than the free centre starts unmarked.

### US-3: Validate a card
As a player, I want malformed cards refused, so that play only happens on legitimate cards.

- AC-3.1: A card must receive exactly 24 numbers; any other count is rejected with an error stating exactly 24 numbers are required.
- AC-3.2: The 24 numbers must be unique; duplicates are rejected with an error whose message is exactly "card numbers must be unique".
- AC-3.3: Each number must fall within its column's range; a number outside its column is rejected with an error naming the offending column (e.g. a number not valid for column B).

### US-4: Mark called numbers
As a player, I want called numbers marked on my card, so that my progress toward a win is tracked.

- AC-4.1: Calling a number that is on the card marks its space and reports a hit.
- AC-4.2: Calling a valid number that is not on the card reports no hit and marks nothing.
- AC-4.3: Calls outside 1-75 are rejected with an error stating the number must be between 1 and 75.
- AC-4.4: The boundary calls 1 and 75 are accepted as valid calls.

### US-5: Detect a winning card
As a player, I want the card to recognise a completed line, so that I know the moment I can shout bingo.

- AC-5.1: A freshly dealt card has no win.
- AC-5.2: Five marked spaces across any row form a win.
- AC-5.3: Five marked spaces down any column form a win.
- AC-5.4: The free centre counts as marked, so the middle row and the N column each need only their four numbered spaces marked.
- AC-5.5: Either diagonal through the centre forms a win, and each needs only its four numbered spaces marked thanks to the free centre.
- AC-5.6: An incomplete row, or marks scattered without completing any line, is not a win.

## Traceability
```json
{
  "test_column_letter_for_range_starts": ["AC-1.1"],
  "test_column_letter_for_range_ends": ["AC-1.1"],
  "test_column_letter_rejects_numbers_outside_one_to_seventy_five": ["AC-1.2"],
  "test_card_places_numbers_column_major": ["AC-2.1"],
  "test_centre_space_is_free_and_pre_marked": ["AC-2.2"],
  "test_all_numbered_spaces_start_unmarked": ["AC-2.3"],
  "test_card_requires_exactly_twenty_four_numbers": ["AC-3.1"],
  "test_card_numbers_must_be_unique": ["AC-3.2"],
  "test_card_numbers_must_fit_their_column_range": ["AC-3.3"],
  "test_marking_a_called_number_on_the_card": ["AC-4.1"],
  "test_marking_a_called_number_not_on_the_card": ["AC-4.2"],
  "test_marking_rejects_numbers_outside_one_to_seventy_five": ["AC-4.3"],
  "test_new_card_has_no_bingo": ["AC-5.1"],
  "test_horizontal_line_is_bingo": ["AC-5.2"],
  "test_middle_row_needs_only_four_marks": ["AC-5.4"],
  "test_vertical_line_is_bingo": ["AC-5.3"],
  "test_n_column_needs_only_four_marks": ["AC-5.4"],
  "test_diagonal_line_is_bingo": ["AC-5.5"],
  "test_anti_diagonal_line_is_bingo": ["AC-5.5"],
  "test_four_marks_in_a_row_are_not_bingo": ["AC-5.6"],
  "test_scattered_marks_are_not_bingo": ["AC-5.6"],
  "test_marking_accepts_the_boundary_calls_one_and_seventy_five": ["AC-4.4"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
