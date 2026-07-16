# Maze solving from text art

## Overview
A solver for mazes drawn as text art. Walls are drawn with hash or asterisk characters, corridors with spaces or dots, and the drawing marks exactly one start and one exit. The solver validates and parses the drawing, then returns the shortest walkable route from start to exit as a sequence of grid coordinates — or reports that no route exists.

## User Stories

### US-1: Reading the drawing
As a puzzle setter, I want maze drawings validated and parsed, so that only well-formed mazes are ever walked.

- AC-1.1: The drawing legend: # and * are walls, space and . are open corridor cells, S marks the start and E marks the exit.
- AC-1.2: The parsed maze reports its width and height, the coordinates of the start and of the exit, and whether any given cell is open or walled.
- AC-1.3: Coordinates are (x, y) pairs: x counts columns from the left edge and y counts rows from the top, both starting at zero.
- AC-1.4: A drawing without exactly one start — whether the start is missing or appears twice — is rejected with the exact message "Maze must contain exactly one start 'S'".
- AC-1.5: A drawing without exactly one exit — missing or duplicated — is rejected with the exact message "Maze must contain exactly one exit 'E'".
- AC-1.6: Any character outside the legend, anywhere in the drawing including its edges and corners, is rejected with a message containing "Unknown maze character".
- AC-1.7: Blank lines surrounding the drawing are dropped, but spaces at the start of a line are kept as corridor cells at their original coordinates.

### US-2: Walking the shortest route
As a puzzle solver, I want the shortest route from start to exit, so that the maze is traversed efficiently.

- AC-2.1: The route is returned as the full sequence of visited cell coordinates, beginning with the start cell and ending with the exit cell.
- AC-2.2: A start directly beside the exit yields a route of exactly two coordinates.
- AC-2.3: Consecutive coordinates on the route differ by exactly one square horizontally or vertically — never diagonally.
- AC-2.4: The route follows corridors wherever they lead: around corners, around dividing walls, and upward as well as downward.
- AC-2.5: When several routes exist, the route returned is the shortest one.
- AC-2.6: Dot corridor cells are walked exactly like space cells.

### US-3: Unreachable exits
As a puzzle solver, I want a clear signal when the exit cannot be reached, so that impossible mazes are not walked forever.

- AC-3.1: A walled-off exit raises a no-path error with the exact message "No path to exit".
- AC-3.2: Cells touching only at a corner are not connected: an exit adjacent to the start only diagonally is unreachable.
- AC-3.3: Both wall characters block movement: a corridor closed by either # or * makes the exit unreachable.

## Traceability
```json
{
  "test_straight_corridor_path": ["AC-2.1"],
  "test_start_next_to_exit_gives_a_two_cell_path": ["AC-2.2"],
  "test_dots_are_corridors_too": ["AC-2.6"],
  "test_l_shaped_path_turns_a_corner": ["AC-2.4"],
  "test_walker_takes_the_shortest_of_two_routes": ["AC-2.5"],
  "test_walker_navigates_around_a_dividing_wall": ["AC-2.4"],
  "test_every_step_is_orthogonal_and_path_spans_start_to_exit": ["AC-2.1", "AC-2.3"],
  "test_walled_off_exit_raises_no_path_error": ["AC-3.1"],
  "test_diagonal_adjacency_is_not_a_connection": ["AC-3.2"],
  "test_asterisks_are_walls_too": ["AC-1.1", "AC-3.3"],
  "test_parsed_maze_exposes_dimensions_start_and_exit": ["AC-1.2", "AC-1.3"],
  "test_maze_without_a_start_is_rejected": ["AC-1.4"],
  "test_maze_without_an_exit_is_rejected": ["AC-1.5"],
  "test_maze_with_two_starts_is_rejected": ["AC-1.4"],
  "test_maze_with_two_exits_is_rejected": ["AC-1.5"],
  "test_unknown_maze_characters_are_rejected": ["AC-1.6"],
  "test_walker_climbs_upward_toward_an_exit_above_the_start": ["AC-2.4"],
  "test_only_surrounding_newlines_are_trimmed_not_spaces": ["AC-1.7"],
  "test_unknown_characters_at_the_text_edges_are_rejected": ["AC-1.6"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
