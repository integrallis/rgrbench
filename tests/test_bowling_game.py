"""
Port of C# Bowling Game TestGame.cs
Complete port with all test cases
"""

from bowling_game.game import Game


def test_can_get_calculate_single_scores() -> None:
    """Port of Can_Get_Calculate_Single_Scores"""
    game = Game()
    game.roll(0)
    assert game.score() == 0


def test_can_get_calculate_scores() -> None:
    """Port of Can_Get_Calculate_Scores"""
    game = Game()
    for _ in range(10):  # 10 frames
        game.roll(0)
    assert game.score() == 0


def test_can_get_calculate_spare_scores() -> None:
    """Port of Can_Get_Calculate_Spare_Scores"""
    game = Game()
    # Roll spare
    game.roll(5)
    game.roll(5)
    game.roll(3)
    # Remaining rolls
    for _ in range(17):
        game.roll(0)
    assert game.score() == 16


def test_can_get_calculate_strike_scores() -> None:
    """Port of Can_Get_Calculate_Strike_Scores"""
    game = Game()
    # Roll strike
    game.roll(10)
    game.roll(3)
    game.roll(4)
    # Remaining rolls
    for _ in range(16):
        game.roll(0)
    assert game.score() == 24


def test_can_get_calculate_full_game_scores() -> None:
    """Port of Can_Get_Calculate_Full_Game_Scores"""
    game = Game()
    # Perfect game - 12 strikes
    for _ in range(12):
        game.roll(10)
    assert game.score() == 300


def test_can_get_calculate_strike_in_second_frame_scores() -> None:
    """A strike after an open frame earns the next two rolls as bonus"""
    game = Game()
    # Open first frame
    game.roll(1)
    game.roll(2)
    # Strike in second frame
    game.roll(10)
    game.roll(3)
    game.roll(4)
    # Remaining rolls
    for _ in range(14):
        game.roll(0)
    # Frame 1: 3, Frame 2: 10 + 3 + 4 = 17, Frame 3: 3 + 4 = 7
    assert game.score() == 27


def test_can_get_calculate_spare_in_second_frame_scores() -> None:
    """A spare after an open frame adds its bonus to the running score"""
    game = Game()
    # Open first frame
    game.roll(1)
    game.roll(2)
    # Spare in second frame
    game.roll(5)
    game.roll(5)
    game.roll(3)
    # Remaining rolls
    for _ in range(15):
        game.roll(0)
    # Frame 1: 3, Frame 2: 10 + 3 = 13, Frame 3: 3 + 0 = 3
    assert game.score() == 19
