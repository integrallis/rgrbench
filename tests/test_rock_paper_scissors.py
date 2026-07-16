"""Rock Paper Scissors kata: judge a round between two injected moves.

Kata catalogued at tddbuddy.com/katas/rock-paper-scissors; implementation and
tests original (MIT), machine-authored from the specification, 2026.
"""


def test_rock_beats_scissors() -> None:
    """Test 1: Rock defeats scissors, so the player wins"""
    from rock_paper_scissors import Move, Outcome, play

    assert play(Move.ROCK, Move.SCISSORS) is Outcome.PLAYER_WINS


def test_scissors_beat_paper() -> None:
    """Test 2: Scissors defeat paper, so the player wins"""
    from rock_paper_scissors import Move, Outcome, play

    assert play(Move.SCISSORS, Move.PAPER) is Outcome.PLAYER_WINS


def test_paper_beats_rock() -> None:
    """Test 3: Paper defeats rock, so the player wins"""
    from rock_paper_scissors import Move, Outcome, play

    assert play(Move.PAPER, Move.ROCK) is Outcome.PLAYER_WINS


def test_scissors_lose_to_rock() -> None:
    """Test 4: Scissors against rock means the player loses"""
    from rock_paper_scissors import Move, Outcome, play

    assert play(Move.SCISSORS, Move.ROCK) is Outcome.PLAYER_LOSES


def test_paper_loses_to_scissors() -> None:
    """Test 5: Paper against scissors means the player loses"""
    from rock_paper_scissors import Move, Outcome, play

    assert play(Move.PAPER, Move.SCISSORS) is Outcome.PLAYER_LOSES


def test_rock_loses_to_paper() -> None:
    """Test 6: Rock against paper means the player loses"""
    from rock_paper_scissors import Move, Outcome, play

    assert play(Move.ROCK, Move.PAPER) is Outcome.PLAYER_LOSES


def test_rock_ties_rock() -> None:
    """Test 7: Identical rock moves tie"""
    from rock_paper_scissors import Move, Outcome, play

    assert play(Move.ROCK, Move.ROCK) is Outcome.TIE


def test_paper_ties_paper() -> None:
    """Test 8: Identical paper moves tie"""
    from rock_paper_scissors import Move, Outcome, play

    assert play(Move.PAPER, Move.PAPER) is Outcome.TIE


def test_scissors_tie_scissors() -> None:
    """Test 9: Identical scissors moves tie"""
    from rock_paper_scissors import Move, Outcome, play

    assert play(Move.SCISSORS, Move.SCISSORS) is Outcome.TIE


def test_spock_smashes_scissors() -> None:
    """Test 10: Spock smashes scissors, so Spock's player wins"""
    from rock_paper_scissors import Move, Outcome, play

    assert play(Move.SPOCK, Move.SCISSORS) is Outcome.PLAYER_WINS
    assert play(Move.SCISSORS, Move.SPOCK) is Outcome.PLAYER_LOSES


def test_spock_vaporizes_rock() -> None:
    """Test 11: Spock vaporizes rock, so Spock's player wins"""
    from rock_paper_scissors import Move, Outcome, play

    assert play(Move.SPOCK, Move.ROCK) is Outcome.PLAYER_WINS
    assert play(Move.ROCK, Move.SPOCK) is Outcome.PLAYER_LOSES


def test_paper_disproves_spock() -> None:
    """Test 12: Paper disproves Spock, so paper's player wins"""
    from rock_paper_scissors import Move, Outcome, play

    assert play(Move.PAPER, Move.SPOCK) is Outcome.PLAYER_WINS
    assert play(Move.SPOCK, Move.PAPER) is Outcome.PLAYER_LOSES


def test_spock_ties_spock() -> None:
    """Test 13: Identical Spock moves tie"""
    from rock_paper_scissors import Move, Outcome, play

    assert play(Move.SPOCK, Move.SPOCK) is Outcome.TIE


def test_every_pairing_has_a_verdict() -> None:
    """Test 14: All sixteen move pairings judge to one of the three outcomes"""
    from rock_paper_scissors import Move, Outcome, play

    for player in Move:
        for opponent in Move:
            assert play(player, opponent) in set(Outcome)


def test_ties_happen_exactly_on_identical_moves() -> None:
    """Test 15: A round ties exactly when both moves are the same"""
    from rock_paper_scissors import Move, Outcome, play

    for player in Move:
        for opponent in Move:
            is_tie = play(player, opponent) is Outcome.TIE
            assert is_tie == (player is opponent)


def test_wins_and_losses_are_symmetric() -> None:
    """Test 16: If the player wins a pairing, swapping the moves is a loss"""
    from rock_paper_scissors import Move, Outcome, play

    for player in Move:
        for opponent in Move:
            if play(player, opponent) is Outcome.PLAYER_WINS:
                assert play(opponent, player) is Outcome.PLAYER_LOSES


def test_moves_form_a_closed_set_of_four() -> None:
    """Test 17: The move enum contains rock, paper, scissors and Spock only"""
    from rock_paper_scissors import Move

    assert {move.name for move in Move} == {"ROCK", "PAPER", "SCISSORS", "SPOCK"}


def test_outcomes_form_a_closed_set_of_three() -> None:
    """Test 18: The outcome enum contains win, lose and tie only"""
    from rock_paper_scissors import Outcome

    assert {outcome.name for outcome in Outcome} == {
        "PLAYER_WINS",
        "PLAYER_LOSES",
        "TIE",
    }
