# Look-and-say sequence

## Overview
The look-and-say sequence: each term describes the previous one by reading its runs of identical digits aloud as "count, then digit". One operation advances a term a single step; another applies the transformation a chosen number of times to a seed term. Terms are non-empty strings of digits, and iteration counts may not be negative.

## User Stories

### US-1: Read a term aloud
As a sequence explorer, I want the next term derived by reading runs of identical digits as count-then-digit, so that the sequence unfolds one step at a time.

- AC-1.1: Runs are read left to right as their length followed by their digit: "1" becomes "11", "11" becomes "21", "21" becomes "1211", "1211" becomes "111221", "111221" becomes "312211", "2" becomes "12", and "3211" becomes "131221".
- AC-1.2: A run of ten or more identical digits reads as a multi-digit count: ten 1s become "101".
- AC-1.3: "22" reads as itself — a fixed point of the transformation.
- AC-1.4: Every digit is a valid term character, including zero and nine: "10" becomes "1110" and "9" becomes "19".

### US-2: Iterate from a seed
As a sequence explorer, I want the transformation applied a chosen number of times to a seed, so that I can jump straight to any later term.

- AC-2.1: Zero iterations return the seed unchanged.
- AC-2.2: n iterations apply the single-step reading n times: from "1", one step gives "11", two steps give "21", and five steps give "312211"; from "2", one step gives "12".
- AC-2.3: A fixed point survives repeated iteration: "22" is still "22" after three steps.

### US-3: Input validation
As a sequence explorer, I want malformed input rejected with a clear message, so that mistakes surface immediately.

- AC-3.1: A negative iteration count is rejected with the message exactly "iterations must be non-negative".
- AC-3.2: A term that is empty or contains any non-digit character — letters of either case included — is rejected with the message exactly "term must be a non-empty string of digits".

## Traceability
```json
{
  "test_next_term_of_one": ["AC-1.1"],
  "test_next_term_of_double_one": ["AC-1.1"],
  "test_next_term_of_two_one": ["AC-1.1"],
  "test_next_term_of_one_two_one_one": ["AC-1.1"],
  "test_next_term_of_one_one_one_two_two_one": ["AC-1.1"],
  "test_next_term_of_two": ["AC-1.1"],
  "test_double_two_is_a_fixed_point": ["AC-1.3"],
  "test_next_term_of_mixed_digits": ["AC-1.1"],
  "test_run_of_ten_digits_yields_two_digit_count": ["AC-1.2"],
  "test_zero_iterations_return_seed_unchanged": ["AC-2.1"],
  "test_one_iteration_from_one": ["AC-2.2"],
  "test_two_iterations_from_one": ["AC-2.2"],
  "test_five_iterations_from_one": ["AC-2.2"],
  "test_one_iteration_from_two": ["AC-2.2"],
  "test_fixed_point_survives_repeated_iterations": ["AC-2.3"],
  "test_negative_iterations_are_rejected": ["AC-3.1"],
  "test_empty_term_is_rejected": ["AC-3.2"],
  "test_non_digit_term_is_rejected": ["AC-3.2"],
  "test_term_containing_zero_is_accepted": ["AC-1.4"],
  "test_term_of_nine_is_accepted": ["AC-1.4"],
  "test_uppercase_letter_in_term_is_rejected": ["AC-3.2"],
  "test_negative_iterations_error_names_the_rule": ["AC-3.1"],
  "test_invalid_term_error_names_the_rule": ["AC-3.2"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
