"""Grid-based snake game engine with injected food positions."""

from collections.abc import Iterable, Iterator

_DIRECTIONS: dict[str, tuple[int, int]] = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}
_OPPOSITES: dict[str, str] = {
    "up": "down",
    "down": "up",
    "left": "right",
    "right": "left",
}


class SnakeGame:
    """Snake on a walled grid, advanced one cell per :meth:`tick`.

    Coordinates are ``(x, y)`` with ``(0, 0)`` the top-left cell, ``x``
    growing rightwards and ``y`` growing downwards. Food placement is
    driven by the injected ``food_positions`` source; candidates that
    fall on the snake are skipped, and an exhausted source leaves the
    board without food.
    """

    def __init__(
        self,
        width: int,
        height: int,
        food_positions: Iterable[tuple[int, int]],
    ) -> None:
        if width < 1 or height < 1:
            raise ValueError("grid dimensions must be positive")
        self._width = width
        self._height = height
        self._food_source: Iterator[tuple[int, int]] = iter(food_positions)
        self._snake: list[tuple[int, int]] = [(0, 0)]
        self._direction = "right"
        self._score = 0
        self._game_over = False
        self._food = self._spawn_food()

    @property
    def snake(self) -> list[tuple[int, int]]:
        """Occupied cells, head first."""
        return list(self._snake)

    @property
    def direction(self) -> str:
        return self._direction

    @property
    def food(self) -> tuple[int, int] | None:
        return self._food

    @property
    def score(self) -> int:
        return self._score

    @property
    def game_over(self) -> bool:
        return self._game_over

    def change_direction(self, direction: str) -> None:
        """Set the heading for subsequent ticks; reversals are ignored."""
        if direction not in _DIRECTIONS:
            raise ValueError(f"unknown direction: {direction!r}")
        if direction == _OPPOSITES[self._direction]:
            return
        self._direction = direction

    def tick(self) -> None:
        """Advance one cell; grow on food, die on wall or body contact.

        Once the game is over, further ticks leave the state unchanged.
        """
        if self._game_over:
            return
        delta_x, delta_y = _DIRECTIONS[self._direction]
        head_x, head_y = self._snake[0]
        new_head = (head_x + delta_x, head_y + delta_y)
        if not (0 <= new_head[0] < self._width and 0 <= new_head[1] < self._height):
            self._game_over = True
            return
        growing = new_head == self._food
        body = self._snake if growing else self._snake[:-1]
        if new_head in body:
            self._game_over = True
            return
        self._snake.insert(0, new_head)
        if growing:
            self._score += 1
            self._food = self._spawn_food()
        else:
            self._snake.pop()

    def _spawn_food(self) -> tuple[int, int] | None:
        for position in self._food_source:
            if position not in self._snake:
                return position
        return None
