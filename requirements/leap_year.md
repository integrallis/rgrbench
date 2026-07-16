# Leap year determination

## Overview
A calendar rule service that decides whether a given year is a leap year under the Gregorian calendar: years divisible by four gain the extra day, except century years, which are leap years only when divisible by 400.

## User Stories

### US-1: The every-four-years rule
As a calendar user, I want years divisible by four recognised as leap years, so that February gains its extra day on schedule.

- AC-1.1: A non-century year divisible by four is a leap year — 1992 and 1996 are leap years.
- AC-1.2: A year not divisible by four is not a leap year — 2001, 2005 and 2013 are not leap years.

### US-2: The century correction
As a calendar user, I want century years judged by the 400-year rule, so that the calendar stays aligned with the seasons.

- AC-2.1: A century year not divisible by 400 is not a leap year — 1900 and 2100 are not leap years.
- AC-2.2: A century year divisible by 400 is a leap year — 1600 and 2000 are leap years.

## Traceability
```json
{
  "test_can_test_for_leap_year": ["AC-1.1"],
  "test_can_test_for_leap_years": ["AC-1.1", "AC-1.2"],
  "test_year_divisible_by_4_is_leap": ["AC-1.1"],
  "test_year_not_divisible_by_4_is_not_leap": ["AC-1.2"],
  "test_year_2001_is_not_leap": ["AC-1.2"],
  "test_year_2005_is_not_leap": ["AC-1.2"],
  "test_century_years_not_divisible_by_400_are_not_leap": ["AC-2.1"],
  "test_century_years_divisible_by_400_are_leap": ["AC-2.2"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
