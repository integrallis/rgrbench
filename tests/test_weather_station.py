"""
Tests for Weather Station kata - readings, statistics, observer notifications
"""

from datetime import datetime

import pytest


def _reading(
    hour: int = 12,
    temperature: float = 20.0,
    humidity: float = 50.0,
    pressure: float = 1013.0,
    day: int = 1,
) -> "object":
    from weather_station import Reading

    return Reading(datetime(2026, 3, day, hour, 0), temperature, humidity, pressure)


def test_humidity_below_zero_is_rejected() -> None:
    """Test 1: Humidity below 0 percent is invalid"""
    from weather_station import Reading

    with pytest.raises(ValueError, match="humidity must be between 0 and 100"):
        Reading(datetime(2026, 3, 1, 9, 0), 20.0, -1.0, 1013.0)


def test_humidity_above_hundred_is_rejected() -> None:
    """Test 2: Humidity above 100 percent is invalid"""
    from weather_station import Reading

    with pytest.raises(ValueError, match="humidity must be between 0 and 100"):
        Reading(datetime(2026, 3, 1, 9, 0), 20.0, 100.5, 1013.0)


def test_humidity_boundaries_are_valid() -> None:
    """Test 3: Humidity of exactly 0 and exactly 100 is accepted"""
    from weather_station import Reading

    assert Reading(datetime(2026, 3, 1, 9, 0), 20.0, 0.0, 1013.0).humidity == 0.0
    assert Reading(datetime(2026, 3, 1, 9, 0), 20.0, 100.0, 1013.0).humidity == 100.0


def test_non_positive_pressure_is_rejected() -> None:
    """Test 4: Pressure must be positive"""
    from weather_station import Reading

    with pytest.raises(ValueError, match="pressure must be positive"):
        Reading(datetime(2026, 3, 1, 9, 0), 20.0, 50.0, 0.0)


def test_current_reading_is_the_latest() -> None:
    """Test 5: The station reports the most recently recorded reading"""
    from weather_station import WeatherStation

    station = WeatherStation()
    first = _reading(hour=9, temperature=18.0)
    second = _reading(hour=10, temperature=21.0)
    station.record(first)
    station.record(second)
    assert station.current_reading == second
    assert station.readings == (first, second)


def test_current_reading_is_none_before_any_reading() -> None:
    """Test 6: With no readings there is no current reading"""
    from weather_station import WeatherStation

    assert WeatherStation().current_reading is None


def test_min_max_and_average_temperature() -> None:
    """Test 7: Min, max, and average cover all recorded readings"""
    from weather_station import WeatherStation

    station = WeatherStation()
    for hour, temperature in [(9, 10.0), (12, 30.0), (15, 20.0)]:
        station.record(_reading(hour=hour, temperature=temperature))
    assert station.min_temperature() == 10.0
    assert station.max_temperature() == 30.0
    assert station.average_temperature() == 20.0


def test_average_over_inclusive_time_window() -> None:
    """Test 8: A timestamp window bounds statistics inclusively"""
    from datetime import datetime

    from weather_station import WeatherStation

    station = WeatherStation()
    for day, temperature in [(1, 10.0), (2, 20.0), (3, 30.0), (4, 40.0)]:
        station.record(_reading(day=day, temperature=temperature))
    start = datetime(2026, 3, 2, 12, 0)
    end = datetime(2026, 3, 3, 12, 0)
    assert station.average_temperature(start=start, end=end) == 25.0
    assert station.min_temperature(start=start) == 20.0
    assert station.max_temperature(end=end) == 30.0


def test_statistics_without_readings_are_an_error() -> None:
    """Test 9: Asking for statistics before any reading raises"""
    from weather_station import WeatherStation

    station = WeatherStation()
    with pytest.raises(ValueError, match="^no readings recorded$"):
        station.average_temperature()


