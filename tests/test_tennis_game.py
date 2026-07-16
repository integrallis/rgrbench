"""Tennis Game - Classic TDD Kata
Ported from Python implementation by giorgiosironi
"""


def test_score_names_zero() -> None:
    """Test 1: Score name for 0 points is '0'"""
    from tennis_game.tennis import Scores

    scores = Scores()
    assert scores.score_name(0) == "0"


def test_score_names_fifteen() -> None:
    """Test 2: Score name for 1 point is '15'"""
    from tennis_game.tennis import Scores

    scores = Scores()
    assert scores.score_name(1) == "15"


def test_score_names_thirty() -> None:
    """Test 3: Score name for 2 points is '30'"""
    from tennis_game.tennis import Scores

    scores = Scores()
    assert scores.score_name(2) == "30"


def test_score_names_forty() -> None:
    """Test 4: Score name for 3 points is '40'"""
    from tennis_game.tennis import Scores

    scores = Scores()
    assert scores.score_name(3) == "40"


def test_set_initialization() -> None:
    """Test 5: Tennis set starts with both players at 0"""
    from tennis_game.tennis import Set

    tennis_set = Set()
    assert tennis_set.first_score() == "0"
    assert tennis_set.second_score() == "0"


def test_score_grows() -> None:
    """Test 6: Score grows as players score points"""
    from tennis_game.tennis import Set

    tennis_set = Set()
    tennis_set.first_scores()
    assert tennis_set.first_score() == "15"
    assert tennis_set.second_score() == "0"

    tennis_set.second_scores()
    assert tennis_set.second_score() == "15"


def test_player1_wins_at_40() -> None:
    """Test 7: Player 1 wins when scoring at 40"""
    from tennis_game.tennis import Set

    tennis_set = Set()
    tennis_set.first_scores(3)  # Score 3 times to reach 40
    assert tennis_set.winner() is None

    tennis_set.first_scores()  # Score once more to win
    assert tennis_set.winner() == 1


def test_player2_wins_at_40() -> None:
    """Test 8: Player 2 wins when scoring at 40"""
    from tennis_game.tennis import Set

    tennis_set = Set()
    tennis_set.second_scores(3)  # Score 3 times to reach 40
    assert tennis_set.winner() is None

    tennis_set.second_scores()  # Score once more to win
    assert tennis_set.winner() == 2


def test_deuce_requires_two_point_lead() -> None:
    """Test 9: Deuce requires 2-point lead to win"""
    from tennis_game.tennis import Set

    tennis_set = Set()
    tennis_set.first_scores(3)  # Both at 40 (deuce)
    tennis_set.second_scores(3)

    tennis_set.first_scores()  # Player 1 advantage
    assert tennis_set.winner() is None

    tennis_set.first_scores()  # Player 1 wins with 2-point lead
    assert tennis_set.winner() == 1


def test_return_to_deuce_from_advantage() -> None:
    """Test 10: Can return to deuce from advantage"""
    from tennis_game.tennis import Set

    tennis_set = Set()
    tennis_set.first_scores(3)  # Both at 40 (deuce)
    tennis_set.second_scores(3)

    tennis_set.first_scores()  # Player 1 advantage
    tennis_set.second_scores()  # Back to deuce
    tennis_set.first_scores()  # Player 1 advantage again
    tennis_set.second_scores()  # Back to deuce again

    assert tennis_set.winner() is None
    assert tennis_set.first_score() == "40"
    assert tennis_set.second_score() == "40"


def test_advantage_score_display() -> None:
    """Test 11: Advantage is displayed as 'A'"""
    from tennis_game.tennis import Set

    tennis_set = Set()
    tennis_set.first_scores(3)  # Both at 40 (deuce)
    tennis_set.second_scores(3)

    tennis_set.first_scores()  # Player 1 advantage
    assert tennis_set.first_score() == "A"
    assert tennis_set.second_score() == "40"

    tennis_set.second_scores()  # Back to deuce
    tennis_set.second_scores()  # Player 2 advantage
    assert tennis_set.first_score() == "40"
    assert tennis_set.second_score() == "A"


def test_forty_love_is_not_advantage() -> None:
    """Test 12: Player 1 at 40 with player 2 at love shows '40', not advantage"""
    from tennis_game.tennis import Set

    tennis_set = Set()
    tennis_set.first_scores(3)  # Player 1 at 40, player 2 still at love
    assert tennis_set.first_score() == "40"
    assert tennis_set.second_score() == "0"


def test_love_forty_is_not_advantage() -> None:
    """Test 13: Player 2 at 40 with player 1 at love shows '40', not advantage"""
    from tennis_game.tennis import Set

    tennis_set = Set()
    tennis_set.second_scores(3)  # Player 2 at 40, player 1 still at love
    assert tennis_set.first_score() == "0"
    assert tennis_set.second_score() == "40"


def test_player2_advantage_from_deuce() -> None:
    """Test 14: Player 2 advantage directly from deuce is displayed as 'A'"""
    from tennis_game.tennis import Set

    tennis_set = Set()
    tennis_set.first_scores(3)  # Both at 40 (deuce)
    tennis_set.second_scores(3)

    tennis_set.second_scores()  # Player 2 advantage
    assert tennis_set.first_score() == "40"
    assert tennis_set.second_score() == "A"
    assert tennis_set.winner() is None


def test_player2_wins_from_advantage() -> None:
    """Test 15: Player 2 wins with a 2-point lead from deuce"""
    from tennis_game.tennis import Set

    tennis_set = Set()
    tennis_set.first_scores(3)  # Both at 40 (deuce)
    tennis_set.second_scores(3)

    tennis_set.second_scores()  # Player 2 advantage
    assert tennis_set.winner() is None

    tennis_set.second_scores()  # Player 2 wins with 2-point lead
    assert tennis_set.winner() == 2
