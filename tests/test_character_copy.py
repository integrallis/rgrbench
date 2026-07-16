"""Character Copy kata tests.

The Copier reads from a source and writes to a destination until it meets a newline,
which is never written. The in-memory fakes below are the kata's own source and
destination abstractions, fed and inspected directly by the tests.
"""

import pytest


class FakeSource:
    """In-memory character source backed by a string."""

    def __init__(self, text: str) -> None:
        self._text = text
        self.position = 0

    def read_char(self) -> str:
        if self.position >= len(self._text):
            return ""
        char = self._text[self.position]
        self.position += 1
        return char

    def read_chars(self, count: int) -> str:
        chunk = self._text[self.position : self.position + count]
        self.position += len(chunk)
        return chunk


class FakeDestination:
    """In-memory character sink recording every write."""

    def __init__(self) -> None:
        self.writes: list[str] = []

    def write_char(self, char: str) -> None:
        self.writes.append(char)

    def write_chars(self, chars: str) -> None:
        self.writes.append(chars)

    @property
    def text(self) -> str:
        return "".join(self.writes)


def test_copies_a_single_character_before_newline() -> None:
    """Test 1: one character before the newline is copied."""
    from character_copy import Copier

    destination = FakeDestination()
    Copier(FakeSource("a\n"), destination).copy()

    assert destination.text == "a"


def test_copies_characters_in_order() -> None:
    """Test 2: all characters before the newline arrive in source order."""
    from character_copy import Copier

    destination = FakeDestination()
    Copier(FakeSource("hello\n"), destination).copy()

    assert destination.text == "hello"
    assert destination.writes == ["h", "e", "l", "l", "o"]


def test_writes_nothing_when_first_character_is_newline() -> None:
    """Test 3: a leading newline means nothing is written."""
    from character_copy import Copier

    destination = FakeDestination()
    Copier(FakeSource("\nabc"), destination).copy()

    assert destination.writes == []


def test_newline_itself_is_never_written() -> None:
    """Test 4: the terminating newline does not appear in the destination."""
    from character_copy import Copier

    destination = FakeDestination()
    Copier(FakeSource("ab\n"), destination).copy()

    assert "\n" not in destination.text


def test_characters_after_newline_are_not_copied() -> None:
    """Test 5: content after the newline never reaches the destination."""
    from character_copy import Copier

    destination = FakeDestination()
    Copier(FakeSource("ab\ncd"), destination).copy()

    assert destination.text == "ab"


def test_reading_stops_at_the_newline() -> None:
    """Test 6: the copier reads exactly up to and including the newline."""
    from character_copy import Copier

    source = FakeSource("ab\ncd")
    Copier(source, FakeDestination()).copy()

    assert source.position == 3


def test_exhausted_source_stops_copying() -> None:
    """Test 7: a source that runs out (returns '') ends the copy."""
    from character_copy import Copier

    destination = FakeDestination()
    Copier(FakeSource("ab"), destination).copy()

    assert destination.text == "ab"


def test_copies_spaces_and_punctuation() -> None:
    """Test 8: ordinary characters, including spaces, are copied verbatim."""
    from character_copy import Copier

    destination = FakeDestination()
    Copier(FakeSource("It works!\n"), destination).copy()

    assert destination.text == "It works!"


def test_copy_multiple_copies_chunk_before_newline() -> None:
    """Test 9: batch copy writes a whole chunk that contains no newline."""
    from character_copy import Copier

    destination = FakeDestination()
    Copier(FakeSource("abc\n"), destination).copy_multiple(3)

    assert destination.text == "abc"


def test_copy_multiple_truncates_chunk_at_newline() -> None:
    """Test 10: a chunk containing the newline is written only up to it."""
    from character_copy import Copier

    destination = FakeDestination()
    Copier(FakeSource("ab\ncd"), destination).copy_multiple(5)

    assert destination.writes == ["ab"]


def test_copy_multiple_writes_nothing_for_leading_newline() -> None:
    """Test 11: batch copy of a source starting with newline writes nothing."""
    from character_copy import Copier

    destination = FakeDestination()
    Copier(FakeSource("\nabc"), destination).copy_multiple(2)

    assert destination.writes == []


def test_copy_multiple_spans_several_chunks_until_newline() -> None:
    """Test 12: batch copy keeps reading chunks until the newline appears."""
    from character_copy import Copier

    destination = FakeDestination()
    Copier(FakeSource("abcdef\ngh"), destination).copy_multiple(2)

    assert destination.writes == ["ab", "cd", "ef"]
    assert destination.text == "abcdef"


def test_copy_multiple_never_writes_past_the_newline() -> None:
    """Test 13: nothing after the newline is written, even mid-chunk."""
    from character_copy import Copier

    destination = FakeDestination()
    Copier(FakeSource("abcde\nfgh"), destination).copy_multiple(4)

    assert destination.text == "abcde"
    assert "\n" not in destination.text
    assert "f" not in destination.text


def test_copy_multiple_stops_on_short_chunk() -> None:
    """Test 14: a chunk shorter than requested means the source is exhausted."""
    from character_copy import Copier

    destination = FakeDestination()
    Copier(FakeSource("abc"), destination).copy_multiple(2)

    assert destination.writes == ["ab", "c"]


def test_copy_multiple_with_empty_source_writes_nothing() -> None:
    """Test 15: an empty source produces no writes at all."""
    from character_copy import Copier

    destination = FakeDestination()
    Copier(FakeSource(""), destination).copy_multiple(3)

    assert destination.writes == []


def test_copy_multiple_rejects_non_positive_count() -> None:
    """Test 16: a batch size below 1 raises ValueError."""
    from character_copy import Copier

    copier = Copier(FakeSource("abc\n"), FakeDestination())

    with pytest.raises(ValueError, match="count must be at least 1"):
        copier.copy_multiple(0)


def test_copy_multiple_accepts_a_count_of_one() -> None:
    """Test 17: a batch size of exactly 1 is valid and copies one char at a time."""
    from character_copy import Copier

    destination = FakeDestination()
    Copier(FakeSource("ab\ncd"), destination).copy_multiple(1)

    assert destination.writes == ["a", "b"]


def test_copy_multiple_rejection_message_is_exact() -> None:
    """Test 18: the batch-size rejection carries exactly the specified message."""
    from character_copy import Copier

    copier = Copier(FakeSource("abc\n"), FakeDestination())

    with pytest.raises(ValueError) as excinfo:
        copier.copy_multiple(0)
    assert str(excinfo.value) == "count must be at least 1"


def test_copy_multiple_stops_at_the_first_newline_in_a_chunk() -> None:
    """Test 19: a chunk holding two newlines is cut at the first, not the last."""
    from character_copy import Copier

    destination = FakeDestination()
    Copier(FakeSource("a\nb\ncd"), destination).copy_multiple(4)

    assert destination.writes == ["a"]
