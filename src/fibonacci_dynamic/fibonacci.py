"""Fibonacci Dynamic Programming Implementation

Demonstrates memoized fibonacci calculation through TDD
"""


class Fibonacci:
    """Dynamic programming fibonacci calculator using memoization."""

    def __init__(self) -> None:
        """Initialize with memoization cache."""
        self._cache: dict[int, int] = {}

    def get_number(self, n: int) -> int:
        """Returns the nth fibonacci number using dynamic programming."""
        if n < 1:
            raise ValueError("Fibonacci sequence is not defined for negative numbers")
        if n == 1:
            return 0
        if n == 2:
            return 1

        if n in self._cache:
            return self._cache[n]

        result = self.get_number(n - 1) + self.get_number(n - 2)
        self._cache[n] = result
        return result
