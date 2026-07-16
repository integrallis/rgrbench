"""Maze walker kata.

A maze arrives as string art: '#' or '*' cells are walls, spaces and '.' are
corridors, and exactly one 'S' and one 'E' mark the start and the exit. The
walker explores with breadth-first search, moving only up, down, left or
right - never diagonally - and reports the shortest route as the list of
(x, y) coordinates visited from start to exit inclusive, where x is the
column and y is the row counted from the top-left corner. When the exit
cannot be reached a NoPathError is raised; malformed mazes (missing or
duplicated markers, unknown characters) are rejected with ValueError at
parse time.

Kata catalogued at tddbuddy.com/katas/maze-walker; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from __future__ import annotations

from collections import deque

_WALL_CHARS = frozenset("#*")
_OPEN_CHARS = frozenset(" .")

Coordinate = tuple[int, int]


class NoPathError(Exception):
    """Raised when no route exists from the start to the exit."""


class Maze:
    """A parsed grid maze with a single start and a single exit."""

    def __init__(
        self,
        open_cells: frozenset[Coordinate],
        start: Coordinate,
        exit: Coordinate,
        width: int,
        height: int,
    ) -> None:
        self._open_cells = open_cells
        self.start = start
        self.exit = exit
        self.width = width
        self.height = height

    @classmethod
    def from_text(cls, text: str) -> Maze:
        """Parse a maze from string art (see module docstring for the legend)."""
        lines = text.strip("\n").splitlines()
        open_cells: set[Coordinate] = set()
        start: Coordinate | None = None
        exit_: Coordinate | None = None
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char in _WALL_CHARS:
                    continue
                if char in _OPEN_CHARS:
                    open_cells.add((x, y))
                elif char == "S":
                    if start is not None:
                        raise ValueError("Maze must contain exactly one start 'S'")
                    start = (x, y)
                    open_cells.add((x, y))
                elif char == "E":
                    if exit_ is not None:
                        raise ValueError("Maze must contain exactly one exit 'E'")
                    exit_ = (x, y)
                    open_cells.add((x, y))
                else:
                    raise ValueError(f"Unknown maze character: {char!r}")
        if start is None:
            raise ValueError("Maze must contain exactly one start 'S'")
        if exit_ is None:
            raise ValueError("Maze must contain exactly one exit 'E'")
        width = max(len(line) for line in lines)
        return cls(frozenset(open_cells), start, exit_, width, len(lines))

    def is_open(self, x: int, y: int) -> bool:
        """Return True when (x, y) is a corridor, start or exit cell."""
        return (x, y) in self._open_cells


class MazeWalker:
    """Finds the shortest orthogonal route through a maze via BFS."""

    def __init__(self, maze: Maze) -> None:
        self._maze = maze

    def walk(self) -> list[Coordinate]:
        """Return the shortest path from start to exit, both inclusive.

        Raises NoPathError when the exit is unreachable.
        """
        maze = self._maze
        start, goal = maze.start, maze.exit
        came_from: dict[Coordinate, Coordinate | None] = {start: None}
        frontier: deque[Coordinate] = deque([start])
        while frontier:
            current = frontier.popleft()
            if current == goal:
                break
            x, y = current
            for neighbor in ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)):
                if neighbor not in came_from and maze.is_open(*neighbor):
                    came_from[neighbor] = current
                    frontier.append(neighbor)
        if goal not in came_from:
            raise NoPathError("No path to exit")
        path: list[Coordinate] = [goal]
        while (previous := came_from[path[-1]]) is not None:
            path.append(previous)
        path.reverse()
        return path


def walk_maze(text: str) -> list[Coordinate]:
    """Parse ``text`` and return the shortest path through it."""
    return MazeWalker(Maze.from_text(text)).walk()
