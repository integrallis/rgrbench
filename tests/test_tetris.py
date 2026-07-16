"""Tetris - Step-by-step TDD Tutorial
Ported from Java implementation by Esko Luontola
"""


def test_new_board_is_empty() -> None:
    """Test 1: A new board is empty"""
    from tetris.board import Board

    board = Board(3, 3)
    assert str(board) == "...\n...\n...\n"


def test_board_with_different_dimensions() -> None:
    """Test 2: Board respects given dimensions"""
    from tetris.board import Board

    board = Board(4, 2)
    assert str(board) == "....\n....\n"


def test_new_board_has_no_falling_blocks() -> None:
    """Test 3: A new board has no falling blocks"""
    from tetris.board import Board

    board = Board(3, 3)
    assert board.has_falling() is False


def test_when_block_is_dropped_it_is_falling() -> None:
    """Test 4: When a block is dropped, the block is falling"""
    from tetris.block import Block
    from tetris.board import Board

    board = Board(3, 3)
    board.drop(Block("X"))
    assert board.has_falling() is True


def test_block_starts_from_top_middle() -> None:
    """Test 5: Block starts from the top middle"""
    from tetris.block import Block
    from tetris.board import Board

    board = Board(3, 3)
    board.drop(Block("X"))
    assert str(board) == ".X.\n...\n...\n"


def test_block_moves_down_one_row_per_tick() -> None:
    """Test 6: Block moves down one row per tick"""
    from tetris.block import Block
    from tetris.board import Board

    board = Board(3, 3)
    board.drop(Block("X"))
    board.tick()
    assert str(board) == "...\n.X.\n...\n"


def test_at_most_one_block_falling_at_a_time() -> None:
    """Test 7: At most one block may be falling at a time"""
    import pytest

    from tetris.block import Block
    from tetris.board import Board

    board = Board(3, 3)
    board.drop(Block("X"))
    with pytest.raises(ValueError, match="already falling"):
        board.drop(Block("Y"))


def test_block_is_still_falling_on_last_row() -> None:
    """Test 8: Block is still falling on the last row"""
    from tetris.block import Block
    from tetris.board import Board

    board = Board(3, 3)
    board.drop(Block("X"))
    board.tick()
    board.tick()
    assert str(board) == "...\n...\n.X.\n"
    assert board.has_falling() is True


def test_block_stops_when_hits_bottom() -> None:
    """Test 9: Block stops when it hits the bottom"""
    from tetris.block import Block
    from tetris.board import Board

    board = Board(3, 3)
    board.drop(Block("X"))
    board.tick()
    board.tick()
    board.tick()
    assert str(board) == "...\n...\n.X.\n"
    assert board.has_falling() is False


def test_block_lands_on_another_block() -> None:
    """Test 10: Block lands on another block"""
    from tetris.block import Block
    from tetris.board import Board

    board = Board(3, 3)
    board.drop(Block("X"))
    board.tick()
    board.tick()
    board.tick()
    assert board.has_falling() is False

    board.drop(Block("Y"))
    board.tick()
    board.tick()
    assert str(board) == "...\n.Y.\n.X.\n"
    assert board.has_falling() is False


def test_piece_consists_of_many_blocks() -> None:
    """Test 11: A piece consists of many blocks"""
    from tetris.piece import Piece

    piece = Piece(".X.\n.X.\n...\n")
    assert str(piece) == ".X.\n.X.\n...\n"


def test_piece_can_be_rotated_right() -> None:
    """Test 12: Piece can be rotated right"""
    from tetris.piece import Piece

    piece = Piece(".X.\n.X.\n...\n")
    piece = piece.rotate_right()
    assert str(piece) == "...\n.XX\n...\n"


def test_piece_can_be_rotated_left() -> None:
    """Test 13: Piece can be rotated left"""
    from tetris.piece import Piece

    piece = Piece(".X.\n.X.\n...\n")
    piece = piece.rotate_left()
    assert str(piece) == "...\nXX.\n...\n"


def test_t_shape_tetromino() -> None:
    """Test 14: The T-shape tetromino"""
    from tetris.tetromino import Tetromino

    shape = Tetromino.T_SHAPE
    assert str(shape) == ".T.\nTTT\n...\n"


