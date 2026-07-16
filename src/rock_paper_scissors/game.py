"""Rock Paper Scissors kata (with the Spock extension).

Judge a single round between a player and an opponent. Both moves are passed
in as inputs -- nothing is random -- and the closed sets of moves and
outcomes are modelled as enums. Rock blunts scissors, scissors cut paper and
paper covers rock; identical moves tie. The bonus fourth gesture follows the
extension rules: Spock smashes scissors, Spock vaporises rock, and paper
disproves Spock. Round judgement is a pure table lookup, so the game logic
itself contains no if statements.

Kata catalogued at tddbuddy.com/katas/rock-paper-scissors; implementation and
tests original (MIT), machine-authored from the specification, 2026.
"""

from enum import Enum


class Move(Enum):
    """The closed set of hand gestures."""

    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"
    SPOCK = "spock"


class Outcome(Enum):
    """The result of a round from the player's point of view."""

    PLAYER_WINS = "player wins"
    PLAYER_LOSES = "player loses"
    TIE = "tie"


_BEATS: dict[Move, frozenset[Move]] = {
    Move.ROCK: frozenset({Move.SCISSORS}),
    Move.PAPER: frozenset({Move.ROCK, Move.SPOCK}),
    Move.SCISSORS: frozenset({Move.PAPER}),
    Move.SPOCK: frozenset({Move.SCISSORS, Move.ROCK}),
}

def _judge(player: Move, opponent: Move) -> Outcome:
    if player is opponent:
        return Outcome.TIE
    if opponent in _BEATS[player]:
        return Outcome.PLAYER_WINS
    return Outcome.PLAYER_LOSES


def play(player: Move, opponent: Move) -> Outcome:
    """Judge one round given both moves."""
    return _judge(player, opponent)
