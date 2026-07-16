"""Tests for the Anagram Detector kata.

Anagrams have identical letters with matching frequencies, compared
case-insensitively with spaces and punctuation ignored; a word is never an
anagram of itself. Covers pair detection, finding anagrams in a candidate
list, and grouping a word list into anagram clusters.
"""


def test_listen_and_silent_are_anagrams() -> None:
    """Test 1: "listen" and "silent" are anagrams"""
    from anagram_detector import is_anagram

    assert is_anagram("listen", "silent") is True


def test_hello_and_world_are_not_anagrams() -> None:
    """Test 2: "hello" and "world" are not anagrams"""
    from anagram_detector import is_anagram

    assert is_anagram("hello", "world") is False


def test_cat_and_tac_are_anagrams() -> None:
    """Test 3: "cat" and "tac" are anagrams"""
    from anagram_detector import is_anagram

    assert is_anagram("cat", "tac") is True


def test_word_is_not_anagram_of_itself() -> None:
    """Test 4: "cat" is not an anagram of "cat" """
    from anagram_detector import is_anagram

    assert is_anagram("cat", "cat") is False


def test_comparison_is_case_insensitive() -> None:
    """Test 5: "Cat" and "tac" are anagrams despite the case difference"""
    from anagram_detector import is_anagram

    assert is_anagram("Cat", "tac") is True


def test_empty_strings_are_not_anagrams() -> None:
    """Test 6: Two empty strings are not anagrams"""
    from anagram_detector import is_anagram

    assert is_anagram("", "") is False


def test_single_identical_letter_is_not_anagram() -> None:
    """Test 7: "a" is not an anagram of "a" """
    from anagram_detector import is_anagram

    assert is_anagram("a", "a") is False


def test_two_letter_swap_is_anagram() -> None:
    """Test 8: "ab" and "ba" are anagrams"""
    from anagram_detector import is_anagram

    assert is_anagram("ab", "ba") is True


def test_same_letters_different_frequencies_are_not_anagrams() -> None:
    """Test 9: "aab" and "abb" differ in letter frequencies"""
    from anagram_detector import is_anagram

    assert is_anagram("aab", "abb") is False


def test_same_word_in_different_case_is_still_itself() -> None:
    """Test 10: "Cat" and "cat" are the same word case-insensitively, not anagrams"""
    from anagram_detector import is_anagram

    assert is_anagram("Cat", "cat") is False


def test_spaces_are_ignored() -> None:
    """Test 11: "Dormitory" and "Dirty Room" are anagrams once spaces are ignored"""
    from anagram_detector import is_anagram

    assert is_anagram("Dormitory", "Dirty Room") is True


def test_punctuation_is_ignored() -> None:
    """Test 12: "Astronomer" and "Moon starer!" are anagrams once punctuation is ignored"""
    from anagram_detector import is_anagram

    assert is_anagram("Astronomer", "Moon starer!") is True


def test_find_anagrams_returns_all_matches() -> None:
    """Test 13: "listen" matches both "silent" and "tinsel" """
    from anagram_detector import find_anagrams

    assert find_anagrams("listen", ["silent", "tinsel"]) == ["silent", "tinsel"]


def test_find_anagrams_returns_empty_when_no_matches() -> None:
    """Test 14: "listen" matches nothing in ["hello", "world"]"""
    from anagram_detector import find_anagrams

    assert find_anagrams("listen", ["hello", "world"]) == []


def test_find_anagrams_filters_non_matches() -> None:
    """Test 15: "master" matches "stream" and "maters" but not "pigeon" """
    from anagram_detector import find_anagrams

    assert find_anagrams("master", ["stream", "maters", "pigeon"]) == [
        "stream",
        "maters",
    ]


def test_find_anagrams_excludes_the_subject_word_itself() -> None:
    """Test 16: The subject word appearing among the candidates is not a match"""
    from anagram_detector import find_anagrams

    assert find_anagrams("cat", ["cat", "tac"]) == ["tac"]


def test_group_anagrams_clusters_mutual_anagrams() -> None:
    """Test 17: "eat", "tea", and "ate" form a single cluster"""
    from anagram_detector import group_anagrams

    assert group_anagrams(["eat", "tea", "ate"]) == [["eat", "tea", "ate"]]


def test_group_anagrams_keeps_unrelated_words_apart() -> None:
    """Test 18: "abc" and "def" form singleton clusters"""
    from anagram_detector import group_anagrams

    assert group_anagrams(["abc", "def"]) == [["abc"], ["def"]]


def test_group_anagrams_of_empty_list_is_empty() -> None:
    """Test 19: An empty word list yields no clusters"""
    from anagram_detector import group_anagrams

    assert group_anagrams([]) == []


def test_group_anagrams_orders_clusters_by_first_appearance() -> None:
    """Test 20: Clusters appear in the order their first word appears"""
    from anagram_detector import group_anagrams

    assert group_anagrams(["eat", "abc", "tea", "cba"]) == [
        ["eat", "tea"],
        ["abc", "cba"],
    ]
