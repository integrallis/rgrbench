"""Calc Stats implementation - calculates statistics from number lists"""

from enum import Enum


class CalcStats:
    """Static class for calculating statistics"""

    class StatType(Enum):
        """Types of statistics that can be calculated"""

        MINIMUM = 1
        MAXIMUM = 2
        ELEMENT_COUNT = 3
        AVERAGE = 4

    @staticmethod
    def number_stats(numbers: list[int], stat_type: "CalcStats.StatType") -> str:
        """Calculate statistics for a list of numbers"""
        if stat_type == CalcStats.StatType.MINIMUM:
            return str(min(numbers))
        elif stat_type == CalcStats.StatType.MAXIMUM:
            return str(max(numbers))
        elif stat_type == CalcStats.StatType.ELEMENT_COUNT:
            return str(len(numbers))
        elif stat_type == CalcStats.StatType.AVERAGE:
            return str(sum(numbers) / len(numbers))
        return ""
