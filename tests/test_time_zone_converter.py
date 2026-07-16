"""Time Zone Converter kata: pure conversion of injected datetimes between
fixed IANA zones via zoneinfo; the system clock is never consulted.

Kata catalogued at tddbuddy.com/katas/time-zone-converter; implementation and
tests original (MIT), machine-authored from the specification, 2026.
"""


def test_utc_to_new_york_standard_time() -> None:
    """Test 1: Noon UTC in January is 07:00 in New York (UTC-5)"""
    from datetime import datetime

    from time_zone_converter import convert

    result = convert(datetime(2021, 1, 15, 12, 0), "UTC", "America/New_York")
    assert (result.year, result.month, result.day) == (2021, 1, 15)
    assert (result.hour, result.minute) == (7, 0)


def test_utc_to_new_york_summer_offset() -> None:
    """Test 2: Noon UTC in July is 08:00 in New York (UTC-4)"""
    from datetime import datetime

    from time_zone_converter import convert

    result = convert(datetime(2021, 7, 15, 12, 0), "UTC", "America/New_York")
    assert (result.hour, result.minute) == (8, 0)


def test_result_carries_destination_offset() -> None:
    """Test 3: The converted datetime is aware with the destination offset"""
    from datetime import datetime, timedelta

    from time_zone_converter import convert

    result = convert(datetime(2021, 1, 15, 12, 0), "UTC", "America/New_York")
    assert result.tzinfo is not None
    assert result.utcoffset() == timedelta(hours=-5)


def test_conversion_preserves_the_instant() -> None:
    """Test 4: Source and converted datetimes denote the same instant"""
    from datetime import datetime
    from zoneinfo import ZoneInfo

    from time_zone_converter import convert

    result = convert(datetime(2021, 1, 15, 12, 0), "UTC", "Asia/Kolkata")
    assert result == datetime(2021, 1, 15, 12, 0, tzinfo=ZoneInfo("UTC"))


def test_crossing_midnight_into_the_previous_date() -> None:
    """Test 5: 01:00 in New York is 22:00 the previous day in Los Angeles"""
    from datetime import datetime

    from time_zone_converter import convert

    result = convert(
        datetime(2021, 1, 15, 1, 0), "America/New_York", "America/Los_Angeles"
    )
    assert (result.year, result.month, result.day) == (2021, 1, 14)
    assert (result.hour, result.minute) == (22, 0)


def test_half_hour_offset_zone() -> None:
    """Test 6: Noon UTC is 17:30 in India (UTC+5:30)"""
    from datetime import datetime

    from time_zone_converter import convert

    result = convert(datetime(2021, 1, 15, 12, 0), "UTC", "Asia/Kolkata")
    assert (result.hour, result.minute) == (17, 30)


def test_quarter_hour_offset_zone() -> None:
    """Test 7: Noon UTC is 17:45 in Nepal (UTC+5:45)"""
    from datetime import datetime

    from time_zone_converter import convert

    result = convert(datetime(2021, 1, 15, 12, 0), "UTC", "Asia/Kathmandu")
    assert (result.hour, result.minute) == (17, 45)


def test_half_hour_offset_back_to_utc() -> None:
    """Test 8: 09:30 in India is 04:00 UTC"""
    from datetime import datetime

    from time_zone_converter import convert

    result = convert(datetime(2021, 3, 10, 9, 30), "Asia/Kolkata", "UTC")
    assert (result.hour, result.minute) == (4, 0)


def test_international_date_line_swing() -> None:
    """Test 9: Honolulu (UTC-10) to Kiritimati (UTC+14) is a 24-hour swing"""
    from datetime import datetime

    from time_zone_converter import convert

    result = convert(
        datetime(2021, 6, 1, 12, 0), "Pacific/Honolulu", "Pacific/Kiritimati"
    )
    assert (result.year, result.month, result.day) == (2021, 6, 2)
    assert (result.hour, result.minute) == (12, 0)


