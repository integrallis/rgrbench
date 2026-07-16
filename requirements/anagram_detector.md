# Anagram detection

## Overview
A word-play tool that decides whether two pieces of text are anagrams of each other, finds all anagrams of a subject word within a candidate list, and sorts a list of words into anagram clusters. Two texts are anagrams when they contain the same letters with the same frequencies, compared case-insensitively and ignoring spaces and punctuation — with the twist that a word is never counted as an anagram of itself.

## User Stories

### US-1: Detect whether two texts are anagrams
As a word-game player, I want to know whether two texts are anagrams, so that I can verify a proposed rearrangement.

- AC-1.1: Two different words whose letters match with equal frequencies are anagrams (examples: "listen"/"silent", "cat"/"tac", "ab"/"ba").
- AC-1.2: Texts whose letters differ, or whose shared letters occur with different frequencies, are not anagrams (examples: "hello"/"world"; "aab"/"abb").
- AC-1.3: Letter comparison is case-insensitive ("Cat" and "tac" are anagrams).
- AC-1.4: A word is never an anagram of itself: identical words, identical single letters, the same word differing only in letter case, and two empty texts are all rejected.
- AC-1.5: Spaces are ignored ("Dormitory" and "Dirty Room" are anagrams).
- AC-1.6: Punctuation is ignored ("Astronomer" and "Moon starer!" are anagrams).

### US-2: Find anagrams in a candidate list
As a word-game player, I want all anagrams of a subject word picked out of a candidate list, so that I can see every valid rearrangement at once.

- AC-2.1: All candidates that are anagrams of the subject are returned, preserving their order in the candidate list ("listen" against "silent" and "tinsel" returns both).
- AC-2.2: When no candidate matches, the result is an empty collection.
- AC-2.3: Candidates that are not anagrams are filtered out while matches are kept ("master" keeps "stream" and "maters" but drops "pigeon").
- AC-2.4: A candidate identical to the subject word is not a match, following the a-word-is-not-its-own-anagram rule.

### US-3: Group a word list into anagram clusters
As a word-game player, I want a word list organised into clusters of mutual anagrams, so that related words are presented together.

- AC-3.1: Words that are anagrams of one another form a single cluster ("eat", "tea", "ate" cluster together).
- AC-3.2: Words unrelated to any other word each form their own single-word cluster.
- AC-3.3: An empty word list yields no clusters.
- AC-3.4: Clusters are ordered by the first appearance of any of their words in the input, and words inside a cluster keep their input order.

## Traceability
```json
{
  "test_listen_and_silent_are_anagrams": ["AC-1.1"],
  "test_hello_and_world_are_not_anagrams": ["AC-1.2"],
  "test_cat_and_tac_are_anagrams": ["AC-1.1"],
  "test_word_is_not_anagram_of_itself": ["AC-1.4"],
  "test_comparison_is_case_insensitive": ["AC-1.3"],
  "test_empty_strings_are_not_anagrams": ["AC-1.4"],
  "test_single_identical_letter_is_not_anagram": ["AC-1.4"],
  "test_two_letter_swap_is_anagram": ["AC-1.1"],
  "test_same_letters_different_frequencies_are_not_anagrams": ["AC-1.2"],
  "test_same_word_in_different_case_is_still_itself": ["AC-1.3", "AC-1.4"],
  "test_spaces_are_ignored": ["AC-1.5"],
  "test_punctuation_is_ignored": ["AC-1.6"],
  "test_find_anagrams_returns_all_matches": ["AC-2.1"],
  "test_find_anagrams_returns_empty_when_no_matches": ["AC-2.2"],
  "test_find_anagrams_filters_non_matches": ["AC-2.3"],
  "test_find_anagrams_excludes_the_subject_word_itself": ["AC-2.4"],
  "test_group_anagrams_clusters_mutual_anagrams": ["AC-3.1"],
  "test_group_anagrams_keeps_unrelated_words_apart": ["AC-3.2"],
  "test_group_anagrams_of_empty_list_is_empty": ["AC-3.3"],
  "test_group_anagrams_orders_clusters_by_first_appearance": ["AC-3.4"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
