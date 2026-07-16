"""Fluent, exception-free integer calculator with undo/redo and save."""


def _is_integer(value: object) -> bool:
    """Accept int values only; bool is excluded despite subclassing int."""
    return isinstance(value, int) and not isinstance(value, bool)


class Calculator:
    """Chainable integer calculator that never raises.

    Invalid input (non-integers, operations before seeding, undo/redo
    with empty history) leaves the calculator unchanged and returns it,
    keeping the chain intact.
    """

    def __init__(self) -> None:
        self._value: int | None = None
        self._undo_stack: list[int] = []
        self._redo_stack: list[int] = []

    def seed(self, value: int) -> "Calculator":
        """Set the starting value; calls after the first are ignored."""
        if self._value is None and _is_integer(value):
            self._value = value
        return self

    def plus(self, value: int) -> "Calculator":
        """Add an integer to the current value."""
        return self._apply(value, 1)

    def minus(self, value: int) -> "Calculator":
        """Subtract an integer from the current value."""
        return self._apply(value, -1)

    def undo(self) -> "Calculator":
        """Revert the most recent operation, never past the seed."""
        if self._undo_stack and self._value is not None:
            self._redo_stack.append(self._value)
            self._value = self._undo_stack.pop()
        return self

    def redo(self) -> "Calculator":
        """Restore the most recently undone operation."""
        if self._redo_stack and self._value is not None:
            self._undo_stack.append(self._value)
            self._value = self._redo_stack.pop()
        return self

    def save(self) -> "Calculator":
        """Persist the current state; undo and redo become no-ops."""
        self._undo_stack.clear()
        self._redo_stack.clear()
        return self

    def result(self) -> int:
        """Return the current value, or 0 when never seeded."""
        return 0 if self._value is None else self._value

    def _apply(self, value: int, sign: int) -> "Calculator":
        if self._value is None or not _is_integer(value):
            return self
        self._undo_stack.append(self._value)
        self._redo_stack.clear()
        self._value += sign * value
        return self
