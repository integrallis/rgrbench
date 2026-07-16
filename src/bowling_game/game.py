class Game:
    """Port of C# Game class"""

    def __init__(self) -> None:
        self._rolls: list[int] = [0] * 21
        self._current_roll: int = 0

    def roll(self, pins: int) -> None:
        """Port of Roll"""
        self._rolls[self._current_roll] = pins
        self._current_roll += 1

    def score(self) -> int:
        """Port of Score"""
        score = 0
        frame_index = 0
        for _frame in range(10):
            if self._is_strike(frame_index):
                score += self._strike_bonus(frame_index)
                frame_index += 1
            elif self._is_spare(frame_index):
                score += 10 + self._spare_bonus(frame_index)
                frame_index += 2
            else:
                score += self._sum_of_balls_in_frames(frame_index)
                frame_index += 2
        return score

    def _is_strike(self, frame_index: int) -> bool:
        """Port of IsStrike"""
        return self._rolls[frame_index] == 10

    def _sum_of_balls_in_frames(self, frame_index: int) -> int:
        """Port of SumOfBallsInFrames"""
        return self._rolls[frame_index] + self._rolls[frame_index + 1]

    def _spare_bonus(self, frame_index: int) -> int:
        """Port of SpareBonus"""
        return self._rolls[frame_index + 2]

    def _is_spare(self, frame_index: int) -> bool:
        """Port of IsSpare"""
        return self._rolls[frame_index] + self._rolls[frame_index + 1] == 10

    def _strike_bonus(self, frame_index: int) -> int:
        """Port of StrikeBonus"""
        return 10 + self._rolls[frame_index + 1] + self._rolls[frame_index + 2]
