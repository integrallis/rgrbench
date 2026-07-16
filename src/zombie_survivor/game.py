"""Zombie Survivor kata - the game holding survivors and its history.

A game begins with zero survivors; survivors can join at any time but
their names must be unique within the game. The game level equals the
highest level among living survivors (Blue when none are alive), and
the game ends once it has survivors and all of them are dead. The game
keeps a history of noteworthy events: its start (timestamped by an
injected clock), survivors joining, equipment acquisitions, wounds,
deaths, survivor level-ups, game level changes, and the game's end.

Kata catalogued at tddbuddy.com/katas/zombie-survivor; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from datetime import datetime
from typing import Callable

from zombie_survivor.survivor import Level, Survivor


class Game:
    """A zombie apocalypse game session with survivors and history."""

    def __init__(self, clock: Callable[[], datetime]) -> None:
        self._survivors: list[Survivor] = []
        self._level = Level.BLUE
        self._end_recorded = False
        self._history: list[str] = [f"Game started at {clock().isoformat()}"]

    @property
    def survivors(self) -> tuple[Survivor, ...]:
        """Survivors in the game, in joining order."""
        return tuple(self._survivors)

    @property
    def has_ended(self) -> bool:
        """True once the game has survivors and all of them are dead."""
        return bool(self._survivors) and all(
            not survivor.is_alive for survivor in self._survivors
        )

    @property
    def level(self) -> Level:
        """Highest level among living survivors, Blue when none live."""
        levels = [survivor.level for survivor in self._survivors if survivor.is_alive]
        if not levels:
            return Level.BLUE
        return max(levels, key=lambda level: level.value)

    @property
    def history(self) -> tuple[str, ...]:
        """Every event recorded so far, oldest first."""
        return tuple(self._history)

    def add_survivor(self, survivor: Survivor) -> None:
        """Add a survivor; names must be unique within the game."""
        if any(existing.name == survivor.name for existing in self._survivors):
            raise ValueError(f"A survivor named '{survivor.name}' already exists")
        self._survivors.append(survivor)
        survivor.add_listener(self._on_survivor_event)
        self._history.append(f"{survivor.name} joined the game")
        self._sync(death_announced=not survivor.is_alive)

    def _on_survivor_event(self, kind: str, message: str) -> None:
        self._history.append(message)
        self._sync(death_announced=kind == "died")

    def _sync(self, death_announced: bool) -> None:
        if self.has_ended:
            if death_announced and not self._end_recorded:
                self._history.append("The game has ended: all survivors died")
                self._end_recorded = True
            return
        current = self.level
        if current is not self._level:
            self._level = current
            self._history.append(f"Game level changed to {current.name.title()}")
