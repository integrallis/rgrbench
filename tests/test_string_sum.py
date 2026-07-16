"""
Port of C# StringSum TestStringSumKata.cs
Complete port with all test cases
"""

from string_sum.string_sum_kata import StringSumKata


def test_add_return_sum() -> None:
    """Port of TestCase('', null, '0')"""
    result = StringSumKata.sum("", None)
    assert result == "0"


def test_add_two_numbers_return_sum() -> None:
    """Sum of two numeric strings ('1', '2') is '3'"""
    result = StringSumKata.sum("1", "2")
    assert result == "3"


def test_add_treats_null_or_empty_as_zero() -> None:
    """A null or empty operand counts as zero, the other operand is kept"""
    assert StringSumKata.sum("5", "") == "5"
    assert StringSumKata.sum(None, "7") == "7"
