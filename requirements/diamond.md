# Alphabet diamond printer

## Overview
A text-figure generator for the classic alphabet diamond: given a target letter, it produces a diamond-shaped figure that starts at the letter A, widens row by row through the alphabet until the target letter, then narrows symmetrically back to A. The figure is returned as text, one row per line.

## User Stories

### US-1: Generate the diamond for a chosen letter
As a puzzle enthusiast, I want to request the diamond figure for any letter, so that I can render the classic alphabet diamond exactly.

- AC-1.1: The diamond for the letter A is the single character A, on one row.
- AC-1.2: The diamond for the letter B is exactly this three-row figure:

```
 A
B B
 A
```

- AC-1.3: The diamond for the letter C is exactly this five-row figure:

```
  A
 B B
C   C
 B B
  A
```

- AC-1.4: The diamond for the letter D is exactly this seven-row figure:

```
   A
  B B
 C   C
D     D
 C   C
  B B
   A
```

- AC-1.5: For the letter E, the top row is the letter A preceded by four spaces, and the middle row is two E characters separated by seven spaces.

### US-2: Every diamond follows the geometry rules
As a puzzle enthusiast, I want every diamond to obey the shape rules regardless of the target letter, so that all figures are well-formed.

- AC-2.1: A diamond whose target is the Nth letter of the alphabet has 2N-1 rows, and its widest row is 2N-1 characters wide (A gives 1, B gives 3, C gives 5, E gives 9).
- AC-2.2: The first and last rows each contain a single A.
- AC-2.3: Every row except the first and last contains exactly two occurrences of one and the same letter.
- AC-2.4: The figure is vertically symmetric: the list of rows reads the same top-to-bottom as bottom-to-top.
- AC-2.5: Each row, once padded with spaces to the figure's full width, reads the same forwards and backwards.
- AC-2.6: Moving down the top half, the gap between a row's letter pair grows by two spaces per row (for E the interior gaps are 1, 3, 5, 7).
- AC-2.7: The rows use letters in unbroken alphabetical order from A down to the target letter and back to A, with no letter skipped.
- AC-2.8: Rows carry only the leading spaces needed to position their letters; they have no trailing spaces.

### US-3: Accept forgiving input, reject invalid input
As a user, I want lowercase input accepted and anything that is not a single letter rejected with a clear message, so that mistakes are caught immediately.

- AC-3.1: A lowercase letter produces the same diamond as its uppercase form.
- AC-3.2: Input that is not a single letter A through Z — digits, punctuation, whitespace, the empty string, or strings of more than one character — is rejected as invalid.
- AC-3.3: A single character whose uppercase form is more than one letter (for example the character ß, which uppercases to SS) is rejected as invalid.
- AC-3.4: The rejection error carries exactly the message: Input must be a single letter A-Z
- AC-3.5: Z is a valid target: its diamond has 51 rows, and its widest row is a Z, 49 spaces, and a Z.

## Traceability
```json
{
  "test_diamond_for_a_is_a_single_letter": ["AC-1.1"],
  "test_diamond_for_b_matches_specification_example": ["AC-1.2", "AC-2.8"],
  "test_diamond_for_c_matches_specification_example": ["AC-1.3", "AC-2.8"],
  "test_diamond_for_d_matches_specification_example": ["AC-1.4", "AC-2.8"],
  "test_diamond_for_e_first_and_middle_rows": ["AC-1.5"],
  "test_height_and_width_match_specification_table": ["AC-2.1"],
  "test_first_and_last_rows_contain_a_single_a": ["AC-2.2"],
  "test_inner_rows_contain_exactly_two_identical_letters": ["AC-2.3"],
  "test_diamond_is_vertically_symmetric": ["AC-2.4"],
  "test_diamond_is_horizontally_symmetric": ["AC-2.5"],
  "test_inner_gap_grows_by_two_per_row": ["AC-2.6"],
  "test_lowercase_input_is_normalised_to_uppercase": ["AC-3.1"],
  "test_rows_use_letters_in_alphabetical_sequence": ["AC-2.7"],
  "test_invalid_input_is_rejected": ["AC-3.2"],
  "test_diamond_for_z_spans_the_full_alphabet": ["AC-3.5", "AC-2.8"],
  "test_single_character_that_uppercases_to_two_letters_is_rejected": ["AC-3.3"],
  "test_rejection_message_is_exact": ["AC-3.4"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
