"""Last Sunday kata.

Given a year, determine the date of the final Sunday in every one of its
twelve months. The year is an injected input (no system clock is consulted)
and each result is rendered in ISO ``YYYY-MM-DD`` form. Boundary behaviour
follows the Gregorian calendar: leap-year Februaries may end on the 29th
(which is itself the answer when it falls on a Sunday), century years not
divisible by 400 keep a 28-day February, and a year may end with December 31
being a Sunday.

Kata catalogued at tddbuddy.com/katas/last-sunday; implementation and tests
original (MIT), machine-authored from the specification, 2026.
"""

import calendar
from datetime import date, timedelta


def last_sunday_of_month(year: int, month: int) -> date:
    """Return the date of the final Sunday of the given month."""
    if not 1 <= month <= 12:
        raise ValueError(f"month must be in 1..12, got {month}")
    last_day = date(year, month, calendar.monthrange(year, month)[1])
    return last_day - timedelta(days=(last_day.weekday() + 1) % 7)


def last_sundays(year: int) -> list[str]:
    """Return the last Sunday of each month of ``year`` as ISO date strings."""
    return [last_sunday_of_month(year, month).isoformat() for month in range(1, 13)]
