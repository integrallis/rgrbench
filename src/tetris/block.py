"""Tetris Block - A single falling block"""


class Block:
    """Represents a single block"""

    def __init__(self, char: str) -> None:
        """Initialize a block with given character"""
        self.char = char
