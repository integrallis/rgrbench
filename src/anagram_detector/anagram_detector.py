"""Anagram Detector kata.

Two words are anagrams when, after lowercasing and discarding spaces and
punctuation, they contain exactly the same letters with the same
frequencies. Comparison is case-insensitive, and a word never counts as an
anagram of itself: if the two normalised forms are identical (including
when both are empty), the answer is False.

Three operations are provided: is_anagram decides a single pair,
find_anagrams filters a candidate list down to the anagrams of a subject
word (preserving candidate order), and group_anagrams partitions a word
list into clusters of mutual anagrams, keeping words in their original
order and clusters ordered by first appearance; a word with no partner
forms a singleton cluster.

Kata catalogued at tddbuddy.com/katas/anagram-detector; implementation and
tests original (MIT), machine-authored from the specification, 2026.
"""


def is_anagram(first: str, second: str) -> bool:
    """Return True when the two words are anagrams of each other."""
    normalised_first = _normalise(first)
    normalised_second = _normalise(second)
    if normalised_first == normalised_second:
        return False
    return sorted(normalised_first) == sorted(normalised_second)


def find_anagrams(subject: str, candidates: list[str]) -> list[str]:
    """Return the candidates that are anagrams of the subject, in order."""
    return [candidate for candidate in candidates if is_anagram(subject, candidate)]


def group_anagrams(words: list[str]) -> list[list[str]]:
    """Partition words into anagram clusters ordered by first appearance."""
    clusters: dict[str, list[str]] = {}
    for word in words:
        key = "".join(sorted(_normalise(word)))
        clusters.setdefault(key, []).append(word)
    return list(clusters.values())


def _normalise(word: str) -> str:
    """Lowercase the word and drop spaces and punctuation."""
    return "".join(ch for ch in word.casefold() if ch.isalnum())
