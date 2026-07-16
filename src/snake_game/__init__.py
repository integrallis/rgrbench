"""Snake Game kata: deterministic snake engine on a walled grid.

`SnakeGame(width, height, food_positions)` runs snake on a rectangular
grid with walls on all four edges. Cells are ``(x, y)`` tuples with
``(0, 0)`` top-left, ``x`` increasing rightwards and ``y`` increasing
downwards. The snake starts at ``(0, 0)``, length 1, heading right.

Each `tick()` moves the head one cell in the current direction, then:

- onto food: the snake grows (tail stays), the score rises by 1, and
  the next food is placed;
- onto an empty cell: the tail follows the head;
- onto a wall or the snake's own body: the game ends. The cell being
  vacated by the tail this tick counts as empty. After game over,
  further ticks change nothing.

`change_direction(name)` accepts 'up', 'down', 'left', 'right';
a direct reversal of the current heading is ignored, and any other
string raises ValueError("unknown direction: ..."). Randomness is
injected: ``food_positions`` is an iterable of cells consumed in order,
one at a time; candidates lying on the snake are skipped, and when the
source is exhausted the board holds no food (``food`` is None) and the
snake keeps moving without growing. Exposed read-only state: ``snake``
(head-first cell list), ``direction``, ``food``, ``score``,
``game_over``. Non-positive grid dimensions raise ValueError.

Kata catalogued at tddbuddy.com/katas/snake-game; implementation and
tests original (MIT), machine-authored from the specification, 2026.
"""

from snake_game.game import SnakeGame

__all__ = ["SnakeGame"]