# Step 4: Falling Pieces
def test_when_piece_is_dropped_board_has_3x3_blocks() -> None:
    """Test 15: When a piece is dropped, it starts from the top middle"""
    from tetris.board import Board
    from tetris.tetromino import Tetromino

    board = Board(6, 8)
    board.drop(Tetromino.T_SHAPE)
    assert (
        str(board) == "...T..\n..TTT.\n......\n......\n......\n......\n......\n......\n"
    )


def test_piece_falls_with_tick() -> None:
    """Test 16: Piece falls one row per tick"""
    from tetris.board import Board
    from tetris.tetromino import Tetromino

    board = Board(6, 8)
    board.drop(Tetromino.T_SHAPE)
    board.tick()
    assert (
        str(board) == "......\n...T..\n..TTT.\n......\n......\n......\n......\n......\n"
    )


def test_piece_lands_on_bottom() -> None:
    """Test 17: Piece lands when it hits the bottom"""
    from tetris.board import Board
    from tetris.tetromino import Tetromino

    board = Board(6, 8)
    board.drop(Tetromino.T_SHAPE)
    # Move piece to bottom (starts at rows 0-1, needs to go to rows 6-7)
    for _ in range(6):
        board.tick()
    # After 6 ticks, should be at rows 6-7 and still falling
    assert board.has_falling() is True
    board.tick()  # 7th tick should land it
    assert (
        str(board) == "......\n......\n......\n......\n......\n......\n...T..\n..TTT.\n"
    )
    assert board.has_falling() is False


def test_piece_collision_check() -> None:
    """Test 18: Piece collision detection"""
    from tetris.board import Board
    from tetris.tetromino import Tetromino

    board = Board(6, 8)
    board.drop(Tetromino.T_SHAPE)
    # Move piece to bottom
    for _ in range(7):
        board.tick()
    # Piece should have landed
    assert board.has_falling() is False

    # Drop another piece
    board.drop(Tetromino.T_SHAPE)
    # Move it down close to the first piece
    for _ in range(4):
        board.tick()
    # It should stop on top of the first piece
    board.tick()
    assert (
        str(board) == "......\n......\n......\n......\n...T..\n..TTT.\n...T..\n..TTT.\n"
    )
    assert board.has_falling() is False


def test_board_handles_both_blocks_and_pieces() -> None:
    """Test 19: Board can handle both Block and Piece types"""
    from tetris.block import Block
    from tetris.board import Board
    from tetris.tetromino import Tetromino

    board = Board(6, 8)
    # Drop a single block first
    board.drop(Block("X"))
    board.tick()
    board.tick()
    board.tick()
    assert board.has_falling() is True
    # Continue moving block to bottom
    for _ in range(5):
        board.tick()
    assert board.has_falling() is False

    # Now drop a piece
    board.drop(Tetromino.T_SHAPE)
    assert board.has_falling() is True
    # Move piece down
    for _ in range(5):
        board.tick()
    # Should land on the block
    board.tick()
    assert board.has_falling() is False


# Step 5: Moving a Falling Piece
def test_can_move_piece_left() -> None:
    """Test 20: Can move a falling piece left"""
    from tetris.board import Board
    from tetris.tetromino import Tetromino

    board = Board(6, 8)
    board.drop(Tetromino.T_SHAPE)
    board.move_left()
    assert (
        str(board) == "..T...\n.TTT..\n......\n......\n......\n......\n......\n......\n"
    )


def test_can_move_piece_right() -> None:
    """Test 21: Can move a falling piece right"""
    from tetris.board import Board
    from tetris.tetromino import Tetromino

    board = Board(6, 8)
    board.drop(Tetromino.T_SHAPE)
    board.move_right()
    assert (
        str(board) == "....T.\n...TTT\n......\n......\n......\n......\n......\n......\n"
    )


def test_piece_cannot_move_past_boundaries() -> None:
    """Test 22: Piece cannot move past left/right boundaries"""
    from tetris.board import Board
    from tetris.tetromino import Tetromino

    board = Board(6, 8)
    board.drop(Tetromino.T_SHAPE)
    # Move left twice (should stop at boundary)
    board.move_left()
    board.move_left()
    board.move_left()  # Should not move past left edge
    assert (
        str(board) == ".T....\nTTT...\n......\n......\n......\n......\n......\n......\n"
    )

    # Reset and test right boundary
    board2 = Board(6, 8)
    board2.drop(Tetromino.T_SHAPE)
    # Move right once (should stop at boundary, piece is 3 wide)
    board2.move_right()
    board2.move_right()  # Should not move past right edge
    assert (
        str(board2)
        == "....T.\n...TTT\n......\n......\n......\n......\n......\n......\n"
    )


