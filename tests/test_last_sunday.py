"""Last Sunday kata: the final Sunday of each month of a given year.

Kata catalogued at tddbuddy.com/katas/last-sunday; implementation and tests
original (MIT), machine-authored from the specification, 2026.
"""


def test_year_2013_full_listing() -> None:
    """Test 1: The worked example year 2013 yields the twelve documented dates"""
    from last_sunday import last_sundays

    assert last_sundays(2013) == [
        "2013-01-27",
        "2013-02-24",
        "2013-03-31",
        "2013-04-28",
        "2013-05-26",
        "2013-06-30",
        "2013-07-28",
        "2013-08-25",
        "2013-09-29",
        "2013-10-27",
        "2013-11-24",
        "2013-12-29",
    ]


def test_returns_twelve_entries() -> None:
    """Test 2: One date is produced per month of the year"""
    from last_sunday import last_sundays

    assert len(last_sundays(2013)) == 12


def test_entries_are_iso_formatted() -> None:
    """Test 3: Each entry uses the YYYY-MM-DD format"""
    from last_sunday import last_sundays

    for entry in last_sundays(2013):
        year, month, day = entry.split("-")
        assert len(year) == 4
        assert len(month) == 2
        assert len(day) == 2


def test_every_entry_is_a_sunday() -> None:
    """Test 4: Every reported date falls on a Sunday"""
    from datetime import date

    from last_sunday import last_sundays

    for entry in last_sundays(2021):
        assert date.fromisoformat(entry).weekday() == 6


def test_entries_cover_months_january_through_december_in_order() -> None:
    """Test 5: Results are ordered January through December"""
    from datetime import date

    from last_sunday import last_sundays

    months = [date.fromisoformat(entry).month for entry in last_sundays(2019)]
    assert months == list(range(1, 13))


def test_leap_day_sunday_is_the_last_sunday() -> None:
    """Test 6: When Feb 29 exists and falls on a Sunday it is the answer (2032)"""
    from last_sunday import last_sundays

    assert last_sundays(2032)[1] == "2032-02-29"


def test_leap_year_february_when_leap_day_is_not_sunday() -> None:
    """Test 7: Leap-year February with Feb 29 on a weekday (2024) yields Feb 25"""
    from last_sunday import last_sundays

    assert last_sundays(2024)[1] == "2024-02-25"


def test_century_year_not_divisible_by_400_has_short_february() -> None:
    """Test 8: 2100 is not a leap year, so its February ends on the 28th"""
    from last_sunday import last_sundays

    assert last_sundays(2100)[1] == "2100-02-28"


def test_year_ending_on_a_sunday() -> None:
    """Test 9: Year 2000 ends with December 31 falling on a Sunday"""
    from last_sunday import last_sundays

    assert last_sundays(2000)[11] == "2000-12-31"


def test_single_month_lookup_returns_date_object() -> None:
    """Test 10: Looking up one month returns a date with the expected value"""
    from datetime import date

    from last_sunday import last_sunday_of_month

    assert last_sunday_of_month(2013, 1) == date(2013, 1, 27)


def test_single_month_lookup_march_2013() -> None:
    """Test 11: March 2013 ends on Sunday the 31st, the month's final day"""
    from datetime import date

    from last_sunday import last_sunday_of_month

    assert last_sunday_of_month(2013, 3) == date(2013, 3, 31)


def test_single_month_lookup_is_within_final_week() -> None:
    """Test 12: The last Sunday always lies within seven days of month end"""
    import calendar

    from last_sunday import last_sunday_of_month

    for month in range(1, 13):
        result = last_sunday_of_month(2023, month)
        month_length = calendar.monthrange(2023, month)[1]
        assert month_length - result.day < 7


def test_month_zero_is_rejected() -> None:
    """Test 13: Month 0 is outside 1..12 and raises ValueError"""
    import pytest

    from last_sunday import last_sunday_of_month

    with pytest.raises(ValueError, match="month must be in 1..12"):
        last_sunday_of_month(2013, 0)


def test_month_thirteen_is_rejected() -> None:
    """Test 14: Month 13 is outside 1..12 and raises ValueError"""
    import pytest

    from last_sunday import last_sunday_of_month

    with pytest.raises(ValueError, match="month must be in 1..12"):
        last_sunday_of_month(2013, 13)


def test_year_2032_full_listing() -> None:
    """Test 15: A leap year (2032) yields twelve Sundays including the leap day"""
    from last_sunday import last_sundays

    assert last_sundays(2032) == [
        "2032-01-25",
        "2032-02-29",
        "2032-03-28",
        "2032-04-25",
        "2032-05-30",
        "2032-06-27",
        "2032-07-25",
        "2032-08-29",
        "2032-09-26",
        "2032-10-31",
        "2032-11-28",
        "2032-12-26",
    ]
