"""Snake Game kata - deterministic snake engine on a walled grid.

Covers initial state, per-tick movement, direction changes and the
no-reversal rule, growth and scoring on food, injected food placement
(occupied cells skipped, exhausted source), wall and self collisions,
the vacated-tail exception, and the frozen state after game over.
"""


def test_initial_state() -> None:
    """Test 1: The snake starts at (0, 0), length 1, heading right

    Score is zero, the game is live, and the first injected food is on
    the board.
    """
    from snake_game import SnakeGame

    # GIVEN / WHEN
    game = SnakeGame(10, 10, [(5, 5)])

    # THEN
    assert game.snake == [(0, 0)]
    assert game.direction == "right"
    assert game.score == 0
    assert game.game_over is False
    assert game.food == (5, 5)


def test_initial_food_skips_the_snake_start_cell() -> None:
    """Test 2: Food never spawns on the snake, even at setup"""
    from snake_game import SnakeGame

    game = SnakeGame(10, 10, [(0, 0), (3, 3)])

    assert game.food == (3, 3)


def test_tick_moves_one_cell_right() -> None:
    """Test 3: One tick advances the head one cell in the current direction"""
    from snake_game import SnakeGame

    # GIVEN
    game = SnakeGame(10, 10, [(9, 9)])

    # WHEN
    game.tick()

    # THEN
    assert game.snake == [(1, 0)]


def test_successive_ticks_keep_moving() -> None:
    """Test 4: Each tick moves exactly one cell; length stays 1 off food"""
    from snake_game import SnakeGame

    game = SnakeGame(10, 10, [(9, 9)])

    game.tick()
    game.tick()
    game.tick()

    assert game.snake == [(3, 0)]
    assert game.score == 0


def test_change_direction_takes_effect_on_next_tick() -> None:
    """Test 5: A perpendicular direction change redirects movement"""
    from snake_game import SnakeGame

    # GIVEN
    game = SnakeGame(10, 10, [(9, 9)])
    game.tick()

    # WHEN
    game.change_direction("down")
    game.tick()

    # THEN
    assert game.snake == [(1, 1)]
    assert game.direction == "down"


def test_reversal_is_ignored() -> None:
    """Test 6: Moving right, a change to left is ignored"""
    from snake_game import SnakeGame

    game = SnakeGame(10, 10, [(9, 9)])

    game.change_direction("left")

    assert game.direction == "right"
    game.tick()
    assert game.snake == [(1, 0)]


def test_reversal_is_ignored_for_a_longer_snake() -> None:
    """Test 7: The no-reversal rule also protects a grown snake"""
    from snake_game import SnakeGame

    # GIVEN a snake of length 2 heading right
    game = SnakeGame(10, 10, [(1, 0)])
    game.tick()
    assert game.snake == [(1, 0), (0, 0)]

    # WHEN
    game.change_direction("left")
    game.tick()

    # THEN it kept going right instead of dying on its own body
    assert game.direction == "right"
    assert game.snake == [(2, 0), (1, 0)]
    assert game.game_over is False


def test_unknown_direction_is_rejected() -> None:
    """Test 8: An unrecognised direction name raises ValueError"""
    import pytest

    from snake_game import SnakeGame

    game = SnakeGame(10, 10, [(9, 9)])

    with pytest.raises(ValueError, match="unknown direction: 'north'"):
        game.change_direction("north")


def test_eating_food_grows_scores_and_spawns_next_food() -> None:
    """Test 9: Reaching food grows the snake by one and scores one point

    The tail stays put on the growth tick and the next injected food
    appears.
    """
    from snake_game import SnakeGame

    # GIVEN
    game = SnakeGame(10, 10, [(1, 0), (7, 7)])

    # WHEN
    game.tick()

    # THEN
    assert game.snake == [(1, 0), (0, 0)]
    assert game.score == 1
    assert game.food == (7, 7)


def test_each_food_eaten_adds_one_segment_and_one_point() -> None:
    """Test 10: Growth and score accumulate across several foods"""
    from snake_game import SnakeGame

    game = SnakeGame(10, 10, [(1, 0), (2, 0), (3, 0)])

    game.tick()
    game.tick()
    game.tick()

    assert game.snake == [(3, 0), (2, 0), (1, 0), (0, 0)]
    assert game.score == 3


def test_food_spawn_skips_cells_occupied_by_the_snake() -> None:
    """Test 11: Injected positions on the snake's body are passed over"""
    from snake_game import SnakeGame

    # GIVEN food at (1,0), then a candidate on the snake, then a free cell
    game = SnakeGame(10, 10, [(1, 0), (0, 0), (5, 5)])

    # WHEN the snake eats and occupies (1,0) and (0,0)
    game.tick()

    # THEN the occupied candidate was skipped
    assert game.snake == [(1, 0), (0, 0)]
    assert game.food == (5, 5)


