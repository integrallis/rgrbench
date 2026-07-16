"""Fibonacci - Dynamic programming implementation"""


class Fibonacci:
    """Calculate Fibonacci numbers using dynamic programming"""

    def __init__(self) -> None:
        """Initialize with memoization cache"""
        self.cache: dict[int, int] = {}

    def get_number(self, n: int) -> int:
        """Get the nth Fibonacci number using dynamic programming"""
        if n < 1:
            raise TypeError("Fibonacci numbers start from 1")

        if n in self.cache:
            return self.cache[n]

        if n == 1:
            result = 0
        elif n == 2:
            result = 1
        else:
            result = self.get_number(n - 1) + self.get_number(n - 2)

        self.cache[n] = result
        return result
