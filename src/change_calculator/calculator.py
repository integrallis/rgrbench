"""Change Calculator - Greedy algorithm for making change"""


class ChangeCalculator:
    """Calculate minimum coins needed for change"""

    def __init__(self) -> None:
        self.coins = [25, 10, 5, 1]  # US coins: quarter, dime, nickel, penny

    def calculate_change(self, amount: int) -> list[int]:
        """Calculate coins needed for given amount"""
        result = []
        remaining = amount

        for coin in self.coins:
            while remaining >= coin:
                result.append(coin)
                remaining -= coin

        return result
