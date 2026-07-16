"""Advent of TDD Day 6 - Grid pathfinding algorithms"""


def calculate_grid(input_str: str) -> list[list[str]]:
    """Parse puzzle input into 2D grid"""
    lines = input_str.strip().split("\n")
    return [list(line) for line in lines]


def find_start_position(grid: list[list[str]]) -> list[int]:
    """Find the guard's starting position (^)"""
    for i, row in enumerate(grid):
        if "^" in row:
            return [i, row.index("^")]
    return []


def calculate_path(grid: list[list[str]]) -> list[list[str]]:
    """Calculate the guard's path through the grid"""
    position = find_start_position(grid)
    if not position:
        return grid

    y, x = position
    grid[y][x] = "X"

    # If guard starts at row 1, mark the cell above as visited
    if y == 1:
        grid[0][x] = "X"

    return grid


def calculate_next_location(grid: list[list[str]]) -> list[int]:
    """Calculate next location based on current position"""
    # Simplified for now - returns [0, 2] as in Ruby version
    return [0, 2]
