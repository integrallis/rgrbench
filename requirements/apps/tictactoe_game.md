# Tic-tac-toe game web service

## Overview
An HTTP service hosting tic-tac-toe games. Clients create games, submit moves by board
position, and fetch game state over a JSON API. The service tracks whose turn it is,
rejects illegal moves, and detects wins and draws. It also reports its own health.

## User Stories

### US-1: Service health
As an operator, I want a health endpoint, so that I can verify the service is up.

- AC-1.1: A health request succeeds and reports the service as healthy.

### US-2: Play a game
As a player, I want to create a game and make moves, so that two players can play on a shared board.

- AC-2.1: Creating a game returns a created status with a numeric identifier (numbered from 1), an in-progress status, X as the current player, and an empty nine-cell board.
- AC-2.2: Submitting a move by position marks that cell for the current player (X moves first) and returns the updated state, with the turn passing to the other player.
- AC-2.3: A move to an occupied position is rejected as a bad request.
- AC-2.4: A game can be fetched by its identifier, returning its current state.

### US-3: Game resolution
As a player, I want the service to recognize the end of the game, so that results are announced.

- AC-3.1: Three in a row across a row wins for the player who completed it, and the game status reports the win.
- AC-3.2: A full board with no winner is reported as a draw.

## Traceability
```json
{
  "test_health_check_returns_200": ["AC-1.1"],
  "test_create_new_game": ["AC-2.1"],
  "test_make_move_in_game": ["AC-2.2"],
  "test_move_to_occupied_position_returns_400": ["AC-2.3"],
  "test_get_game_by_id": ["AC-2.4"],
  "test_win_detection_horizontal": ["AC-3.1"],
  "test_draw_detection": ["AC-3.2"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
