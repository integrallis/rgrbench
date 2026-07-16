# Fibonacci number lookup

## Overview
A lookup service for the Fibonacci sequence, addressed by position counting from 1: the sequence begins 0, 1, 1, 2, 3, 5, and each later number is the sum of the two before it. Asking for the number at a given position returns that Fibonacci number; positions below 1 are refused because the sequence starts at position 1. The suite describes this as the dynamic-programming variant of the lookup.

## User Stories

### US-1: Look up Fibonacci numbers by position
As a mathematics student, I want the Fibonacci number at any position, so that I can explore the sequence without computing it by hand.

- AC-1.1: The number at position 1 is 0.
- AC-1.2: The number at position 2 is 1.
- AC-1.3: The number at position 3 is 1.
- AC-1.4: Larger positions follow the sequence: position 10 yields 34 and position 15 yields 377.

### US-2: Refuse positions outside the sequence
As a mathematics student, I want positions below 1 refused with a clear explanation, so that off-by-one mistakes surface immediately.

- AC-2.1: A negative position is refused with a type error.
- AC-2.2: Position 0 is refused with a type error whose message is exactly "Fibonacci numbers start from 1".

## Traceability
```json
{
  "test_first_fibonacci_number": ["AC-1.1"],
  "test_second_fibonacci_number": ["AC-1.2"],
  "test_third_fibonacci_number": ["AC-1.3"],
  "test_larger_fibonacci_numbers": ["AC-1.4"],
  "test_negative_number_raises_error": ["AC-2.1"],
  "test_number_below_one_raises_error_with_message": ["AC-2.2"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
