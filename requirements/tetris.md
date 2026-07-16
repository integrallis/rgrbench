# Falling-blocks puzzle board

## Overview
The playing field of a falling-blocks puzzle. Single blocks and multi-block pieces are dropped onto a rectangular board, descend one row per timed tick, can be steered sideways and rotated while falling, and become part of the settled landscape when they land. The board renders its state as rows of text so the game can be displayed.

## User Stories

### US-1: See the board
As a player, I want the board drawn as rows of text, so that I can see the state of play.

- AC-1.1: The board is a rectangle of the width and height it was created with; every cell of an empty board shows as a dot.
- AC-1.2: The board renders one text row per board row, each row ending with a line break (a fresh 3-by-3 board renders as three rows of "...").

### US-2: Drop single blocks that fall and land
As a player, I want a dropped block to appear at the top middle and fall one row per tick until it lands, so that gravity behaves predictably.

- AC-2.1: A new board has nothing falling.
- AC-2.2: Dropping a block puts it in play as the falling block, shown by its letter.
- AC-2.3: A dropped block appears in the top row at the middle column (on a 3-wide board the second column; on a 6-wide board the fourth).
- AC-2.4: Each tick moves the falling block down exactly one row.
- AC-2.5: A block that has reached the bottom row is still falling; on the following tick it stops where it is and nothing is falling any more.
- AC-2.6: Only one block or piece may fall at a time; dropping another while one is falling is refused with the message exactly "already falling".
- AC-2.7: A falling block stops and settles on top of a landed block rather than passing through it.

### US-3: Define pieces by their shape
As a game designer, I want multi-block pieces described by shape drawings that can be rotated, so that the classic tetrominoes are supported.

- AC-3.1: A piece is defined by a multi-row shape drawing and renders exactly as that drawing.
- AC-3.2: Rotating a piece to the right or to the left turns its drawing 90 degrees in that direction (worked example: rotating the drawing with rows ".X.", ".X.", "..." right gives rows "...", ".XX", "..."; rotating it left gives "...", "XX.", "...").
- AC-3.3: The stock T-shape renders as the rows ".T.", "TTT", "...".
- AC-3.4: A tetromino built from a shape drawing keeps and renders that shape.

### US-4: Play whole pieces on the board
As a player, I want whole pieces to drop, fall and land just like blocks, so that the game plays with the full shapes.

- AC-4.1: A dropped piece appears at the top of the board, horizontally centred; when the free space cannot split evenly the piece sits one column right of exact centre (on a 6-wide board the T-shape's top rows read "...T.." and "..TTT."; on a 7-wide board, "....T.." and "...TTT.").
- AC-4.2: A falling piece descends one row per tick.
- AC-4.3: A piece lands when it can fall no further, keeping its shape and position — including when it has been steered up against a side wall.
- AC-4.4: A falling piece stops and settles on top of previously landed material instead of overlapping it.
- AC-4.5: Single blocks and multi-block pieces can be dropped onto the same board in succession, and each falls and lands by the same rules.
- AC-4.6: Empty cells in a falling piece's drawing are transparent: landed blocks behind them stay visible.
- AC-4.7: A piece with no room to fall at all lands immediately in its starting rows.
- AC-4.8: Piece cells that would lie beyond the board's right edge or below its bottom are clipped — never shown and never landed.

### US-5: Steer the falling piece
As a player, I want to nudge the falling piece left and right, so that I can position it before it lands.

- AC-5.1: Moving left or right shifts the falling piece one column in that direction.
- AC-5.2: Nothing can move past the side boundaries; a move that would cross an edge does nothing.
- AC-5.3: Single falling blocks can be steered left and right just like pieces.
- AC-5.4: When nothing is falling, move and rotate commands leave the board untouched.

### US-6: Rotate the falling piece
As a player, I want to rotate the falling piece in either direction, so that I can orient it before it lands.

- AC-6.1: The falling piece can be rotated clockwise or counter-clockwise in place on the board.
- AC-6.2: If the rotated piece would not fit — blocked by a boundary or by landed material — the rotation is abandoned and the board is unchanged.
- AC-6.3: Rotating a single plain block changes nothing, and the block keeps falling.

## Traceability
```json
{
  "test_new_board_is_empty": ["AC-1.1", "AC-1.2"],
  "test_board_with_different_dimensions": ["AC-1.1"],
  "test_new_board_has_no_falling_blocks": ["AC-2.1"],
  "test_when_block_is_dropped_it_is_falling": ["AC-2.2"],
  "test_block_starts_from_top_middle": ["AC-2.3"],
  "test_block_moves_down_one_row_per_tick": ["AC-2.4"],
  "test_at_most_one_block_falling_at_a_time": ["AC-2.6"],
  "test_block_is_still_falling_on_last_row": ["AC-2.5"],
  "test_block_stops_when_hits_bottom": ["AC-2.5"],
  "test_block_lands_on_another_block": ["AC-2.7"],
  "test_piece_consists_of_many_blocks": ["AC-3.1"],
  "test_piece_can_be_rotated_right": ["AC-3.2"],
  "test_piece_can_be_rotated_left": ["AC-3.2"],
  "test_t_shape_tetromino": ["AC-3.3"],
  "test_when_piece_is_dropped_board_has_3x3_blocks": ["AC-4.1"],
  "test_piece_falls_with_tick": ["AC-4.2"],
  "test_piece_lands_on_bottom": ["AC-4.3"],
  "test_piece_collision_check": ["AC-4.4"],
  "test_board_handles_both_blocks_and_pieces": ["AC-4.5"],
  "test_can_move_piece_left": ["AC-5.1"],
  "test_can_move_piece_right": ["AC-5.1"],
  "test_piece_cannot_move_past_boundaries": ["AC-5.2"],
  "test_can_rotate_falling_piece": ["AC-6.1"],
  "test_piece_cannot_rotate_if_blocked": ["AC-6.2"],
  "test_dropping_on_falling_block_reports_already_falling": ["AC-2.6"],
  "test_block_starts_from_top_middle_of_wider_board": ["AC-2.3"],
  "test_piece_starts_from_top_middle_of_odd_width_board": ["AC-4.1"],
  "test_block_can_be_moved_left": ["AC-5.3"],
  "test_block_can_be_moved_right": ["AC-5.3"],
  "test_block_cannot_move_left_past_boundary": ["AC-5.2", "AC-5.3"],
  "test_block_cannot_move_right_past_boundary": ["AC-5.2", "AC-5.3"],
  "test_single_block_cannot_be_rotated": ["AC-6.3"],
  "test_falling_piece_does_not_hide_landed_blocks": ["AC-4.6"],
  "test_piece_lands_at_top_when_no_room_to_fall": ["AC-4.7"],
  "test_piece_lands_against_left_wall": ["AC-4.3"],
  "test_piece_overhanging_right_edge_is_clipped": ["AC-4.8"],
  "test_piece_overhanging_bottom_is_clipped": ["AC-4.8"],
  "test_tetromino_keeps_its_given_shape": ["AC-3.4"],
  "test_can_rotate_falling_piece_counter_clockwise": ["AC-6.1"],
  "test_piece_cannot_rotate_left_if_blocked": ["AC-6.2"],
  "test_rotate_left_ignores_single_block": ["AC-6.3"],
  "test_moves_on_empty_board_are_no_ops": ["AC-5.4"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