def test_statistics_over_empty_window_are_an_error() -> None:
    """Test 10: A window matching no readings raises"""
    from datetime import datetime

    from weather_station import WeatherStation

    station = WeatherStation()
    station.record(_reading(day=1))
    with pytest.raises(ValueError, match="no readings recorded"):
        station.min_temperature(start=datetime(2026, 3, 5, 0, 0))


def test_trend_rising() -> None:
    """Test 11: Three strictly increasing temperatures read as rising"""
    from weather_station import WeatherStation

    station = WeatherStation()
    for hour, temperature in [(9, 10.0), (10, 12.0), (11, 15.0)]:
        station.record(_reading(hour=hour, temperature=temperature))
    assert station.temperature_trend() == "rising"


def test_trend_falling() -> None:
    """Test 12: Three strictly decreasing temperatures read as falling"""
    from weather_station import WeatherStation

    station = WeatherStation()
    for hour, temperature in [(9, 15.0), (10, 12.0), (11, 10.0)]:
        station.record(_reading(hour=hour, temperature=temperature))
    assert station.temperature_trend() == "falling"


def test_trend_steady_for_flat_or_mixed_temperatures() -> None:
    """Test 13: Repeated or zig-zag temperatures read as steady"""
    from weather_station import WeatherStation

    station = WeatherStation()
    for hour, temperature in [(9, 10.0), (10, 10.0), (11, 10.0)]:
        station.record(_reading(hour=hour, temperature=temperature))
    assert station.temperature_trend() == "steady"

    zigzag = WeatherStation()
    for hour, temperature in [(9, 10.0), (10, 14.0), (11, 12.0)]:
        zigzag.record(_reading(hour=hour, temperature=temperature))
    assert zigzag.temperature_trend() == "steady"


def test_trend_needs_at_least_two_readings() -> None:
    """Test 14: Zero or one reading reads as steady"""
    from weather_station import WeatherStation

    station = WeatherStation()
    assert station.temperature_trend() == "steady"
    station.record(_reading(temperature=10.0))
    assert station.temperature_trend() == "steady"


def test_trend_uses_only_the_three_most_recent_readings() -> None:
    """Test 15: Older readings do not affect the trend"""
    from weather_station import WeatherStation

    station = WeatherStation()
    for hour, temperature in [(8, 30.0), (9, 5.0), (10, 6.0), (11, 7.0)]:
        station.record(_reading(hour=hour, temperature=temperature))
    assert station.temperature_trend() == "rising"


def test_observers_receive_each_recorded_reading() -> None:
    """Test 16: Every registered observer is notified of a new reading"""
    from weather_station import CurrentConditionsDisplay, WeatherStation

    station = WeatherStation()
    first_display = CurrentConditionsDisplay()
    second_display = CurrentConditionsDisplay()
    station.add_observer(first_display)
    station.add_observer(second_display)
    station.record(_reading(temperature=21.5, humidity=60.0, pressure=1013.2))
    expected = "Current conditions: 21.5°C, 60.0% humidity, 1013.2 hPa"
    assert first_display.render() == expected
    assert second_display.render() == expected


def test_removed_observer_is_no_longer_notified() -> None:
    """Test 17: After removal an observer stops receiving readings"""
    from weather_station import CurrentConditionsDisplay, WeatherStation

    station = WeatherStation()
    display = CurrentConditionsDisplay()
    station.add_observer(display)
    station.remove_observer(display)
    station.record(_reading())
    assert display.render() == "No data"


def test_removing_an_unknown_observer_is_ignored() -> None:
    """Test 18: Removing an observer that was never added is a no-op"""
    from weather_station import CurrentConditionsDisplay, WeatherStation

    station = WeatherStation()
    station.remove_observer(CurrentConditionsDisplay())
    station.record(_reading())
    assert station.current_reading is not None


