"""
Port of C# WordWrapTest.cs
Tests for Word Wrap kata - wrapping text at specified column width
"""


def test_can_wrap_single_line() -> None:
    """Test 1: Can wrap single line text"""
    from word_wrap.word_wrap import WordWrap

    result = WordWrap.wrap("Let's  Go", 5)
    expected = "Let's\nGo"

    assert result == expected


def test_can_handle_null_word() -> None:
    """Test 2: Should return empty string for null"""
    from word_wrap.word_wrap import WordWrap

    result = WordWrap.wrap(None, 5)
    expected = ""

    assert result == expected


def test_can_handle_null_or_whitespace() -> None:
    """Test 3: Should return empty string for null or whitespace"""
    from word_wrap.word_wrap import WordWrap

    # Test null
    assert WordWrap.wrap(None, 5) == ""
    # Test single space
    assert WordWrap.wrap(" ", 5) == ""


def test_can_handle_newline_character() -> None:
    """Test 4: Existing newlines are preserved; each segment wraps independently"""
    from word_wrap.word_wrap import WordWrap

    # Single newline
    assert WordWrap.wrap("\n", 1) == "\n"
    # "Let's Go" breaks at the space; "outside." (8 chars, one word) splits at the width
    result = WordWrap.wrap("\nLet's Go\noutside.", 5)
    expected = "\nLet's\nGo\noutsi\nde."
    assert result == expected


def test_can_wrap_multiple_lines() -> None:
    """Test 5: Wraps at word boundaries across a longer text"""
    from word_wrap.word_wrap import WordWrap

    # Break at the last space that fits within each 7-column window
    assert WordWrap.wrap("Lets go outside now", 7) == "Lets go\noutside\nnow"

    # Additional coverage for general case with newlines
    assert WordWrap.wrap("test\ncase", 10) == "test\ncase"


def test_word_longer_than_width_is_split_at_width() -> None:
    """Test 5b: A single word longer than the width is split at the width"""
    from word_wrap.word_wrap import WordWrap

    assert WordWrap.wrap("extraordinary", 5) == "extra\nordin\nary"


def test_can_handle_whitespace_only_tab() -> None:
    """Test 6: Should return empty string for whitespace-only text such as a tab"""
    from word_wrap.word_wrap import WordWrap

    assert WordWrap.wrap("\t", 5) == ""


def test_can_preserve_consecutive_newlines() -> None:
    """Test 7: Consecutive newlines are preserved, not collapsed to empty"""
    from word_wrap.word_wrap import WordWrap

    assert WordWrap.wrap("\n\n", 5) == "\n\n"


def test_segments_within_column_width_are_unchanged() -> None:
    """Test 8: Segments around an existing newline that fit the width stay as-is"""
    from word_wrap.word_wrap import WordWrap

    assert WordWrap.wrap("XX\nXX", 5) == "XX\nXX"


def test_column_count_restarts_after_existing_newline() -> None:
    """Test 9: Column counting restarts after an existing newline"""
    from word_wrap.word_wrap import WordWrap

    # Each 3-letter segment fits within a width of 4, so no break is inserted
    assert WordWrap.wrap("abc\ndef", 4) == "abc\ndef"


def test_column_count_restarts_after_inserted_break() -> None:
    """Test 10: Column counting restarts after an inserted line break"""
    from word_wrap.word_wrap import WordWrap

    # After breaking at width 3, the remaining 2 letters fit on the new line
    assert WordWrap.wrap("aaa bb", 3) == "aaa\nbb"


def test_text_shorter_than_column_width_is_unchanged() -> None:
    """Test 11: Text shorter than the column width is returned unchanged"""
    from word_wrap.word_wrap import WordWrap

    assert WordWrap.wrap("Xmas day", 10) == "Xmas day"


def test_preserves_tab_indentation_after_newline() -> None:
    """Test 12: Only spaces are trimmed at line starts; tabs are preserved"""
    from word_wrap.word_wrap import WordWrap

    assert WordWrap.wrap("ab\n\tcd", 10) == "ab\n\tcd"


def test_line_exactly_at_width_with_space_is_unchanged() -> None:
    """Test 13: A line exactly at the column width is not wrapped, space or not"""
    from word_wrap.word_wrap import WordWrap

    assert WordWrap.wrap("ab cd", 5) == "ab cd"


def test_break_at_space_in_second_position() -> None:
    """Test 14: A one-letter first word still breaks at its space"""
    from word_wrap.word_wrap import WordWrap

    assert WordWrap.wrap("a bcdef", 5) == "a\nbcdef"


def test_leading_space_line_hard_breaks_at_width() -> None:
    """Test 15: A line starting with a space hard-breaks at the width (no empty head)"""
    from word_wrap.word_wrap import WordWrap

    assert WordWrap.wrap(" hello", 3) == " he\nllo"


def test_tab_after_break_space_is_preserved() -> None:
    """Test 16: Only spaces are consumed at a break; a tab survives onto the new line"""
    from word_wrap.word_wrap import WordWrap

    assert WordWrap.wrap("ab \tcd", 3) == "ab\n\tcd"


def test_word_starting_with_x_survives_break() -> None:
    """Test 17: Only spaces are consumed at a break — letters of the next word never are"""
    from word_wrap.word_wrap import WordWrap

    assert WordWrap.wrap("ab Xcd", 3) == "ab\nXcd"


def test_trailing_spaces_do_not_produce_trailing_newline() -> None:
    """Test 18: Trailing spaces beyond the width are dropped, not turned into a line"""
    from word_wrap.word_wrap import WordWrap

    assert WordWrap.wrap("hi  ", 2) == "hi"
