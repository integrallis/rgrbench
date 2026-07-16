# Weather station monitoring

## Overview
A weather station collects timestamped readings of temperature, humidity, and
barometric pressure, and serves three audiences at once: it answers statistical
questions about temperature over any time window, it reads the short-term temperature
trend, and it pushes every new reading to attached display and alerting devices the
moment it is recorded.

## User Stories

### US-1: Record validated readings
As a meteorologist, I want every reading validated and kept in arrival order, so that the station's data can be trusted and the latest conditions are always at hand.

- AC-1.1: A reading carries a timestamp, a temperature, a humidity, and a pressure; humidity must lie between 0 and 100 percent inclusive — exactly 0 and exactly 100 are accepted, while values outside are rejected with an error whose message contains "humidity must be between 0 and 100".
- AC-1.2: Pressure must be positive; zero or below is rejected with an error whose message contains "pressure must be positive".
- AC-1.3: The station keeps every recorded reading in order and reports the most recently recorded one as the current reading.
- AC-1.4: Before anything has been recorded there is no current reading.

### US-2: Answer temperature statistics over a time window
As a meteorologist, I want minimum, maximum, and average temperature — over everything or over a chosen period — so that I can summarise conditions for any stretch of time.

- AC-2.1: Minimum, maximum, and average temperature cover all recorded readings when no window is given.
- AC-2.2: A window may bound the statistics by a start timestamp, an end timestamp, or both; the bounds are inclusive.
- AC-2.3: Readings before the window's start or after its end are excluded from windowed minimum and maximum.
- AC-2.4: Asking for statistics when no readings qualify — none recorded at all, or none inside the window — is an error whose message reads "no readings recorded".

### US-3: Read the short-term temperature trend
As a forecaster, I want the station to summarise the recent temperature direction as rising, falling, or steady, so that I can glance at where conditions are heading.

- AC-3.1: The trend considers only the three most recent readings; older ones have no influence.
- AC-3.2: Strictly increasing temperatures over the considered readings read as "rising"; two readings are enough.
- AC-3.3: Strictly decreasing temperatures over the considered readings read as "falling"; two readings are enough.
- AC-3.4: Anything else — repeated values or a zig-zag, whether it ends above or below where it started — reads as "steady".
- AC-3.5: With zero or one reading the trend is "steady".

### US-4: Notify attached displays of each reading
As a station operator, I want display devices to receive every new reading automatically, so that what is shown always matches what was recorded.

- AC-4.1: Every attached device is notified of each newly recorded reading.
- AC-4.2: A detached device receives nothing further, and detaching a device that was never attached is silently ignored.
- AC-4.3: The current-conditions display renders the latest reading as "Current conditions: <temperature>°C, <humidity>% humidity, <pressure> hPa" — for example "Current conditions: 21.5°C, 60.0% humidity, 1013.2 hPa" — and shows "No data" before it has received anything.
- AC-4.4: The statistics display folds in each temperature it observes and renders "Temperature min <lowest>°C, max <highest>°C, avg <average>°C"; it shows "No data" before it has received anything.

### US-5: Raise temperature alerts on thresholds
As a station operator, I want an alert whenever the temperature leaves a configured band, so that extreme conditions are flagged immediately.

- AC-5.1: A reading strictly above the configured high threshold records the alert "ALERT: temperature <value>°C above threshold <high>°C".
- AC-5.2: A reading strictly below the configured low threshold records the alert "ALERT: temperature <value>°C below threshold <low>°C".
- AC-5.3: A reading exactly at a threshold raises no alert.

## Traceability
```json
{
  "test_humidity_below_zero_is_rejected": ["AC-1.1"],
  "test_humidity_above_hundred_is_rejected": ["AC-1.1"],
  "test_humidity_boundaries_are_valid": ["AC-1.1"],
  "test_non_positive_pressure_is_rejected": ["AC-1.2"],
  "test_current_reading_is_the_latest": ["AC-1.3"],
  "test_current_reading_is_none_before_any_reading": ["AC-1.4"],
  "test_min_max_and_average_temperature": ["AC-2.1"],
  "test_average_over_inclusive_time_window": ["AC-2.2"],
  "test_statistics_without_readings_are_an_error": ["AC-2.4"],
  "test_statistics_over_empty_window_are_an_error": ["AC-2.4"],
  "test_trend_rising": ["AC-3.2"],
  "test_trend_falling": ["AC-3.3"],
  "test_trend_steady_for_flat_or_mixed_temperatures": ["AC-3.4"],
  "test_trend_needs_at_least_two_readings": ["AC-3.5"],
  "test_trend_uses_only_the_three_most_recent_readings": ["AC-3.1"],
  "test_observers_receive_each_recorded_reading": ["AC-4.1", "AC-4.3"],
  "test_removed_observer_is_no_longer_notified": ["AC-4.2"],
  "test_removing_an_unknown_observer_is_ignored": ["AC-4.2"],
  "test_current_conditions_display_before_data": ["AC-4.3"],
  "test_statistics_display_tracks_observed_temperatures": ["AC-4.4"],
  "test_statistics_display_before_data": ["AC-4.4"],
  "test_high_temperature_alert": ["AC-5.1"],
  "test_reading_at_threshold_does_not_alert": ["AC-5.3"],
  "test_low_temperature_alert": ["AC-5.2"],
  "test_windowed_min_and_max_ignore_readings_outside_the_window": ["AC-2.3"],
  "test_trend_with_exactly_two_readings": ["AC-3.2", "AC-3.3"],
  "test_trend_zigzag_ending_below_start_is_steady": ["AC-3.4"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
