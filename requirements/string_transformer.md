# Chainable text styling pipeline

## Overview
A text styling tool wraps a piece of text and offers small transformations — capitalising words, reversing, stripping whitespace, restyling into snake case or camel case, truncating, repeating, and replacing — which can be chained in any order; the finished text is read out at the end of the pipeline.

## User Stories

### US-1: Capitalise words
As a writer preparing headings, I want each word's first letter uppercased, so that text reads like a title.

- AC-1.1: The first letter of every word is uppercased (worked example: "hello world" becomes "Hello World").
- AC-1.2: Letters other than each word's first are left untouched ("hello WORLD" becomes "Hello WORLD").
- AC-1.3: Capitalising empty text yields empty text.
- AC-1.4: Words begin only after separators; an uppercase letter inside a word does not start a new word ("teXas rocks" becomes "TeXas Rocks").

### US-2: Reverse text and strip whitespace
As an editor cleaning copy, I want to reverse text or strip all whitespace from it, so that I can produce mirrored or compacted variants.

- AC-2.1: Reversing turns the whole text back to front ("hello world" becomes "dlrow olleh").
- AC-2.2: Whitespace removal deletes every space ("hello world" becomes "helloworld").
- AC-2.3: Whitespace removal also deletes tabs and line breaks.

### US-3: Restyle into identifier conventions
As a developer generating identifiers, I want text restyled into snake case or camel case, so that names follow my naming convention.

- AC-3.1: Snake case joins words with underscores ("hello world" becomes "hello_world").
- AC-3.2: Hyphens count as word separators for snake case ("hello-world test" becomes "hello_world_test").
- AC-3.3: Snake case lowercases every word ("Hello World" becomes "hello_world").
- AC-3.4: Camel case lowercases the first word and capitalises every later word, joining all words with nothing in between ("Hello World" becomes "helloWorld"; "one two three" becomes "oneTwoThree").
- AC-3.5: Camel case normalises fully uppercase input ("HELLO WORLD" becomes "helloWorld").
- AC-3.6: Camel case of a single word is just that word lowercased.
- AC-3.7: Camel case of text containing no words at all — empty text or separators only — yields empty text.

### US-4: Truncate and repeat
As a layout author, I want text truncated to a length or repeated a number of times, so that it fits the slot it is destined for.

- AC-4.1: Truncating cuts the text to the requested number of characters and appends the ellipsis character "…" whenever something was cut ("hello world" truncated to 5 becomes "hello…").
- AC-4.2: Truncating to a length equal to or beyond the text's length leaves the text unchanged, with no ellipsis.
- AC-4.3: Truncating to zero removes everything, leaving only the ellipsis.
- AC-4.4: A negative truncation length is refused with the message exactly "length must not be negative".
- AC-4.5: Repeating produces the text the requested number of times, separated by single spaces ("ha" repeated 3 times becomes "ha ha ha").
- AC-4.6: Repeating once leaves the text unchanged; repeating zero times yields empty text.
- AC-4.7: A negative repeat count is refused with the message exactly "times must not be negative".

### US-5: Replace text and chain transformations
As a power user, I want to substitute text and chain several transformations together, so that one pipeline produces the finished result.

- AC-5.1: Replacement substitutes every occurrence of the target text ("hello world hello" with "hello" replaced by "bye" becomes "bye world bye").
- AC-5.2: Transformations chain and are applied strictly in the order requested; requesting the same transformations in a different order can give a different result.
- AC-5.3: With no transformations requested, the output is the original text unchanged.

## Traceability
```json
{
  "test_capitalise_first_letter_of_each_word": ["AC-1.1"],
  "test_capitalise_leaves_other_letters_unchanged": ["AC-1.2"],
  "test_capitalise_empty_string": ["AC-1.3"],
  "test_reverse_entire_string": ["AC-2.1"],
  "test_remove_whitespace": ["AC-2.2"],
  "test_remove_whitespace_covers_tabs_and_newlines": ["AC-2.3"],
  "test_snake_case_basic": ["AC-3.1"],
  "test_snake_case_handles_hyphens": ["AC-3.2"],
  "test_snake_case_lowercases": ["AC-3.3"],
  "test_camel_case_basic": ["AC-3.4"],
  "test_camel_case_uppercase_input": ["AC-3.5"],
  "test_camel_case_single_word": ["AC-3.6"],
  "test_truncate_adds_ellipsis_when_cut": ["AC-4.1"],
  "test_truncate_leaves_short_text_unchanged": ["AC-4.2"],
  "test_truncate_exact_length_is_unchanged": ["AC-4.2"],
  "test_truncate_negative_length_is_rejected": ["AC-4.4"],
  "test_repeat_with_space_separator": ["AC-4.5"],
  "test_repeat_boundaries": ["AC-4.6"],
  "test_repeat_negative_times_is_rejected": ["AC-4.7"],
  "test_replace_all_occurrences": ["AC-5.1"],
  "test_chaining_capitalise_then_reverse": ["AC-5.2"],
  "test_chaining_snake_case_then_capitalise": ["AC-5.2"],
  "test_operations_are_applied_in_order": ["AC-5.2"],
  "test_result_without_operations_returns_initial_text": ["AC-5.3"],
  "test_capitalise_only_starts_words_after_separators": ["AC-1.4"],
  "test_camel_case_of_text_without_words_is_empty": ["AC-3.7"],
  "test_camel_case_joins_three_or_more_words_directly": ["AC-3.4"],
  "test_truncate_to_zero_keeps_only_the_ellipsis": ["AC-4.3"],
  "test_negative_count_rejections_carry_exact_messages": ["AC-4.4", "AC-4.7"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
