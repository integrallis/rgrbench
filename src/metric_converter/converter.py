"""Metric Converter kata.

A single pure function converts quantities from metric units to their
imperial counterparts. Five conversions are supported, each one-directional
(metric to imperial only):

* kilometers to miles       (kilometers x 0.621371)
* Celsius to Fahrenheit     (celsius x 1.8 + 32)
* kilograms to pounds       (kilograms / 0.45359237)
* liters to US gallons      (liters / 3.785411784)
* liters to UK gallons      (liters / 4.54609)

The nine recognised units are modelled as an enum so call sites cannot drift
between spellings. Requesting any pair outside the supported set raises a
domain error.

Kata catalogued at tddbuddy.com/katas/metric-converter; implementation and
tests original (MIT), machine-authored from the specification, 2026.
"""

from collections.abc import Callable
from enum import Enum


class Unit(Enum):
    """The nine units recognised by the converter."""

    KILOMETERS = "kilometers"
    MILES = "miles"
    CELSIUS = "celsius"
    FAHRENHEIT = "fahrenheit"
    KILOGRAMS = "kilograms"
    POUNDS = "pounds"
    LITERS = "liters"
    US_GALLONS = "us gallons"
    UK_GALLONS = "uk gallons"


class UnsupportedConversionError(ValueError):
    """Raised when a conversion pair is outside the supported set."""


_MILES_PER_KILOMETER = 0.621371
_KILOGRAMS_PER_POUND = 0.45359237
_LITERS_PER_US_GALLON = 3.785411784
_LITERS_PER_UK_GALLON = 4.54609

_CONVERSIONS: dict[tuple[Unit, Unit], Callable[[float], float]] = {
    (Unit.KILOMETERS, Unit.MILES): lambda value: value * _MILES_PER_KILOMETER,
    (Unit.CELSIUS, Unit.FAHRENHEIT): lambda value: value * 1.8 + 32,
    (Unit.KILOGRAMS, Unit.POUNDS): lambda value: value / _KILOGRAMS_PER_POUND,
    (Unit.LITERS, Unit.US_GALLONS): lambda value: value / _LITERS_PER_US_GALLON,
    (Unit.LITERS, Unit.UK_GALLONS): lambda value: value / _LITERS_PER_UK_GALLON,
}


def convert(value: float, from_unit: Unit, to_unit: Unit) -> float:
    """Convert ``value`` from a metric unit to an imperial unit."""
    try:
        conversion = _CONVERSIONS[(from_unit, to_unit)]
    except KeyError:
        raise UnsupportedConversionError(
            f"unsupported conversion: {from_unit.value} to {to_unit.value}"
        ) from None
    return conversion(value)
