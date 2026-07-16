# Bounded last-in-first-out stack

## Overview
A last-in-first-out container of the classic pushdown kind. Values are pushed on top and popped off in reverse order of arrival. A maximum capacity may be chosen when the stack is created; a full stack refuses further pushes and an empty stack refuses pops, each failure carrying its own distinct error.

## User Stories

### US-1: Pushing and popping in last-in-first-out order
As a developer, I want values stored last-in-first-out, so that the most recently added value is always the first retrieved.

- AC-1.1: A newly created stack is empty.
- AC-1.2: Emptiness tracks contents: pushing one value and popping it leaves the stack empty, while pushing two values and popping one leaves it non-empty.
- AC-1.3: Popping returns values in the reverse of the order they were pushed.

### US-2: Refusing to pop when empty
As a developer, I want popping an empty stack to fail loudly, so that underflows never pass silently.

- AC-2.1: Popping an empty stack fails with a dedicated empty-stack error.
- AC-2.2: The empty-stack failure message is exactly "Cannot pop from empty stack".

### US-3: Enforcing an optional capacity
As a developer, I want an optional upper bound on the stack, so that unbounded growth can be prevented.

- AC-3.1: A maximum capacity may be set at creation; pushing onto a stack already holding that many values fails with a dedicated full-stack error.
- AC-3.2: The full-stack failure message is exactly "Stack is full".
- AC-3.3: A capacity of zero is valid — the very first push already fails as full.
- AC-3.4: A negative capacity is rejected at creation with the exact message "Capacity cannot be negative".

## Traceability
```json
{
  "test_new_stack_is_empty": ["AC-1.1"],
  "test_push_then_pop": ["AC-1.2"],
  "test_push_twice_pop_once": ["AC-1.2"],
  "test_pop_empty_stack_throws": ["AC-2.1"],
  "test_push_to_full_stack_throws": ["AC-3.1"],
  "test_stack_with_negative_size_throws": ["AC-3.4"],
  "test_stack_with_zero_capacity": ["AC-3.3"],
  "test_pop_returns_pushed_items_in_lifo_order": ["AC-1.3"],
  "test_pop_empty_stack_error_message": ["AC-2.2"],
  "test_push_to_full_stack_error_message": ["AC-3.2"],
  "test_negative_capacity_error_message": ["AC-3.4"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
