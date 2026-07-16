# Adding numbers from delimited text

## Overview
A calculator accepts a single piece of text containing zero or more whole numbers separated by delimiters and returns their sum. Blank input counts as zero, line breaks work alongside commas as separators, callers can declare their own delimiter character, oversized values are ignored, and negative values are refused with a descriptive error.

## User Stories

### US-1: Add the numbers in a line of text
As a user entering figures as a single piece of text, I want the calculator to add every number in the text, so that I do not have to separate and total them myself.

- AC-1.1: Empty or absent input yields a total of 0.
- AC-1.2: Input holding a single number yields that number's value (for example "2" yields 2, and "0" yields 0).
- AC-1.3: Numbers separated by commas are all added together, however many there are.

### US-2: Accept multi-line input
As a user pasting figures laid out on several lines, I want line breaks to act as separators alongside commas, so that multi-line text still adds up.

- AC-2.1: A line break between two numbers separates them exactly like a comma.
- AC-2.2: Commas and line breaks may be freely mixed within one input.

### US-3: Declare a custom delimiter
As a user whose data uses its own separator character, I want to declare that character at the start of the input, so that the calculator can add numbers separated by it.

- AC-3.1: An input beginning with two slashes, a single delimiter character, and a line break uses that character to separate the numbers that follow (worked example: declaring ";" and then giving 1;2 yields 3; the same works for other characters such as "*").
- AC-3.2: The delimiter declaration ends at the first line break; a trailing line break after the numbers is insignificant and does not change the total.
- AC-3.3: All other rules — zero values, the upper limit, and the ban on negatives — hold unchanged when a custom delimiter is in use.

### US-4: Police out-of-range and invalid values
As a bookkeeper, I want oversized and negative values policed, so that totals stay trustworthy.

- AC-4.1: Numbers greater than 1000 are ignored and contribute nothing to the total.
- AC-4.2: The value 1000 itself is included in the total.
- AC-4.3: Any negative number is refused: the calculator fails with the message exactly "string contains [N], which does not meet rule. entered number should not negative.", where N is the offending negative value (for example -1, -2 or -5).

## Traceability
```json
{
  "test_add_return_zero_when_supplied_empty_string": ["AC-1.1"],
  "test_add_return_zero_when_supplied_null": ["AC-1.1"],
  "test_add_return_number_when_supplied_single_1": ["AC-1.2"],
  "test_add_return_sum_when_supplied_two_numbers": ["AC-1.3"],
  "test_add_return_zero_when_supplied_single_0": ["AC-1.2"],
  "test_add_return_number_when_supplied_single_2": ["AC-1.2"],
  "test_add_return_number_when_supplied_single_3": ["AC-1.2"],
  "test_add_return_sum_when_supplied_multiple_numbers_with_555": ["AC-1.3"],
  "test_add_return_sum_with_newline_delimiter": ["AC-2.1"],
  "test_add_return_sum_with_mixed_delimiters_1": ["AC-2.2"],
  "test_add_return_sum_with_mixed_delimiters_2": ["AC-2.2"],
  "test_add_return_sum_0_1": ["AC-1.3"],
  "test_add_return_sum_0_1_1": ["AC-1.3"],
  "test_add_return_sum_0_2": ["AC-1.3"],
  "test_add_return_sum_0_2_2": ["AC-1.3"],
  "test_add_return_sum_0_3": ["AC-1.3"],
  "test_add_return_sum_0_3_2": ["AC-1.3"],
  "test_add_return_sum_0_3_3": ["AC-1.3"],
  "test_add_ignore_numbers_greater_than_1000": ["AC-4.1"],
  "test_add_include_1000_exactly": ["AC-4.2"],
  "test_add_with_custom_delimiter_star": ["AC-3.1"],
  "test_add_with_custom_delimiter_semicolon": ["AC-3.1"],
  "test_add_with_custom_delimiter_semicolon_multiple": ["AC-3.1"],
  "test_add_throw_exception_for_negative_number": ["AC-4.3"],
  "test_add_throw_exception_for_negative_with_custom_delimiter": ["AC-4.3", "AC-3.3"],
  "test_add_throw_exception_for_single_negative_number": ["AC-4.3"],
  "test_add_include_single_number_1000_exactly": ["AC-4.2"],
  "test_add_ignore_single_number_greater_than_1000": ["AC-4.1"],
  "test_add_with_custom_delimiter_and_zero": ["AC-3.1", "AC-3.3"],
  "test_add_with_custom_delimiter_include_1000_exactly": ["AC-4.2", "AC-3.3"],
  "test_add_with_custom_delimiter_ignore_numbers_greater_than_1000": ["AC-4.1", "AC-3.3"],
  "test_add_with_custom_delimiter_and_trailing_newline": ["AC-3.2"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
