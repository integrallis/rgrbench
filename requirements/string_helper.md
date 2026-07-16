# Matching opening and closing letter pairs

## Overview
A text check that reports whether a piece of text begins and ends with the same two-character sequence, used to spot "bookended" words and phrases automatically.

## User Stories

### US-1: Spot bookended text
As an editor scanning words, I want to know whether a text opens and closes with the same two characters, so that bookended terms can be flagged automatically.

- AC-1.1: Text shorter than two characters — empty text or a single character — never matches.
- AC-1.2: Text of exactly two characters always matches, because its opening pair and its closing pair are the same two characters.
- AC-1.3: Longer text matches exactly when its first two characters, in order, are identical to its last two characters, in order (worked examples: "AAA" and "ABCAB" match; "ABC" and "ABCDEBA" do not).

## Traceability
```json
{
  "test_are_first_and_last_two_chars_same_empty_string": ["AC-1.1"],
  "test_are_first_and_last_two_chars_same_single_char": ["AC-1.1"],
  "test_are_first_and_last_two_chars_same_two_chars": ["AC-1.2"],
  "test_are_first_and_last_two_chars_same_three_chars_not_matching": ["AC-1.3"],
  "test_are_first_and_last_two_chars_same_three_chars_matching": ["AC-1.3"],
  "test_are_first_and_last_two_chars_same_five_chars_matching": ["AC-1.3"],
  "test_are_first_and_last_two_chars_same_seven_chars_not_matching": ["AC-1.3"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
