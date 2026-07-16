# Polite greeter

## Overview
A greeter composes an English greeting for one person, for nobody in particular, or for a
group. Groups are joined grammatically with "and" and an Oxford comma. Names written
entirely in uppercase are shouts and are answered with a shout of their own, kept separate
from the normal greeting. Entries containing commas are split into several names unless the
entry is wrapped in double quotes, which protects its commas.

## User Stories

### US-1: Greet one person, or nobody
As a host, I want a personal greeting for a single guest and a friendly fallback when no name is given, so that everyone is welcomed.

- AC-1.1: A single name is greeted as "Hello, <name>." (worked example: Bob is greeted with "Hello, Bob.").
- AC-1.2: A missing name, or an empty list of names, yields "Hello, my friend."
- AC-1.3: A list containing exactly one name is greeted the same way as that single name on its own.

### US-2: Greet a group grammatically
As a host, I want groups of names joined naturally, so that the greeting reads like proper English.

- AC-2.1: Two names are joined with "and": "Hello, Jill and Jane."
- AC-2.2: Three or more names are separated by commas with an Oxford comma before the final "and" (worked example: "Hello, Amy, Brian, and Charlotte.").

### US-3: Shout back at shouted names
As a host, I want shouted names answered in kind but kept apart from the normal greeting, so that the tone matches each guest.

- AC-3.1: A name written entirely in uppercase is a shout and is answered with a shouted greeting of the form "HELLO <NAME>!" (worked example: "HELLO JERRY!").
- AC-3.2: Lowercase and mixed-case names are not shouts and receive the normal greeting.
- AC-3.3: When normal and shouted names are mixed, the normal greeting comes first, followed by a separate shouted greeting introduced by "AND" (worked example: "Hello, Amy and Charlotte. AND HELLO BRIAN!").
- AC-3.4: Several shouted names share a single shout, joined by "AND" (worked example: "HELLO BRIAN AND JERRY!").

### US-4: Split on commas, respect quoting
As a host, I want entries containing commas handled sensibly, so that both multi-name entries and names containing commas come out right.

- AC-4.1: An entry containing a comma is split into separate names, and each split name is stripped of surrounding spaces.
- AC-4.2: An entry wrapped in double quotes is a single name: the quotes are removed and any commas inside are kept (worked example: an entry quoting "Charlie, Dianne" stays one name).
- AC-4.3: A lone opening quote does not make an entry quoted; the quote character remains part of the name (worked example: an entry of a quote followed by Bob greets as "Hello, "Bob.").
- AC-4.4: An entry consisting only of a pair of double quotes has its quotes removed, leaving an empty name (worked example: the greeting reads "Hello, .").

## Traceability
```json
{
  "test_greets_a_single_name": ["AC-1.1"],
  "test_greets_none_as_a_friend": ["AC-1.2"],
  "test_shouts_back_at_a_shouted_name": ["AC-3.1"],
  "test_greets_two_names_with_and": ["AC-2.1"],
  "test_greets_three_names_with_oxford_comma": ["AC-2.2"],
  "test_separates_shouted_names_from_normal_names": ["AC-3.3"],
  "test_greets_a_single_name_in_a_list": ["AC-1.3"],
  "test_greets_four_names_with_oxford_comma": ["AC-2.2"],
  "test_shouts_at_two_shouted_names_together": ["AC-3.4"],
  "test_shouts_at_a_single_shouted_name_in_a_list": ["AC-1.3", "AC-3.1"],
  "test_mixes_one_normal_and_one_shouted_name": ["AC-3.3"],
  "test_mixes_multiple_normal_and_multiple_shouted_names": ["AC-3.3", "AC-3.4"],
  "test_splits_comma_delimited_entries": ["AC-4.1"],
  "test_quoted_entries_keep_their_commas": ["AC-4.2"],
  "test_greets_an_empty_list_as_a_friend": ["AC-1.2"],
  "test_lowercase_name_is_not_shouted": ["AC-3.2"],
  "test_mixed_case_name_is_not_shouted": ["AC-3.2"],
  "test_split_names_are_stripped_of_surrounding_spaces": ["AC-4.1"],
  "test_entry_with_only_an_opening_quote_is_not_quoted": ["AC-4.3"],
  "test_empty_quoted_entry_yields_an_empty_name": ["AC-4.4"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
