"""Age Calculator kata tests.

Age in whole years computed from an injected birth date and reference date; no system
clock. Covers the worked example, birthday boundaries, the 29 February rule, the
future-birthdate guard, and the birthday-week bonus.
"""

import pytest


def test_worked_example_zenith_is_six() -> None:
    """Test 1: born 28 October 2016, reference 5 November 2022 -> age 6."""
    from datetime import date

    from age_calculator import calculate_age

    assert calculate_age(date(2016, 10, 28), date(2022, 11, 5)) == 6


def test_age_is_zero_before_first_birthday() -> None:
    """Test 2: a few months after birth the age is still 0."""
    from datetime import date

    from age_calculator import calculate_age

    assert calculate_age(date(2020, 6, 15), date(2021, 6, 14)) == 0


def test_age_increments_on_the_birthday_itself() -> None:
    """Test 3: on the exact anniversary the new age is reached."""
    from datetime import date

    from age_calculator import calculate_age

    assert calculate_age(date(2000, 5, 10), date(2020, 5, 10)) == 20


def test_age_is_one_less_on_the_day_before_the_birthday() -> None:
    """Test 4: the day before the anniversary the previous age still applies."""
    from datetime import date

    from age_calculator import calculate_age

    assert calculate_age(date(2000, 5, 10), date(2020, 5, 9)) == 19


def test_age_on_the_day_after_the_birthday() -> None:
    """Test 5: the day after the anniversary the new age applies."""
    from datetime import date

    from age_calculator import calculate_age

    assert calculate_age(date(2000, 5, 10), date(2020, 5, 11)) == 20


def test_same_day_birth_and_reference_is_zero() -> None:
    """Test 6: birth date equal to the reference date gives age 0."""
    from datetime import date

    from age_calculator import calculate_age

    assert calculate_age(date(2022, 3, 3), date(2022, 3, 3)) == 0


def test_reference_just_after_new_year_before_birthday() -> None:
    """Test 7: born 31 December, referenced 1 January the next year -> age 0."""
    from datetime import date

    from age_calculator import calculate_age

    assert calculate_age(date(2021, 12, 31), date(2022, 1, 1)) == 0


def test_leap_day_baby_has_not_aged_on_feb_28_of_non_leap_year() -> None:
    """Test 8: a 29 February baby is still the previous age on 28 February of a
    non-leap year."""
    from datetime import date

    from age_calculator import calculate_age

    assert calculate_age(date(2016, 2, 29), date(2017, 2, 28)) == 0


def test_leap_day_baby_ages_on_march_1_of_non_leap_year() -> None:
    """Test 9: a 29 February baby turns older on 1 March in a non-leap year."""
    from datetime import date

    from age_calculator import calculate_age

    assert calculate_age(date(2016, 2, 29), date(2017, 3, 1)) == 1


def test_leap_day_baby_ages_on_feb_29_of_leap_year() -> None:
    """Test 10: in a leap year the 29 February baby ages on 29 February."""
    from datetime import date

    from age_calculator import calculate_age

    assert calculate_age(date(2016, 2, 29), date(2020, 2, 29)) == 4
    assert calculate_age(date(2016, 2, 29), date(2020, 2, 28)) == 3


def test_future_birthdate_raises_value_error_with_exact_message() -> None:
    """Test 11: a birth date after the reference date raises ValueError with the
    byte-identical message 'birthdate is after today'."""
    from datetime import date

    from age_calculator import calculate_age

    with pytest.raises(ValueError) as exc_info:
        calculate_age(date(2030, 1, 1), date(2022, 11, 5))
    assert str(exc_info.value) == "birthdate is after today"


def test_birthdate_one_day_in_future_raises() -> None:
    """Test 12: even a single day in the future triggers the guard."""
    from datetime import date

    from age_calculator import calculate_age

    with pytest.raises(ValueError, match="birthdate is after today"):
        calculate_age(date(2022, 11, 6), date(2022, 11, 5))


def test_birthday_week_saturday_starts_on_that_weeks_sunday() -> None:
    """Test 13: 9 September 2017 is a Saturday; its birthday week starts on
    September 3, 2017 (the Sunday of that week)."""
    from datetime import date

    from age_calculator import birthday_week_start

    assert birthday_week_start(date(2017, 9, 9)) == "September 3, 2017"


def test_birthday_week_sunday_starts_six_days_back() -> None:
    """Test 14: 3 September 2017 is a Sunday; its birthday week starts on
    August 28, 2017 (six days earlier)."""
    from datetime import date

    from age_calculator import birthday_week_start

    assert birthday_week_start(date(2017, 9, 3)) == "August 28, 2017"


def test_birthday_week_thursday_starts_on_that_weeks_sunday() -> None:
    """Test 15: 7 September 2017 is a Thursday; the week starts on the preceding
    Sunday, September 3, 2017."""
    from datetime import date

    from age_calculator import birthday_week_start

    assert birthday_week_start(date(2017, 9, 7)) == "September 3, 2017"


def test_birthday_week_friday_starts_on_that_weeks_sunday() -> None:
    """Test 16: 8 September 2017 is a Friday; the week starts on September 3, 2017."""
    from datetime import date

    from age_calculator import birthday_week_start

    assert birthday_week_start(date(2017, 9, 8)) == "September 3, 2017"


def test_birthday_week_wednesday_starts_six_days_back() -> None:
    """Test 17: 6 September 2017 is a Wednesday; six days back is
    August 31, 2017."""
    from datetime import date

    from age_calculator import birthday_week_start

    assert birthday_week_start(date(2017, 9, 6)) == "August 31, 2017"


def test_birthday_week_monday_starts_six_days_back() -> None:
    """Test 18: 4 September 2017 is a Monday; six days back is August 29, 2017."""
    from datetime import date

    from age_calculator import birthday_week_start

    assert birthday_week_start(date(2017, 9, 4)) == "August 29, 2017"
