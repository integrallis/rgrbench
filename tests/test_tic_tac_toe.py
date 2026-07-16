"""Tic Tac Toe - Classic game implementation
TDD implementation from scratch
"""


def test_new_game_has_empty_board() -> None:
    """Test 1: A new game has an empty board"""
    from tic_tac_toe.game import TicTacToe

    game = TicTacToe()
    assert game.board == [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "],
    ]


def test_x_plays_first() -> None:
    """Test 2: X plays first"""
    from tic_tac_toe.game import TicTacToe

    game = TicTacToe()
    assert game.current_player == "X"


def test_can_place_x_on_board() -> None:
    """Test 3: Can place X on the board"""
    from tic_tac_toe.game import TicTacToe

    game = TicTacToe()
    game.play(0, 0)
    board = game.board
    assert board[0][0] == "X"


def test_players_alternate_turns() -> None:
    """Test 4: Players alternate turns"""
    from tic_tac_toe.game import TicTacToe

    game = TicTacToe()
    assert game.current_player == "X"
    game.play(0, 0)
    assert game.current_player == "O"


def test_detect_horizontal_win() -> None:
    """Test 5: Detect horizontal win"""
    from tic_tac_toe.game import TicTacToe

    game = TicTacToe()
    game.play(0, 0)  # X
    game.play(1, 0)  # O
    game.play(0, 1)  # X
    game.play(1, 1)  # O
    game.play(0, 2)  # X wins
    assert game.winner == "X"


def test_detect_vertical_win() -> None:
    """Test 6: Detect vertical win"""
    from tic_tac_toe.game import TicTacToe

    game = TicTacToe()
    game.play(0, 0)  # X
    game.play(0, 1)  # O
    game.play(1, 0)  # X
    game.play(1, 1)  # O
    game.play(2, 0)  # X wins
    assert game.winner == "X"


def test_detect_diagonal_win() -> None:
    """Test 7: Detect diagonal win"""
    from tic_tac_toe.game import TicTacToe

    game = TicTacToe()
    game.play(0, 0)  # X
    game.play(0, 1)  # O
    game.play(1, 1)  # X
    game.play(0, 2)  # O
    game.play(2, 2)  # X wins
    assert game.winner == "X"

    # Test other diagonal
    game2 = TicTacToe()
    game2.play(0, 2)  # X
    game2.play(0, 0)  # O
    game2.play(1, 1)  # X
    game2.play(1, 0)  # O
    game2.play(2, 0)  # X wins
    assert game2.winner == "X"


def test_detect_anti_diagonal_win_completed_at_top_right() -> None:
    """Test 7b: Detect anti-diagonal win when the final move is top-right"""
    from tic_tac_toe.game import TicTacToe

    game = TicTacToe()
    game.play(2, 0)  # X
    game.play(0, 0)  # O
    game.play(1, 1)  # X
    game.play(1, 0)  # O
    game.play(0, 2)  # X wins
    assert game.winner == "X"


def test_detect_draw() -> None:
    """Test 8: Detect draw when board is full with no winner"""
    from tic_tac_toe.game import TicTacToe

    game = TicTacToe()
    game.play(0, 0)  # X
    game.play(0, 1)  # O
    game.play(0, 2)  # X
    game.play(1, 0)  # O
    game.play(1, 2)  # X
    game.play(1, 1)  # O
    game.play(2, 0)  # X
    game.play(2, 2)  # O
    game.play(2, 1)  # X
    assert game.winner is None
    assert game.is_draw is True

    # Test not draw when board not full
    game2 = TicTacToe()
    game2.play(0, 0)  # X
    game2.play(0, 1)  # O
    assert game2.is_draw is False
