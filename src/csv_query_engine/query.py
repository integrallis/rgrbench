"""Chainable query pipeline over CSV text held in memory."""

import csv
import io
from collections.abc import Callable

_OPERATORS = ("=", "!=", ">", "<", ">=", "<=")
_DIRECTIONS = ("asc", "desc")


class UnknownColumnError(Exception):
    """Raised when a query references a column absent from the header."""


def _as_number(value: object) -> float | None:
    """Return the numeric value of a cell or comparison value, if any."""
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value))
    except ValueError:
        return None


def _matches(cell: str, operator: str, value: str | int | float) -> bool:
    """Compare a cell against a value, numerically when both sides are numeric."""
    cell_number = _as_number(cell)
    value_number = _as_number(value)
    left: float | str
    right: float | str
    if cell_number is not None and value_number is not None:
        left, right = cell_number, value_number
    else:
        left, right = cell, str(value)
    if operator == "=":
        return left == right
    if operator == "!=":
        return left != right
    if operator == ">":
        return left > right
    if operator == "<":
        return left < right
    if operator == ">=":
        return left >= right
    return left <= right


class CsvQuery:
    """A chainable, immutable query over CSV text.

    Each operation returns a new query; operations are applied in the
    order they are called.
    """

    def __init__(self, csv_text: str) -> None:
        parsed = [row for row in csv.reader(io.StringIO(csv_text)) if row]
        if not parsed:
            raise ValueError("CSV text must include a header row")
        self._columns: list[str] = list(parsed[0])
        self._rows: list[dict[str, str]] = [
            dict(zip(self._columns, row)) for row in parsed[1:]
        ]

    @classmethod
    def _from_state(cls, columns: list[str], rows: list[dict[str, str]]) -> "CsvQuery":
        query = cls.__new__(cls)
        query._columns = columns
        query._rows = rows
        return query

    def _require_column(self, column: str) -> None:
        if column not in self._columns:
            raise UnknownColumnError(f"unknown column: {column}")

    def select(self, *columns: str) -> "CsvQuery":
        """Restrict result rows to the named columns, in the order given."""
        for column in columns:
            self._require_column(column)
        projected = [{column: row[column] for column in columns} for row in self._rows]
        return CsvQuery._from_state(list(columns), projected)

    def where(self, column: str, operator: str, value: str | int | float) -> "CsvQuery":
        """Keep rows whose column satisfies the operator against the value."""
        self._require_column(column)
        if operator not in _OPERATORS:
            raise ValueError(f"unknown operator: {operator}")
        matching = [row for row in self._rows if _matches(row[column], operator, value)]
        return CsvQuery._from_state(self._columns, matching)

    def order_by(self, column: str, direction: str = "asc") -> "CsvQuery":
        """Sort rows by a column, ascending or descending, with a stable sort."""
        self._require_column(column)
        if direction not in _DIRECTIONS:
            raise ValueError(f"direction must be 'asc' or 'desc', got {direction!r}")
        numeric = all(_as_number(row[column]) is not None for row in self._rows)
        key: Callable[[dict[str, str]], float | str]
        if numeric:
            key = lambda row: float(row[column])  # noqa: E731
        else:
            key = lambda row: row[column]  # noqa: E731
        ordered = sorted(self._rows, key=key, reverse=direction == "desc")
        return CsvQuery._from_state(self._columns, ordered)

    def limit(self, n: int) -> "CsvQuery":
        """Keep only the first n rows of the current result."""
        if n < 0:
            raise ValueError(f"limit must be non-negative, got {n}")
        return CsvQuery._from_state(self._columns, self._rows[:n])

    def rows(self) -> list[dict[str, str]]:
        """Return the result rows as dictionaries keyed by column name."""
        return [dict(row) for row in self._rows]

    def count(self) -> int:
        """Return the number of rows in the current result."""
        return len(self._rows)
