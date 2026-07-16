"""Time Zone Converter kata.

Convert a given wall-clock datetime from a source time zone to a destination
time zone. The moment to convert is always injected -- the system clock is
never consulted -- and zones are fixed, named entries in the IANA database
resolved through ``zoneinfo`` (covering whole-hour, half-hour and
quarter-hour offsets). The conversion is pure offset arithmetic on the given
instant, so crossings of midnight, month, leap-day and year boundaries, and
even the International Date Line, fall out of standard library date handling.
An ISO 8601 string form is provided alongside the datetime form, and unknown
zone names or invalid datetime strings are rejected with clear errors.

Kata catalogued at tddbuddy.com/katas/time-zone-converter; implementation and
tests original (MIT), machine-authored from the specification, 2026.
"""

from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def _zone(name: str) -> ZoneInfo:
    """Resolve a fixed IANA zone name, rejecting unknown names."""
    try:
        return ZoneInfo(name)
    except (ZoneInfoNotFoundError, ValueError):
        raise ValueError(f"unknown time zone: {name!r}") from None


def convert(moment: datetime, from_zone: str, to_zone: str) -> datetime:
    """Convert a naive wall-clock ``moment`` in ``from_zone`` to ``to_zone``.

    Returns an aware datetime carrying the destination zone.
    """
    if moment.tzinfo is not None:
        raise ValueError(
            "moment must be naive; it is interpreted as local time in from_zone"
        )
    return moment.replace(tzinfo=_zone(from_zone)).astimezone(_zone(to_zone))


def convert_iso(moment: str, from_zone: str, to_zone: str) -> str:
    """Convert an ISO 8601 datetime string, returning ISO 8601 with offset."""
    return convert(datetime.fromisoformat(moment), from_zone, to_zone).isoformat()
