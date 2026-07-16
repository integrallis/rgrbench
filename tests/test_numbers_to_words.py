"""Numbers to Words kata: spell integers 0..9999 as English words.

Kata catalogued at tddbuddy.com/katas/numbers-to-words; implementation and
tests original (MIT), machine-authored from the specification, 2026.
"""


def test_zero() -> None:
    """Test 1: 0 is spelled 'zero'"""
    from numbers_to_words import number_to_words

    assert number_to_words(0) == "zero"


def test_single_digit_five() -> None:
    """Test 2: 5 is spelled 'five'"""
    from numbers_to_words import number_to_words

    assert number_to_words(5) == "five"


def test_single_digit_eight() -> None:
    """Test 3: 8 is spelled 'eight'"""
    from numbers_to_words import number_to_words

    assert number_to_words(8) == "eight"


def test_ten() -> None:
    """Test 4: 10 is spelled 'ten'"""
    from numbers_to_words import number_to_words

    assert number_to_words(10) == "ten"


def test_teens_are_single_words() -> None:
    """Test 5: Teens such as 13 and 19 are single unhyphenated words"""
    from numbers_to_words import number_to_words

    assert number_to_words(13) == "thirteen"
    assert number_to_words(19) == "nineteen"


def test_round_tens_have_no_hyphen() -> None:
    """Test 6: Round tens such as 20 and 90 are single words"""
    from numbers_to_words import number_to_words

    assert number_to_words(20) == "twenty"
    assert number_to_words(90) == "ninety"


def test_twenty_one_is_hyphenated() -> None:
    """Test 7: 21 is the hyphenated compound 'twenty-one'"""
    from numbers_to_words import number_to_words

    assert number_to_words(21) == "twenty-one"


def test_seventy_seven_is_hyphenated() -> None:
    """Test 8: 77 is the hyphenated compound 'seventy-seven'"""
    from numbers_to_words import number_to_words

    assert number_to_words(77) == "seventy-seven"


def test_ninety_nine_is_hyphenated() -> None:
    """Test 9: 99, the largest two-digit number, is 'ninety-nine'"""
    from numbers_to_words import number_to_words

    assert number_to_words(99) == "ninety-nine"


def test_one_hundred_keeps_leading_one() -> None:
    """Test 10: 100 is 'one hundred', never just 'hundred'"""
    from numbers_to_words import number_to_words

    assert number_to_words(100) == "one hundred"


def test_hundreds_with_units_remainder() -> None:
    """Test 11: 303 is 'three hundred three' with no 'and'"""
    from numbers_to_words import number_to_words

    assert number_to_words(303) == "three hundred three"


def test_hundreds_with_compound_remainder() -> None:
    """Test 12: 555 is 'five hundred fifty-five'"""
    from numbers_to_words import number_to_words

    assert number_to_words(555) == "five hundred fifty-five"


def test_no_and_between_hundreds_and_remainder() -> None:
    """Test 13: The word 'and' never joins hundreds to the remainder"""
    from numbers_to_words import number_to_words

    assert " and " not in number_to_words(303)
    assert " and " not in number_to_words(555)


def test_hundreds_with_teen_remainder() -> None:
    """Test 14: 115 is 'one hundred fifteen'"""
    from numbers_to_words import number_to_words

    assert number_to_words(115) == "one hundred fifteen"


def test_one_thousand_keeps_leading_one() -> None:
    """Test 15: 1000 is 'one thousand'"""
    from numbers_to_words import number_to_words

    assert number_to_words(1000) == "one thousand"


def test_round_thousands() -> None:
    """Test 16: 2000 is 'two thousand'"""
    from numbers_to_words import number_to_words

    assert number_to_words(2000) == "two thousand"


def test_thousands_with_round_hundreds() -> None:
    """Test 17: 2400 is 'two thousand four hundred'"""
    from numbers_to_words import number_to_words

    assert number_to_words(2400) == "two thousand four hundred"


def test_full_four_digit_number() -> None:
    """Test 18: 3466 is 'three thousand four hundred sixty-six'"""
    from numbers_to_words import number_to_words

    assert number_to_words(3466) == "three thousand four hundred sixty-six"


def test_thousands_skipping_hundreds() -> None:
    """Test 19: 5005 is 'five thousand five' with the empty hundreds omitted"""
    from numbers_to_words import number_to_words

    assert number_to_words(5005) == "five thousand five"


def test_largest_supported_number() -> None:
    """Test 20: 9999 is 'nine thousand nine hundred ninety-nine'"""
    from numbers_to_words import number_to_words

    assert number_to_words(9999) == "nine thousand nine hundred ninety-nine"


def test_negative_numbers_are_rejected() -> None:
    """Test 21: Negative input is outside 0..9999 and raises ValueError"""
    import pytest

    from numbers_to_words import number_to_words

    with pytest.raises(ValueError, match="must be in 0..9999"):
        number_to_words(-1)


def test_numbers_above_9999_are_rejected() -> None:
    """Test 22: 10000 is outside 0..9999 and raises ValueError"""
    import pytest

    from numbers_to_words import number_to_words

    with pytest.raises(ValueError, match="must be in 0..9999"):
        number_to_words(10000)
