# Adding two numbers

## Overview
The smallest possible arithmetic service: it adds two numbers and returns the result, handling positive numbers, negative numbers, and zero alike.

## User Stories

### US-1: Add a pair of numbers
As a user of a basic calculator, I want two numbers added together, so that I get their total.

- AC-1.1: Adding two positive numbers yields their sum (1 plus 1 is 2).
- AC-1.2: Negative numbers take part in the sum correctly, whether mixed with positives or added to each other (-1 plus 1 is 0; -5 plus -3 is -8).
- AC-1.3: Zero behaves as the identity: adding zero to any value, in either position, leaves the value unchanged.

## Traceability
```json
{
  "test_sum_two_numbers": ["AC-1.1"],
  "test_sum_negative_numbers": ["AC-1.2"],
  "test_sum_with_zero": ["AC-1.3"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
