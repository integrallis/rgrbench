"""String Helper - String manipulation utilities
Ported from Java implementation by in28minutes
"""


def test_are_first_and_last_two_chars_same_empty_string() -> None:
    """Test 1: Empty string returns False"""
    from string_helper.helper import StringHelper

    helper = StringHelper()
    assert helper.are_first_and_last_two_chars_same("") is False


def test_are_first_and_last_two_chars_same_single_char() -> None:
    """Test 2: Single character returns False"""
    from string_helper.helper import StringHelper

    helper = StringHelper()
    assert helper.are_first_and_last_two_chars_same("A") is False


def test_are_first_and_last_two_chars_same_two_chars() -> None:
    """Test 3: Two characters returns True"""
    from string_helper.helper import StringHelper

    helper = StringHelper()
    assert helper.are_first_and_last_two_chars_same("AB") is True


def test_are_first_and_last_two_chars_same_three_chars_not_matching() -> None:
    """Test 4: Three characters ABC returns False"""
    from string_helper.helper import StringHelper

    helper = StringHelper()
    assert helper.are_first_and_last_two_chars_same("ABC") is False


def test_are_first_and_last_two_chars_same_three_chars_matching() -> None:
    """Test 5: Three characters AAA returns True"""
    from string_helper.helper import StringHelper

    helper = StringHelper()
    assert helper.are_first_and_last_two_chars_same("AAA") is True


def test_are_first_and_last_two_chars_same_five_chars_matching() -> None:
    """Test 6: Five characters ABCAB returns True"""
    from string_helper.helper import StringHelper

    helper = StringHelper()
    assert helper.are_first_and_last_two_chars_same("ABCAB") is True


def test_are_first_and_last_two_chars_same_seven_chars_not_matching() -> None:
    """Test 7: Seven characters ABCDEBA returns False"""
    from string_helper.helper import StringHelper

    helper = StringHelper()
    assert helper.are_first_and_last_two_chars_same("ABCDEBA") is False
