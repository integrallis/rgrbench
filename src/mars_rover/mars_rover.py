"""Mars Rover kata.

A rover lands on a rectangular planet grid at a starting coordinate, facing
one of the compass points N/E/S/W. The grid uses screen-style coordinates: x
grows eastward and y grows southward, so a rover at (0, 0) facing south that
drives forward twice, turns left and drives forward twice again ends at
(2, 2). Commands arrive as a string of single letters - f (forward), b
(backward), l (turn left), r (turn right) - executed in order. Driving off an
edge wraps around to the opposite side of the grid, planets being spheres.
Known obstacle coordinates may be supplied up front: before every move the
destination square is checked, and when it holds an obstacle the rover stays
on its last valid square, abandons the rest of the command string, and reports
the encounter through its status ("blocked") and last_obstacle state instead
of raising an exception. Turning is never blocked. Direction letters are
accepted case-insensitively; unknown directions or commands raise ValueError.

Kata catalogued at tddbuddy.com/katas/mars-rover; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from __future__ import annotations

from collections.abc import Iterable

_HEADINGS = "NESW"  # clockwise order
_VECTORS: dict[str, tuple[int, int]] = {
    "N": (0, -1),
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0),
}

STATUS_OK = "ok"
STATUS_BLOCKED = "blocked"


class MarsRover:
    """A rover that drives, turns, wraps at grid edges and detects obstacles."""

    def __init__(
        self,
        location: tuple[int, int] = (0, 0),
        direction: str = "N",
        grid_size: tuple[int, int] = (100, 100),
        obstacles: Iterable[tuple[int, int]] | None = None,
    ) -> None:
        heading = direction.upper()
        if heading not in _VECTORS:
            raise ValueError(f"Unknown direction: {direction}")
        width, height = grid_size
        if width <= 0 or height <= 0:
            raise ValueError("Grid dimensions must be positive")
        self._x, self._y = location
        self._heading = heading
        self._width = width
        self._height = height
        self._obstacles = frozenset(
            (x, y) for x, y in (obstacles if obstacles is not None else ())
        )
        self._status = STATUS_OK
        self._last_obstacle: tuple[int, int] | None = None

    @property
    def location(self) -> tuple[int, int]:
        """Current (x, y) position on the grid."""
        return (self._x, self._y)

    @property
    def direction(self) -> str:
        """Current heading, one of N/E/S/W."""
        return self._heading

    @property
    def status(self) -> str:
        """Either "ok" or "blocked" (an obstacle stopped the last drive)."""
        return self._status

    @property
    def last_obstacle(self) -> tuple[int, int] | None:
        """Coordinates of the obstacle that blocked the rover, if any."""
        return self._last_obstacle

    def execute(self, commands: str) -> None:
        """Run a command string; stops early if an obstacle blocks a move."""
        for command in commands:
            if self._status == STATUS_BLOCKED:
                return
            self._apply(command)

    def _apply(self, command: str) -> None:
        if command == "f":
            self._move(1)
        elif command == "b":
            self._move(-1)
        elif command == "l":
            self._turn(-1)
        elif command == "r":
            self._turn(1)
        else:
            raise ValueError(f"Unknown command: {command}")

    def _turn(self, step: int) -> None:
        index = _HEADINGS.index(self._heading)
        self._heading = _HEADINGS[(index + step) % len(_HEADINGS)]

    def _move(self, sign: int) -> None:
        dx, dy = _VECTORS[self._heading]
        destination = (
            (self._x + sign * dx) % self._width,
            (self._y + sign * dy) % self._height,
        )
        if destination in self._obstacles:
            self._status = STATUS_BLOCKED
            self._last_obstacle = destination
            return
        self._x, self._y = destination
