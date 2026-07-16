"""
Tests for the Time Sheet Calculator kata (tddbuddy.com/katas/timesheet-calc).
Expected durations come from the kata's published examples plus boundary cases.
"""


def test_standard_day_with_break() -> None:
    """Test 1: 08:42 to 16:20 with a 00:30 break is 07:08 (kata example)"""
    from timesheet_calculator import calculate_work_hours

    assert calculate_work_hours("08:42", "16:20", "00:30") == "07:08"


def test_overnight_shift_with_break() -> None:
    """Test 2: 17:02 to 02:09 with a 00:35 break crosses midnight and is 08:32
    (kata example)"""
    from timesheet_calculator import calculate_work_hours

    assert calculate_work_hours("17:02", "02:09", "00:35") == "08:32"


def test_day_without_break() -> None:
    """Test 3: 07:02 to 16:22 with no break is 09:20 (kata example)"""
    from timesheet_calculator import calculate_work_hours

    assert calculate_work_hours("07:02", "16:22") == "09:20"


def test_zero_break_equals_no_break() -> None:
    """Test 4: A 00:00 break gives the same result as omitting the break"""
    from timesheet_calculator import calculate_work_hours

    assert calculate_work_hours("07:02", "16:22", "00:00") == "09:20"


def test_identical_start_and_end_is_zero() -> None:
    """Test 5: Equal start and end times mean no time worked"""
    from timesheet_calculator import calculate_work_hours

    assert calculate_work_hours("09:00", "09:00") == "00:00"


def test_almost_full_day() -> None:
    """Test 6: 00:00 to 23:59 is 23:59"""
    from timesheet_calculator import calculate_work_hours

    assert calculate_work_hours("00:00", "23:59") == "23:59"


def test_overnight_shift_without_break() -> None:
    """Test 7: 23:00 to 01:00 crosses midnight and is 02:00"""
    from timesheet_calculator import calculate_work_hours

    assert calculate_work_hours("23:00", "01:00") == "02:00"


def test_short_duration_is_zero_padded() -> None:
    """Test 8: An eight-minute stint formats as 00:08"""
    from timesheet_calculator import calculate_work_hours

    assert calculate_work_hours("09:05", "09:13") == "00:08"


def test_three_digit_times_without_colon() -> None:
    """Test 9: Three-digit input without a colon, e.g. '800' means 8:00"""
    from timesheet_calculator import calculate_work_hours

    assert calculate_work_hours("800", "1530") == "07:30"


def test_four_digit_times_without_colon_including_break() -> None:
    """Test 10: Four-digit inputs without colons match the colon form"""
    from timesheet_calculator import calculate_work_hours

    assert calculate_work_hours("0842", "1620", "0030") == "07:08"


def test_colon_and_colonless_inputs_can_be_mixed() -> None:
    """Test 11: Colon and colon-free notations may be combined in one call"""
    from timesheet_calculator import calculate_work_hours

    assert calculate_work_hours("08:42", "1620", "00:30") == "07:08"


def test_am_pm_notation() -> None:
    """Test 12: 8:00 AM to 4:30 PM is 08:30"""
    from timesheet_calculator import calculate_work_hours

    assert calculate_work_hours("8:00 AM", "4:30 PM") == "08:30"


def test_twelve_am_is_midnight() -> None:
    """Test 13: 12:00 AM means midnight"""
    from timesheet_calculator import calculate_work_hours

    assert calculate_work_hours("12:00 AM", "1:00 AM") == "01:00"


def test_twelve_pm_is_noon() -> None:
    """Test 14: 12:00 PM means noon"""
    from timesheet_calculator import calculate_work_hours

    assert calculate_work_hours("12:00 PM", "1:00 PM") == "01:00"


def test_lowercase_meridiem_is_accepted() -> None:
    """Test 15: Lowercase am/pm suffixes are accepted"""
    from timesheet_calculator import calculate_work_hours

    assert calculate_work_hours("9:00 am", "5:00 pm") == "08:00"