def test_current_conditions_display_before_data() -> None:
    """Test 19: The conditions display shows a placeholder before updates"""
    from weather_station import CurrentConditionsDisplay

    assert CurrentConditionsDisplay().render() == "No data"


def test_statistics_display_tracks_observed_temperatures() -> None:
    """Test 20: The statistics display folds in each observed temperature"""
    from weather_station import StatisticsDisplay, WeatherStation

    station = WeatherStation()
    display = StatisticsDisplay()
    station.add_observer(display)
    for hour, temperature in [(9, 10.0), (12, 30.0), (15, 20.0)]:
        station.record(_reading(hour=hour, temperature=temperature))
    assert display.render() == "Temperature min 10.0°C, max 30.0°C, avg 20.0°C"


def test_statistics_display_before_data() -> None:
    """Test 21: The statistics display shows a placeholder before updates"""
    from weather_station import StatisticsDisplay

    assert StatisticsDisplay().render() == "No data"


def test_high_temperature_alert() -> None:
    """Test 22: A reading strictly above the high threshold raises an alert"""
    from weather_station import TemperatureAlert, WeatherStation

    station = WeatherStation()
    alert = TemperatureAlert(high=40.0)
    station.add_observer(alert)
    station.record(_reading(hour=9, temperature=41.0))
    assert alert.alerts == ("ALERT: temperature 41.0°C above threshold 40.0°C",)


def test_reading_at_threshold_does_not_alert() -> None:
    """Test 23: A reading exactly at the threshold raises no alert"""
    from weather_station import TemperatureAlert, WeatherStation

    station = WeatherStation()
    alert = TemperatureAlert(high=40.0, low=0.0)
    station.add_observer(alert)
    station.record(_reading(hour=9, temperature=40.0))
    station.record(_reading(hour=10, temperature=0.0))
    assert alert.alerts == ()


def test_low_temperature_alert() -> None:
    """Test 24: A reading strictly below the low threshold raises an alert"""
    from weather_station import TemperatureAlert, WeatherStation

    station = WeatherStation()
    alert = TemperatureAlert(low=0.0)
    station.add_observer(alert)
    station.record(_reading(hour=9, temperature=-5.0))
    station.record(_reading(hour=10, temperature=5.0))
    assert alert.alerts == ("ALERT: temperature -5.0°C below threshold 0.0°C",)


def test_windowed_min_and_max_ignore_readings_outside_the_window() -> None:
    """Test 25: Min and max exclude readings before the start and after the end"""
    from datetime import datetime

    from weather_station import WeatherStation

    station = WeatherStation()
    for day, temperature in [(1, 30.0), (2, 20.0), (3, 25.0), (4, 5.0)]:
        station.record(_reading(day=day, temperature=temperature))
    start = datetime(2026, 3, 2, 0, 0)
    end = datetime(2026, 3, 3, 23, 0)
    assert station.min_temperature(start=start, end=end) == 20.0
    assert station.max_temperature(start=start, end=end) == 25.0


def test_trend_with_exactly_two_readings() -> None:
    """Test 26: Two readings are enough to read a rising or falling trend"""
    from weather_station import WeatherStation

    rising = WeatherStation()
    for hour, temperature in [(9, 10.0), (10, 12.0)]:
        rising.record(_reading(hour=hour, temperature=temperature))
    assert rising.temperature_trend() == "rising"

    falling = WeatherStation()
    for hour, temperature in [(9, 12.0), (10, 10.0)]:
        falling.record(_reading(hour=hour, temperature=temperature))
    assert falling.temperature_trend() == "falling"


def test_trend_zigzag_ending_below_start_is_steady() -> None:
    """Test 27: A rise then a fall below the starting temperature reads as steady"""
    from weather_station import WeatherStation

    station = WeatherStation()
    for hour, temperature in [(9, 10.0), (10, 14.0), (11, 8.0)]:
        station.record(_reading(hour=hour, temperature=temperature))
    assert station.temperature_trend() == "steady"
