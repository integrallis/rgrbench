"""
Port of C# LeapYear LeapYearTest.cs
Complete port with all test cases
"""

import pytest

from leap_year.leap_year import LeapYear


def test_can_test_for_leap_year() -> None:
    """Port of CanTestForLeapYear"""
    assert LeapYear.is_leap_year(1996) is True


@pytest.mark.parametrize(
    "expected_result,year",
    [
        (False, 2013),
        (False, 2001),
        (True, 1996),
        (True, 1992),
    ],
)
def test_can_test_for_leap_years(expected_result: bool, year: int) -> None:
    """Port of CanTestForLeapYears"""
    assert LeapYear.is_leap_year(year) == expected_result


def test_year_divisible_by_4_is_leap() -> None:
    """Port of CanTestForLeapYears - test case for 1992"""
    assert LeapYear.is_leap_year(1992) is True


def test_year_not_divisible_by_4_is_not_leap() -> None:
    """Port of CanTestForLeapYears - test case for 2013"""
    assert LeapYear.is_leap_year(2013) is False


def test_year_2001_is_not_leap() -> None:
    """Port of CanTestForLeapYears - test case for 2001"""
    assert LeapYear.is_leap_year(2001) is False


def test_year_2005_is_not_leap() -> None:
    """2005 is not divisible by 4, so it is not a leap year"""
    assert LeapYear.is_leap_year(2005) is False


def test_century_years_not_divisible_by_400_are_not_leap() -> None:
    """Gregorian century rule: 1900 and 2100 are not leap years"""
    from leap_year.leap_year import LeapYear

    assert LeapYear.is_leap_year(1900) is False
    assert LeapYear.is_leap_year(2100) is False


def test_century_years_divisible_by_400_are_leap() -> None:
    """Gregorian century rule: 1600 and 2000 are leap years"""
    from leap_year.leap_year import LeapYear

    assert LeapYear.is_leap_year(1600) is True
    assert LeapYear.is_leap_year(2000) is True
