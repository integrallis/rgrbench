"""Tests for the End-of-Line Trim kata.

trim removes trailing spaces and tabs from each line while preserving
leading whitespace and each line's original terminator, handling Unix
("\\n") and Windows ("\\r\\n") endings, including mixed within one input.
A lone carriage return is content, not a terminator.
"""


def test_text_without_trailing_whitespace_is_unchanged() -> None:
    """Test 1: "abc" has nothing to trim"""
    from end_of_line_trim import trim

    assert trim("abc") == "abc"


def test_trailing_space_is_removed() -> None:
    """Test 2: "abc " loses its trailing space"""
    from end_of_line_trim import trim

    assert trim("abc ") == "abc"


def test_trailing_tab_is_removed() -> None:
    """Test 3: "abc\\t" loses its trailing tab"""
    from end_of_line_trim import trim

    assert trim("abc\t") == "abc"


def test_leading_whitespace_is_preserved() -> None:
    """Test 4: " abc" keeps its leading space"""
    from end_of_line_trim import trim

    assert trim(" abc") == " abc"


def test_windows_line_endings_are_preserved() -> None:
    """Test 5: Trailing space before "\\r\\n" is removed, terminator kept"""
    from end_of_line_trim import trim

    assert trim("ab\r\ncd \r\n") == "ab\r\ncd\r\n"


def test_terminator_only_line_passes_through() -> None:
    """Test 6: "\\r\\n" alone is returned unchanged"""
    from end_of_line_trim import trim

    assert trim("\r\n") == "\r\n"


def test_empty_string_is_unchanged() -> None:
    """Test 7: The empty string trims to itself"""
    from end_of_line_trim import trim

    assert trim("") == ""


def test_mixed_line_endings_are_each_preserved() -> None:
    """Test 8: Unix and Windows endings mixed in one input both survive"""
    from end_of_line_trim import trim

    assert trim("a \nb\t\r\nc ") == "a\nb\r\nc"


def test_lone_carriage_return_is_content() -> None:
    """Test 9: A "\\r" not followed by "\\n" stays in the line as content"""
    from end_of_line_trim import trim

    assert trim("ab \rcd \n") == "ab \rcd\n"


def test_mixed_trailing_spaces_and_tabs_are_removed() -> None:
    """Test 10: A run of trailing spaces and tabs is removed entirely"""
    from end_of_line_trim import trim

    assert trim("abc \t \t") == "abc"


def test_interior_whitespace_is_preserved() -> None:
    """Test 11: Whitespace between words is untouched"""
    from end_of_line_trim import trim

    assert trim("a  b \n") == "a  b\n"


def test_whitespace_only_unix_line_keeps_terminator() -> None:
    """Test 12: A line of just a space keeps only its "\\n" """
    from end_of_line_trim import trim

    assert trim(" \n") == "\n"


def test_every_line_is_trimmed() -> None:
    """Test 13: Trailing whitespace is removed from all lines, not just one"""
    from end_of_line_trim import trim

    assert trim("x \ny \nz ") == "x\ny\nz"


def test_bare_newline_is_unchanged() -> None:
    """Test 14: "\\n" alone is returned unchanged"""
    from end_of_line_trim import trim

    assert trim("\n") == "\n"


def test_leading_whitespace_preserved_on_every_line() -> None:
    """Test 15: Leading spaces and tabs survive on each line"""
    from end_of_line_trim import trim

    assert trim("  a \n\tb\t\n") == "  a\n\tb\n"


def test_lone_carriage_return_at_end_of_input_is_content() -> None:
    """Test 16: A final "\\r" with no "\\n" after it is kept as content"""
    from end_of_line_trim import trim

    assert trim("ab\r") == "ab\r"


def test_carriage_return_before_crlf_terminator_is_content() -> None:
    """Test 17: In "a\\r\\r\\n" the first "\\r" is content, not trailing
    whitespace, and survives"""
    from end_of_line_trim import trim

    assert trim("a\r\r\n") == "a\r\r\n"


def test_content_carriage_return_survives_trimming_before_newline() -> None:
    """Test 18: Spaces after a content "\\r" are trimmed; the "\\r" stays"""
    from end_of_line_trim import trim

    assert trim("ab\r \n") == "ab\r\n"


def test_only_spaces_and_tabs_are_trimmed_never_other_characters() -> None:
    """Test 19: Trailing letters are kept on every line style; only the
    spaces and tabs after them are removed"""
    from end_of_line_trim import trim

    assert trim("aX \nbX\t\r\nX ") == "aX\nbX\r\nX"
