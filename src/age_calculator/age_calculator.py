"""Age Calculator kata.

Compute a person's age in whole years from two explicit dates: the birth date and a
reference date to compare against. Both dates are inputs; the system clock is never
consulted, so results are stable regardless of when or where the code runs.

Rules:

- The age is the number of whole years between the birth date and the reference date.
  Example: born 28 October 2016, reference 5 November 2022 -> age 6.
- A person born on 29 February turns a year older on 1 March in non-leap years (and on
  29 February in leap years). This falls out of comparing (month, day) tuples: on
  28 February, (2, 28) < (2, 29) still holds, so the age is decremented.
- If the birth date is after the reference date, a ValueError is raised with the
  message "birthdate is after today".
- Bonus: the start of a person's "birthday week", returned as a string such as
  "September 3, 2017". If the birthday falls on Thursday, Friday or Saturday the week
  starts on the Sunday of that week; if it falls on Sunday through Wednesday the week
  starts six days before the birthday.

Kata catalogued at tddbuddy.com/katas/age-calculator; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from __future__ import annotations

import calendar
from datetime import date, timedelta

_THURSDAY_TO_SATURDAY = (3, 4, 5)  # date.weekday(): Monday=0 ... Sunday=6


def calculate_age(birth_date: date, reference_date: date) -> int:
    """Return the age in whole years on ``reference_date`` for ``birth_date``.

    Raises ValueError("birthdate is after today") when the birth date is after the
    reference date.
    """
    if birth_date > reference_date:
        raise ValueError("birthdate is after today")
    age = reference_date.year - birth_date.year
    if (reference_date.month, reference_date.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age


def birthday_week_start(birthday: date) -> str:
    """Return the first day of the birthday week as e.g. "September 3, 2017".

    Thursday-Saturday birthdays: the week starts on the Sunday of that week.
    Sunday-Wednesday birthdays: the week starts six days before the birthday.
    """
    if birthday.weekday() in _THURSDAY_TO_SATURDAY:
        # Step back to the most recent Sunday (Monday=0 ... Sunday=6).
        start = birthday - timedelta(days=birthday.weekday() + 1)
    else:
        start = birthday - timedelta(days=6)
    return f"{calendar.month_name[start.month]} {start.day}, {start.year}"
