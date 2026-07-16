# Conway's Game of Life on an unbounded plane

## Overview
A cellular-automaton world on an unbounded two-dimensional plane. Each cell is either
alive or dead; the world advances in discrete generations under Conway's rules of
underpopulation, survival, overpopulation, and reproduction. Worlds are immutable values:
stepping produces a new world, worlds compare equal by their live cells, and patterns can
be exchanged with a textual notation where "*" marks a live cell and "." a dead one.

## User Stories

### US-1: Evolve the world by Conway's rules
As a simulation user, I want each generation computed by the classic life rules, so that populations evolve as Conway defined.

- AC-1.1: A live cell with fewer than two live neighbours dies of underpopulation.
- AC-1.2: A live cell with two or three live neighbours survives into the next generation.
- AC-1.3: A live cell with more than three live neighbours dies of overpopulation.
- AC-1.4: A dead cell with exactly three live neighbours becomes alive; two live neighbours are not enough for reproduction.
- AC-1.5: An empty world stays empty: nothing is ever born from no live cells.
- AC-1.6: A cell's neighbourhood is exactly the eight surrounding cells, including the diagonals.

### US-2: Watch classic patterns behave canonically
As a Life enthusiast, I want the well-known patterns to behave as documented, so that I can trust the simulation.

- AC-2.1: Still lifes — the two-by-two block and the beehive — reproduce themselves exactly, generation after generation.
- AC-2.2: The blinker (a line of three) alternates between vertical and horizontal, returning to its original shape after two generations.
- AC-2.3: The toad changes shape after one generation and returns to its original shape after two.
- AC-2.4: The glider translates itself diagonally by one cell every four generations.

### US-3: Read and write patterns as text
As a user, I want to describe patterns as rows of text and print any region of the plane, so that I can set up and inspect worlds visually.

- AC-3.1: A world can be built from rows of text in which "*" marks a live cell and "." a dead one; rows run down the vertical axis and columns across the horizontal axis.
- AC-3.2: A rectangular window of the plane, anchored at the origin with a given width and height, renders as text rows using "*" for live cells and "." for dead cells.
- AC-3.3: A pattern built from rows of text renders back to exactly those rows.

### US-4: Treat worlds as immutable values on an unbounded plane
As a developer, I want worlds to behave as immutable values, so that generations can be compared, stored, and shared safely.

- AC-4.1: A world created with no cells has a population of zero and an empty set of live cells.
- AC-4.2: Advancing a generation returns a new world and leaves the original world's live cells untouched.
- AC-4.3: The plane is unbounded and defaults to dead: any coordinate arbitrarily far from every pattern reports a dead cell.
- AC-4.4: Two worlds with the same live cells are equal and hash alike, regardless of the order in which their cells were listed.
- AC-4.5: Hashing depends on the set of live cells, so distinct worlds do not all collide on one hash.
- AC-4.6: The number of live neighbours can be queried for any coordinate, whether that cell is live, adjacent to the pattern, or far away.

## Traceability
```json
{
  "test_empty_grid_has_no_live_cells": ["AC-4.1"],
  "test_empty_grid_stays_empty": ["AC-1.5"],
  "test_lone_cell_dies_of_underpopulation": ["AC-1.1"],
  "test_pair_of_cells_dies_of_underpopulation": ["AC-1.1"],
  "test_live_cell_with_two_neighbours_survives": ["AC-1.2"],
  "test_live_cell_with_three_neighbours_survives": ["AC-1.2"],
  "test_live_cell_with_four_neighbours_dies_of_overpopulation": ["AC-1.3"],
  "test_dead_cell_with_three_neighbours_is_born": ["AC-1.4"],
  "test_dead_cell_with_two_neighbours_stays_dead": ["AC-1.4"],
  "test_block_still_life_is_stable": ["AC-2.1"],
  "test_beehive_still_life_is_stable": ["AC-2.1"],
  "test_blinker_flips_from_vertical_to_horizontal": ["AC-2.2"],
  "test_blinker_oscillates_with_period_two": ["AC-2.2"],
  "test_toad_oscillates_with_period_two": ["AC-2.3"],
  "test_glider_translates_diagonally_every_four_generations": ["AC-2.4"],
  "test_from_rows_builds_grid_from_text_pattern": ["AC-3.1"],
  "test_render_displays_window_of_the_plane": ["AC-3.2"],
  "test_render_round_trips_with_from_rows": ["AC-3.3"],
  "test_next_generation_does_not_mutate_original_grid": ["AC-4.2"],
  "test_live_neighbours_counts_all_eight_surrounding_cells": ["AC-1.6", "AC-4.6"],
  "test_cells_far_from_any_pattern_are_dead": ["AC-4.3"],
  "test_grids_with_same_cells_are_equal_and_hash_alike": ["AC-4.4"],
  "test_hash_varies_with_the_live_cell_set": ["AC-4.5"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