def test_no_food_once_the_source_is_exhausted() -> None:
    """Test 12: An exhausted food source leaves the board foodless

    The snake keeps moving without growing.
    """
    from snake_game import SnakeGame

    game = SnakeGame(10, 10, [(1, 0)])
    game.tick()
    assert game.food is None

    game.tick()

    assert game.snake == [(2, 0), (1, 0)]
    assert game.score == 1


def test_hitting_the_right_wall_ends_the_game() -> None:
    """Test 13: Crossing the right edge is fatal; the fatal move is not applied"""
    from snake_game import SnakeGame

    # GIVEN a 3-wide grid
    game = SnakeGame(3, 3, [(2, 2)])
    game.tick()
    game.tick()
    assert game.snake == [(2, 0)]

    # WHEN
    game.tick()

    # THEN
    assert game.game_over is True
    assert game.snake == [(2, 0)]


def test_hitting_the_top_wall_ends_the_game() -> None:
    """Test 14: Moving up from row 0 is fatal"""
    from snake_game import SnakeGame

    game = SnakeGame(10, 10, [(9, 9)])
    game.change_direction("up")

    game.tick()

    assert game.game_over is True


def test_running_into_own_body_ends_the_game() -> None:
    """Test 15: The head touching a body segment is fatal

    Grow to length 5 along the top row, then hook back into the body
    with down, left, up.
    """
    from snake_game import SnakeGame

    # GIVEN a length-5 snake: (4,0)..(0,0)
    game = SnakeGame(10, 10, [(1, 0), (2, 0), (3, 0), (4, 0)])
    for _ in range(4):
        game.tick()
    assert game.snake == [(4, 0), (3, 0), (2, 0), (1, 0), (0, 0)]

    # WHEN hooking back into the body
    game.change_direction("down")
    game.tick()
    game.change_direction("left")
    game.tick()
    game.change_direction("up")
    game.tick()

    # THEN
    assert game.game_over is True


def test_moving_into_the_vacating_tail_cell_is_safe() -> None:
    """Test 16: The tail cell freed this tick does not kill the snake

    A length-4 snake circling a 2x2 block re-enters each tail cell just
    as it is vacated, so it can loop indefinitely.
    """
    from snake_game import SnakeGame

    # GIVEN a length-4 snake filling the 2x2 block at the origin
    game = SnakeGame(10, 10, [(1, 0), (1, 1), (0, 1)])
    game.tick()
    game.change_direction("down")
    game.tick()
    game.change_direction("left")
    game.tick()
    assert game.snake == [(0, 1), (1, 1), (1, 0), (0, 0)]

    # WHEN circling the block twice
    for _ in range(2):
        game.change_direction("up")
        game.tick()
        game.change_direction("right")
        game.tick()
        game.change_direction("down")
        game.tick()
        game.change_direction("left")
        game.tick()

    # THEN the snake is alive and intact
    assert game.game_over is False
    assert len(game.snake) == 4


def test_tick_after_game_over_changes_nothing() -> None:
    """Test 17: A finished game ignores further ticks"""
    from snake_game import SnakeGame

    # GIVEN a game ended on the top wall
    game = SnakeGame(10, 10, [(9, 9)])
    game.change_direction("up")
    game.tick()
    assert game.game_over is True
    frozen_snake = game.snake
    frozen_score = game.score

    # WHEN
    game.tick()

    # THEN
    assert game.game_over is True
    assert game.snake == frozen_snake
    assert game.score == frozen_score


def test_non_positive_grid_dimensions_are_rejected() -> None:
    """Test 18: A zero-width or zero-height grid raises ValueError"""
    import pytest

    from snake_game import SnakeGame

    with pytest.raises(ValueError, match=r"^grid dimensions must be positive$"):
        SnakeGame(0, 10, [])

    with pytest.raises(ValueError, match=r"^grid dimensions must be positive$"):
        SnakeGame(10, 0, [])


def test_single_cell_grid_is_accepted() -> None:
    """Test 19: A 1x1 grid is valid; the snake fills it and dies on the first tick"""
    from snake_game import SnakeGame

    # GIVEN the smallest legal grid
    game = SnakeGame(1, 1, [])
    assert game.snake == [(0, 0)]
    assert game.game_over is False

    # WHEN
    game.tick()

    # THEN the only possible move hits a wall
    assert game.game_over is True


def test_hitting_the_bottom_wall_ends_the_game() -> None:
    """Test 20: Crossing the bottom edge is fatal; the fatal move is not applied"""
    from snake_game import SnakeGame

    # GIVEN a 3-tall grid with the snake on the bottom row
    game = SnakeGame(3, 3, [(2, 2)])
    game.change_direction("down")
    game.tick()
    game.tick()
    assert game.snake == [(0, 2)]

    # WHEN
    game.tick()

    # THEN
    assert game.game_over is True
    assert game.snake == [(0, 2)]
