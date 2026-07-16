# Metric-to-imperial unit conversion

## Overview
A one-directional unit converter that turns metric measurements into their imperial counterparts: kilometers to miles, Celsius to Fahrenheit, kilograms to pounds, and liters to US or UK gallons. Only these metric-to-imperial pairings are supported; every other pairing — the reverse direction, a mismatch of dimensions, or a unit converted to itself — is refused with a descriptive error.

## User Stories

### US-1: Distance
As a traveler, I want kilometers converted to miles, so that I can read road distances in imperial units.

- AC-1.1: Kilometers convert to miles at 0.621371 miles per kilometer, scaling linearly (1 km is 0.621371 miles; 100 km is 62.1371 miles).
- AC-1.2: Zero kilometers converts to zero miles.

### US-2: Temperature
As a traveler, I want Celsius converted to Fahrenheit, so that I can read the weather in imperial units.

- AC-2.1: Celsius converts to Fahrenheit by the standard formula — multiply by nine fifths and add 32 — so 30 degrees Celsius is 86 degrees Fahrenheit.
- AC-2.2: The freezing point of water, 0 degrees Celsius, converts to 32 degrees Fahrenheit.
- AC-2.3: The boiling point of water, 100 degrees Celsius, converts to 212 degrees Fahrenheit.
- AC-2.4: The crossover point holds: minus 40 degrees Celsius converts to minus 40 degrees Fahrenheit.

### US-3: Mass
As a shopper, I want kilograms converted to pounds, so that I can read weights in imperial units.

- AC-3.1: Kilograms convert to pounds at one pound per 0.45359237 kilograms, so 1 kg is 1 divided by 0.45359237 pounds and 5 kg is approximately 11.02311310 pounds.

### US-4: Volume
As a shopper, I want liters converted to gallons of either standard, so that I can read volumes wherever I am.

- AC-4.1: Liters convert to US gallons at 3.785411784 liters per US gallon (so 3.785411784 liters is exactly 1 US gallon).
- AC-4.2: Liters convert to UK gallons at 4.54609 liters per UK gallon (so 4.54609 liters is exactly 1 UK gallon).
- AC-4.3: The two standards differ: the same volume in liters yields fewer UK gallons than US gallons.

### US-5: Guarding the supported set
As an integrator, I want unsupported conversions refused loudly, so that unit mistakes surface immediately instead of producing wrong numbers.

- AC-5.1: The converter recognises exactly nine units: kilometers, miles, Celsius, Fahrenheit, kilograms, pounds, liters, US gallons and UK gallons.
- AC-5.2: Only the metric-to-imperial direction is supported: reversing a supported pair (miles to kilometers, or Fahrenheit to Celsius) is refused.
- AC-5.3: Pairing units of different dimensions (such as kilometers to pounds) is refused.
- AC-5.4: Converting a unit to itself is refused.
- AC-5.5: The refusal is raised as a dedicated unsupported-conversion error that is also a standard value error, so callers can handle it generically.
- AC-5.6: The refusal message contains the words "unsupported conversion" and names both units of the offending pair in plain lowercase words (for example "miles" and "kilometers").

## Traceability
```json
{
  "test_one_kilometer_to_miles": ["AC-1.1"],
  "test_one_hundred_kilometers_to_miles": ["AC-1.1"],
  "test_zero_kilometers_to_miles": ["AC-1.2"],
  "test_thirty_celsius_to_fahrenheit": ["AC-2.1"],
  "test_freezing_point_celsius_to_fahrenheit": ["AC-2.2"],
  "test_boiling_point_celsius_to_fahrenheit": ["AC-2.3"],
  "test_minus_forty_crossover_point": ["AC-2.4"],
  "test_five_kilograms_to_pounds": ["AC-3.1"],
  "test_one_kilogram_to_pounds": ["AC-3.1"],
  "test_one_us_gallon_worth_of_liters": ["AC-4.1"],
  "test_one_liter_to_us_gallons": ["AC-4.1"],
  "test_one_uk_gallon_worth_of_liters": ["AC-4.2"],
  "test_ten_liters_to_uk_gallons": ["AC-4.2"],
  "test_us_and_uk_gallons_differ": ["AC-4.3"],
  "test_reverse_direction_is_unsupported": ["AC-5.2"],
  "test_fahrenheit_to_celsius_is_unsupported": ["AC-5.2"],
  "test_cross_dimension_pair_is_unsupported": ["AC-5.3"],
  "test_identity_pair_is_unsupported": ["AC-5.4"],
  "test_domain_error_is_a_value_error": ["AC-5.5"],
  "test_error_message_names_both_units": ["AC-5.6"],
  "test_nine_units_are_recognised": ["AC-5.1"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
