"""Tetris Board - Game board implementation"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tetris.block import Block
    from tetris.piece import Piece


class Board:
    """Represents the Tetris game board"""

    def __init__(self, width: int, height: int) -> None:
        """Initialize a new board with given dimensions"""
        self.width = width
        self.height = height
        # Initialize empty board
        self.grid = [["." for _ in range(width)] for _ in range(height)]
        self.falling_block: Block | Piece | None = None
        self.falling_row = 0
        self.falling_col = 0

    def __str__(self) -> str:
        """Return string representation of the board"""
        # Create a copy of the grid to display
        display_grid = [row[:] for row in self.grid]

        # Add falling block/piece if present
        if self.falling_block:
            # Check if it's a Block or Piece
            if hasattr(self.falling_block, "char"):
                # It's a Block
                display_grid[self.falling_row][
                    self.falling_col
                ] = self.falling_block.char
            else:
                # It's a Piece - need to render the shape
                shape_lines = str(self.falling_block).strip().split("\n")
                for i, line in enumerate(shape_lines):
                    for j, char in enumerate(line):
                        if char != ".":
                            row = self.falling_row + i
                            col = self.falling_col + j
                            if 0 <= row < self.height and 0 <= col < self.width:
                                display_grid[row][col] = char

        rows = ["".join(row) for row in display_grid]
        return "\n".join(rows) + "\n"

    def has_falling(self) -> bool:
        """Check if there are any falling blocks"""
        return self.falling_block is not None

    def drop(self, block: Block | Piece) -> None:
        """Drop a block onto the board"""
        if self.falling_block is not None:
            raise ValueError("already falling")
        self.falling_block = block
        self.falling_row = 0
        # For pieces, center the 3x3 shape
        if hasattr(block, "shape"):
            # It's a Piece - center its 3x3 shape
            self.falling_col = (self.width - 3) // 2 + 1
        else:
            # It's a Block
            self.falling_col = self.width // 2

    def move_left(self) -> None:
        """Move the falling piece left"""
        if not self.falling_block:
            return

        new_col = self.falling_col - 1

        # Check if it's a Block or Piece
        if hasattr(self.falling_block, "char"):
            # Block logic
            if (
                new_col >= 0 and self.grid[self.falling_row][new_col] == "."
            ):
                self.falling_col = new_col
        else:
            # Piece logic - check if all blocks can move left
            if self._can_piece_move_to(self.falling_row, new_col):
                self.falling_col = new_col

    def rotate_right(self) -> None:
        """Rotate the falling piece 90 degrees clockwise"""
        if not self.falling_block or hasattr(self.falling_block, "char"):
            return

        # Rotate the piece and check if it fits
        rotated_piece = self.falling_block.rotate_right()
        # Temporarily switch pieces to check collision
        original_piece = self.falling_block
        self.falling_block = rotated_piece

        if self._can_piece_move_to(self.falling_row, self.falling_col):
            # Keep the rotation
            pass
        else:
            # Revert if rotation doesn't fit
            self.falling_block = original_piece

    def rotate_left(self) -> None:
        """Rotate the falling piece 90 degrees counter-clockwise"""
        if not self.falling_block or hasattr(
            self.falling_block, "char"
        ):
            return  # Can't rotate a single block

        # Rotate the piece and check if it fits
        rotated_piece = self.falling_block.rotate_left()
        # Temporarily switch pieces to check collision
        original_piece = self.falling_block
        self.falling_block = rotated_piece

        if self._can_piece_move_to(
            self.falling_row, self.falling_col
        ):
            # Keep the rotation
            pass
        else:
            # Revert if rotation doesn't fit
            self.falling_block = original_piece

    def move_right(self) -> None:
        """Move the falling piece right"""
        if not self.falling_block:
            return

        new_col = self.falling_col + 1

        # Check if it's a Block or Piece
        if hasattr(self.falling_block, "char"):
            # Block logic
            if (
                new_col < self.width and self.grid[self.falling_row][new_col] == "."
            ):
                self.falling_col = new_col
        else:
            # Piece logic - check if all blocks can move right
            if self._can_piece_move_to(self.falling_row, new_col):
                self.falling_col = new_col

    def tick(self) -> None:
        """Move the falling block down one row"""
        if self.falling_block:
            next_row = self.falling_row + 1

            # Check if it's a Block or Piece
            if hasattr(self.falling_block, "char"):
                # Block logic
                if (
                    next_row >= self.height
                    or self.grid[next_row][self.falling_col] != "."
                ):
                    # Land the block at current position
                    self.grid[self.falling_row][
                        self.falling_col
                    ] = self.falling_block.char
                    self.falling_block = None
                else:
                    # Move down
                    self.falling_row = next_row
            else:
                # Piece logic - check collision for all blocks in the piece
                can_move = self._can_piece_move_to(next_row, self.falling_col)
                if can_move:
                    self.falling_row = next_row
                else:
                    # Land the piece
                    self._land_piece()
                    self.falling_block = None

    def _can_piece_move_to(self, row: int, col: int) -> bool:
        """Check if a piece can move to the given position"""
        if not self.falling_block or hasattr(self.falling_block, "char"):
            return False

        shape_lines = str(self.falling_block).strip().split("\n")
        for i, line in enumerate(shape_lines):
            for j, char in enumerate(line):
                if char != ".":
                    check_row = row + i
                    check_col = col + j
                    # Check bounds
                    if (
                        check_row >= self.height
                        or check_col < 0
                        or check_col >= self.width
                    ):
                        return False
                    # Check collision with existing blocks
                    if self.grid[check_row][check_col] != ".":
                        return False
        return True

    def _land_piece(self) -> None:
        """Land the current piece on the board"""
        if not self.falling_block or hasattr(self.falling_block, "char"):
            return

        shape_lines = str(self.falling_block).strip().split("\n")
        for i, line in enumerate(shape_lines):
            for j, char in enumerate(line):
                if char != ".":
                    row = self.falling_row + i
                    col = self.falling_col + j
                    if 0 <= row < self.height and 0 <= col < self.width:
                        self.grid[row][col] = char
