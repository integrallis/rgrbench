# Bracket balance checking

## Overview
A validator for strings made of square brackets. A string is balanced when its brackets form complete pairs in the correct sequence: every opening bracket has a matching closing bracket, nesting is consistent, and a closing bracket never arrives before its opener. The validator answers yes or no for any such string.

## User Stories

### US-1: Accept balanced bracket strings
As a text validator user, I want correctly paired bracket strings accepted, so that well-formed input passes the check.

- AC-1.1: The empty string is balanced.
- AC-1.2: A single matched pair is balanced, as are multiple pairs in sequence ("[]" and "[][]").
- AC-1.3: Pairs nested inside other pairs are balanced, including mixes of nesting and sequencing ("[[]]" and "[[[][]]]").
- AC-1.4: Nesting depth is not limited by a small bound: fifty openers followed by fifty closers are balanced.

### US-2: Reject unbalanced bracket strings
As a text validator user, I want malformed bracket strings rejected, so that broken input is caught.

- AC-2.1: A closing bracket arriving before its opener makes the string unbalanced ("][" and "][][").
- AC-2.2: Opening brackets left unmatched make the string unbalanced ("[", "[[", "[[]").
- AC-2.3: Closing brackets with no matching opener make the string unbalanced ("]", "]]", "[]]").
- AC-2.4: Extra unmatched brackets after otherwise valid pairs make the string unbalanced ("[][]][").

## Traceability
```json
{
  "test_empty_string_is_balanced": ["AC-1.1"],
  "test_single_pair_is_balanced": ["AC-1.2"],
  "test_sequential_pairs_are_balanced": ["AC-1.2"],
  "test_nested_pair_is_balanced": ["AC-1.3"],
  "test_complex_nesting_is_balanced": ["AC-1.3"],
  "test_closing_before_opening_is_unbalanced": ["AC-2.1"],
  "test_misaligned_pairs_are_unbalanced": ["AC-2.1"],
  "test_extra_unmatched_brackets_are_unbalanced": ["AC-2.4"],
  "test_lone_opening_bracket_is_unbalanced": ["AC-2.2"],
  "test_lone_closing_bracket_is_unbalanced": ["AC-2.3"],
  "test_two_openers_are_unbalanced": ["AC-2.2"],
  "test_two_closers_are_unbalanced": ["AC-2.3"],
  "test_extra_closer_after_pair_is_unbalanced": ["AC-2.3"],
  "test_unclosed_nested_opener_is_unbalanced": ["AC-2.2"],
  "test_deep_nesting_is_balanced": ["AC-1.4"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
