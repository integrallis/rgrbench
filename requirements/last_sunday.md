# Last Sunday of each month

## Overview
A calendar helper that reports the final Sunday of every month. Given a year, it lists the
last Sunday of each of the twelve months in order; a single month of a year can also be
looked up on its own. Leap years — including the century rule — are honored, and
out-of-range months are refused.

## User Stories

### US-1: List a year's last Sundays
As a scheduler, I want the last Sunday of every month of a year, so that I can plan month-end Sunday events.

- AC-1.1: A year yields exactly twelve entries, one per month, ordered January through December.
- AC-1.2: Each entry is written as an ISO calendar date: four-digit year, two-digit month, and two-digit day, separated by dashes.
- AC-1.3: Every entry falls on a Sunday.
- AC-1.4: Worked example: the year 2013 yields 2013-01-27, 2013-02-24, 2013-03-31, 2013-04-28, 2013-05-26, 2013-06-30, 2013-07-28, 2013-08-25, 2013-09-29, 2013-10-27, 2013-11-24, 2013-12-29.
- AC-1.5: When December 31 falls on a Sunday, it is December's entry (as in the year 2000).

### US-2: Honor leap-year rules
As a scheduler, I want February handled correctly in every kind of year, so that leap days never throw the calendar off.

- AC-2.1: In a leap year whose February 29 falls on a Sunday, the leap day itself is February's entry (worked example: the year 2032 yields 2032-01-25, 2032-02-29, 2032-03-28, 2032-04-25, 2032-05-30, 2032-06-27, 2032-07-25, 2032-08-29, 2032-09-26, 2032-10-31, 2032-11-28, 2032-12-26).
- AC-2.2: In a leap year whose February 29 falls on a weekday, February's entry is the Sunday before it (2024 gives 2024-02-25).
- AC-2.3: A century year not divisible by 400 is not a leap year, so its February ends on the 28th (2100 gives 2100-02-28).

### US-3: Look up a single month
As a scheduler, I want the last Sunday of one specific month, so that I can check a single date without listing the whole year.

- AC-3.1: The last Sunday of a given month of a given year is returned as a calendar date (worked examples: January 2013 gives January 27; March 2013 gives March 31, the month's final day).
- AC-3.2: The last Sunday always lies within the final seven days of its month.
- AC-3.3: A month outside 1 through 12 is refused as an error with the message "month must be in 1..12".

## Traceability
```json
{
  "test_year_2013_full_listing": ["AC-1.4"],
  "test_returns_twelve_entries": ["AC-1.1"],
  "test_entries_are_iso_formatted": ["AC-1.2"],
  "test_every_entry_is_a_sunday": ["AC-1.3"],
  "test_entries_cover_months_january_through_december_in_order": ["AC-1.1"],
  "test_leap_day_sunday_is_the_last_sunday": ["AC-2.1"],
  "test_leap_year_february_when_leap_day_is_not_sunday": ["AC-2.2"],
  "test_century_year_not_divisible_by_400_has_short_february": ["AC-2.3"],
  "test_year_ending_on_a_sunday": ["AC-1.5"],
  "test_single_month_lookup_returns_date_object": ["AC-3.1"],
  "test_single_month_lookup_march_2013": ["AC-3.1"],
  "test_single_month_lookup_is_within_final_week": ["AC-3.2"],
  "test_month_zero_is_rejected": ["AC-3.3"],
  "test_month_thirteen_is_rejected": ["AC-3.3"],
  "test_year_2032_full_listing": ["AC-2.1"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
