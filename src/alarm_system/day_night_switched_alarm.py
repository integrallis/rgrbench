"""DayNightSwitchedAlarm - TDD Ebook Object Composition Example"""

from .alarm import Alarm


class DayNightSwitchedAlarm(Alarm):
    """Decorator alarm that switches behavior based on time of day"""

    def __init__(self, wrapped_alarm: Alarm, is_day: bool) -> None:
        """Initialize with wrapped alarm and day/night state"""
        self._wrapped_alarm = wrapped_alarm
        self._is_day = is_day

    def trigger(self) -> str:
        """Trigger alarm during day, silent during night"""
        if self._is_day:
            return self._wrapped_alarm.trigger()
        return ""
