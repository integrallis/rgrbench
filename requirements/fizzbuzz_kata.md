# FizzBuzz counting game

## Overview
The classic FizzBuzz counting game over the numbers 1 to 100: each number is called out as itself, except that multiples of 3 are called "Fizz", multiples of 5 are called "Buzz", and multiples of both are called "FizzBuzz". The game can call out a single number or produce the whole sequence in one go, and it refuses any number outside the 1-to-100 rule with a precise explanation.

## User Stories

### US-1: Call out a single number
As a player, I want any single number called out according to the game's rules, so that I can check one answer at a time.

- AC-1.1: A number divisible by neither 3 nor 5 is called out as the number itself (1 is called "1").
- AC-1.2: A multiple of 3 that is not a multiple of 5 is called "Fizz" (3).
- AC-1.3: A multiple of 5 that is not a multiple of 3 is called "Buzz" (5, and 100 at the upper boundary).
- AC-1.4: A multiple of both 3 and 5 is called "FizzBuzz" (15 and 30).

### US-2: Play the whole game at once
As a player, I want the full sequence produced in one call, so that I can see the entire game from 1 to 100.

- AC-2.1: When no particular number is requested, the calls for 1 through 100 are produced in order as a single line of text joined by single spaces, beginning "1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz" and ending "97 98 Fizz Buzz".

### US-3: Enforce the 1-to-100 rule
As a player, I want numbers outside the game refused with an exact explanation, so that invalid play is impossible.

- AC-3.1: Numbers below 1 and numbers above 100 are refused (0, -1, and 101 are all rejected).
- AC-3.2: The refusal message is exactly: entered number is [N], which does not meet rule, entered number should be between 1 to 100. — where N is replaced by the offending number, brackets included.

## Traceability
```json
{
  "test_can_test_fizz": ["AC-2.1"],
  "test_can_test_single_number_1": ["AC-1.1"],
  "test_can_test_single_number_3": ["AC-1.2"],
  "test_can_test_single_number_5": ["AC-1.3"],
  "test_can_test_single_number_15": ["AC-1.4"],
  "test_can_test_single_number_30": ["AC-1.4"],
  "test_can_test_single_number_100": ["AC-1.3"],
  "test_can_throw_argument_exception_when_number_is_negative_1": ["AC-3.1", "AC-3.2"],
  "test_can_throw_argument_exception_when_number_is_101": ["AC-3.1", "AC-3.2"],
  "test_can_throw_argument_exception_when_number_is_0": ["AC-3.1", "AC-3.2"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
