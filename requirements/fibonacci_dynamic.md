# Fibonacci numbers with memoization

## Overview
A Fibonacci sequence service addressed by position counting from 1: the sequence begins 0, 1, 1, 2, 3, 5, and each later number is the sum of the two before it. Asking for the number at a given position returns that Fibonacci number; negative positions are refused because the sequence is not defined there. The suite describes this as the dynamic-programming variant, memoized so that larger positions are computed efficiently.

## User Stories

### US-1: Look up Fibonacci numbers by position
As a mathematics student, I want the Fibonacci number at any position, so that I can explore the sequence without computing it by hand.

- AC-1.1: The number at position 1 is 0.
- AC-1.2: The number at position 2 is 1.
- AC-1.3: The number at position 3 is 1.
- AC-1.4: Positions beyond the seeded start follow the sequence: position 6 yields 5.

### US-2: Refuse positions where the sequence is undefined
As a mathematics student, I want invalid positions refused with a clear reason, so that misuse surfaces immediately.

- AC-2.1: A negative position is refused as an invalid value.
- AC-2.2: The refusal carries exactly the message "Fibonacci sequence is not defined for negative numbers".

## Traceability
```json
{
  "test_the_first_number_should_be_zero": ["AC-1.1"],
  "test_the_second_number_should_be_one": ["AC-1.2"],
  "test_the_third_number_should_be_one": ["AC-1.3"],
  "test_long_argument_should_calculate_with_memoization": ["AC-1.4"],
  "test_negative_number_should_raise_exception": ["AC-2.1", "AC-2.2"],
  "test_negative_number_error_message": ["AC-2.2"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
