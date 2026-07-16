# Minimum-finding utilities

## Overview
A small library of minimum-finding operations covering different calling styles: comparing exactly two numbers, taking any number of candidates, requiring at least one candidate, restricting the winner to a low–high range, and manufacturing reusable range-restricted finders. It also includes a deliberately unusable variant that always refuses, demonstrating an operation whose contract demands arguments it cannot accept.

## User Stories

### US-1: Find the smallest of my numbers
As a developer, I want the smallest value among the numbers I supply, so that I can select minima under several calling styles.

- AC-1.1: Given exactly two numbers, the smaller one is returned (1 and 34 give 1).
- AC-1.2: The single-value variant returns the one value it is given.
- AC-1.3: The any-count variant returns the smallest of all supplied candidates (1, 2, 3, 4 give 1).
- AC-1.4: Duplicates and negative values are handled: the smallest of -5, -5, 0, 3, -2 is -5.
- AC-1.5: The any-count variant refuses an empty candidate list as an invalid value.
- AC-1.6: The at-least-one variant takes a required first value plus any further values and returns the smallest among all of them (124 against 1123, 1421, 12 gives 12).
- AC-1.7: The required first value participates in the comparison and wins when it is the smallest (3 against 10, 20 gives 3).
- AC-1.8: The at-least-one variant accepts exactly one value and returns it.

### US-2: A variant that always refuses
As a developer, I want a variant that accepts no input and always refuses when called, so that the argument-requirement contract is observable.

- AC-2.1: Calling the no-argument variant raises a type error.
- AC-2.2: The error message is exactly "Function requires arguments".

### US-3: Find the smallest within bounds
As a developer, I want the smallest candidate lying within a named low–high range, so that out-of-range values are ignored.

- AC-3.1: Given candidates plus named low and high bounds, the result is the smallest candidate within the range (-54, 45, 23 with bounds 0 to 127 give 23).
- AC-3.2: The bounds are inclusive at the bottom: a candidate equal to the low bound is eligible and wins when smallest (0 with bounds 0 to 127 is returned).
- AC-3.3: The bounds are inclusive at the top: a candidate equal to the high bound is eligible (127 with bounds 0 to 127 is returned when it is the only in-range candidate).
- AC-3.4: When no candidate falls within the range, the high bound itself is returned.

### US-4: Manufacture pre-configured bounded finders
As a developer, I want to create a finder with its bounds fixed up front, so that I can reuse it without repeating the bounds.

- AC-4.1: Given low and high bounds, a callable finder is produced.
- AC-4.2: The produced finder returns the smallest of its candidates within the fixed bounds (bounds 0 to 255; candidates -5, 12, 13 give 12).

## Traceability
```json
{
  "test_get_min_should_return_smaller_of_two_numbers": ["AC-1.1"],
  "test_get_min_without_arguments_should_raise_type_error": ["AC-2.1"],
  "test_get_min_with_one_argument_should_return_that_value": ["AC-1.2"],
  "test_get_min_with_many_arguments_should_return_smallest": ["AC-1.3"],
  "test_get_min_with_one_or_more_arguments_should_return_smallest": ["AC-1.6"],
  "test_get_min_bounded_should_return_smallest_within_bounds": ["AC-3.1"],
  "test_make_min_should_return_callable_bounded_function": ["AC-4.1", "AC-4.2"],
  "test_get_min_bounded_with_no_valid_args_should_return_high": ["AC-3.4"],
  "test_get_min_without_arguments_should_raise_with_exact_message": ["AC-2.2"],
  "test_get_min_with_one_or_more_arguments_when_first_is_smallest": ["AC-1.7"],
  "test_get_min_with_many_arguments_handles_duplicates_and_negatives": ["AC-1.4"],
  "test_get_min_with_many_arguments_with_no_arguments_raises_value_error": ["AC-1.5"],
  "test_get_min_bounded_includes_value_equal_to_low": ["AC-3.2"],
  "test_get_min_bounded_includes_value_equal_to_high": ["AC-3.3"],
  "test_get_min_with_exactly_one_argument": ["AC-1.8"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
