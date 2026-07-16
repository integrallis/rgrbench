# Guard patrol map tracing

## Overview
A puzzle solver that reads a text map of a patrolled area and traces a guard's walk. The map arrives as lines of single-character cells: open ground is a dot, obstructions are hash marks, and a guard facing up is drawn as a caret. The solver parses the map into a grid, locates the guard, reports where the guard steps next, and produces a copy of the map with every cell the guard visited marked with an X.

## User Stories

### US-1: Parse the map text into a grid
As a puzzle solver, I want the raw map text turned into a grid of cells, so that positions can be addressed by row and column.

- AC-1.1: Each line of the input becomes one grid row, and each character of the line becomes one single-character cell, in order (worked example: a four-line map of dots and hash marks becomes a four-row grid of those characters).
- AC-1.2: Rows are split on newlines only; every other character, including spaces, is kept as its own cell.

### US-2: Locate the guard
As a puzzle solver, I want to find the guard's starting position on the grid, so that the walk can be traced from the right place.

- AC-2.1: The guard's position is reported as a row-and-column pair (row first, zero-based), wherever the caret cell sits — top row, bottom row, or anywhere between.
- AC-2.2: When no guard appears on the grid, the position report is empty.

### US-3: Trace the guard's walk
As a puzzle solver, I want a marked-up copy of the grid showing every cell the guard visited, so that the patrol coverage is visible.

- AC-3.1: The guard walks straight up from its starting cell to the top edge of the grid; every cell it occupies along the way, including the starting cell, is replaced with "X" in the result (worked examples: a guard on the top row yields a single X at its own cell; a guard on the bottom row of a two-row grid yields an X in its column on both rows).
- AC-3.2: When the grid has no guard, the traced grid is identical to the input grid.

### US-4: Report the guard's next location
As a puzzle solver, I want to know the next location on the guard's walk, so that the patrol can be stepped through incrementally.

- AC-4.1: For the worked example grid whose guard sits on the top row at column 2, the next-location report is row 0, column 2, given as a row-and-column pair.

## Traceability
```json
{
  "test_parse_grid_from_input": ["AC-1.1"],
  "test_parse_grid_splits_rows_on_newlines_only": ["AC-1.2"],
  "test_find_guard_position_bottom_row": ["AC-2.1"],
  "test_find_guard_position_top_row": ["AC-2.1"],
  "test_find_guard_position_not_found": ["AC-2.2"],
  "test_calculate_path_top_row": ["AC-3.1"],
  "test_calculate_path_bottom_row": ["AC-3.1"],
  "test_calculate_path_no_guard": ["AC-3.2"],
  "test_calculate_next_location": ["AC-4.1"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
