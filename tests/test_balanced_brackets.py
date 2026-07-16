"""Tests for the Balanced Brackets kata.

A string of "[" and "]" is balanced when brackets form complete pairs in
the correct sequence: every opener has a matching closer, nesting is
consistent, and a closer never precedes its opener.
"""


def test_empty_string_is_balanced() -> None:
    """Test 1: The empty string is balanced"""
    from balanced_brackets import is_balanced

    assert is_balanced("") is True


def test_single_pair_is_balanced() -> None:
    """Test 2: "[]" is a single matched pair"""
    from balanced_brackets import is_balanced

    assert is_balanced("[]") is True


def test_sequential_pairs_are_balanced() -> None:
    """Test 3: "[][]" contains multiple sequential pairs"""
    from balanced_brackets import is_balanced

    assert is_balanced("[][]") is True


def test_nested_pair_is_balanced() -> None:
    """Test 4: "[[]]" nests one pair inside another"""
    from balanced_brackets import is_balanced

    assert is_balanced("[[]]") is True


def test_complex_nesting_is_balanced() -> None:
    """Test 5: "[[[][]]]" combines nesting and sequencing"""
    from balanced_brackets import is_balanced

    assert is_balanced("[[[][]]]") is True


def test_closing_before_opening_is_unbalanced() -> None:
    """Test 6: "][" closes before it opens"""
    from balanced_brackets import is_balanced

    assert is_balanced("][") is False


def test_misaligned_pairs_are_unbalanced() -> None:
    """Test 7: "][][" has misaligned pairs"""
    from balanced_brackets import is_balanced

    assert is_balanced("][][") is False


def test_extra_unmatched_brackets_are_unbalanced() -> None:
    """Test 8: "[][]][" has extra unmatched brackets"""
    from balanced_brackets import is_balanced

    assert is_balanced("[][]][") is False


def test_lone_opening_bracket_is_unbalanced() -> None:
    """Test 9: "[" has no closer"""
    from balanced_brackets import is_balanced

    assert is_balanced("[") is False


def test_lone_closing_bracket_is_unbalanced() -> None:
    """Test 10: "]" has no opener"""
    from balanced_brackets import is_balanced

    assert is_balanced("]") is False


def test_two_openers_are_unbalanced() -> None:
    """Test 11: "[[" leaves two pairs incomplete"""
    from balanced_brackets import is_balanced

    assert is_balanced("[[") is False


def test_two_closers_are_unbalanced() -> None:
    """Test 12: "]]" has no openers"""
    from balanced_brackets import is_balanced

    assert is_balanced("]]") is False


def test_extra_closer_after_pair_is_unbalanced() -> None:
    """Test 13: "[]]" has one closer too many"""
    from balanced_brackets import is_balanced

    assert is_balanced("[]]") is False


def test_unclosed_nested_opener_is_unbalanced() -> None:
    """Test 14: "[[]" leaves the outer opener unclosed"""
    from balanced_brackets import is_balanced

    assert is_balanced("[[]") is False


def test_deep_nesting_is_balanced() -> None:
    """Test 15: Fifty openers followed by fifty closers are balanced"""
    from balanced_brackets import is_balanced

    assert is_balanced("[" * 50 + "]" * 50) is True
