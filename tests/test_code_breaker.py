"""Code Breaker kata tests.

Feedback scoring for a Mastermind-style game: '+' per correct digit in the correct
position, '-' per correct digit in the wrong position, exact matches consumed first,
all plusses before minuses. The secret is constructor input - no randomness.
"""

import pytest


def test_no_matching_digits_gives_empty_feedback() -> None:
    """Test 1: secret 1234, guess 5678 -> '' (no digit occurs in the secret)."""
    from code_breaker import CodeBreaker

    assert CodeBreaker("1234").guess("5678") == ""


def test_single_exact_match() -> None:
    """Test 2: secret 1234, guess 1578 -> '+' (only the 1 matches, in place)."""
    from code_breaker import CodeBreaker

    assert CodeBreaker("1234").guess("1578") == "+"


def test_all_exact_matches() -> None:
    """Test 3: secret 1234, guess 1234 -> '++++' (every digit in place)."""
    from code_breaker import CodeBreaker

    assert CodeBreaker("1234").guess("1234") == "++++"


def test_all_partial_matches() -> None:
    """Test 4: secret 1234, guess 4321 -> '----' (every digit present, none in
    place)."""
    from code_breaker import CodeBreaker

    assert CodeBreaker("1234").guess("4321") == "----"


def test_mixed_exact_and_partial_matches() -> None:
    """Test 5: secret 1234, guess 1243 -> '++--' (1 and 2 exact; 4 and 3
    swapped)."""
    from code_breaker import CodeBreaker

    assert CodeBreaker("1234").guess("1243") == "++--"


def test_exact_match_consumes_duplicate_secret_digit() -> None:
    """Test 6: secret 1124, guess 5167 -> '+' (the 1 at position 2 is exact; the
    guess has no second 1 to earn a partial)."""
    from code_breaker import CodeBreaker

    assert CodeBreaker("1124").guess("5167") == "+"


def test_guess_digit_absent_from_secret_earns_nothing() -> None:
    """Test 7: secret 1111, guess 1112 -> '+++' (three exact; 2 is not in the
    secret)."""
    from code_breaker import CodeBreaker

    assert CodeBreaker("1111").guess("1112") == "+++"


def test_plusses_precede_minuses_regardless_of_position() -> None:
    """Test 8: secret 1234, guess 2134 -> '++--' (exacts at positions 3 and 4
    are reported before the swapped 2 and 1)."""
    from code_breaker import CodeBreaker

    assert CodeBreaker("1234").guess("2134") == "++--"


def test_duplicate_guess_digits_earn_only_available_copies() -> None:
    """Test 9: secret 1234, guess 5115 -> '-' (the secret has a single 1, so
    the second 1 in the guess earns nothing)."""
    from code_breaker import CodeBreaker

    assert CodeBreaker("1234").guess("5115") == "-"


def test_duplicate_secret_digits_reward_duplicate_guesses() -> None:
    """Test 10: secret 1122, guess 2211 -> '----' (two 1s and two 2s all in the
    wrong positions)."""
    from code_breaker import CodeBreaker

    assert CodeBreaker("1122").guess("2211") == "----"


def test_same_instance_scores_multiple_guesses() -> None:
    """Test 11: the feedback engine is stateless across guesses."""
    from code_breaker import CodeBreaker

    breaker = CodeBreaker("1234")

    assert breaker.guess("5678") == ""
    assert breaker.guess("1234") == "++++"
    assert breaker.guess("4321") == "----"


def test_secret_shorter_than_four_digits_is_rejected() -> None:
    """Test 12: a 3-digit secret raises ValueError."""
    from code_breaker import CodeBreaker

    with pytest.raises(ValueError, match="^code must be 4 to 6 characters long$"):
        CodeBreaker("123")


def test_secret_longer_than_six_digits_is_rejected() -> None:
    """Test 13: a 7-digit secret raises ValueError."""
    from code_breaker import CodeBreaker

    with pytest.raises(ValueError, match="^code must be 4 to 6 characters long$"):
        CodeBreaker("1234567")


def test_secret_with_digit_outside_alphabet_is_rejected() -> None:
    """Test 14: digits outside 1-6 (e.g. 0 or 7) are rejected by default."""
    from code_breaker import CodeBreaker

    with pytest.raises(ValueError) as exc_info:
        CodeBreaker("1207")
    assert str(exc_info.value) == "code may only contain characters from '123456'"


def test_guess_digits_outside_alphabet_simply_never_match() -> None:
    """Test 15: the kata's examples score guesses like 5678 against a 1-6
    secret, so out-of-range guess digits are legal and earn nothing."""
    from code_breaker import CodeBreaker

    assert CodeBreaker("1234").guess("1789") == "+"


def test_guess_length_must_match_secret_length() -> None:
    """Test 16: a guess of a different length than the secret is rejected."""
    from code_breaker import CodeBreaker

    with pytest.raises(
        ValueError, match="^guess must be the same length as the secret$"
    ):
        CodeBreaker("1234").guess("12345")


def test_bonus_five_digit_code_is_supported() -> None:
    """Test 17: bonus - a 5-digit secret scores 5-digit guesses."""
    from code_breaker import CodeBreaker

    breaker = CodeBreaker("12345")

    assert breaker.guess("12345") == "+++++"
    assert breaker.guess("23451") == "-----"


def test_bonus_custom_digit_range_is_supported() -> None:
    """Test 18: bonus - a wider alphabet admits digits the default rejects."""
    from code_breaker import CodeBreaker

    breaker = CodeBreaker("1278", alphabet="12345678")

    assert breaker.guess("1287") == "++--"


def test_bonus_six_digit_code_is_supported() -> None:
    """Test 19: bonus - a 6-digit secret scores 6-digit guesses."""
    from code_breaker import CodeBreaker

    breaker = CodeBreaker("123456")

    assert breaker.guess("123456") == "++++++"
    assert breaker.guess("234561") == "------"
