"""Tic Tac Toe - Game logic.

This module implements a classic Tic Tac Toe game with proper encapsulation
and win detection. The game follows standard rules where two players ('X' and 'O')
take turns placing their marks on a 3x3 grid. A player wins by getting three
of their marks in a row (horizontally, vertically, or diagonally).

Example:
    >>> game = TicTacToe()
    >>> game.play(0, 0)  # X plays at top-left
    >>> game.play(1, 1)  # O plays at center
    >>> print(game.current_player)
    X
"""


class TicTacToe:
    """A Tic Tac Toe game implementation.

    This class manages the game state, validates moves, detects wins and draws,
    and alternates between players. The board is represented as a 3x3 grid where
    empty cells contain spaces (" "), X's are marked with "X", and O's with "O".

    Attributes:
        _board: Private 3x3 list of lists representing the game board.
        _current_player: Private string indicating whose turn it is ("X" or "O").
        _winner: Private string indicating the winner ("X", "O", or None).
    """

    def __init__(self) -> None:
        """Initialize a new Tic Tac Toe game.

        Creates an empty 3x3 board with all cells set to empty (" ").
        Sets the starting player to "X" and initializes winner as None.
        """
        self._board = [[" " for _ in range(3)] for _ in range(3)]
        self._current_player = "X"
        self._winner: str | None = None

    @property
    def board(self) -> list[list[str]]:
        """Get a copy of the current board state.

        Returns a defensive copy of the board to prevent external modification
        of the internal game state.

        Returns:
            A 3x3 list of lists containing the current board state.
            Each cell contains " " (empty), "X", or "O".
        """
        return [row[:] for row in self._board]

    @property
    def current_player(self) -> str:
        """Get the player whose turn it is.

        Returns:
            The current player's mark: "X" or "O".
        """
        return self._current_player

    def play(self, row: int, col: int) -> None:
        """Make a move at the specified position.

        Places the current player's mark at the given row and column,
        checks for a win condition, and switches to the other player.

        Args:
            row: The row index (0-2) where the move should be placed.
            col: The column index (0-2) where the move should be placed.
        """
        self._board[row][col] = self._current_player

        if self._check_win(row, col):
            self._winner = self._current_player

        self._switch_player()

    def _check_win(self, row: int, col: int) -> bool:
        """Check if the current move results in a win.

        Checks all possible win conditions: horizontal, vertical, and diagonal.

        Args:
            row: The row index (0-2) of the last move.
            col: The column index (0-2) of the last move.

        Returns:
            True if the current player has won, False otherwise.
        """
        return (
            self._check_horizontal_win(row)
            or self._check_vertical_win(col)
            or self._check_diagonal_win(row, col)
        )

    def _check_horizontal_win(self, row: int) -> bool:
        """Check if the current player has won horizontally.

        Args:
            row: The row index (0-2) to check.

        Returns:
            True if all cells in the row belong to the current player.
        """
        return all(self._board[row][c] == self._current_player for c in range(3))

    def _check_vertical_win(self, col: int) -> bool:
        """Check if the current player has won vertically.

        Args:
            col: The column index (0-2) to check.

        Returns:
            True if all cells in the column belong to the current player.
        """
        return all(self._board[r][col] == self._current_player for r in range(3))

    def _check_diagonal_win(self, row: int, col: int) -> bool:
        """Check if the current player has won diagonally.

        Checks both the main diagonal (top-left to bottom-right) and the
        anti-diagonal (top-right to bottom-left).

        Args:
            row: The row index (0-2) of the last move.
            col: The column index (0-2) of the last move.

        Returns:
            True if the current player has won on either diagonal.
        """
        return self._check_main_diagonal_win(row, col) or self._check_anti_diagonal_win(
            row, col
        )

    def _check_main_diagonal_win(self, row: int, col: int) -> bool:
        """Check if the current player has won on the main diagonal.

        The main diagonal runs from top-left (0,0) to bottom-right (2,2).
        Only checks if the move was placed on this diagonal.

        Args:
            row: The row index (0-2) of the last move.
            col: The column index (0-2) of the last move.

        Returns:
            True if the move is on the main diagonal and all cells on it
            belong to the current player.
        """
        return row == col and all(
            self._board[i][i] == self._current_player for i in range(3)
        )

    def _check_anti_diagonal_win(self, row: int, col: int) -> bool:
        """Check if the current player has won on the anti-diagonal.

        The anti-diagonal runs from top-right (0,2) to bottom-left (2,0).
        Only checks if the move was placed on this diagonal.

        Args:
            row: The row index (0-2) of the last move.
            col: The column index (0-2) of the last move.

        Returns:
            True if the move is on the anti-diagonal and all cells on it
            belong to the current player.
        """
        return row + col == 2 and all(
            self._board[i][2 - i] == self._current_player for i in range(3)
        )

    def _switch_player(self) -> None:
        """Switch to the other player.

        Toggles the current player from "X" to "O" or from "O" to "X".
        """
        self._current_player = "O" if self._current_player == "X" else "X"

    def _is_board_full(self) -> bool:
        """Check if the board is completely filled.

        Returns:
            True if all cells on the board contain a player's mark.
        """
        return all(" " not in row for row in self._board)

    @property
    def winner(self) -> str | None:
        """Get the winner of the game.

        Returns:
            The winner's mark ("X" or "O"), or None if there is no winner yet.
        """
        return self._winner

    @property
    def is_draw(self) -> bool:
        """Check if the game is a draw.

        A draw occurs when the board is full and there is no winner.

        Returns:
            True if the game is a draw, False otherwise.
        """
        return self._is_board_full() and self._winner is None
