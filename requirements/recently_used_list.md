# Recently used items list

## Overview
A bounded, most-recent-first list of items, of the kind that backs a "recent files" menu. Newly used items go to the front, the list holds each item at most once, and once the list is full the oldest entry is dropped to make room. Entries can be read back by position, with position zero always the most recently used item.

## User Stories

### US-1: Tracking recently used items, newest first
As a user, I want the items I use recorded with the newest first, so that I can quickly return to what I touched last.

- AC-1.1: An added item is kept on the list, and the item count reflects it.
- AC-1.2: Reading the whole list returns items in most-recently-added-first order.

### US-2: Keeping items unique
As a user, I want an item to appear on the list only once, so that repeats do not crowd out other entries.

- AC-2.1: Adding an item that is already on the list does not create a second entry and does not consume capacity.

### US-3: Bounding the list's size
As a user, I want the list capped at a fixed capacity, so that it stays short and relevant.

- AC-3.1: The default capacity is five items.
- AC-3.2: Adding to a full list drops the oldest entry, keeping only the most recent items up to capacity.
- AC-3.3: A different capacity can be chosen when the list is created, and the list reports the capacity it was given.

### US-4: Reading items by position
As a user, I want to fetch an item by its position, so that I can pick out a specific recent entry.

- AC-4.1: Items are retrieved by zero-based position, where position zero is the most recently used item.
- AC-4.2: A position past the last item is rejected with the exact message "supplied index [N] should not greater than [M]." where N is the supplied position and M is the last valid position.
- AC-4.3: A negative position is rejected with the exact message "supplied index [N] should be non-negative and not greater than [M]." where N is the supplied position and M is the last valid position.

### US-5: Rejecting empty entries
As a user, I want blank entries kept out, so that the list only ever holds usable items.

- AC-5.1: Adding a missing value or empty text is rejected with the exact message "List items should not be Empty or Null. But it was [V]" where V is the rejected value — a missing value renders as None, and empty text renders as nothing between the brackets.

## Traceability
```json
{
  "test_can_add_items": ["AC-1.1"],
  "test_can_add_unique_items": ["AC-2.1", "AC-1.2"],
  "test_can_add_items_in_lifo_order": ["AC-1.2"],
  "test_can_avoid_insertion_of_items_beyond_list_size": ["AC-3.2", "AC-2.1"],
  "test_can_test_item_by_index": ["AC-4.1"],
  "test_can_test_default_list_size": ["AC-3.1"],
  "test_can_throw_argument_exception_when_supplied_index_is_out_of_scope": ["AC-4.2"],
  "test_can_throw_argument_exception_when_supplied_index_contain_negative_value": ["AC-4.3"],
  "test_can_throw_argument_exception_when_supplied_item_is_null_or_empty": ["AC-5.1"],
  "test_can_define_list_size": ["AC-3.3"],
  "test_can_get_most_recently_used_item_at_index_zero": ["AC-4.1"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
