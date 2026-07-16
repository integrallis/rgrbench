"""Bingo card: 5x5 grid with a free centre, marking, and line detection."""

from collections.abc import Sequence

CARD_SIZE = 5
FREE_ROW = 2
FREE_COLUMN = 2
NUMBERS_PER_CARD = CARD_SIZE * CARD_SIZE - 1

COLUMN_RANGES: dict[str, range] = {
    "B": range(1, 16),
    "I": range(16, 31),
    "N": range(31, 46),
    "G": range(46, 61),
    "O": range(61, 76),
}

_COLUMN_LETTERS = "BINGO"


def column_letter(number: int) -> str:
    """Return the column letter (B, I, N, G, or O) for a called number."""
    for letter, valid in COLUMN_RANGES.items():
        if number in valid:
            return letter
    raise ValueError(f"number must be between 1 and 75, got {number}")


class BingoCard:
    """A 5x5 bingo card whose centre space is free (pre-marked).

    Numbers are supplied column-major: five for B, five for I, four for
    N (the centre space is free), five for G, and five for O. Each
    number must be unique and fall within its column's range.
    """

    def __init__(self, numbers: Sequence[int]) -> None:
        if len(numbers) != NUMBERS_PER_CARD:
            raise ValueError(
                f"card requires exactly {NUMBERS_PER_CARD} numbers, got {len(numbers)}"
            )
        if len(set(numbers)) != NUMBERS_PER_CARD:
            raise ValueError("card numbers must be unique")
        self._grid: list[list[int | None]] = [[None] * CARD_SIZE for _ in range(CARD_SIZE)]
        self._marked: list[list[bool]] = [[False] * CARD_SIZE for _ in range(CARD_SIZE)]
        self._marked[FREE_ROW][FREE_COLUMN] = True
        self._positions: dict[int, tuple[int, int]] = {}
        remaining = iter(numbers)
        for column, letter in enumerate(_COLUMN_LETTERS):
            for row in range(CARD_SIZE):
                if row == FREE_ROW and column == FREE_COLUMN:
                    continue
                number = next(remaining)
                if number not in COLUMN_RANGES[letter]:
                    raise ValueError(f"{number} is not valid for column {letter}")
                self._grid[row][column] = number
                self._positions[number] = (row, column)

    def number_at(self, row: int, column: int) -> int | None:
        """Return the number at a grid position, or None for the free space."""
        return self._grid[row][column]

    def is_marked(self, row: int, column: int) -> bool:
        """Return whether the space at a grid position is marked."""
        return self._marked[row][column]

    def mark(self, number: int) -> bool:
        """Mark a called number; return whether the number is on this card.

        Called numbers must be between 1 and 75.
        """
        if not 1 <= number <= 75:
            raise ValueError(f"number must be between 1 and 75, got {number}")
        position = self._positions.get(number)
        if position is None:
            return False
        row, column = position
        self._marked[row][column] = True
        return True

    def has_bingo(self) -> bool:
        """Return whether any row, column, or main diagonal is fully marked."""
        columns = [
            [self._marked[row][column] for row in range(CARD_SIZE)]
            for column in range(CARD_SIZE)
        ]
        diagonal = [self._marked[index][index] for index in range(CARD_SIZE)]
        anti_diagonal = [
            self._marked[index][CARD_SIZE - 1 - index] for index in range(CARD_SIZE)
        ]
        lines = [*self._marked, *columns, diagonal, anti_diagonal]
        return any(all(line) for line in lines)
