# Time zone conversion

## Overview
People scheduling across regions need to know what a given local date and time in one
place corresponds to in another. The converter takes a wall-clock moment together with
a named source zone and a named destination zone (standard IANA zone names such as
"America/New_York" or "Asia/Kolkata") and produces the equivalent wall-clock moment in
the destination, honouring daylight saving, fractional-hour offsets, and calendar
rollovers. It works purely on the moment it is given — it never consults the system
clock — and it also offers a text-to-text form for ISO 8601 date-time strings.

## User Stories

### US-1: Convert a local time between two named zones
As a meeting organiser, I want a local time in one zone expressed in another zone, so that participants everywhere see the correct local time.

- AC-1.1: A wall-clock moment given for a source zone converts to the correct wall clock in the destination; noon UTC on 15 January 2021 is 07:00 that day in New York (UTC-5).
- AC-1.2: Daylight saving is honoured: noon UTC in July is 08:00 in New York (UTC-4).
- AC-1.3: The converted result knows its zone: it carries the destination's UTC offset (minus five hours for New York in January).
- AC-1.4: The source moment and the converted result denote the same instant in time.
- AC-1.5: Converting between identical zones leaves the wall-clock time unchanged.
- AC-1.6: Converting to another zone and back recovers the original wall-clock time.

### US-2: Handle calendar boundaries
As a meeting organiser, I want conversions that cross a date boundary to land on the right calendar day, so that overnight, year-end, and leap-day differences never confuse a schedule.

- AC-2.1: A conversion may fall on the previous day: 01:00 in New York is 22:00 the previous day in Los Angeles.
- AC-2.2: Crossing the international date line can move a full day forward: noon in Honolulu (UTC-10) is noon the next day in Kiritimati (UTC+14).
- AC-2.3: The year boundary is honoured: 20:00 on 31 December 2020 in New York is already 01:00 on 1 January 2021 in UTC.
- AC-2.4: Leap days are honoured: 23:00 UTC on 29 February 2020 is 04:30 on 1 March in India.

### US-3: Support fractional-hour zones without losing precision
As a traveller, I want zones with half-hour and quarter-hour offsets handled exactly, so that times in places like India and Nepal come out right to the minute.

- AC-3.1: Half-hour offsets are exact: noon UTC is 17:30 in India (UTC+5:30), and 09:30 in India is 04:00 UTC.
- AC-3.2: Quarter-hour offsets are exact: noon UTC is 17:45 in Nepal (UTC+5:45).
- AC-3.3: Conversions between whole-hour zones never disturb the minutes or seconds of the moment.

### US-4: Convert ISO 8601 text
As an integrator, I want to convert date-time text directly, so that systems exchanging ISO 8601 strings need no extra conversion steps.

- AC-4.1: An ISO 8601 date-time string converts to an ISO 8601 string carrying the destination offset: "2021-07-15T12:00:00" from UTC to New York yields "2021-07-15T08:00:00-04:00".
- AC-4.2: Fractional offsets render in the output text: UTC noon to India yields "2021-01-15T17:30:00+05:30".

### US-5: Reject ambiguous or unknown input
As an integrator, I want bad input refused with a clear message, so that errors surface at the boundary instead of producing wrong times.

- AC-5.1: Malformed date-time text is rejected as invalid.
- AC-5.2: An unrecognised zone name — whether source or destination — is rejected with an error whose message contains "unknown time zone".
- AC-5.3: A moment that already carries zone information is ambiguous input and is rejected with an error whose message opens with "moment must be naive".

## Traceability
```json
{
  "test_utc_to_new_york_standard_time": ["AC-1.1"],
  "test_utc_to_new_york_summer_offset": ["AC-1.2"],
  "test_result_carries_destination_offset": ["AC-1.3"],
  "test_conversion_preserves_the_instant": ["AC-1.4"],
  "test_crossing_midnight_into_the_previous_date": ["AC-2.1"],
  "test_half_hour_offset_zone": ["AC-3.1"],
  "test_quarter_hour_offset_zone": ["AC-3.2"],
  "test_half_hour_offset_back_to_utc": ["AC-3.1"],
  "test_international_date_line_swing": ["AC-2.2"],
  "test_year_boundary_transition": ["AC-2.3"],
  "test_leap_day_transition": ["AC-2.4"],
  "test_same_zone_keeps_the_wall_clock": ["AC-1.5"],
  "test_round_trip_returns_the_original_wall_clock": ["AC-1.6"],
  "test_minutes_and_seconds_are_preserved": ["AC-3.3"],
  "test_iso_string_conversion": ["AC-4.1"],
  "test_iso_string_conversion_to_half_hour_zone": ["AC-4.2"],
  "test_invalid_iso_string_is_rejected": ["AC-5.1"],
  "test_unknown_source_zone_is_rejected": ["AC-5.2"],
  "test_unknown_destination_zone_is_rejected": ["AC-5.2"],
  "test_aware_input_is_rejected": ["AC-5.3"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
