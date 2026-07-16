"""Darts Game - 301 scoring system
Ported from Java implementation by danidemi
"""


def test_game_starts_at_301() -> None:
    """Test 1: A new game starts with score 301"""
    from darts.game import Darts

    game = Darts()
    assert game.score() == 301
    assert game.is_finished() is False


def test_normal_throw_scoring() -> None:
    """Test 2: Should correctly score a normal throw"""
    from darts.game import Darts

    game = Darts()
    game.dart(20)
    assert game.score() == 281


def test_double_throw_scoring() -> None:
    """Test 3: Should count a double throw"""
    from darts.game import Darts, Multiplier

    game = Darts()
    game.dart(20, Multiplier.DOUBLE)
    assert game.score() == 301 - 20 * 2


def test_triple_throw_scoring() -> None:
    """Test 4: Should count a triple throw"""
    from darts.game import Darts, Multiplier

    game = Darts()
    game.dart(20, Multiplier.TRIPLE)
    assert game.score() == 301 - 20 * 3


def test_turn_and_darts_counting_initially() -> None:
    """Test 5: Should count turn and darts initially"""
    from darts.game import Darts

    game = Darts()
    assert game.get_turn() == 1
    assert game.darts_left() == 3


def test_turn_and_darts_counting() -> None:
    """Test 6: Should count turn and darts properly"""
    from darts.game import Darts

    game = Darts()

    game.dart(1)
    assert game.get_turn() == 1
    assert game.darts_left() == 2

    game.dart(1)
    assert game.get_turn() == 1
    assert game.darts_left() == 1

    game.dart(1)
    assert game.get_turn() == 2
    assert game.darts_left() == 3


def test_go_bust_reaching_1() -> None:
    """Test 7: Should go bust when reaching 1"""
    from darts.game import Darts, Multiplier

    game = Darts()

    # Get to 121
    for _ in range(3):
        game.dart(20, Multiplier.TRIPLE)

    # Try to get to 1 (bust!)
    game.dart(20, Multiplier.TRIPLE)
    game.dart(20, Multiplier.TRIPLE)

    assert game.score() == 121
    assert game.get_turn() == 3
    assert game.darts_left() == 3


def test_go_bust_below_zero() -> None:
    """Test 8: Should go bust when going below zero"""
    from darts.game import Darts, Multiplier

    game = Darts()

    # Get to 121
    for _ in range(3):
        game.dart(20, Multiplier.TRIPLE)

    game.dart(15, Multiplier.TRIPLE)  # 76
    game.dart(15, Multiplier.TRIPLE)  # 31
    game.dart(20, Multiplier.TRIPLE)  # -29 Bust!

    assert game.score() == 121
    assert game.get_turn() == 3
    assert game.darts_left() == 3


def test_complete_game_with_double() -> None:
    """Test 9: Should complete a game with a double"""
    from darts.game import Darts, Multiplier

    game = Darts()

    # Get to 121
    for _ in range(3):
        game.dart(20, Multiplier.TRIPLE)

    game.dart(17, Multiplier.TRIPLE)  # 70
    game.dart(20, Multiplier.TRIPLE)  # 10
    game.dart(5, Multiplier.DOUBLE)  # 0 - WIN!

    assert game.is_finished() is True


def test_reaching_zero_with_single_is_bust() -> None:
    """A single-20 checkout attempt to exactly zero busts and restores the turn score"""
    from darts.game import Darts, Multiplier

    game = Darts()
    for _ in range(3):
        game.dart(20, Multiplier.TRIPLE)  # score 121, turn 2
    game.dart(20, Multiplier.TRIPLE)  # 61
    game.dart(7)  # 54
    game.dart(17, Multiplier.DOUBLE)  # 20 — turn ends, score 20
    game.dart(20)  # exactly 0 WITHOUT a double: bust
    assert game.is_finished() is False
    assert game.score() == 20  # restored to start of turn
    assert game.darts_left() == 3


def test_reaching_one_on_last_dart_is_also_bust() -> None:
    """Score 1 is a bust even on the turn's final dart (no double can finish from 1)"""
    from darts.game import Darts, Multiplier

    game = Darts()
    for _ in range(3):
        game.dart(20, Multiplier.TRIPLE)  # 121
    game.dart(20, Multiplier.TRIPLE)  # 61
    game.dart(20)  # 41
    game.dart(20, Multiplier.DOUBLE)  # 1 on the last dart: bust
    assert game.score() == 121
    assert game.darts_left() == 3
