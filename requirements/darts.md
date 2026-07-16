# Darts 301 scoring

## Overview
Scorekeeping for a game of 301 darts. The player starts at 301 points and subtracts each dart's value — face value, doubled, or tripled — across turns of three darts. The game is won by reaching exactly zero with a double; a dart that would leave exactly 1, take the score below zero, or reach zero without a double is a bust that cancels the whole turn.

## User Stories

### US-1: Start of game
As a darts player, I want a new game to begin at 301 with a fresh turn, so that play starts from the standard position.

- AC-1.1: A new game has a score of 301 and is not finished.
- AC-1.2: A new game is on turn 1 with 3 darts available.

### US-2: Scoring throws
As a darts player, I want each dart's value subtracted from my score, so that the score always shows what remains.

- AC-2.1: A plain dart subtracts its face value: 20 from 301 leaves 281.
- AC-2.2: A double subtracts twice the face value.
- AC-2.3: A triple subtracts three times the face value.

### US-3: Turns of three darts
As a darts player, I want play organised into turns of three darts, so that the game tracks whose dart is next.

- AC-3.1: The darts remaining decrease with each throw within a turn, and the third throw ends the turn: the game then reports the next turn number with 3 darts available again.

### US-4: Going bust
As a darts player, I want an unfinishable throw to void the turn, so that the checkout rules of 301 are enforced.

- AC-4.1: A dart that leaves a score of exactly 1 is a bust — even on the turn's final dart, since no double can finish from 1.
- AC-4.2: A dart that would take the score below zero is a bust.
- AC-4.3: A dart that reaches exactly zero without being a double is a bust.
- AC-4.4: A bust restores the score to its value at the start of the turn, ends the turn immediately — forfeiting any remaining darts — and leaves the game unfinished.

### US-5: Winning
As a darts player, I want the game to end when I check out correctly, so that victory is recognised.

- AC-5.1: Reaching exactly zero with a double finishes the game.

## Traceability
```json
{
  "test_game_starts_at_301": ["AC-1.1"],
  "test_normal_throw_scoring": ["AC-2.1"],
  "test_double_throw_scoring": ["AC-2.2"],
  "test_triple_throw_scoring": ["AC-2.3"],
  "test_turn_and_darts_counting_initially": ["AC-1.2"],
  "test_turn_and_darts_counting": ["AC-3.1"],
  "test_go_bust_reaching_1": ["AC-4.1", "AC-4.4"],
  "test_go_bust_below_zero": ["AC-4.2", "AC-4.4"],
  "test_complete_game_with_double": ["AC-5.1"],
  "test_reaching_zero_with_single_is_bust": ["AC-4.3", "AC-4.4"],
  "test_reaching_one_on_last_dart_is_also_bust": ["AC-4.1", "AC-4.4"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