def test_year_boundary_transition() -> None:
    """Test 10: New Year's Eve 20:00 in New York is already 2021 in UTC"""
    from datetime import datetime

    from time_zone_converter import convert

    result = convert(datetime(2020, 12, 31, 20, 0), "America/New_York", "UTC")
    assert (result.year, result.month, result.day) == (2021, 1, 1)
    assert (result.hour, result.minute) == (1, 0)


def test_leap_day_transition() -> None:
    """Test 11: Late on leap day 2020 in UTC rolls into March 1 in India"""
    from datetime import datetime

    from time_zone_converter import convert

    result = convert(datetime(2020, 2, 29, 23, 0), "UTC", "Asia/Kolkata")
    assert (result.year, result.month, result.day) == (2020, 3, 1)
    assert (result.hour, result.minute) == (4, 30)


def test_same_zone_keeps_the_wall_clock() -> None:
    """Test 12: Converting UTC to UTC leaves the wall-clock time unchanged"""
    from datetime import datetime

    from time_zone_converter import convert

    result = convert(datetime(2021, 1, 15, 12, 34, 56), "UTC", "UTC")
    assert (result.hour, result.minute, result.second) == (12, 34, 56)


def test_round_trip_returns_the_original_wall_clock() -> None:
    """Test 13: Converting there and back recovers the original wall clock"""
    from datetime import datetime

    from time_zone_converter import convert

    original = datetime(2021, 4, 5, 6, 7)
    there = convert(original, "America/New_York", "Asia/Kathmandu")
    back = convert(there.replace(tzinfo=None), "Asia/Kathmandu", "America/New_York")
    assert back.replace(tzinfo=None) == original


def test_minutes_and_seconds_are_preserved() -> None:
    """Test 14: Whole-hour zone changes never disturb minutes or seconds"""
    from datetime import datetime

    from time_zone_converter import convert

    result = convert(datetime(2021, 1, 15, 9, 41, 23), "UTC", "America/New_York")
    assert (result.minute, result.second) == (41, 23)


def test_iso_string_conversion() -> None:
    """Test 15: ISO 8601 input converts to ISO 8601 output with offset"""
    from time_zone_converter import convert_iso

    result = convert_iso("2021-07-15T12:00:00", "UTC", "America/New_York")
    assert result == "2021-07-15T08:00:00-04:00"


def test_iso_string_conversion_to_half_hour_zone() -> None:
    """Test 16: ISO output renders half-hour offsets such as +05:30"""
    from time_zone_converter import convert_iso

    result = convert_iso("2021-01-15T12:00:00", "UTC", "Asia/Kolkata")
    assert result == "2021-01-15T17:30:00+05:30"


def test_invalid_iso_string_is_rejected() -> None:
    """Test 17: A malformed datetime string raises ValueError"""
    import pytest

    from time_zone_converter import convert_iso

    with pytest.raises(ValueError):
        convert_iso("not-a-datetime", "UTC", "Asia/Kolkata")


def test_unknown_source_zone_is_rejected() -> None:
    """Test 18: An unknown source zone name raises ValueError"""
    from datetime import datetime

    import pytest

    from time_zone_converter import convert

    with pytest.raises(ValueError, match="unknown time zone"):
        convert(datetime(2021, 1, 15, 12, 0), "Mars/Olympus_Mons", "UTC")


def test_unknown_destination_zone_is_rejected() -> None:
    """Test 19: An unknown destination zone name raises ValueError"""
    from datetime import datetime

    import pytest

    from time_zone_converter import convert

    with pytest.raises(ValueError, match="unknown time zone"):
        convert(datetime(2021, 1, 15, 12, 0), "UTC", "Atlantis/Central")


def test_aware_input_is_rejected() -> None:
    """Test 20: An already-aware datetime is ambiguous input and raises,
    with a message that opens by saying the moment must be naive"""
    from datetime import UTC, datetime

    import pytest

    from time_zone_converter import convert

    with pytest.raises(ValueError, match="^moment must be naive"):
        convert(datetime(2021, 1, 15, 12, 0, tzinfo=UTC), "UTC", "Asia/Kolkata")
