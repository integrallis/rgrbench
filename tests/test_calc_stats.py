"""
Port of C# CalcStatTest.cs
Tests for Calc Stats kata - calculating statistics from number lists
"""


def test_can_find_minimum_value() -> None:
    """Test 1: Can find minimum value in a list"""
    from calc_stats.calc_stats import CalcStats

    numbers = [1, -1, 2, -2, 6, 9, 15, -2, 92, 11]
    result = CalcStats.number_stats(numbers, CalcStats.StatType.MINIMUM)
    expected = "-2"

    assert result == expected


def test_can_find_maximum_value() -> None:
    """Test 2: Can find maximum value in a list"""
    from calc_stats.calc_stats import CalcStats

    numbers = [1, -1, 2, -2, 6, 9, 15, -2, 92, 11]
    result = CalcStats.number_stats(numbers, CalcStats.StatType.MAXIMUM)
    expected = "92"

    assert result == expected


def test_can_get_element_count() -> None:
    """Test 3: Can get count of elements in a list"""
    from calc_stats.calc_stats import CalcStats

    numbers = [1, -1, 2, -2, 6, 9, 15, -2, 92, 11]
    result = CalcStats.number_stats(numbers, CalcStats.StatType.ELEMENT_COUNT)
    expected = "10"

    assert result == expected


def test_can_get_average_of_series() -> None:
    """Test 4: Can get average of numbers in a list"""
    from calc_stats.calc_stats import CalcStats

    numbers = [1, -1, 2, -2, 6, 9, 15, -2, 92, 11]
    result = CalcStats.number_stats(numbers, CalcStats.StatType.AVERAGE)
    expected = "13.1"

    assert result == expected


def test_handles_invalid_stat_type() -> None:
    """Test edge case: handle invalid stat type"""
    from enum import Enum

    from calc_stats.calc_stats import CalcStats

    # Create a fake enum value for coverage
    class FakeStatType(Enum):
        INVALID = 99

    # This should return empty string for unhandled types
    # Note: In real code, this would be better as an exception
    result = CalcStats.number_stats([1, 2, 3], FakeStatType.INVALID)  # type: ignore
    assert result == ""
