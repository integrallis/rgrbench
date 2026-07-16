# Prime factor decomposition

## Overview
A factoring service breaks a positive whole number into the list of prime numbers whose
product reconstructs it, listing each prime once per occurrence, in ascending order.

## User Stories

### US-1: Decomposing a number into prime factors
As a student of number theory, I want any positive whole number decomposed into its prime factors, so that the multiplicative structure of the number is laid bare.

- AC-1.1: The number 1 has no prime factors and yields the empty list.
- AC-1.2: A prime number yields a single factor: itself; 2 yields 2 and 3 yields 3.
- AC-1.3: A composite number yields its prime factors in ascending order, repeated
  according to multiplicity, so that their product equals the number; 4 yields 2 and 2,
  6 yields 2 and 3, 8 yields 2, 2, and 2, and 9 yields 3 and 3.
- AC-1.4: Large numbers decompose exactly; 5 to the 9th power times 7 to the 13th power
  yields nine 5s followed by thirteen 7s.

## Traceability
```json
{
  "test_one": ["AC-1.1"],
  "test_two": ["AC-1.2"],
  "test_three": ["AC-1.2"],
  "test_four": ["AC-1.3"],
  "test_six": ["AC-1.3"],
  "test_eight": ["AC-1.3"],
  "test_nine": ["AC-1.3"],
  "test_large_number": ["AC-1.4"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
