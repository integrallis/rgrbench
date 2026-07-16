"""Poker Hands kata - rank five-card hands and compare two players.

Covers detection of all nine hand categories, category ordering,
value-based tie-breaking with the announced deciding value, ties, and
input validation.
"""


def test_high_card_category() -> None:
    """Test 1: Five unmatched, non-consecutive, mixed-suit cards are high card"""
    from poker_hands import hand_category

    assert hand_category("2H 3D 5S 9C KD") == "high card"


def test_pair_category() -> None:
    """Test 2: Two cards of the same value form a pair"""
    from poker_hands import hand_category

    assert hand_category("2H 2D 5S 9C KD") == "pair"


def test_two_pairs_category() -> None:
    """Test 3: Two different pairs form two pairs"""
    from poker_hands import hand_category

    assert hand_category("2H 2D 5S 5C KD") == "two pairs"


def test_three_of_a_kind_category() -> None:
    """Test 4: Three cards of the same value form three of a kind"""
    from poker_hands import hand_category

    assert hand_category("2H 2D 2S 9C KD") == "three of a kind"


def test_straight_category() -> None:
    """Test 5: Five consecutive values of mixed suits form a straight"""
    from poker_hands import hand_category

    assert hand_category("2H 3D 4S 5C 6D") == "straight"


def test_flush_category() -> None:
    """Test 6: Five same-suit, non-consecutive cards form a flush"""
    from poker_hands import hand_category

    assert hand_category("2S 8S AS QS 3S") == "flush"


def test_full_house_category() -> None:
    """Test 7: A triple plus a pair form a full house"""
    from poker_hands import hand_category

    assert hand_category("2H 4S 4C 2D 4H") == "full house"


def test_four_of_a_kind_category() -> None:
    """Test 8: Four cards of the same value form four of a kind"""
    from poker_hands import hand_category

    assert hand_category("9H 9D 9S 9C KD") == "four of a kind"


def test_straight_flush_category() -> None:
    """Test 9: Consecutive same-suit cards form a straight flush

    Also exercises the '10' spelling of the ten card.
    """
    from poker_hands import hand_category

    assert hand_category("10H JH QH KH AH") == "straight flush"


def test_ace_is_high_only_so_wheel_is_not_a_straight() -> None:
    """Test 10: A-2-3-4-5 is not a straight because aces rank high only"""
    from poker_hands import hand_category

    assert hand_category("AH 2D 3S 4C 5D") == "high card"


def test_t_is_the_ten_card() -> None:
    """Test 11: 'T' denotes the ten, so TH and TD pair up"""
    from poker_hands import hand_category

    assert hand_category("TH TD 5S 9C KD") == "pair"


def test_high_card_decided_by_ace() -> None:
    """Test 12: Higher top card wins between two high-card hands

    Canonical example: White's ace beats Black's king.
    """
    from poker_hands import compare_hands

    result = compare_hands("2H 3D 5S 9C KD", "2C 3H 4S 8C AH")

    assert result == "White wins. - with high card: Ace"


def test_full_house_beats_flush() -> None:
    """Test 13: Full house outranks flush; only the category is announced"""
    from poker_hands import compare_hands

    result = compare_hands("2H 4S 4C 2D 4H", "2S 8S AS QS 3S")

    assert result == "Black wins. - with full house"


def test_high_card_tie_broken_by_next_highest() -> None:
    """Test 14: Equal top cards fall through to the next value

    Canonical example: kings tie, Black's 9 beats White's 8.
    """
    from poker_hands import compare_hands

    result = compare_hands("2H 3D 5S 9C KD", "2C 3H 4S 8C KH")

    assert result == "Black wins. - with high card: 9"


def test_identical_ranks_tie() -> None:
    """Test 15: Hands equal in every value are a tie regardless of suits"""
    from poker_hands import compare_hands

    assert compare_hands("2H 3D 5S 9C KD", "2D 3H 5C 9S KH") == "Tie."


def test_pair_decided_by_pair_value() -> None:
    """Test 16: Between two pairs, the higher pair value wins"""
    from poker_hands import compare_hands

    result = compare_hands("8H 8D 5S 9C KD", "6H 6D 5C 9S KH")

    assert result == "Black wins. - with pair: 8"


def test_equal_pairs_decided_by_kicker() -> None:
    """Test 17: Equal pair values fall through to the highest kicker"""
    from poker_hands import compare_hands

    result = compare_hands("8H 8D 5S 9C KD", "8S 8C 5C 9S QH")

    assert result == "Black wins. - with pair: King"


def test_two_pairs_decided_by_second_pair() -> None:
    """Test 18: Equal high pairs fall through to the lower pair"""
    from poker_hands import compare_hands

    result = compare_hands("KH KD 5S 5C 9D", "KS KC 3H 3D 9C")

    assert result == "Black wins. - with two pairs: 5"


def test_straight_decided_by_highest_card() -> None:
    """Test 19: Between two straights, the higher-topped run wins"""
    from poker_hands import compare_hands

    result = compare_hands("2H 3D 4S 5C 6D", "3H 4D 5S 6C 7D")

    assert result == "White wins. - with straight: 7"


def test_straight_flush_beats_four_of_a_kind() -> None:
    """Test 20: Straight flush is the highest category"""
    from poker_hands import compare_hands

    result = compare_hands("9H 9D 9S 9C KD", "2S 3S 4S 5S 6S")

    assert result == "White wins. - with straight flush"


def test_flush_decided_by_high_card_rules() -> None:
    """Test 21: Between two flushes, high-card comparison decides"""
    from poker_hands import compare_hands

    result = compare_hands("2S 8S AS QS 3S", "2H 8H KH QH 3H")

    assert result == "Black wins. - with flush: Ace"


def test_four_of_a_kind_decided_by_quad_value() -> None:
    """Test 22: The quad value outweighs any kicker"""
    from poker_hands import compare_hands

    result = compare_hands("9H 9D 9S 9C 2D", "8H 8D 8S 8C AD")

    assert result == "Black wins. - with four of a kind: 9"


def test_ten_is_named_10_in_the_verdict() -> None:
    """Test 23: A deciding ten is announced as '10'"""
    from poker_hands import compare_hands

    result = compare_hands("2H 3D 5S 9C TD", "2C 3H 4S 9D 8H")

    assert result == "Black wins. - with high card: 10"


def test_wrong_card_count_is_rejected() -> None:
    """Test 24: A hand must contain exactly five cards"""
    import pytest

    from poker_hands import hand_category

    with pytest.raises(ValueError, match="^a hand must contain exactly 5 cards$"):
        hand_category("2H 3D 5S 9C")


def test_malformed_card_is_rejected() -> None:
    """Test 25: An unknown value or suit raises ValueError naming the card"""
    import pytest

    from poker_hands import hand_category

    with pytest.raises(ValueError, match="invalid card: '1Z'"):
        hand_category("2H 3D 5S 9C 1Z")


def test_card_with_unknown_suit_is_rejected() -> None:
    """Test 26: A valid value paired with an unknown suit letter raises ValueError"""
    import pytest

    from poker_hands import hand_category

    with pytest.raises(ValueError, match="invalid card: '9Z'"):
        hand_category("2H 3D 5S 9C 9Z")


def test_card_with_unknown_value_is_rejected() -> None:
    """Test 27: An unknown value paired with a valid suit raises ValueError"""
    import pytest

    from poker_hands import hand_category

    with pytest.raises(ValueError, match="invalid card: '1H'"):
        hand_category("2H 3D 5S 9C 1H")
