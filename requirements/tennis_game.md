# Tennis game scoring

## Overview
Scorekeeping for a single game of tennis between two players: points are announced with the traditional call names (0, 15, 30, 40), a game is won by scoring beyond 40 while ahead, and games tied at 40 follow the deuce-and-advantage rules until one player leads by two points.

## User Stories

### US-1: Announce points with tennis call names
As a scoreboard operator, I want point counts announced with the traditional call names, so that scores read the way tennis is spoken.

- AC-1.1: The first four point counts are announced as "0", "15", "30" and "40" for zero, one, two and three points respectively.

### US-2: Follow the score as it grows
As a spectator, I want each player's announced score to grow as they win points, so that I can follow the game.

- AC-2.1: A new game starts with both players announced at "0".
- AC-2.2: When a player wins a point, that player's announced score advances to the next call name while the opponent's announcement is unchanged.

### US-3: Declare the winner at the right moment
As a chair umpire, I want the game to declare its winner at the right moment, so that play ends correctly.

- AC-3.1: The game reports no winner while neither player has scored more than three points.
- AC-3.2: A player on "40" who wins the next point wins the game — provided the game is not tied at "40" — and the game reports whether player 1 or player 2 won.

### US-4: Resolve deuce with advantage
As a chair umpire, I want games tied at "40" resolved by a two-point lead, so that the deuce rule is honoured.

- AC-4.1: When both players are on "40", the next point gives the scorer advantage, announced as "A" while the opponent stays at "40"; the game still has no winner.
- AC-4.2: If the player without advantage wins a point, the game returns to deuce and both players are announced at "40" again, however many times this repeats.
- AC-4.3: A player holding advantage who wins the next point wins the game, having achieved the two-point lead.
- AC-4.4: A player on "40" whose opponent is on "0" is announced as "40", never as advantage.

## Traceability
```json
{
  "test_score_names_zero": ["AC-1.1"],
  "test_score_names_fifteen": ["AC-1.1"],
  "test_score_names_thirty": ["AC-1.1"],
  "test_score_names_forty": ["AC-1.1"],
  "test_set_initialization": ["AC-2.1"],
  "test_score_grows": ["AC-2.2"],
  "test_player1_wins_at_40": ["AC-3.1", "AC-3.2"],
  "test_player2_wins_at_40": ["AC-3.1", "AC-3.2"],
  "test_deuce_requires_two_point_lead": ["AC-4.1", "AC-4.3"],
  "test_return_to_deuce_from_advantage": ["AC-4.2"],
  "test_advantage_score_display": ["AC-4.1"],
  "test_forty_love_is_not_advantage": ["AC-4.4"],
  "test_love_forty_is_not_advantage": ["AC-4.4"],
  "test_player2_advantage_from_deuce": ["AC-4.1"],
  "test_player2_wins_from_advantage": ["AC-4.3"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
