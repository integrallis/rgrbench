"""Alarm interface - TDD Ebook Object Composition Example"""

from abc import ABC, abstractmethod


class Alarm(ABC):
    """Abstract base class for all alarm types"""

    @abstractmethod
    def trigger(self) -> str:
        """Trigger the alarm and return the alarm sound/message"""
        pass
