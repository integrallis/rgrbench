"""Tests for the Conway's Sequence kata (look-and-say).

Each term describes the previous one by reading runs of identical digits as
"count then digit". next_term produces one step; look_and_say applies the
transformation n times, with zero iterations returning the seed unchanged.
"""


def test_next_term_of_one() -> None:
    """Test 1: "1" is one 1, read as "11" """
    from conways_sequence import next_term

    assert next_term("1") == "11"


def test_next_term_of_double_one() -> None:
    """Test 2: "11" is two 1s, read as "21" """
    from conways_sequence import next_term

    assert next_term("11") == "21"


def test_next_term_of_two_one() -> None:
    """Test 3: "21" is one 2 then one 1, read as "1211" """
    from conways_sequence import next_term

    assert next_term("21") == "1211"


def test_next_term_of_one_two_one_one() -> None:
    """Test 4: "1211" is one 1, one 2, two 1s, read as "111221" """
    from conways_sequence import next_term

    assert next_term("1211") == "111221"


def test_next_term_of_one_one_one_two_two_one() -> None:
    """Test 5: "111221" is three 1s, two 2s, one 1, read as "312211" """
    from conways_sequence import next_term

    assert next_term("111221") == "312211"


def test_next_term_of_two() -> None:
    """Test 6: "2" is one 2, read as "12" """
    from conways_sequence import next_term

    assert next_term("2") == "12"


def test_double_two_is_a_fixed_point() -> None:
    """Test 7: "22" is two 2s, which reads as "22" again"""
    from conways_sequence import next_term

    assert next_term("22") == "22"


def test_next_term_of_mixed_digits() -> None:
    """Test 8: "3211" is one 3, one 2, two 1s, read as "131221" """
    from conways_sequence import next_term

    assert next_term("3211") == "131221"


def test_run_of_ten_digits_yields_two_digit_count() -> None:
    """Test 9: Ten 1s read as "101" - a multi-digit count"""
    from conways_sequence import next_term

    assert next_term("1111111111") == "101"


def test_zero_iterations_return_seed_unchanged() -> None:
    """Test 10: look_and_say("1", 0) is "1" """
    from conways_sequence import look_and_say

    assert look_and_say("1", 0) == "1"


def test_one_iteration_from_one() -> None:
    """Test 11: look_and_say("1", 1) is "11" """
    from conways_sequence import look_and_say

    assert look_and_say("1", 1) == "11"


def test_two_iterations_from_one() -> None:
    """Test 12: look_and_say("1", 2) is "21" """
    from conways_sequence import look_and_say

    assert look_and_say("1", 2) == "21"


def test_five_iterations_from_one() -> None:
    """Test 13: look_and_say("1", 5) is "312211" """
    from conways_sequence import look_and_say

    assert look_and_say("1", 5) == "312211"


def test_one_iteration_from_two() -> None:
    """Test 14: look_and_say("2", 1) is "12" """
    from conways_sequence import look_and_say

    assert look_and_say("2", 1) == "12"


def test_fixed_point_survives_repeated_iterations() -> None:
    """Test 15: look_and_say("22", 3) stays "22" """
    from conways_sequence import look_and_say

    assert look_and_say("22", 3) == "22"


def test_negative_iterations_are_rejected() -> None:
    """Test 16: A negative iteration count raises ValueError"""
    import pytest

    from conways_sequence import look_and_say

    with pytest.raises(ValueError):
        look_and_say("1", -1)


def test_empty_term_is_rejected() -> None:
    """Test 17: An empty term raises ValueError"""
    import pytest

    from conways_sequence import next_term

    with pytest.raises(ValueError):
        next_term("")


def test_non_digit_term_is_rejected() -> None:
    """Test 18: A term containing non-digits raises ValueError"""
    import pytest

    from conways_sequence import next_term

    with pytest.raises(ValueError):
        next_term("1a1")


def test_term_containing_zero_is_accepted() -> None:
    """Test 19: "10" is one 1 then one 0, read as "1110" """
    from conways_sequence import next_term

    assert next_term("10") == "1110"


def test_term_of_nine_is_accepted() -> None:
    """Test 20: "9" is one 9, read as "19" """
    from conways_sequence import next_term

    assert next_term("9") == "19"


def test_uppercase_letter_in_term_is_rejected() -> None:
    """Test 21: A term containing an uppercase letter raises ValueError"""
    import pytest

    from conways_sequence import next_term

    with pytest.raises(ValueError):
        next_term("1A1")


def test_negative_iterations_error_names_the_rule() -> None:
    """Test 22: Rejecting a negative count reports "iterations must be non-negative" """
    import pytest

    from conways_sequence import look_and_say

    with pytest.raises(ValueError) as excinfo:
        look_and_say("1", -1)
    assert str(excinfo.value) == "iterations must be non-negative"


def test_invalid_term_error_names_the_rule() -> None:
    """Test 23: Rejecting a bad term reports "term must be a non-empty string of digits" """
    import pytest

    from conways_sequence import next_term

    with pytest.raises(ValueError) as excinfo:
        next_term("1a1")
    assert str(excinfo.value) == "term must be a non-empty string of digits"
