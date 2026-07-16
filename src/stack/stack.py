"""Stack data structure implementation"""


class EmptyStackError(Exception):
    """Exception raised when popping from empty stack"""

    pass


class FullStackError(Exception):
    """Exception raised when pushing to full stack"""

    pass


class Stack:
    """Stack implementation using list"""

    def __init__(self, capacity: int | None = None) -> None:
        if capacity is not None and capacity < 0:
            raise ValueError("Capacity cannot be negative")
        self.items: list[int] = []
        self.capacity = capacity

    def is_empty(self) -> bool:
        """Check if stack is empty"""
        return len(self.items) == 0

    def push(self, item: int) -> None:
        """Push item onto stack"""
        if self.capacity is not None and len(self.items) >= self.capacity:
            raise FullStackError("Stack is full")
        self.items.append(item)

    def pop(self) -> int:
        """Pop item from stack"""
        if self.is_empty():
            raise EmptyStackError("Cannot pop from empty stack")
        return self.items.pop()
