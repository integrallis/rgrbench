"""Tetris Tetrominoes - The standard Tetris shapes"""

from typing import ClassVar

from tetris.piece import Piece


class Tetromino(Piece):
    """Represents a standard Tetris tetromino shape"""

    T_SHAPE: ClassVar["Tetromino"]

    def __init__(self, shape: str) -> None:
        """Initialize a tetromino with given shape"""
        super().__init__(shape)


# Define the standard tetromino shapes
Tetromino.T_SHAPE = Tetromino(".T.\nTTT\n...\n")
