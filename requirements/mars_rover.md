# Planetary rover command control

## Overview
A ground-control model of a rover exploring a rectangular planetary grid. The rover holds a location and a compass heading, executes strings of single-letter driving commands, and treats the map as the surface of a planet: driving off one edge re-enters on the opposite edge. Obstacles stop the rover in its tracks, and the blockage is reported as rover state rather than as a failure.

## User Stories

### US-1: Deployment
As a mission operator, I want to deploy the rover with a starting position, heading and grid, so that every mission starts from a known state.

- AC-1.1: The rover reports the location and heading it was deployed with.
- AC-1.2: Deployed without arguments, the rover starts at (0, 0) facing N on a 100 by 100 grid, with status "ok" and no obstacle on record.
- AC-1.3: Heading letters are case-insensitive: a lowercase letter is accepted and reported as its uppercase compass point.
- AC-1.4: An unknown heading letter is rejected with the exact message "Unknown direction: " followed by the offending letter.
- AC-1.5: A grid with a zero width or a zero height is rejected with the exact message "Grid dimensions must be positive".
- AC-1.6: A 1 by 1 grid is accepted.

### US-2: Driving
As a mission operator, I want to send the rover command strings, so that it drives across the surface.

- AC-2.1: The command f moves the rover one square forward in its facing direction; on the map, x grows eastward and y grows southward.
- AC-2.2: The command b moves the rover one square backward, opposite to its facing direction, without changing the heading.
- AC-2.3: A command string is executed sequentially, one letter at a time, each command acting on the state the previous one left.
- AC-2.4: Worked example: on a 100 by 100 grid, starting at (0, 0) facing S, the command string fflff ends at (2, 2) facing E.
- AC-2.5: An unknown command letter is rejected with the exact message "Unknown command: " followed by the offending letter.

### US-3: Turning
As a mission operator, I want turn commands, so that the rover changes heading in place.

- AC-3.1: The command l turns the rover 90 degrees counterclockwise, cycling N to W to S to E and back to N, without moving it.
- AC-3.2: The command r turns the rover 90 degrees clockwise, cycling N to E to S to W and back to N, without moving it.

### US-4: Edge wrapping
As a mission operator, I want the rover to wrap around the grid edges, so that the map behaves like the closed surface of a planet.

- AC-4.1: Moving off the top edge (y zero, heading N) re-enters at the bottom row (y equal to the grid height minus one).
- AC-4.2: Moving off the bottom edge (heading S) re-enters at the top row (y zero).
- AC-4.3: Moving off the right edge (x equal to the grid width minus one, heading E) re-enters at the left column (x zero).
- AC-4.4: Moving off the left edge (x zero, heading W) re-enters at the right column (x equal to the grid width minus one).
- AC-4.5: Backward moves wrap across edges the same way.
- AC-4.6: On a 1 by 1 grid, a forward move wraps onto the same square and the status stays "ok".

### US-5: Obstacles
As a mission operator, I want the rover to stop in front of obstacles and report them, so that the mission survives surprises on the surface.

- AC-5.1: A move whose destination holds an obstacle leaves the rover at its last valid position, sets its status to "blocked", and records the obstacle's coordinates as the last obstacle encountered.
- AC-5.2: The remainder of the command string after a blocked move is not executed: neither moves nor turns.
- AC-5.3: Driving into an obstacle raises no error; the outcome is carried entirely in the rover's state.
- AC-5.4: A run that passes near, but never into, obstacles finishes with status "ok" and no obstacle on record.
- AC-5.5: Destinations reached by wrapping across an edge are obstacle-checked like any other square.
- AC-5.6: Turning is never blocked by obstacles, even when the rover is surrounded.

## Traceability
```json
{
  "test_rover_reports_its_initial_state": ["AC-1.1"],
  "test_rover_defaults": ["AC-1.2"],
  "test_lowercase_direction_is_accepted": ["AC-1.3"],
  "test_invalid_direction_is_rejected": ["AC-1.4"],
  "test_forward_moves_one_square_in_the_facing_direction": ["AC-2.1"],
  "test_backward_moves_one_square_away_from_the_facing_direction": ["AC-2.2"],
  "test_turning_left_cycles_counterclockwise": ["AC-3.1"],
  "test_turning_right_cycles_clockwise": ["AC-3.2"],
  "test_specification_walkthrough_fflff": ["AC-2.4"],
  "test_commands_execute_sequentially": ["AC-2.3"],
  "test_moving_north_off_the_top_edge_wraps_to_the_bottom": ["AC-4.1"],
  "test_moving_south_off_the_bottom_edge_wraps_to_the_top": ["AC-4.2"],
  "test_moving_east_off_the_right_edge_wraps_to_the_left": ["AC-4.3"],
  "test_moving_west_off_the_left_edge_wraps_to_the_right": ["AC-4.4"],
  "test_backward_moves_also_wrap": ["AC-4.5"],
  "test_obstacle_stops_the_rover_at_the_last_valid_position": ["AC-5.1"],
  "test_obstacle_aborts_the_rest_of_the_command_string": ["AC-5.2"],
  "test_blocking_is_state_not_an_exception": ["AC-5.3"],
  "test_unblocked_run_keeps_status_ok": ["AC-5.4"],
  "test_obstacle_across_a_wrapped_edge_blocks_the_move": ["AC-5.5"],
  "test_turning_is_never_blocked_by_obstacles": ["AC-5.6"],
  "test_unknown_command_is_rejected": ["AC-2.5"],
  "test_grid_with_a_zero_dimension_is_rejected": ["AC-1.5"],
  "test_single_cell_grid_is_valid_and_wraps_onto_itself": ["AC-1.6", "AC-4.6"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
