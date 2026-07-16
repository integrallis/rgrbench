# Minesweeper field hints

## Overview
A minesweeper-style playing field is laid out as a rectangular grid of cells. Mines are
placed on chosen cells, and every cell can then be asked for a hint: mined cells announce
themselves with a special marker, while safe cells report how many mines surround them.

## User Stories

### US-1: Laying out a field
As a puzzle setter, I want to create a rectangular field of a chosen width and height and place mines on individual cells, so that a minesweeper board can be prepared for play.

- AC-1.1: A field is created with a given width and height; cells are addressed by
  zero-based column and row positions, with the origin at the top-left corner.
- AC-1.2: In a field where no mine has been placed, every cell reports a hint of 0.

### US-2: Recognising mined cells
As a player, I want a cell that holds a mine to be reported with a distinct mine marker, so that mined cells are never confused with safe cells.

- AC-2.1: A cell on which a mine has been placed reports the mine marker value -1 in
  place of a neighbour count.
- AC-2.2: When every cell of the field is mined, every cell reports the mine marker.

### US-3: Counting neighbouring mines
As a player, I want each safe cell to report the number of mines around it, so that I can reason about where the mines are.

- AC-3.1: A mine-free cell reports the count of mines in its adjacent cells, where
  adjacency includes horizontal, vertical, and diagonal neighbours.
- AC-3.2: In a 2-by-2 field every cell is adjacent to every other cell, so with one mine
  each of the three remaining cells reports 1, with two mines each remaining cell reports
  2, and with three mines the one remaining cell reports 3.
- AC-3.3: A cell with no mine in any adjacent cell reports 0 even when the field contains
  mines elsewhere.
- AC-3.4: Worked 3-by-3 example: with mines on the two leftmost cells of the top row, the
  remaining top-row cell reports 1, the middle row reports 2, 2, 1, and the bottom row
  reports 0, 0, 0.

## Traceability
```json
{
  "test_build_field_size_of_one_by_one_and_zero_mine": ["AC-1.2"],
  "test_build_field_size_of_one_by_one_and_one_mine": ["AC-2.1"],
  "test_build_two_by_two_field_and_one_of_mine_topleftcorner": ["AC-1.1", "AC-2.1", "AC-3.2"],
  "test_build_two_by_two_field_and_one_of_mine_bottomrightcorner": ["AC-1.1", "AC-2.1", "AC-3.2"],
  "test_build_two_by_two_field_and_one_of_mine_bottomleftcorner": ["AC-1.1", "AC-2.1", "AC-3.2"],
  "test_build_two_by_two_field_and_one_of_mine_toprightcorner": ["AC-1.1", "AC-2.1", "AC-3.2"],
  "test_build_two_by_two_field_and_two_of_mine": ["AC-2.1", "AC-3.2"],
  "test_build_two_by_two_field_and_three_of_mine": ["AC-2.1", "AC-3.2"],
  "test_build_two_by_two_field_and_four_of_mine": ["AC-2.2"],
  "test_build_three_by_three_field_and_two_of_mine": ["AC-3.1", "AC-3.3", "AC-3.4"],
  "test_build_three_by_three_field_and_three_of_mine": ["AC-2.1", "AC-3.1"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
