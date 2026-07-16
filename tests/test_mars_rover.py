"""
Tests for the Mars Rover kata (tddbuddy.com/katas/mars-rover).
Coordinates: x grows eastward, y grows southward. Commands: f/b/l/r.
Edges wrap; obstacles block moves and are reported as rover state.
"""

import pytest


def test_rover_reports_its_initial_state() -> None:
    """Test 1: The constructor sets location and direction"""
    from mars_rover import MarsRover

    rover = MarsRover((3, 4), "E", (50, 50))

    assert rover.location == (3, 4)
    assert rover.direction == "E"


def test_rover_defaults() -> None:
    """Test 2: Defaults are (0, 0) facing N on a 100x100 grid with status ok"""
    from mars_rover import MarsRover

    rover = MarsRover()

    assert rover.location == (0, 0)
    assert rover.direction == "N"
    assert rover.status == "ok"
    assert rover.last_obstacle is None


def test_lowercase_direction_is_accepted() -> None:
    """Test 3: Direction letters are case-insensitive ('e' == 'E')"""
    from mars_rover import MarsRover

    assert MarsRover((0, 0), "e", (50, 50)).direction == "E"


def test_invalid_direction_is_rejected() -> None:
    """Test 4: An unknown direction letter raises ValueError naming the culprit"""
    from mars_rover import MarsRover

    with pytest.raises(ValueError, match=r"^Unknown direction: Q$"):
        MarsRover((0, 0), "Q", (50, 50))


@pytest.mark.parametrize(
    "direction,expected_location",
    [("N", (5, 4)), ("S", (5, 6)), ("E", (6, 5)), ("W", (4, 5))],
)
def test_forward_moves_one_square_in_the_facing_direction(
    direction: str, expected_location: tuple[int, int]
) -> None:
    """Test 5: 'f' advances one square toward the current heading"""
    from mars_rover import MarsRover

    rover = MarsRover((5, 5), direction, (100, 100))
    rover.execute("f")

    assert rover.location == expected_location


@pytest.mark.parametrize(
    "direction,expected_location",
    [("N", (5, 6)), ("S", (5, 4)), ("E", (4, 5)), ("W", (6, 5))],
)
def test_backward_moves_one_square_away_from_the_facing_direction(
    direction: str, expected_location: tuple[int, int]
) -> None:
    """Test 6: 'b' retreats one square opposite to the current heading"""
    from mars_rover import MarsRover

    rover = MarsRover((5, 5), direction, (100, 100))
    rover.execute("b")

    assert rover.location == expected_location


def test_turning_left_cycles_counterclockwise() -> None:
    """Test 7: 'l' cycles N -> W -> S -> E -> N without moving"""
    from mars_rover import MarsRover

    rover = MarsRover((5, 5), "N", (100, 100))
    headings = []
    for _ in range(4):
        rover.execute("l")
        headings.append(rover.direction)

    assert headings == ["W", "S", "E", "N"]
    assert rover.location == (5, 5)


def test_turning_right_cycles_clockwise() -> None:
    """Test 8: 'r' cycles N -> E -> S -> W -> N without moving"""
    from mars_rover import MarsRover

    rover = MarsRover((5, 5), "N", (100, 100))
    headings = []
    for _ in range(4):
        rover.execute("r")
        headings.append(rover.direction)

    assert headings == ["E", "S", "W", "N"]
    assert rover.location == (5, 5)


def test_specification_walkthrough_fflff() -> None:
    """Test 9: On 100x100 from (0,0) facing S, 'fflff' ends at (2,2) (spec example)"""
    from mars_rover import MarsRover

    rover = MarsRover((0, 0), "S", (100, 100))
    rover.execute("fflff")

    assert rover.location == (2, 2)
    assert rover.direction == "E"


def test_commands_execute_sequentially() -> None:
    """Test 10: A command string is applied in order"""
    from mars_rover import MarsRover

    rover = MarsRover((0, 0), "E", (100, 100))
    rover.execute("ffrff")

    assert rover.location == (2, 2)
    assert rover.direction == "S"


def test_moving_north_off_the_top_edge_wraps_to_the_bottom() -> None:
    """Test 11: Forward off y=0 heading N wraps to y=height-1"""
    from mars_rover import MarsRover

    rover = MarsRover((0, 0), "N", (100, 100))
    rover.execute("f")

    assert rover.location == (0, 99)


def test_moving_south_off_the_bottom_edge_wraps_to_the_top() -> None:
    """Test 12: Forward off y=height-1 heading S wraps to y=0"""
    from mars_rover import MarsRover

    rover = MarsRover((0, 99), "S", (100, 100))
    rover.execute("f")

    assert rover.location == (0, 0)


