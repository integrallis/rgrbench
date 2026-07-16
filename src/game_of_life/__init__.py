"""Game of Life kata.

Simulate Conway's cellular automaton: cells on a plane are alive or dead, and
each generation is computed from the previous one by four rules applied to
every cell at once. A live cell with fewer than two live neighbours dies
(underpopulation); a live cell with two or three live neighbours survives; a
live cell with more than three live neighbours dies (overpopulation); a dead
cell with exactly three live neighbours becomes alive (reproduction). The
plane is unbounded — cells beyond any pattern are dead — which sidesteps
border questions. The grid supports construction from coordinate sets or text
rows, generation stepping, neighbour counting, and a textual rendering of any
rectangular window.

Kata catalogued at tddbuddy.com/katas/game-of-life; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from game_of_life.game_of_life import Cell, Grid

__all__ = ["Cell", "Grid"]
