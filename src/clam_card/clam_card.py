"""Clam Card kata.

A contactless subway travel card that charges per journey, with fare caps over time.
Journey dates are injected by the caller; the system clock is never read.

Network and fares:

- Zone A stations: Asterisk, Amersham, Aldgate, Angel, Anerley.
- Zone B stations: Bison, Bugel, Balham, Bullhead, Barbican.
- A journey wholly within Zone A costs 2.50. If either end of a journey is a Zone B
  station, the Zone B price of 3.00 is charged.
- Charges cap per time period: within a single day at 7.00 (Zone A) / 8.00 (Zone B),
  within a single week at 40.00 / 47.00, and within a single month at 145.00 /
  165.00. However many journeys are made inside a period, the total charged never
  exceeds the applicable cap.
- Stations not on the network raise ``UnknownStationError`` naming the station.

Interpretations documented for this implementation: a day is a calendar date, a week
is an ISO calendar week (Monday-Sunday), and a month is a calendar month. When a
period mixes zones, the cap of the highest zone travelled in that period (Zone B if
any journey touched Zone B) applies; each journey is charged the largest amount that
keeps every period total within its cap.

Kata catalogued at tddbuddy.com/katas/clam-card; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from __future__ import annotations

from datetime import date

ZONE_A_STATIONS = frozenset({"Asterisk", "Amersham", "Aldgate", "Angel", "Anerley"})
ZONE_B_STATIONS = frozenset({"Bison", "Bugel", "Balham", "Bullhead", "Barbican"})

_SINGLE_FARES = {"A": 2.50, "B": 3.00}
_DAY_CAPS = {"A": 7.00, "B": 8.00}
_WEEK_CAPS = {"A": 40.00, "B": 47.00}
_MONTH_CAPS = {"A": 145.00, "B": 165.00}


class UnknownStationError(Exception):
    """Raised when a journey references a station that is not on the network."""


class ClamCard:
    """A travel card charging capped fares for journeys between stations."""

    def __init__(self) -> None:
        self._journeys: list[tuple[date, str, float]] = []

    @property
    def total_charged(self) -> float:
        """Total amount charged to the card so far."""
        return sum(charge for _, _, charge in self._journeys)

    def journey(self, origin: str, destination: str, on: date) -> float:
        """Charge for a journey from ``origin`` to ``destination`` on ``on``.

        Returns the amount charged after applying the day, week and month caps.
        """
        zone = self._journey_zone(origin, destination)
        charge = _SINGLE_FARES[zone]
        for caps, in_period in (
            (_DAY_CAPS, self._same_day),
            (_WEEK_CAPS, self._same_week),
            (_MONTH_CAPS, self._same_month),
        ):
            period = [
                (journey_zone, journey_charge)
                for journey_date, journey_zone, journey_charge in self._journeys
                if in_period(journey_date, on)
            ]
            zones = {zone}.union(journey_zone for journey_zone, _ in period)
            cap = caps["B"] if "B" in zones else caps["A"]
            already_charged = sum(journey_charge for _, journey_charge in period)
            charge = min(charge, max(cap - already_charged, 0.0))
        self._journeys.append((on, zone, charge))
        return charge

    def _journey_zone(self, origin: str, destination: str) -> str:
        zones = {self._station_zone(origin), self._station_zone(destination)}
        return "B" if "B" in zones else "A"

    @staticmethod
    def _station_zone(station: str) -> str:
        if station in ZONE_A_STATIONS:
            return "A"
        if station in ZONE_B_STATIONS:
            return "B"
        raise UnknownStationError(f"Unknown station: {station}")

    @staticmethod
    def _same_day(earlier: date, later: date) -> bool:
        return earlier == later

    @staticmethod
    def _same_week(earlier: date, later: date) -> bool:
        return earlier.isocalendar()[:2] == later.isocalendar()[:2]

    @staticmethod
    def _same_month(earlier: date, later: date) -> bool:
        return (earlier.year, earlier.month) == (later.year, later.month)
