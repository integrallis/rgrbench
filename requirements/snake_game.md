# Deterministic snake arcade engine

## Overview
An engine for the classic snake arcade game on a walled rectangular grid, built to be fully deterministic. Cells are addressed as column-and-row pairs with (0, 0) at the top left: moving right increases the column and moving down increases the row. The game reports the snake as the cells it occupies, head first, alongside its current heading, the score, whether the game has ended, and where the food is. Food locations are supplied up front as a sequence rather than drawn at random, and time advances only through explicit ticks, so every run is reproducible.

## User Stories

### US-1: Starting a game on a valid grid
As a player, I want a fresh game to begin in a known state on a sensible grid, so that every run starts the same way.

- AC-1.1: A new game has a one-segment snake at (0, 0) heading "right", a score of zero, and is not over, with the first supplied food on the board.
- AC-1.2: Grids must have positive width and height, rejected otherwise with the exact message "grid dimensions must be positive"; a one-by-one grid is legal — the snake fills it, and the first tick is fatal.

### US-2: Steering the snake tick by tick
As a player, I want the snake to advance one cell per tick in a direction I control, so that movement is predictable.

- AC-2.1: Each tick advances the head exactly one cell in the current heading; away from food, the snake's length is unchanged as the tail follows.
- AC-2.2: A heading change to "up", "down", "left", or "right" takes effect on the next tick.
- AC-2.3: A change directly opposite the current heading is ignored, whatever the snake's length: the snake keeps its heading and keeps moving.
- AC-2.4: An unrecognized heading name is rejected with an error naming it in quotes, as in "unknown direction: 'north'".

### US-3: Eating food, growing, and scoring
As a player, I want eating food to grow the snake and raise my score, so that progress is rewarded.

- AC-3.1: Food appears at the next position in the supplied sequence, skipping any position currently occupied by the snake — including at setup.
- AC-3.2: When the head reaches the food, the snake grows by one segment — the tail stays put on that tick — the score rises by one, and the next food appears.
- AC-3.3: Growth and score accumulate: every food eaten adds one segment and one point.
- AC-3.4: Once the supplied food positions run out, the board holds no food and the snake keeps moving without growing.

### US-4: Ending the game on collisions
As a player, I want clear and final death rules, so that the game ends fairly and stays ended.

- AC-4.1: Moving past any edge of the grid ends the game, and the fatal move is not applied — the snake stays where it was.
- AC-4.2: The head moving into a cell occupied by the snake's own body ends the game.
- AC-4.3: The tail cell being vacated on the same tick is safe to enter, so a snake can chase its own tail in a loop indefinitely.
- AC-4.4: Once the game is over, further ticks change nothing: the snake, the score, and the game-over state stay frozen.

## Traceability
```json
{
  "test_initial_state": ["AC-1.1"],
  "test_initial_food_skips_the_snake_start_cell": ["AC-3.1"],
  "test_tick_moves_one_cell_right": ["AC-2.1"],
  "test_successive_ticks_keep_moving": ["AC-2.1"],
  "test_change_direction_takes_effect_on_next_tick": ["AC-2.2"],
  "test_reversal_is_ignored": ["AC-2.3"],
  "test_reversal_is_ignored_for_a_longer_snake": ["AC-2.3"],
  "test_unknown_direction_is_rejected": ["AC-2.4"],
  "test_eating_food_grows_scores_and_spawns_next_food": ["AC-3.2"],
  "test_each_food_eaten_adds_one_segment_and_one_point": ["AC-3.3"],
  "test_food_spawn_skips_cells_occupied_by_the_snake": ["AC-3.1"],
  "test_no_food_once_the_source_is_exhausted": ["AC-3.4"],
  "test_hitting_the_right_wall_ends_the_game": ["AC-4.1"],
  "test_hitting_the_top_wall_ends_the_game": ["AC-4.1"],
  "test_running_into_own_body_ends_the_game": ["AC-4.2"],
  "test_moving_into_the_vacating_tail_cell_is_safe": ["AC-4.3"],
  "test_tick_after_game_over_changes_nothing": ["AC-4.4"],
  "test_non_positive_grid_dimensions_are_rejected": ["AC-1.2"],
  "test_single_cell_grid_is_accepted": ["AC-1.2", "AC-4.1"],
  "test_hitting_the_bottom_wall_ends_the_game": ["AC-4.1"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