# Step 6: Rotating a Falling Piece
def test_can_rotate_falling_piece() -> None:
    """Test 23: Can rotate a falling piece"""
    from tetris.board import Board
    from tetris.tetromino import Tetromino

    board = Board(6, 8)
    board.drop(Tetromino.T_SHAPE)
    board.tick()  # Move down to have space to rotate
    board.rotate_right()
    assert (
        str(board) == "......\n...T..\n...TT.\n...T..\n......\n......\n......\n......\n"
    )


def test_piece_cannot_rotate_if_blocked() -> None:
    """Test 24: Piece cannot rotate if blocked by boundaries or other pieces"""
    from tetris.board import Board
    from tetris.tetromino import Tetromino

    # Test rotation blocked by bottom boundary
    board = Board(6, 3)  # Very short board (only 3 rows)
    board.drop(Tetromino.T_SHAPE)
    # Move to bottom row (piece already takes 2 rows, at bottom of 3-row board)
    board.tick()  # This should put piece at bottom
    # Try to rotate, should fail due to bottom boundary
    original_state = str(board)
    board.rotate_right()
    assert str(board) == original_state  # Should not have rotated


# Step 7: Sharpening the specification
def test_dropping_on_falling_block_reports_already_falling() -> None:
    """Test 25: The error for dropping on a falling block has the exact message"""
    import pytest

    from tetris.block import Block
    from tetris.board import Board

    board = Board(3, 3)
    board.drop(Block("X"))
    with pytest.raises(ValueError) as excinfo:
        board.drop(Block("Y"))
    assert str(excinfo.value) == "already falling"


def test_block_starts_from_top_middle_of_wider_board() -> None:
    """Test 26: Block starts from the top middle on a wider board"""
    from tetris.block import Block
    from tetris.board import Board

    board = Board(6, 3)
    board.drop(Block("X"))
    assert str(board) == "...X..\n......\n......\n"


def test_piece_starts_from_top_middle_of_odd_width_board() -> None:
    """Test 27: Piece starts from the top middle on an odd-width board"""
    from tetris.board import Board
    from tetris.tetromino import Tetromino

    board = Board(7, 8)
    board.drop(Tetromino.T_SHAPE)
    assert (
        str(board)
        == "....T..\n...TTT.\n.......\n.......\n.......\n.......\n.......\n.......\n"
    )


def test_block_can_be_moved_left() -> None:
    """Test 28: A falling block can be moved left"""
    from tetris.block import Block
    from tetris.board import Board

    board = Board(3, 3)
    board.drop(Block("X"))
    board.move_left()
    assert str(board) == "X..\n...\n...\n"


def test_block_can_be_moved_right() -> None:
    """Test 29: A falling block can be moved right"""
    from tetris.block import Block
    from tetris.board import Board

    board = Board(3, 3)
    board.drop(Block("X"))
    board.move_right()
    assert str(board) == "..X\n...\n...\n"


def test_block_cannot_move_left_past_boundary() -> None:
    """Test 30: A falling block stops at the left boundary"""
    from tetris.block import Block
    from tetris.board import Board

    board = Board(3, 3)
    board.drop(Block("X"))
    board.move_left()
    board.move_left()  # Should not move past left edge
    assert str(board) == "X..\n...\n...\n"


def test_block_cannot_move_right_past_boundary() -> None:
    """Test 31: A falling block stops at the right boundary"""
    from tetris.block import Block
    from tetris.board import Board

    board = Board(3, 3)
    board.drop(Block("X"))
    board.move_right()
    board.move_right()  # Should not move past right edge
    assert str(board) == "..X\n...\n...\n"


def test_single_block_cannot_be_rotated() -> None:
    """Test 32: Rotating a single falling block leaves the board unchanged"""
    from tetris.block import Block
    from tetris.board import Board

    board = Board(3, 3)
    board.drop(Block("X"))
    board.rotate_right()
    assert str(board) == ".X.\n...\n...\n"
    assert board.has_falling() is True