def test_hour_out_of_range_raises() -> None:
    """Test 16: An hour beyond 23 on the 24-hour clock is rejected"""
    import pytest

    from timesheet_calculator import calculate_work_hours

    with pytest.raises(ValueError):
        calculate_work_hours("25:00", "26:00")


def test_minutes_out_of_range_raise() -> None:
    """Test 17: Minutes beyond 59 are rejected"""
    import pytest

    from timesheet_calculator import calculate_work_hours

    with pytest.raises(ValueError):
        calculate_work_hours("10:75", "11:00")


def test_non_numeric_time_raises() -> None:
    """Test 18: A non-numeric time string is rejected with a message that
    says the time is invalid"""
    import pytest

    from timesheet_calculator import calculate_work_hours

    with pytest.raises(ValueError, match=r"Invalid time"):
        calculate_work_hours("abc", "11:00")


def test_hour_beyond_twelve_with_meridiem_raises() -> None:
    """Test 19: 12-hour notation caps the hour at 12"""
    import pytest

    from timesheet_calculator import calculate_work_hours

    with pytest.raises(ValueError):
        calculate_work_hours("13:00 PM", "14:00")


def test_break_longer_than_shift_raises() -> None:
    """Test 20: A break exceeding the elapsed time is rejected"""
    import pytest

    from timesheet_calculator import calculate_work_hours

    with pytest.raises(ValueError):
        calculate_work_hours("09:00", "09:10", "01:00")


def test_break_error_message_names_the_problem() -> None:
    """Test 21: The break-too-long error message reads exactly
    'Break duration exceeds time worked'"""
    import pytest

    from timesheet_calculator import calculate_work_hours

    with pytest.raises(ValueError, match=r"^Break duration exceeds time worked$"):
        calculate_work_hours("09:00", "09:10", "01:00")


def test_single_digit_minutes_are_rejected() -> None:
    """Test 22: The minutes field must be two digits, so '8:5' is invalid"""
    import pytest

    from timesheet_calculator import calculate_work_hours

    with pytest.raises(ValueError, match=r"Invalid time"):
        calculate_work_hours("8:5", "9:00")


def test_three_digit_hours_are_rejected() -> None:
    """Test 23: The hours field caps at two digits, so '023:00' is invalid"""
    import pytest

    from timesheet_calculator import calculate_work_hours

    with pytest.raises(ValueError, match=r"Invalid time"):
        calculate_work_hours("023:00", "23:30")


def test_minute_sixty_is_rejected() -> None:
    """Test 24: Minute 60, one past the top of the range, is rejected"""
    import pytest

    from timesheet_calculator import calculate_work_hours

    with pytest.raises(ValueError, match=r"Invalid time"):
        calculate_work_hours("10:60", "11:00")


def test_hour_twenty_four_is_rejected() -> None:
    """Test 25: Hour 24, one past the top of the 24-hour clock, is rejected"""
    import pytest

    from timesheet_calculator import calculate_work_hours

    with pytest.raises(ValueError, match=r"Invalid time"):
        calculate_work_hours("24:00", "01:00")


def test_invalid_meridiem_time_error_names_the_offending_value() -> None:
    """Test 26: The error for a bad 12-hour time quotes that input value"""
    import pytest

    from timesheet_calculator import calculate_work_hours

    with pytest.raises(ValueError, match=r"Invalid time: '13:00 PM'"):
        calculate_work_hours("13:00 PM", "14:00")


def test_meridiem_and_24_hour_notations_can_be_mixed() -> None:
    """Test 27: 8:00 AM to 17:00 mixes 12- and 24-hour notation and is 09:00"""
    from timesheet_calculator import calculate_work_hours

    assert calculate_work_hours("8:00 AM", "17:00") == "09:00"


def test_break_in_twelve_hour_notation() -> None:
    """Test 28: A break may use 12-hour notation; 1:00 PM means 13:00, so a
    17-hour shift minus that break leaves 04:00"""
    from timesheet_calculator import calculate_work_hours

    assert calculate_work_hours("06:00", "23:00", "1:00 PM") == "04:00"
