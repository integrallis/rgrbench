# Spelling numbers as English words

## Overview
A number-spelling service turns any whole number from 0 through 9999 into its English
words, following everyday conventions: hyphenated compounds for twenty-one through
ninety-nine, no "and" between parts, and plain spaces between the thousands, hundreds,
and remainder portions.

## User Stories

### US-1: Spelling numbers up to twenty
As a reader of generated documents, I want small numbers spelled with their single everyday names, so that they read naturally.

- AC-1.1: Zero is spelled "zero", and single digits use their names, such as "five" and
  "eight".
- AC-1.2: Ten is spelled "ten", and the teens are single unhyphenated words, such as
  "thirteen" and "nineteen".

### US-2: Spelling two-digit numbers
As a reader, I want tens and their compounds spelled the conventional way, so that numbers like 21 and 99 look as they would in prose.

- AC-2.1: Round tens are single words with no hyphen, such as "twenty" and "ninety".
- AC-2.2: Other two-digit numbers are hyphenated tens-units compounds: 21 is
  "twenty-one", 77 is "seventy-seven", and 99 is "ninety-nine".

### US-3: Spelling hundreds
As a reader, I want three-digit numbers spelled with an explicit hundreds part, so that the wording is unambiguous.

- AC-3.1: 100 is "one hundred"; the leading "one" is always kept.
- AC-3.2: A hundreds part is followed by the spelled remainder separated by a space:
  303 is "three hundred three", 555 is "five hundred fifty-five", and 115 is
  "one hundred fifteen".
- AC-3.3: The word "and" never joins the hundreds to the remainder.

### US-4: Spelling thousands
As a reader, I want four-digit numbers spelled with a thousands part, so that the full supported range reads correctly.

- AC-4.1: 1000 is "one thousand" with the leading "one" kept, and round thousands
  follow the same pattern, such as "two thousand".
- AC-4.2: The thousands part is followed by the spelled remainder: 2400 is
  "two thousand four hundred", 3466 is "three thousand four hundred sixty-six", and an
  empty hundreds part is simply omitted, so 5005 is "five thousand five".
- AC-4.3: The largest supported number, 9999, is
  "nine thousand nine hundred ninety-nine".

### US-5: Rejecting numbers outside the range
As an integrator, I want inputs outside 0 through 9999 refused, so that unsupported numbers can never produce wrong words.

- AC-5.1: Negative numbers are rejected with an error whose message includes
  "must be in 0..9999".
- AC-5.2: Numbers greater than 9999 are rejected with the same error message wording.

## Traceability
```json
{
  "test_zero": ["AC-1.1"],
  "test_single_digit_five": ["AC-1.1"],
  "test_single_digit_eight": ["AC-1.1"],
  "test_ten": ["AC-1.2"],
  "test_teens_are_single_words": ["AC-1.2"],
  "test_round_tens_have_no_hyphen": ["AC-2.1"],
  "test_twenty_one_is_hyphenated": ["AC-2.2"],
  "test_seventy_seven_is_hyphenated": ["AC-2.2"],
  "test_ninety_nine_is_hyphenated": ["AC-2.2"],
  "test_one_hundred_keeps_leading_one": ["AC-3.1"],
  "test_hundreds_with_units_remainder": ["AC-3.2"],
  "test_hundreds_with_compound_remainder": ["AC-3.2"],
  "test_no_and_between_hundreds_and_remainder": ["AC-3.3"],
  "test_hundreds_with_teen_remainder": ["AC-3.2"],
  "test_one_thousand_keeps_leading_one": ["AC-4.1"],
  "test_round_thousands": ["AC-4.1"],
  "test_thousands_with_round_hundreds": ["AC-4.2"],
  "test_full_four_digit_number": ["AC-4.2"],
  "test_thousands_skipping_hundreds": ["AC-4.2"],
  "test_largest_supported_number": ["AC-4.3"],
  "test_negative_numbers_are_rejected": ["AC-5.1"],
  "test_numbers_above_9999_are_rejected": ["AC-5.2"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