def test_falling_piece_does_not_hide_landed_blocks() -> None:
    """Test 33: Empty cells of a falling piece do not hide landed blocks"""
    from tetris.board import Board
    from tetris.tetromino import Tetromino

    board = Board(6, 8)
    board.drop(Tetromino.T_SHAPE)
    for _ in range(7):
        board.tick()
    assert board.has_falling() is False

    board.drop(Tetromino.T_SHAPE)
    for _ in range(4):
        board.tick()
    # The falling piece's empty bottom row overlaps the landed piece's top
    # block, which must remain visible
    assert (
        str(board) == "......\n......\n......\n......\n...T..\n..TTT.\n...T..\n..TTT.\n"
    )
    assert board.has_falling() is True


def test_piece_lands_at_top_when_no_room_to_fall() -> None:
    """Test 34: Piece lands in its starting rows when it cannot fall at all"""
    from tetris.board import Board
    from tetris.tetromino import Tetromino

    board = Board(6, 2)
    board.drop(Tetromino.T_SHAPE)
    board.tick()
    assert board.has_falling() is False
    assert str(board) == "...T..\n..TTT.\n"


def test_piece_lands_against_left_wall() -> None:
    """Test 35: A piece landed at the left wall keeps its leftmost blocks"""
    from tetris.board import Board
    from tetris.tetromino import Tetromino

    board = Board(6, 8)
    board.drop(Tetromino.T_SHAPE)
    board.move_left()
    board.move_left()
    for _ in range(7):
        board.tick()
    assert board.has_falling() is False
    assert (
        str(board) == "......\n......\n......\n......\n......\n......\n.T....\nTTT...\n"
    )


def test_piece_overhanging_right_edge_is_clipped() -> None:
    """Test 36: Piece cells beyond the right edge are neither shown nor landed"""
    from tetris.board import Board
    from tetris.tetromino import Tetromino

    board = Board(2, 8)
    board.drop(Tetromino.T_SHAPE)
    assert str(board) == ".T\nTT\n..\n..\n..\n..\n..\n..\n"
    board.tick()
    assert board.has_falling() is False
    assert str(board) == ".T\nTT\n..\n..\n..\n..\n..\n..\n"


def test_piece_overhanging_bottom_is_clipped() -> None:
    """Test 37: Piece cells below the bottom are neither shown nor landed"""
    from tetris.board import Board
    from tetris.piece import Piece

    board = Board(6, 2)
    board.drop(Piece("XXX\n...\nXXX\n"))
    assert str(board) == "..XXX.\n......\n"
    board.tick()
    assert board.has_falling() is False
    assert str(board) == "..XXX.\n......\n"


def test_tetromino_keeps_its_given_shape() -> None:
    """Test 38: A tetromino constructed with a shape renders that shape"""
    from tetris.tetromino import Tetromino

    piece = Tetromino(".X.\n.X.\n...\n")
    assert str(piece) == ".X.\n.X.\n...\n"


def test_can_rotate_falling_piece_counter_clockwise() -> None:
    """Test 26: Board.rotate_left turns the falling piece 90 degrees counter-clockwise"""
    from tetris.board import Board
    from tetris.tetromino import Tetromino

    board = Board(6, 8)
    board.drop(Tetromino.T_SHAPE)
    board.tick()
    board.rotate_left()
    assert (
        str(board) == "......\n...T..\n..TT..\n...T..\n......\n......\n......\n......\n"
    )


def test_piece_cannot_rotate_left_if_blocked() -> None:
    """Test 27: rotate_left reverts when the rotated piece would not fit"""
    from tetris.board import Board
    from tetris.tetromino import Tetromino

    board = Board(6, 3)
    board.drop(Tetromino.T_SHAPE)
    board.tick()
    original_state = str(board)
    board.rotate_left()
    assert str(board) == original_state


def test_rotate_left_ignores_single_block() -> None:
    """Test 28: A plain block (no rotations) is left untouched by rotate_left"""
    from tetris.block import Block
    from tetris.board import Board

    board = Board(4, 4)
    board.drop(Block("X"))
    original_state = str(board)
    board.rotate_left()
    assert str(board) == original_state


def test_moves_on_empty_board_are_no_ops() -> None:
    """Test 29: Moving or rotating with no falling piece leaves the board unchanged"""
    from tetris.board import Board

    board = Board(4, 4)
    original_state = str(board)
    board.move_left()
    board.move_right()
    board.rotate_left()
    board.rotate_right()
    assert str(board) == original_state
