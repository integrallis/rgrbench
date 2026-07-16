"""Tennis Game - Tennis scoring system implementation"""


class Scores:
    """Manages score names in tennis"""

    def score_name(self, points: int) -> str:
        """Return the tennis score name for given points"""
        score_map = {0: "0", 1: "15", 2: "30", 3: "40"}
        return score_map.get(points, "0")


class Set:
    """Represents a tennis set"""

    def __init__(self) -> None:
        """Initialize a new tennis set"""
        self.first_points = 0
        self.second_points = 0
        self.scores = Scores()

    def first_score(self) -> str:
        """Get the first player's score"""
        # Handle deuce and advantage
        if self.first_points >= 3 and self.second_points >= 3:
            if self.first_points == self.second_points:
                return "40"
            elif self.first_points > self.second_points:
                return "A"
            else:
                return "40"
        return self.scores.score_name(self.first_points)

    def second_score(self) -> str:
        """Get the second player's score"""
        # Handle deuce and advantage
        if self.first_points >= 3 and self.second_points >= 3:
            if self.first_points == self.second_points:
                return "40"
            elif self.second_points > self.first_points:
                return "A"
            else:
                return "40"
        return self.scores.score_name(self.second_points)

    def first_scores(self, times: int = 1) -> None:
        """First player scores a point"""
        self.first_points += times

    def second_scores(self, times: int = 1) -> None:
        """Second player scores a point"""
        self.second_points += times

    def winner(self) -> int | None:
        """Determine if there's a winner"""
        if self.first_points >= 4 and self.first_points - self.second_points >= 2:
            return 1
        if self.second_points >= 4 and self.second_points - self.first_points >= 2:
            return 2
        return None
