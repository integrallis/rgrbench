"""Fibonacci Brute Force Implementation

Demonstrates brute force recursive fibonacci calculation through TDD
"""


class Fibonacci:
    """Brute force fibonacci calculator using recursive approach."""

    def get_number(self, n: int) -> int:
        """Returns the nth fibonacci number using brute force recursion."""
        if n < 1:
            raise ValueError("Fibonacci sequence is not defined for negative numbers")
        if n == 1:
            return 0
        if n == 2:
            return 1
        return self.get_number(n - 1) + self.get_number(n - 2)
