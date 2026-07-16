# Timesheet work-hours calculation

## Overview
Payroll staff need to turn a clock-in time, a clock-out time, and an optional unpaid
break into the hours and minutes an employee worked. Employees write times in several
notations — 24-hour with a colon, compact digits without a colon, or 12-hour with an
AM/PM marker — and shifts may run overnight past midnight. The calculator accepts any
mix of these notations, subtracts the break, and reports the worked duration in a
uniform zero-padded hours-and-minutes form, rejecting inputs that are not sensible
times or breaks.

## User Stories

### US-1: Compute the worked duration of a shift
As a payroll clerk, I want the time worked between clock-in and clock-out computed for me, so that timesheets are totalled consistently without manual arithmetic.

- AC-1.1: The duration from start to end is reported in zero-padded HH:MM form; for example 07:02 to 16:22 is 09:20, and an eight-minute stint from 09:05 to 09:13 is reported as 00:08.
- AC-1.2: An optional break duration is subtracted from the elapsed time; 08:42 to 16:20 with a 00:30 break is 07:08 (canonical worked example).
- AC-1.3: A break of 00:00 gives the same result as giving no break at all.
- AC-1.4: Identical start and end times mean no time worked: 00:00.
- AC-1.5: A shift from 00:00 to 23:59 is 23:59.

### US-2: Handle overnight shifts
As a payroll clerk, I want shifts that cross midnight handled correctly, so that night workers' hours are not miscounted.

- AC-2.1: An end time earlier than the start time means the shift ran into the next day; 23:00 to 01:00 is 02:00.
- AC-2.2: Overnight shifts combine with breaks; 17:02 to 02:09 with a 00:35 break is 08:32 (canonical worked example).

### US-3: Accept flexible time notations
As a payroll clerk, I want to enter times the way employees wrote them down, so that I do not have to transcribe every timesheet into one format.

- AC-3.1: Times may be written without a colon as three or four digits: "800" means 8:00 and "1530" means 15:30, so "800" to "1530" is 07:30; "0842" to "1620" with a "0030" break matches the colon form's 07:08.
- AC-3.2: Colon and colon-free notations may be mixed within a single calculation.
- AC-3.3: Times may use 12-hour notation with an AM/PM marker: 8:00 AM to 4:30 PM is 08:30.
- AC-3.4: 12:00 AM means midnight and 12:00 PM means noon.
- AC-3.5: Lowercase am/pm markers are accepted.
- AC-3.6: 12-hour and 24-hour notations may be mixed in one calculation: 8:00 AM to 17:00 is 09:00.
- AC-3.7: The break may itself use 12-hour notation; a break of 1:00 PM means thirteen hours, so a 06:00-to-23:00 shift minus that break leaves 04:00.

### US-4: Reject invalid times and breaks
As a payroll clerk, I want impossible entries rejected with a clear message, so that bad timesheet data is caught instead of silently producing wrong pay.

- AC-4.1: On the 24-hour clock the hour must be between 00 and 23; hour 24 (one past the top) and hour 25 are both rejected with an error whose message contains "Invalid time".
- AC-4.2: Minutes must be between 00 and 59; minute 60 (one past the top) and minute 75 are both rejected with an error whose message contains "Invalid time".
- AC-4.3: A non-numeric time entry is rejected with an error whose message contains "Invalid time".
- AC-4.4: The minutes field must be exactly two digits, so an entry like "8:5" is rejected as an invalid time.
- AC-4.5: The hours field is at most two digits, so an entry like "023:00" is rejected as an invalid time.
- AC-4.6: In 12-hour notation the hour may not exceed 12; "13:00 PM" is rejected, and the error message quotes the offending value, reading "Invalid time: '13:00 PM'".
- AC-4.7: A break longer than the elapsed shift is rejected, and the error message reads exactly "Break duration exceeds time worked".

## Traceability
```json
{
  "test_standard_day_with_break": ["AC-1.2"],
  "test_overnight_shift_with_break": ["AC-2.2"],
  "test_day_without_break": ["AC-1.1"],
  "test_zero_break_equals_no_break": ["AC-1.3"],
  "test_identical_start_and_end_is_zero": ["AC-1.4"],
  "test_almost_full_day": ["AC-1.5"],
  "test_overnight_shift_without_break": ["AC-2.1"],
  "test_short_duration_is_zero_padded": ["AC-1.1"],
  "test_three_digit_times_without_colon": ["AC-3.1"],
  "test_four_digit_times_without_colon_including_break": ["AC-3.1"],
  "test_colon_and_colonless_inputs_can_be_mixed": ["AC-3.2"],
  "test_am_pm_notation": ["AC-3.3"],
  "test_twelve_am_is_midnight": ["AC-3.4"],
  "test_twelve_pm_is_noon": ["AC-3.4"],
  "test_lowercase_meridiem_is_accepted": ["AC-3.5"],
  "test_hour_out_of_range_raises": ["AC-4.1"],
  "test_minutes_out_of_range_raise": ["AC-4.2"],
  "test_non_numeric_time_raises": ["AC-4.3"],
  "test_hour_beyond_twelve_with_meridiem_raises": ["AC-4.6"],
  "test_break_longer_than_shift_raises": ["AC-4.7"],
  "test_break_error_message_names_the_problem": ["AC-4.7"],
  "test_single_digit_minutes_are_rejected": ["AC-4.4"],
  "test_three_digit_hours_are_rejected": ["AC-4.5"],
  "test_minute_sixty_is_rejected": ["AC-4.2"],
  "test_hour_twenty_four_is_rejected": ["AC-4.1"],
  "test_invalid_meridiem_time_error_names_the_offending_value": ["AC-4.6"],
  "test_meridiem_and_24_hour_notations_can_be_mixed": ["AC-3.6"],
  "test_break_in_twelve_hour_notation": ["AC-3.7"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
