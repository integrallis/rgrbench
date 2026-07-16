"""Darts Game - 301 scoring system"""

from enum import Enum


class Multiplier(Enum):
    """Dart multiplier values"""

    DOUBLE = 2
    TRIPLE = 3


class Darts:
    """A game of 301 darts"""

    def __init__(self) -> None:
        """Initialize a new game"""
        self._score = 301
        self._last_turn_score = 301
        self._is_finished = False
        self._turn = 1
        self._darts_left = 3

    def score(self) -> int:
        """Get current score"""
        return self._score

    def is_finished(self) -> bool:
        """Check if game is finished"""
        return self._is_finished

    def get_turn(self) -> int:
        """Get current turn number"""
        return self._turn

    def darts_left(self) -> int:
        """Get number of darts left in current turn"""
        return self._darts_left

    def dart(self, value: int, multiplier: Multiplier | None = None) -> None:
        """Throw a dart with the given value and optional multiplier"""
        # Calculate actual dart score
        dart_score = value
        if multiplier:
            dart_score *= multiplier.value

        # Calculate new score
        new_score = self._score - dart_score

        # Check for winning condition (must finish with double)
        if new_score == 0 and multiplier == Multiplier.DOUBLE:
            self._is_finished = True
            return

        # Check for bust conditions (double-out): below zero, exactly 1 (no double
        # can finish from 1), or reaching zero without a double
        if new_score < 0 or new_score == 1 or new_score == 0:
            # Bust! Reset to start of turn
            self._score = self._last_turn_score
            self._darts_left = 3
            self._turn += 1
        elif self._darts_left == 1:
            # End of turn
            self._score = new_score
            self._last_turn_score = new_score
            self._darts_left = 3
            self._turn += 1
        else:
            # Continue turn
            self._score = new_score
            self._darts_left -= 1