def test_moving_east_off_the_right_edge_wraps_to_the_left() -> None:
    """Test 13: Forward off x=width-1 heading E wraps to x=0"""
    from mars_rover import MarsRover

    rover = MarsRover((49, 10), "E", (50, 50))
    rover.execute("f")

    assert rover.location == (0, 10)


def test_moving_west_off_the_left_edge_wraps_to_the_right() -> None:
    """Test 14: Forward off x=0 heading W wraps to x=width-1"""
    from mars_rover import MarsRover

    rover = MarsRover((0, 10), "W", (50, 50))
    rover.execute("f")

    assert rover.location == (49, 10)


def test_backward_moves_also_wrap() -> None:
    """Test 15: Backing off an edge wraps to the opposite side"""
    from mars_rover import MarsRover

    rover = MarsRover((0, 0), "S", (100, 100))
    rover.execute("b")

    assert rover.location == (0, 99)


def test_obstacle_stops_the_rover_at_the_last_valid_position() -> None:
    """Test 16: A blocked move leaves the rover in place and reports the obstacle"""
    from mars_rover import MarsRover

    rover = MarsRover((0, 0), "S", (100, 100), obstacles=[(0, 2)])
    rover.execute("ff")

    assert rover.location == (0, 1)
    assert rover.status == "blocked"
    assert rover.last_obstacle == (0, 2)


def test_obstacle_aborts_the_rest_of_the_command_string() -> None:
    """Test 17: Commands after the blocked move are not executed"""
    from mars_rover import MarsRover

    rover = MarsRover((0, 0), "S", (100, 100), obstacles=[(0, 1)])
    rover.execute("fflff")

    assert rover.location == (0, 0)
    assert rover.direction == "S"
    assert rover.status == "blocked"
    assert rover.last_obstacle == (0, 1)


def test_blocking_is_state_not_an_exception() -> None:
    """Test 18: Driving into an obstacle raises nothing; status carries the outcome"""
    from mars_rover import MarsRover

    rover = MarsRover((0, 0), "E", (10, 10), obstacles=[(1, 0)])
    rover.execute("f")

    assert rover.status == "blocked"


def test_unblocked_run_keeps_status_ok() -> None:
    """Test 19: Passing near (not into) an obstacle leaves status ok"""
    from mars_rover import MarsRover

    rover = MarsRover((0, 0), "S", (100, 100), obstacles=[(1, 1)])
    rover.execute("ff")

    assert rover.location == (0, 2)
    assert rover.status == "ok"
    assert rover.last_obstacle is None


def test_obstacle_across_a_wrapped_edge_blocks_the_move() -> None:
    """Test 20: Wrapping destinations are obstacle-checked too"""
    from mars_rover import MarsRover

    rover = MarsRover((0, 0), "N", (100, 100), obstacles=[(0, 99)])
    rover.execute("f")

    assert rover.location == (0, 0)
    assert rover.status == "blocked"
    assert rover.last_obstacle == (0, 99)


def test_turning_is_never_blocked_by_obstacles() -> None:
    """Test 21: 'l' and 'r' succeed even when surrounded by obstacles"""
    from mars_rover import MarsRover

    rover = MarsRover((5, 5), "N", (10, 10), obstacles=[(5, 4), (5, 6), (4, 5), (6, 5)])
    rover.execute("lr")

    assert rover.direction == "N"
    assert rover.status == "ok"


def test_unknown_command_is_rejected() -> None:
    """Test 22: An unknown command letter raises ValueError naming the culprit"""
    from mars_rover import MarsRover

    rover = MarsRover()

    with pytest.raises(ValueError, match=r"^Unknown command: x$"):
        rover.execute("x")


@pytest.mark.parametrize("grid_size", [(0, 10), (10, 0)])
def test_grid_with_a_zero_dimension_is_rejected(grid_size: tuple[int, int]) -> None:
    """Test 23: A zero width or zero height grid raises ValueError"""
    from mars_rover import MarsRover

    with pytest.raises(ValueError, match=r"^Grid dimensions must be positive$"):
        MarsRover((0, 0), "N", grid_size)


def test_single_cell_grid_is_valid_and_wraps_onto_itself() -> None:
    """Test 24: A 1x1 grid is accepted; driving forward wraps onto the same square"""
    from mars_rover import MarsRover

    rover = MarsRover((0, 0), "N", (1, 1))
    rover.execute("f")

    assert rover.location == (0, 0)
    assert rover.status == "ok"
