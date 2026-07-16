"""Advent of TDD Day 6 - Grid Pathfinding
Porting from Ruby implementation
"""


def test_parse_grid_from_input() -> None:
    """Test 1: Parse puzzle input into 2D grid"""
    from advent_day6.pathfinding import calculate_grid

    input_str = "....#\n.....\n.....\n.#..."
    expected = [
        [".", ".", ".", ".", "#"],
        [".", ".", ".", ".", "."],
        [".", ".", ".", ".", "."],
        [".", "#", ".", ".", "."],
    ]
    assert calculate_grid(input_str) == expected


def test_parse_grid_splits_rows_on_newlines_only() -> None:
    """Test 1b: Rows are split on newlines only - each line is one grid row"""
    from advent_day6.pathfinding import calculate_grid

    input_str = ". .#\n.^ ."
    expected = [
        [".", " ", ".", "#"],
        [".", "^", " ", "."],
    ]
    assert calculate_grid(input_str) == expected


def test_find_guard_position_bottom_row() -> None:
    """Test 2: Find guard position in bottom row"""
    from advent_day6.pathfinding import find_start_position

    grid = [[".", ".", ".", ".", "."], [".", "#", "^", ".", "."]]
    assert find_start_position(grid) == [1, 2]


def test_find_guard_position_top_row() -> None:
    """Test 3: Find guard position in top row"""
    from advent_day6.pathfinding import find_start_position

    grid = [[".", ".", "^", ".", "."], [".", "#", ".", ".", "."]]
    assert find_start_position(grid) == [0, 2]


def test_find_guard_position_not_found() -> None:
    """Test 4: Return empty when guard not found"""
    from advent_day6.pathfinding import find_start_position

    grid = [[".", ".", ".", ".", "."], [".", "#", ".", ".", "."]]
    assert find_start_position(grid) == []


def test_calculate_path_top_row() -> None:
    """Test 5: Calculate path with guard in top row"""
    from advent_day6.pathfinding import calculate_path

    grid = [[".", ".", "^", ".", "."], [".", "#", ".", ".", "."]]
    expected = [[".", ".", "X", ".", "."], [".", "#", ".", ".", "."]]
    assert calculate_path(grid) == expected


def test_calculate_path_bottom_row() -> None:
    """Test 6: Calculate path with guard in bottom row"""
    from advent_day6.pathfinding import calculate_path

    grid = [[".", ".", ".", ".", "."], [".", "#", "^", ".", "."]]
    expected = [[".", ".", "X", ".", "."], [".", "#", "X", ".", "."]]
    assert calculate_path(grid) == expected


def test_calculate_path_no_guard() -> None:
    """Test 7: Calculate path when no guard exists"""
    from advent_day6.pathfinding import calculate_path

    grid = [[".", ".", ".", ".", "."], [".", "#", ".", ".", "."]]
    expected = [[".", ".", ".", ".", "."], [".", "#", ".", ".", "."]]
    assert calculate_path(grid) == expected


def test_calculate_next_location() -> None:
    """Test 8: Calculate next location based on current position"""
    from advent_day6.pathfinding import calculate_next_location

    grid = [[".", ".", "^", ".", "."], [".", "#", ".", ".", "."]]
    assert calculate_next_location(grid) == [0, 2]
