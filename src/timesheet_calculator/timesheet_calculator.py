"""Timesheet calculator kata.

Requirements summary (paraphrased): given a start time, an end time and an
optional break duration, compute the time worked and report it as ``HH:mm``.
Times use the 24-hour clock by default. When the end time is earlier than the
start time the shift crosses midnight and the duration still comes out
correct (e.g. 17:02 to 02:09 with a 00:35 break is 08:32). Built-in duration
or date-time arithmetic types are off limits; the maths is done on minutes.
Bonus input formats supported here: three- or four-digit times without a
colon ("800" means 8:00, "1530" means 15:30) and 12-hour times with an
AM/PM suffix. Malformed times raise ``ValueError``, as does a break longer
than the time worked.

Kata catalogued at tddbuddy.com/katas/timesheet-calc; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from __future__ import annotations

_MINUTES_PER_DAY = 24 * 60
_MINUTES_PER_HOUR = 60


def calculate_work_hours(
    start: str, end: str, break_duration: str | None = None
) -> str:
    """Return the time worked between ``start`` and ``end`` as ``HH:mm``.

    ``break_duration`` (``HH:mm``), when given, is subtracted from the
    elapsed time. An end time earlier than the start time is treated as
    crossing midnight.
    """
    elapsed = (_parse_time(end) - _parse_time(start)) % _MINUTES_PER_DAY
    if break_duration is not None:
        elapsed -= _parse_time(break_duration)
    if elapsed < 0:
        raise ValueError("Break duration exceeds time worked")
    return f"{elapsed // _MINUTES_PER_HOUR:02d}:{elapsed % _MINUTES_PER_HOUR:02d}"


def _parse_time(value: str) -> int:
    """Parse a time-of-day string into minutes since midnight."""
    text = value.strip()
    text, meridiem = _split_meridiem(text)
    if ":" in text:
        hours_text, _, minutes_text = text.partition(":")
    elif text.isdigit() and len(text) in (3, 4):
        hours_text, minutes_text = text[:-2], text[-2:]
    else:
        raise ValueError(f"Invalid time: {value!r}")
    if not (
        hours_text.isdigit()
        and 1 <= len(hours_text) <= 2
        and minutes_text.isdigit()
        and len(minutes_text) == 2
    ):
        raise ValueError(f"Invalid time: {value!r}")
    hours, minutes = int(hours_text), int(minutes_text)
    if minutes > 59:
        raise ValueError(f"Invalid time: {value!r}")
    if meridiem is not None:
        hours = _to_24_hour(hours, meridiem, value)
    elif hours > 23:
        raise ValueError(f"Invalid time: {value!r}")
    return hours * _MINUTES_PER_HOUR + minutes


def _split_meridiem(text: str) -> tuple[str, str | None]:
    upper = text.upper()
    for suffix in ("AM", "PM"):
        if upper.endswith(suffix):
            return text[: -len(suffix)].strip(), suffix
    return text, None


def _to_24_hour(hours: int, meridiem: str, original: str) -> int:
    if not 1 <= hours <= 12:
        raise ValueError(f"Invalid time: {original!r}")
    if meridiem == "AM":
        return 0 if hours == 12 else hours
    return 12 if hours == 12 else hours + 12
