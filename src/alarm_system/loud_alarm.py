"""LoudAlarm - TDD Ebook Object Composition Example"""

from .alarm import Alarm


class LoudAlarm(Alarm):
    """Basic loud alarm implementation"""

    def trigger(self) -> str:
        """Trigger the loud alarm"""
        return "LOUD ALARM!"
