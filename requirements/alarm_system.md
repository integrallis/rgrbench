# Composable alarm sounds

## Overview
A home-alarm product line built from small, combinable alarm units. A basic loud alarm produces a fixed warning sound when triggered. A day/night switched alarm wraps any other alarm and decides, based on whether it is currently day, whether the wrapped alarm sounds or stays silent. A hybrid alarm bundles several alarms and sounds them together as one.

## User Stories

### US-1: Loud alarm
As a homeowner, I want a basic alarm that sounds loudly when triggered, so that intrusions are impossible to miss.

- AC-1.1: Triggering the loud alarm produces exactly the sound report "LOUD ALARM!".

### US-2: Day/night switching
As a homeowner, I want an alarm that only sounds during the day, so that I am not woken by night-time triggers.

- AC-2.1: A day/night switched alarm is configured with an alarm to wrap and whether it is currently day; when it is day, triggering it produces the wrapped alarm's sound unchanged.
- AC-2.2: When it is night, triggering it produces silence (an empty sound report).

### US-3: Combining alarms
As a homeowner, I want several alarms to act as one, so that a single trigger sets them all off together.

- AC-3.1: A hybrid alarm holds a collection of alarms; triggering it produces the sounds of all of its member alarms combined into one report, separated by a single space (worked example: two loud alarms together produce "LOUD ALARM! LOUD ALARM!").

## Traceability
```json
{
  "test_loud_alarm_should_trigger_loudly": ["AC-1.1"],
  "test_day_night_switched_alarm_should_trigger_during_day": ["AC-2.1"],
  "test_day_night_switched_alarm_should_be_silent_during_night": ["AC-2.2"],
  "test_hybrid_alarm_should_combine_multiple_alarms": ["AC-3.1"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
