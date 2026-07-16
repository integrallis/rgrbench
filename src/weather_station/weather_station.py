"""Weather Station kata - readings, statistics, and observer notifications.

A ``WeatherStation`` receives timestamped ``Reading`` values as plain
inputs (temperature in degrees Celsius, relative humidity in percent,
barometric pressure in hectopascals). Humidity must lie between 0 and
100 and pressure must be positive. Every recorded reading is pushed to
all registered observers. The station reports the latest reading and
computes minimum, maximum, and average temperature, optionally limited
to an inclusive timestamp window so daily, weekly, or monthly summaries
fall out of the same query; asking for statistics when no reading
matches is an error. The temperature trend looks at the three most
recent readings: strictly increasing means "rising", strictly
decreasing means "falling", anything else (including fewer than two
readings) means "steady". Bundled observers: ``CurrentConditionsDisplay``
renders the latest conditions, ``StatisticsDisplay`` renders min/max/avg
of the temperatures it has seen, and ``TemperatureAlert`` collects alert
messages whenever a reading goes strictly above its high threshold or
strictly below its low threshold.

Kata catalogued at tddbuddy.com/katas/weather-station; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True)
class Reading:
    """A single validated weather reading supplied by the caller."""

    timestamp: datetime
    temperature: float
    humidity: float
    pressure: float

    def __post_init__(self) -> None:
        if not 0 <= self.humidity <= 100:
            raise ValueError("humidity must be between 0 and 100")
        if self.pressure <= 0:
            raise ValueError("pressure must be positive")


class Observer(Protocol):
    """Anything that wants to be told about new readings."""

    def update(self, reading: Reading) -> None:
        """Receive a newly recorded reading."""


class WeatherStation:
    """Stores readings, serves statistics, and notifies observers."""

    def __init__(self) -> None:
        self._readings: list[Reading] = []
        self._observers: list[Observer] = []

    def add_observer(self, observer: Observer) -> None:
        """Register an observer for future readings."""
        self._observers.append(observer)

    def remove_observer(self, observer: Observer) -> None:
        """Unregister an observer; unknown observers are ignored."""
        if observer in self._observers:
            self._observers.remove(observer)

    def record(self, reading: Reading) -> None:
        """Store a reading and notify every registered observer."""
        self._readings.append(reading)
        for observer in self._observers:
            observer.update(reading)

    @property
    def current_reading(self) -> Reading | None:
        """The most recently recorded reading, or None before any."""
        return self._readings[-1] if self._readings else None

    @property
    def readings(self) -> tuple[Reading, ...]:
        """All recorded readings in recording order."""
        return tuple(self._readings)

    def min_temperature(
        self, start: datetime | None = None, end: datetime | None = None
    ) -> float:
        """Lowest temperature, optionally within an inclusive window."""
        return min(self._temperatures(start, end))

    def max_temperature(
        self, start: datetime | None = None, end: datetime | None = None
    ) -> float:
        """Highest temperature, optionally within an inclusive window."""
        return max(self._temperatures(start, end))

    def average_temperature(
        self, start: datetime | None = None, end: datetime | None = None
    ) -> float:
        """Mean temperature, optionally within an inclusive window."""
        temperatures = self._temperatures(start, end)
        return sum(temperatures) / len(temperatures)

    def temperature_trend(self) -> str:
        """Trend over the three most recent readings."""
        recent = [reading.temperature for reading in self._readings[-3:]]
        if len(recent) < 2:
            return "steady"
        if all(later > earlier for earlier, later in zip(recent, recent[1:])):
            return "rising"
        if all(later < earlier for earlier, later in zip(recent, recent[1:])):
            return "falling"
        return "steady"

    def _temperatures(
        self, start: datetime | None, end: datetime | None
    ) -> list[float]:
        temperatures = [
            reading.temperature
            for reading in self._readings
            if (start is None or reading.timestamp >= start)
            and (end is None or reading.timestamp <= end)
        ]
        if not temperatures:
            raise ValueError("no readings recorded")
        return temperatures


class CurrentConditionsDisplay:
    """Observer that renders the most recent conditions."""

    def __init__(self) -> None:
        self._latest: Reading | None = None

    def update(self, reading: Reading) -> None:
        """Remember the latest reading."""
        self._latest = reading

    def render(self) -> str:
        """Render the latest conditions, or a placeholder before any."""
        if self._latest is None:
            return "No data"
        return (
            f"Current conditions: {self._latest.temperature:.1f}°C, "
            f"{self._latest.humidity:.1f}% humidity, "
            f"{self._latest.pressure:.1f} hPa"
        )


class StatisticsDisplay:
    """Observer that tracks min/max/avg of the temperatures it has seen."""

    def __init__(self) -> None:
        self._temperatures: list[float] = []

    def update(self, reading: Reading) -> None:
        """Fold the reading's temperature into the statistics."""
        self._temperatures.append(reading.temperature)

    def render(self) -> str:
        """Render the statistics, or a placeholder before any reading."""
        if not self._temperatures:
            return "No data"
        minimum = min(self._temperatures)
        maximum = max(self._temperatures)
        average = sum(self._temperatures) / len(self._temperatures)
        return (
            f"Temperature min {minimum:.1f}°C, "
            f"max {maximum:.1f}°C, avg {average:.1f}°C"
        )


class TemperatureAlert:
    """Observer that collects messages for threshold-crossing readings."""

    def __init__(self, high: float | None = None, low: float | None = None) -> None:
        self._high = high
        self._low = low
        self._alerts: list[str] = []

    def update(self, reading: Reading) -> None:
        """Record an alert when the reading crosses a threshold."""
        if self._high is not None and reading.temperature > self._high:
            self._alerts.append(
                f"ALERT: temperature {reading.temperature:.1f}°C "
                f"above threshold {self._high:.1f}°C"
            )
        if self._low is not None and reading.temperature < self._low:
            self._alerts.append(
                f"ALERT: temperature {reading.temperature:.1f}°C "
                f"below threshold {self._low:.1f}°C"
            )

    @property
    def alerts(self) -> tuple[str, ...]:
        """All alert messages collected so far."""
        return tuple(self._alerts)
