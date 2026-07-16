# Singly linked sequence

## Overview
An ordered collection built from individually linked cells rather than a built-in container: each cell carries a value and a link to its successor, and the whole collection is entered through a head reference. The collection supports adding at either end, positional reads, insertion and removal at any position, value search, and in-place reversal.

## User Stories

### US-1: Build and inspect the collection
As a developer, I want to build an ordered collection cell by cell, so that I can manage a sequence without relying on built-in containers.

- AC-1.1: A brand-new collection is empty: its size is zero, its contents read back as an empty sequence, and it has no head cell.
- AC-1.2: Adding to the end of an empty collection yields a one-element collection.
- AC-1.3: Successive additions at the end preserve insertion order.
- AC-1.4: An element can be added at the front, taking its place before all existing elements.
- AC-1.5: The head exposes the chain of cells: each cell carries its value and a link to the next cell, and the final cell links to nothing.
- AC-1.6: The reported size tracks every addition — at either end — and every removal.

### US-2: Positional access
As a developer, I want to read the element at any position, so that I can address the sequence directly.

- AC-2.1: Positions count from zero, and every position from the first to the last element can be read.
- AC-2.2: Reading a position outside the range zero to size minus one — including any position of an empty collection — is refused with an out-of-range error carrying the message "index out of bounds".

### US-3: Removal
As a developer, I want to remove the element at a position, so that the collection stays correctly linked afterward.

- AC-3.1: A removal hands back the value that was removed.
- AC-3.2: Removing the first element promotes the second element to the head.
- AC-3.3: Removing a middle element links its former neighbours directly together.
- AC-3.4: Removing the final element drops the tail, leaving the rest intact.
- AC-3.5: Removing the only element leaves an empty collection with no head.
- AC-3.6: Removing at a position outside the range zero to size minus one — including from an empty collection — is refused with an out-of-range error carrying the message "index out of bounds".

### US-4: Insertion at a position
As a developer, I want to insert an element at any position, so that I can splice values into place.

- AC-4.1: Inserting at position zero behaves like adding at the front.
- AC-4.2: Inserting at a middle position shifts that element and its successors one place toward the end, growing the size by exactly one.
- AC-4.3: Inserting at the position equal to the current size appends at the end.
- AC-4.4: Inserting at a position outside the range zero to the current size is refused with an out-of-range error carrying the message "index out of bounds".

### US-5: Search
As a developer, I want to look values up, so that I can tell whether and where a value is stored.

- AC-5.1: Membership is reported as true for stored values and false for absent ones.
- AC-5.2: The reported position of a value is that of its first occurrence, counting from zero, wherever it sits in the collection.
- AC-5.3: The reported position of an absent value is minus one.

### US-6: Reversal
As a developer, I want to reverse the collection in place, so that I can traverse it in the opposite order.

- AC-6.1: Reversal flips the element order while keeping the same size.
- AC-6.2: Reversing an empty or single-element collection leaves it unchanged.

## Traceability
```json
{
  "test_new_list_is_empty": ["AC-1.1"],
  "test_append_to_empty_list_creates_a_single_element_list": ["AC-1.2"],
  "test_append_adds_elements_at_the_end": ["AC-1.3"],
  "test_prepend_adds_elements_at_the_beginning": ["AC-1.4"],
  "test_elements_are_linked_through_node_next_pointers": ["AC-1.5"],
  "test_size_tracks_additions_and_removals": ["AC-1.6"],
  "test_get_returns_the_value_at_each_index": ["AC-2.1"],
  "test_get_with_an_invalid_index_is_an_error": ["AC-2.2"],
  "test_get_on_an_empty_list_is_an_error": ["AC-2.2"],
  "test_remove_returns_the_removed_value": ["AC-3.1"],
  "test_remove_first_element_updates_the_head": ["AC-3.2"],
  "test_remove_middle_element_closes_the_gap": ["AC-3.3"],
  "test_remove_last_element": ["AC-3.4"],
  "test_remove_the_only_element_leaves_an_empty_list": ["AC-3.5"],
  "test_remove_from_an_empty_list_is_an_error": ["AC-3.6"],
  "test_remove_with_an_invalid_index_is_an_error": ["AC-3.6"],
  "test_insert_at_the_beginning": ["AC-4.1"],
  "test_insert_at_a_middle_index_shifts_elements_right": ["AC-4.2"],
  "test_insert_at_size_is_equivalent_to_append": ["AC-4.3"],
  "test_insert_at_an_invalid_index_is_an_error": ["AC-4.4"],
  "test_contains_reports_presence_and_absence": ["AC-5.1"],
  "test_index_of_returns_the_first_occurrence": ["AC-5.2"],
  "test_index_of_a_missing_value_is_minus_one": ["AC-5.3"],
  "test_reverse_reverses_the_element_order": ["AC-6.1"],
  "test_reverse_of_empty_and_single_element_lists_is_harmless": ["AC-6.2"],
  "test_insert_at_a_middle_index_grows_the_size_by_one": ["AC-4.2"],
  "test_index_of_reaches_positions_beyond_the_second": ["AC-5.2"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
