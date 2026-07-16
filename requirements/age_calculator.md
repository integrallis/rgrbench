# Age calculation and birthday week

## Overview
A birthday service that works from two supplied dates — a birth date and a reference date — with no dependence on the system clock. It reports a person's age in whole completed years as of the reference date, guards against birth dates that lie in the future, and, as a bonus feature, tells a person the calendar date on which their "birthday week" begins.

## User Stories

### US-1: Age in whole years
As a person checking an age, I want the age in completed years as of a given reference date, so that the reported age matches everyday usage.

- AC-1.1: Worked example: born 28 October 2016 and referenced on 5 November 2022, the age is 6.
- AC-1.2: The age counts only completed years: before the first anniversary of birth the age is 0, and on the day before any anniversary the previous age still applies — even when the reference date has already crossed into a new calendar year (e.g. born 31 December, referenced 1 January of the next year, the age is 0).
- AC-1.3: The age increments on the anniversary date itself and remains at the new value on the following day.
- AC-1.4: When the birth date equals the reference date, the age is 0.

### US-2: Leap-day birthdays
As a person born on 29 February, I want my age to change on a well-defined day every year, so that my age is unambiguous in non-leap years.

- AC-2.1: In a non-leap year, a 29 February birthday has not yet occurred on 28 February (previous age still applies) and is treated as reached on 1 March.
- AC-2.2: In a leap year, the birthday is reached on 29 February itself, not on 28 February.

### US-3: Future birth dates are rejected
As a person checking an age, I want impossible inputs refused, so that nonsense ages are never reported.

- AC-3.1: A birth date after the reference date is rejected with an error whose message is exactly "birthdate is after today".
- AC-3.2: The guard applies even when the birth date is only one day after the reference date.

### US-4: Birthday week start date
As a person planning a celebration, I want to know the date my birthday week starts, so that I can schedule around it.

- AC-4.1: The result is a formatted date of the form full month name, day number, comma, year — e.g. "September 3, 2017".
- AC-4.2: For a birthday falling on a Thursday, Friday, or Saturday, the birthday week starts on the Sunday of that same week (worked examples: 7, 8, and 9 September 2017 all start their week on "September 3, 2017").
- AC-4.3: For a birthday falling on a Sunday, Monday, or Wednesday, the birthday week starts six days before the birthday (worked examples: 3 September 2017 starts "August 28, 2017"; 4 September 2017 starts "August 29, 2017"; 6 September 2017 starts "August 31, 2017").

## Traceability
```json
{
  "test_worked_example_zenith_is_six": ["AC-1.1"],
  "test_age_is_zero_before_first_birthday": ["AC-1.2"],
  "test_age_increments_on_the_birthday_itself": ["AC-1.3"],
  "test_age_is_one_less_on_the_day_before_the_birthday": ["AC-1.2"],
  "test_age_on_the_day_after_the_birthday": ["AC-1.3"],
  "test_same_day_birth_and_reference_is_zero": ["AC-1.4"],
  "test_reference_just_after_new_year_before_birthday": ["AC-1.2"],
  "test_leap_day_baby_has_not_aged_on_feb_28_of_non_leap_year": ["AC-2.1"],
  "test_leap_day_baby_ages_on_march_1_of_non_leap_year": ["AC-2.1"],
  "test_leap_day_baby_ages_on_feb_29_of_leap_year": ["AC-2.2"],
  "test_future_birthdate_raises_value_error_with_exact_message": ["AC-3.1"],
  "test_birthdate_one_day_in_future_raises": ["AC-3.2"],
  "test_birthday_week_saturday_starts_on_that_weeks_sunday": ["AC-4.1", "AC-4.2"],
  "test_birthday_week_sunday_starts_six_days_back": ["AC-4.1", "AC-4.3"],
  "test_birthday_week_thursday_starts_on_that_weeks_sunday": ["AC-4.2"],
  "test_birthday_week_friday_starts_on_that_weeks_sunday": ["AC-4.2"],
  "test_birthday_week_wednesday_starts_six_days_back": ["AC-4.3"],
  "test_birthday_week_monday_starts_six_days_back": ["AC-4.3"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
