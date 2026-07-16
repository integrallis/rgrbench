"""Tetris Piece - Multi-block pieces that can rotate"""


class Piece:
    """Represents a multi-block piece"""

    def __init__(self, shape: str) -> None:
        """Initialize a piece with given shape string"""
        self.shape = shape

    def __str__(self) -> str:
        """Return string representation of the piece"""
        return self.shape

    def rotate_right(self) -> "Piece":
        """Rotate the piece 90 degrees clockwise"""
        # Parse the shape into a 2D grid
        rows = self.shape.strip().split("\n")
        grid = [list(row) for row in rows]
        size = len(grid)

        # Create rotated grid
        rotated = [[" " for _ in range(size)] for _ in range(size)]
        for r in range(size):
            for c in range(size):
                rotated[c][size - 1 - r] = grid[r][c]

        # Convert back to string
        rotated_shape = "\n".join("".join(row) for row in rotated) + "\n"
        return Piece(rotated_shape)

    def rotate_left(self) -> "Piece":
        """Rotate the piece 90 degrees counter-clockwise"""
        # Parse the shape into a 2D grid
        rows = self.shape.strip().split("\n")
        grid = [list(row) for row in rows]
        size = len(grid)

        # Create rotated grid
        rotated = [[" " for _ in range(size)] for _ in range(size)]
        for r in range(size):
            for c in range(size):
                rotated[size - 1 - c][r] = grid[r][c]

        # Convert back to string
        rotated_shape = "\n".join("".join(row) for row in rotated) + "\n"
        return Piece(rotated_shape)
