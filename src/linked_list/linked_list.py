"""Singly linked list kata.

A from-scratch singly linked list built solely from Node objects (a value plus
a next pointer); no built-in sequence backs the storage and the list keeps a
public head pointer. The list exposes append, prepend, size, get, remove
(returning the removed value), insert_at (where insert_at(size(), v) acts as
append), contains, index_of (first match or -1 when absent), to_list for
inspection, and in-place reverse. Index arguments must lie in range: negative
or out-of-bounds positions raise IndexError("index out of bounds"), including
any removal from an empty list.

Kata catalogued at tddbuddy.com/katas/linked-list; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")

_OUT_OF_BOUNDS = "index out of bounds"


class Node(Generic[T]):
    """A single list cell holding a value and the link to the next cell."""

    def __init__(self, value: T, next: Node[T] | None = None) -> None:
        self.value = value
        self.next = next


class LinkedList(Generic[T]):
    """Singly linked list with 0-based indexing."""

    def __init__(self) -> None:
        self.head: Node[T] | None = None
        self._count = 0

    def size(self) -> int:
        """Return the number of elements in the list."""
        return self._count

    def append(self, value: T) -> None:
        """Add ``value`` at the end of the list."""
        node = Node(value)
        if self.head is None:
            self.head = node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = node
        self._count += 1

    def prepend(self, value: T) -> None:
        """Add ``value`` at the beginning of the list."""
        self.head = Node(value, self.head)
        self._count += 1

    def get(self, index: int) -> T:
        """Return the value at ``index``."""
        return self._node_at(index).value

    def remove(self, index: int) -> T:
        """Remove the element at ``index`` and return its value."""
        if index < 0 or index >= self._count:
            raise IndexError(_OUT_OF_BOUNDS)
        if index == 0:
            assert self.head is not None
            removed = self.head
            self.head = removed.next
        else:
            previous = self._node_at(index - 1)
            assert previous.next is not None
            removed = previous.next
            previous.next = removed.next
        self._count -= 1
        return removed.value

    def insert_at(self, index: int, value: T) -> None:
        """Insert ``value`` at ``index``, shifting later elements right."""
        if index < 0 or index > self._count:
            raise IndexError(_OUT_OF_BOUNDS)
        if index == 0:
            self.prepend(value)
        elif index == self._count:
            self.append(value)
        else:
            previous = self._node_at(index - 1)
            previous.next = Node(value, previous.next)
            self._count += 1

    def contains(self, value: T) -> bool:
        """Return True when ``value`` occurs in the list."""
        return self.index_of(value) != -1

    def index_of(self, value: T) -> int:
        """Return the index of the first occurrence of ``value``, or -1."""
        index = 0
        current = self.head
        while current is not None:
            if current.value == value:
                return index
            current = current.next
            index += 1
        return -1

    def to_list(self) -> list[T]:
        """Return the values as a Python list (inspection convenience)."""
        values: list[T] = []
        current = self.head
        while current is not None:
            values.append(current.value)
            current = current.next
        return values

    def reverse(self) -> None:
        """Reverse the list in place."""
        previous: Node[T] | None = None
        current = self.head
        while current is not None:
            current.next, previous, current = previous, current, current.next
        self.head = previous

    def _node_at(self, index: int) -> Node[T]:
        if index < 0 or index >= self._count:
            raise IndexError(_OUT_OF_BOUNDS)
        current = self.head
        for _ in range(index):
            assert current is not None
            current = current.next
        assert current is not None
        return current
