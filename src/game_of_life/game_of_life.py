"""Conway's Game of Life on an unbounded plane.

The grid is immutable: ``next_generation`` returns a new ``Grid`` and leaves
the original untouched. Live cells are stored as a set of ``(x, y)``
coordinates, so the plane has no borders — every cell outside the live set is
simply dead.
"""

from collections.abc import Iterable, Sequence

Cell = tuple[int, int]

_NEIGHBOUR_OFFSETS: tuple[Cell, ...] = (
    (-1, -1),
    (0, -1),
    (1, -1),
    (-1, 0),
    (1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
)


class Grid:
    """An immutable Game of Life grid on an unbounded plane."""

    def __init__(self, live_cells: Iterable[Cell] = ()) -> None:
        """Create a grid from an iterable of live ``(x, y)`` coordinates."""
        self._live: frozenset[Cell] = frozenset(live_cells)

    @classmethod
    def from_rows(cls, rows: Sequence[str], alive: str = "*") -> "Grid":
        """Build a grid from strings; ``alive`` marks live cells.

        Row index maps to ``y`` and column index to ``x``, so ``rows[0][2]``
        is the cell at ``(2, 0)``.
        """
        cells = {
            (x, y)
            for y, row in enumerate(rows)
            for x, char in enumerate(row)
            if char == alive
        }
        return cls(cells)

    @property
    def live_cells(self) -> frozenset[Cell]:
        """The set of live cell coordinates."""
        return self._live

    @property
    def population(self) -> int:
        """Number of live cells."""
        return len(self._live)

    def is_alive(self, x: int, y: int) -> bool:
        """Whether the cell at ``(x, y)`` is alive."""
        return (x, y) in self._live

    def live_neighbours(self, x: int, y: int) -> int:
        """Number of live cells among the eight neighbours of ``(x, y)``."""
        return sum(
            (x + dx, y + dy) in self._live for dx, dy in _NEIGHBOUR_OFFSETS
        )

    def next_generation(self) -> "Grid":
        """Apply the four rules simultaneously and return the next grid.

        A live cell survives with two or three live neighbours; a dead cell
        with exactly three live neighbours becomes alive; every other cell is
        dead in the next generation.
        """
        neighbour_counts: dict[Cell, int] = {}
        for x, y in self._live:
            for dx, dy in _NEIGHBOUR_OFFSETS:
                cell = (x + dx, y + dy)
                neighbour_counts[cell] = neighbour_counts.get(cell, 0) + 1
        survivors_and_births = {
            cell
            for cell, count in neighbour_counts.items()
            if count == 3 or (count == 2 and cell in self._live)
        }
        return Grid(survivors_and_births)

    def render(self, width: int, height: int, alive: str = "*", dead: str = ".") -> str:
        """Render the window ``0 <= x < width, 0 <= y < height`` as text."""
        return "\n".join(
            "".join(
                alive if (x, y) in self._live else dead for x in range(width)
            )
            for y in range(height)
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Grid):
            return NotImplemented
        return self._live == other._live

    def __hash__(self) -> int:
        return hash(self._live)

    def __repr__(self) -> str:
        return f"Grid({sorted(self._live)!r})"
