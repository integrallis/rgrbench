# Tic-tac-toe

## Overview
A two-player game of tic-tac-toe on a three-by-three board: X and O take turns marking blank squares, the game detects a win along any row, column or diagonal, and a full board with no winner is declared a draw.

## User Stories

### US-1: Start a fresh game
As a player, I want every new game to begin fresh, so that play always starts from the same fair position.

- AC-1.1: A new game presents a three-by-three board of blank squares, arranged as three rows of three; a blank square is shown as a single space.
- AC-1.2: X is the first player to move.

### US-2: Take turns marking squares
As a player, I want moves recorded on the board with turns alternating, so that both players get their go.

- AC-2.1: A move marks the chosen square — addressed by row and then column, counted from the top-left starting at zero — with the letter of the player whose turn it is.
- AC-2.2: After each move the turn passes to the other player, alternating X and O with X first.

### US-3: Win with three in a line
As a player, I want three of my marks in a line to win the game, so that the game ends with a victor.

- AC-3.1: Three matching marks across a row win the game for that player.
- AC-3.2: Three matching marks down a column win the game for that player.
- AC-3.3: Three matching marks along either diagonal win the game, no matter which square completes the line.

### US-4: End stalemates as draws
As a player, I want a full board with no winner declared a draw, so that stalemates end cleanly.

- AC-4.1: When every square is filled and no line is complete, the game reports no winner and declares a draw.
- AC-4.2: While open squares remain, the game is not a draw.

## Traceability
```json
{
  "test_new_game_has_empty_board": ["AC-1.1"],
  "test_x_plays_first": ["AC-1.2"],
  "test_can_place_x_on_board": ["AC-2.1"],
  "test_players_alternate_turns": ["AC-2.2"],
  "test_detect_horizontal_win": ["AC-3.1"],
  "test_detect_vertical_win": ["AC-3.2"],
  "test_detect_diagonal_win": ["AC-3.3"],
  "test_detect_anti_diagonal_win_completed_at_top_right": ["AC-3.3"],
  "test_detect_draw": ["AC-4.1", "AC-4.2"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
