"""
Tests for Text Justification kata - fully justify text to a fixed column width
"""

import pytest


def test_single_word_is_returned_as_is() -> None:
    """Test 1: A single word needs no justification"""
    from text_justification import justify

    assert justify("Word", 10) == ["Word"]


def test_text_fitting_one_line_needs_no_justification() -> None:
    """Test 2: Text shorter than the width stays on one left-aligned line"""
    from text_justification import justify

    assert justify("This is a test", 20) == ["This is a test"]


def test_text_exactly_at_width_fits_one_line() -> None:
    """Test 3: Text exactly as long as the width fits on one line"""
    from text_justification import justify

    assert justify("This is a test", 14) == ["This is a test"]


def test_break_into_two_lines_with_left_aligned_last_line() -> None:
    """Test 4: Greedy fill breaks after 'a'; the last line sits flush-left"""
    from text_justification import justify

    assert justify("This is a test", 9) == ["This is a", "test"]


def test_even_space_distribution() -> None:
    """Test 5: Padding divides evenly across the gaps of a full line"""
    from text_justification import justify

    assert justify("ab cd ef gh", 10) == ["ab  cd  ef", "gh"]


def test_uneven_padding_is_left_heavy() -> None:
    """Test 6: A leftover padding space goes to the leftmost gap"""
    from text_justification import justify

    assert justify("a b c d", 6) == ["a  b c", "d"]


def test_multiple_line_breaks() -> None:
    """Test 7: Longer text produces several justified lines"""
    from text_justification import justify

    assert justify("This is a very long word", 10) == [
        "This  is a",
        "very  long",
        "word",
    ]


def test_classic_leetcode_example_with_flush_left_last_line() -> None:
    """Test 8: Canonical example; the closing line is not right-padded"""
    from text_justification import justify

    assert justify("This is an example of text justification.", 16) == [
        "This    is    an",
        "example  of text",
        "justification.",
    ]


def test_single_word_non_last_line_is_right_padded() -> None:
    """Test 9: A lone word on a non-final line is padded to the width"""
    from text_justification import justify

    assert justify("aaa bbbbbbb cc", 7) == ["aaa    ", "bbbbbbb", "cc"]


def test_oversize_word_overflows_instead_of_splitting() -> None:
    """Test 10: A word longer than the width overflows on its own line"""
    from text_justification import justify

    assert justify("hi extraordinary yo", 5) == ["hi   ", "extraordinary", "yo"]


def test_oversize_single_word() -> None:
    """Test 11: A lone oversize word is returned whole"""
    from text_justification import justify

    assert justify("extraordinary", 5) == ["extraordinary"]


def test_consecutive_spaces_collapse() -> None:
    """Test 12: Runs of spaces count as one separator"""
    from text_justification import justify

    assert justify("This   is  a    test", 9) == ["This is a", "test"]


def test_tabs_and_line_breaks_are_separators() -> None:
    """Test 13: Tabs and newlines separate words like spaces"""
    from text_justification import justify

    assert justify("This\tis\na test", 9) == ["This is a", "test"]


def test_width_of_one() -> None:
    """Test 14: Width one puts each word on its own line"""
    from text_justification import justify

    assert justify("a b", 1) == ["a", "b"]


def test_empty_text_justifies_to_no_lines() -> None:
    """Test 15: The empty string yields an empty list"""
    from text_justification import justify

    assert justify("", 10) == []


def test_whitespace_only_text_justifies_to_no_lines() -> None:
    """Test 16: Whitespace-only text yields an empty list"""
    from text_justification import justify

    assert justify(" \t\n ", 10) == []


def test_zero_width_is_rejected() -> None:
    """Test 17: Width zero raises with a clear message"""
    from text_justification import justify

    with pytest.raises(ValueError, match="^width must be a positive integer$"):
        justify("some text", 0)


def test_negative_width_is_rejected() -> None:
    """Test 18: Negative width raises with a clear message"""
    from text_justification import justify

    with pytest.raises(ValueError, match="^width must be a positive integer$"):
        justify("some text", -3)


def test_none_text_is_rejected() -> None:
    """Test 19: A None text raises with a clear message"""
    from text_justification import justify

    with pytest.raises(ValueError, match="^text must not be None$"):
        justify(None, 10)


def test_every_non_final_line_is_exactly_the_width() -> None:
    """Test 20: All lines except the last are padded to the exact width"""
    from text_justification import justify

    lines = justify("the quick brown fox jumps over the lazy dog", 11)
    assert lines == ["the   quick", "brown   fox", "jumps  over", "the    lazy", "dog"]
    for line in lines[:-1]:
        assert len(line) == 11


def test_words_exactly_filling_a_later_line_share_it() -> None:
    """Test 21: Greedy fill packs a second line whose words exactly reach the width"""
    from text_justification import justify

    assert justify("aaa bb cc", 5) == ["aaa  ", "bb cc"]
