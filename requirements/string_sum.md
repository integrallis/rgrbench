# Adding two numbers held as text

## Overview
A small adding service takes two numbers written as text and returns their sum, also as text. Blank or missing operands count as zero, so the service always produces a numeric answer.

## User Stories

### US-1: Total two numeric text fields
As a clerk processing form fields, I want two numbers held as text added together, so that I get their total without converting the values myself.

- AC-1.1: Two numeric texts yield the text of their sum (worked example: "1" and "2" yield "3").
- AC-1.2: An empty or missing operand counts as zero, so the result equals the other operand's value.
- AC-1.3: When both operands are empty or missing, the result is "0".

## Traceability
```json
{
  "test_add_return_sum": ["AC-1.3"],
  "test_add_two_numbers_return_sum": ["AC-1.1"],
  "test_add_treats_null_or_empty_as_zero": ["AC-1.2"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
