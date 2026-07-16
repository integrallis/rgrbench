"""Poker hand ranking and comparison for the rules in the package docstring."""

from collections import Counter

CATEGORIES: tuple[str, ...] = (
    "high card",
    "pair",
    "two pairs",
    "three of a kind",
    "straight",
    "flush",
    "full house",
    "four of a kind",
    "straight flush",
)

_CARD_VALUES: dict[str, int] = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}
_SUITS = frozenset("CDHS")
_VALUE_NAMES: dict[int, str] = {11: "Jack", 12: "Queen", 13: "King", 14: "Ace"}


def _parse_card(card: str) -> tuple[int, str]:
    """Return (numeric value, suit) for a card string such as '9C' or 'TD'."""
    value_part, suit = card[:-1], card[-1:]
    if suit not in _SUITS or value_part not in _CARD_VALUES:
        raise ValueError(f"invalid card: {card!r}")
    return _CARD_VALUES[value_part], suit


def _rank(hand: str) -> tuple[int, tuple[int, ...]]:
    """Rank a hand as (category index, tiebreaker values).

    Tiebreakers are the distinct card values ordered by how often they
    occur, then by value, both descending. Comparing two ranks of the
    same category with tuple ordering therefore applies the spec's
    tie-breaking rules for every category.
    """
    cards = hand.split()
    if len(cards) != 5:
        raise ValueError("a hand must contain exactly 5 cards")
    parsed = [_parse_card(card) for card in cards]
    counts = Counter(value for value, _ in parsed)
    tiebreakers = tuple(
        sorted(counts, key=lambda value: (counts[value], value), reverse=True)
    )
    count_pattern = sorted(counts.values(), reverse=True)
    is_flush = len({suit for _, suit in parsed}) == 1
    is_straight = len(counts) == 5 and max(counts) - min(counts) == 4

    if is_straight and is_flush:
        category = 8
    elif count_pattern == [4, 1]:
        category = 7
    elif count_pattern == [3, 2]:
        category = 6
    elif is_flush:
        category = 5
    elif is_straight:
        category = 4
    elif count_pattern == [3, 1, 1]:
        category = 3
    elif count_pattern == [2, 2, 1]:
        category = 2
    elif count_pattern == [2, 1, 1, 1]:
        category = 1
    else:
        category = 0
    return category, tiebreakers


def _value_name(value: int) -> str:
    return _VALUE_NAMES.get(value, str(value))


def hand_category(hand: str) -> str:
    """Return the category name of a five-card hand, e.g. 'full house'."""
    return CATEGORIES[_rank(hand)[0]]


def compare_hands(black: str, white: str) -> str:
    """Compare Black's and White's hands and describe the outcome.

    Returns 'Tie.' for equal ranks, '<Name> wins. - with <category>' when
    the categories differ, and '<Name> wins. - with <category>: <value>'
    when the same category is decided by card values, naming the first
    deciding value.
    """
    black_rank = _rank(black)
    white_rank = _rank(white)
    if black_rank == white_rank:
        return "Tie."
    if black_rank > white_rank:
        winner, win_rank, lose_rank = "Black", black_rank, white_rank
    else:
        winner, win_rank, lose_rank = "White", white_rank, black_rank
    category = CATEGORIES[win_rank[0]]
    if win_rank[0] != lose_rank[0]:
        return f"{winner} wins. - with {category}"
    decider = next(
        high for high, low in zip(win_rank[1], lose_rank[1]) if high != low
    )
    return f"{winner} wins. - with {category}: {_value_name(decider)}"
