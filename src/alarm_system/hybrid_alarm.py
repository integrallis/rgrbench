"""HybridAlarm - TDD Ebook Object Composition Example"""

from .alarm import Alarm


class HybridAlarm(Alarm):
    """Composition alarm that combines multiple alarm sources"""

    def __init__(self, alarms: list[Alarm]) -> None:
        """Initialize with list of component alarms"""
        self._alarms = alarms

    def trigger(self) -> str:
        """Trigger all component alarms and combine outputs"""
        results = []
        for alarm in self._alarms:
            result = alarm.trigger()
            if result:  # Only include non-empty results
                results.append(result)
        return " ".join(results)
