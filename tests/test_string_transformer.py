"""
Tests for String Transformer kata - chainable text transformation pipeline
"""

import pytest


def test_capitalise_first_letter_of_each_word() -> None:
    """Test 1: Capitalise uppercases the first letter of each word"""
    from string_transformer import StringTransformer

    assert StringTransformer("hello world").capitalise().result() == "Hello World"


def test_capitalise_leaves_other_letters_unchanged() -> None:
    """Test 2: Capitalise touches only the first letter of each word"""
    from string_transformer import StringTransformer

    assert StringTransformer("hello WORLD").capitalise().result() == "Hello WORLD"


def test_capitalise_empty_string() -> None:
    """Test 3: Capitalising the empty string yields the empty string"""
    from string_transformer import StringTransformer

    assert StringTransformer("").capitalise().result() == ""


def test_reverse_entire_string() -> None:
    """Test 4: Reverse reverses the entire string"""
    from string_transformer import StringTransformer

    assert StringTransformer("hello world").reverse().result() == "dlrow olleh"


def test_remove_whitespace() -> None:
    """Test 5: RemoveWhitespace removes all spaces"""
    from string_transformer import StringTransformer

    assert StringTransformer("hello world").remove_whitespace().result() == (
        "helloworld"
    )


def test_remove_whitespace_covers_tabs_and_newlines() -> None:
    """Test 6: RemoveWhitespace removes tabs and newlines too"""
    from string_transformer import StringTransformer

    assert StringTransformer("a\tb\nc d").remove_whitespace().result() == "abcd"


def test_snake_case_basic() -> None:
    """Test 7: SnakeCase converts spaces to underscores"""
    from string_transformer import StringTransformer

    assert StringTransformer("hello world").snake_case().result() == "hello_world"


def test_snake_case_handles_hyphens() -> None:
    """Test 8: SnakeCase treats hyphens as word separators"""
    from string_transformer import StringTransformer

    assert StringTransformer("hello-world test").snake_case().result() == (
        "hello_world_test"
    )


def test_snake_case_lowercases() -> None:
    """Test 9: SnakeCase lowercases the words"""
    from string_transformer import StringTransformer

    assert StringTransformer("Hello World").snake_case().result() == "hello_world"


def test_camel_case_basic() -> None:
    """Test 10: CamelCase lowercases the first word and capitalises the rest"""
    from string_transformer import StringTransformer

    assert StringTransformer("Hello World").camel_case().result() == "helloWorld"


def test_camel_case_uppercase_input() -> None:
    """Test 11: CamelCase normalises fully uppercase input"""
    from string_transformer import StringTransformer

    assert StringTransformer("HELLO WORLD").camel_case().result() == "helloWorld"


def test_camel_case_single_word() -> None:
    """Test 12: CamelCase of a single word is just the lowercased word"""
    from string_transformer import StringTransformer

    assert StringTransformer("Hello").camel_case().result() == "hello"


def test_truncate_adds_ellipsis_when_cut() -> None:
    """Test 13: Truncate cuts to n characters and appends an ellipsis"""
    from string_transformer import StringTransformer

    assert StringTransformer("hello world").truncate(5).result() == "hello…"


def test_truncate_leaves_short_text_unchanged() -> None:
    """Test 14: Truncate with a large limit leaves the text unchanged"""
    from string_transformer import StringTransformer

    assert StringTransformer("hello world").truncate(50).result() == "hello world"


def test_truncate_exact_length_is_unchanged() -> None:
    """Test 15: Truncate at exactly the text length adds no ellipsis"""
    from string_transformer import StringTransformer

    assert StringTransformer("hello world").truncate(11).result() == "hello world"


def test_truncate_negative_length_is_rejected() -> None:
    """Test 16: Truncate rejects a negative length"""
    from string_transformer import StringTransformer

    with pytest.raises(ValueError, match="length must not be negative"):
        StringTransformer("hello").truncate(-1)


def test_repeat_with_space_separator() -> None:
    """Test 17: Repeat repeats the text n times with a space separator"""
    from string_transformer import StringTransformer

    assert StringTransformer("ha").repeat(3).result() == "ha ha ha"


def test_repeat_boundaries() -> None:
    """Test 18: Repeat once is a no-op; repeat zero times yields empty text"""
    from string_transformer import StringTransformer

    assert StringTransformer("ha").repeat(1).result() == "ha"
    assert StringTransformer("ha").repeat(0).result() == ""


def test_repeat_negative_times_is_rejected() -> None:
    """Test 19: Repeat rejects a negative count"""
    from string_transformer import StringTransformer

    with pytest.raises(ValueError, match="times must not be negative"):
        StringTransformer("ha").repeat(-2)


def test_replace_all_occurrences() -> None:
    """Test 20: Replace substitutes every occurrence of the target"""
    from string_transformer import StringTransformer

    result = StringTransformer("hello world hello").replace("hello", "bye").result()
    assert result == "bye world bye"


def test_chaining_capitalise_then_reverse() -> None:
    """Test 21: Chained capitalise then reverse"""
    from string_transformer import StringTransformer

    result = StringTransformer("hello world").capitalise().reverse().result()
    assert result == "dlroW olleH"


def test_chaining_snake_case_then_capitalise() -> None:
    """Test 22: Chained snake_case then capitalise keeps the underscore"""
    from string_transformer import StringTransformer

    result = StringTransformer("hello world").snake_case().capitalise().result()
    assert result == "Hello_World"


def test_operations_are_applied_in_order() -> None:
    """Test 23: Reversing before capitalising differs from the opposite order"""
    from string_transformer import StringTransformer

    result = StringTransformer("hello world").reverse().capitalise().result()
    assert result == "Dlrow Olleh"


def test_result_without_operations_returns_initial_text() -> None:
    """Test 24: With no operations, result() returns the initial string"""
    from string_transformer import StringTransformer

    assert StringTransformer("hello world").result() == "hello world"


def test_capitalise_only_starts_words_after_separators() -> None:
    """Test 25: An uppercase letter inside a word does not start a new word"""
    from string_transformer import StringTransformer

    assert StringTransformer("teXas rocks").capitalise().result() == "TeXas Rocks"


def test_camel_case_of_text_without_words_is_empty() -> None:
    """Test 26: CamelCase of empty or separator-only text yields the empty string"""
    from string_transformer import StringTransformer

    assert StringTransformer("").camel_case().result() == ""
    assert StringTransformer(" -_ ").camel_case().result() == ""


def test_camel_case_joins_three_or_more_words_directly() -> None:
    """Test 27: CamelCase concatenates every later word with nothing in between"""
    from string_transformer import StringTransformer

    assert StringTransformer("one two three").camel_case().result() == "oneTwoThree"


def test_truncate_to_zero_keeps_only_the_ellipsis() -> None:
    """Test 28: Truncating to zero characters cuts everything, leaving just the ellipsis"""
    from string_transformer import StringTransformer

    assert StringTransformer("hello").truncate(0).result() == "…"


def test_negative_count_rejections_carry_exact_messages() -> None:
    """Test 29: Negative truncate and repeat report their exact messages"""
    from string_transformer import StringTransformer

    with pytest.raises(ValueError) as truncate_error:
        StringTransformer("hello").truncate(-1)
    assert str(truncate_error.value) == "length must not be negative"
    with pytest.raises(ValueError) as repeat_error:
        StringTransformer("ha").repeat(-2)
    assert str(repeat_error.value) == "times must not be negative"
