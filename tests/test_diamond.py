"""
Tests for the Diamond kata (tddbuddy.com/katas/diamond).
The diamond starts at 'A', widens to the given letter, then narrows back.
"""

import pytest


def test_diamond_for_a_is_a_single_letter() -> None:
    """Test 1: Diamond for 'A' is the single letter A"""
    from diamond import diamond

    assert diamond("A") == "A"


def test_diamond_for_b_matches_specification_example() -> None:
    """Test 2: Diamond for 'B' matches the three-row example"""
    from diamond import diamond

    assert diamond("B") == " A\nB B\n A"


def test_diamond_for_c_matches_specification_example() -> None:
    """Test 3: Diamond for 'C' matches the five-row example"""
    from diamond import diamond

    expected = "\n".join(
        [
            "  A",
            " B B",
            "C   C",
            " B B",
            "  A",
        ]
    )
    assert diamond("C") == expected


def test_diamond_for_d_matches_specification_example() -> None:
    """Test 4: Diamond for 'D' matches the seven-row example"""
    from diamond import diamond

    expected = "\n".join(
        [
            "   A",
            "  B B",
            " C   C",
            "D     D",
            " C   C",
            "  B B",
            "   A",
        ]
    )
    assert diamond("D") == expected


def test_diamond_for_e_first_and_middle_rows() -> None:
    """Test 5: Diamond for 'E' starts with '    A' and its middle row is 'E       E'"""
    from diamond import diamond

    rows = diamond("E").split("\n")
    assert rows[0] == "    A"
    assert rows[len(rows) // 2] == "E       E"


@pytest.mark.parametrize(
    "letter,expected_size",
    [("A", 1), ("B", 3), ("C", 5), ("E", 9)],
)
def test_height_and_width_match_specification_table(
    letter: str, expected_size: int
) -> None:
    """Test 6: Height and widest row width follow the spec table (1, 3, 5, 9)"""
    from diamond import diamond

    rows = diamond(letter).split("\n")
    assert len(rows) == expected_size
    assert max(len(row) for row in rows) == expected_size


def test_first_and_last_rows_contain_a_single_a() -> None:
    """Test 7: First and last rows contain a single 'A'"""
    from diamond import diamond

    rows = diamond("F").split("\n")
    assert rows[0].strip() == "A"
    assert rows[-1].strip() == "A"


def test_inner_rows_contain_exactly_two_identical_letters() -> None:
    """Test 8: All rows except the first and last have exactly two identical letters"""
    from diamond import diamond

    rows = diamond("E").split("\n")
    for row in rows[1:-1]:
        letters = row.replace(" ", "")
        assert len(letters) == 2
        assert letters[0] == letters[1]


def test_diamond_is_vertically_symmetric() -> None:
    """Test 9: The top half mirrors the bottom half"""
    from diamond import diamond

    rows = diamond("G").split("\n")
    assert rows == rows[::-1]


def test_diamond_is_horizontally_symmetric() -> None:
    """Test 10: Each row, padded to full width, reads the same reversed"""
    from diamond import diamond

    rows = diamond("F").split("\n")
    width = max(len(row) for row in rows)
    for row in rows:
        padded = row.ljust(width)
        assert padded == padded[::-1]


def test_inner_gap_grows_by_two_per_row() -> None:
    """Test 11: Inner spaces between the letter pair increase by 2 each row down the top half"""
    from diamond import diamond

    rows = diamond("E").split("\n")
    top_half = rows[: len(rows) // 2 + 1]
    gaps = [len(row.strip()) - 2 for row in top_half[1:]]
    assert gaps == [1, 3, 5, 7]


def test_lowercase_input_is_normalised_to_uppercase() -> None:
    """Test 12: Lowercase input produces the same diamond as uppercase"""
    from diamond import diamond

    assert diamond("c") == diamond("C")


def test_rows_use_letters_in_alphabetical_sequence() -> None:
    """Test 13: Row letters run A..target..A with no letter skipped"""
    from diamond import diamond

    rows = diamond("D").split("\n")
    letters = [row.strip()[0] for row in rows]
    assert letters == ["A", "B", "C", "D", "C", "B", "A"]


@pytest.mark.parametrize("bad_input", ["1", "?", "", "AB", " ", "-", "[", "^"])
def test_invalid_input_is_rejected(bad_input: str) -> None:
    """Test 14: Anything other than a single letter A-Z raises ValueError"""
    from diamond import diamond

    with pytest.raises(ValueError):
        diamond(bad_input)


def test_diamond_for_z_spans_the_full_alphabet() -> None:
    """Test 15: 'Z' is accepted and yields a 51-row diamond with Z at the widest row"""
    from diamond import diamond

    rows = diamond("Z").split("\n")
    assert len(rows) == 51
    assert rows[25] == "Z" + " " * 49 + "Z"


def test_single_character_that_uppercases_to_two_letters_is_rejected() -> None:
    """Test 16: 'ß' (whose uppercase form is 'SS') is not a letter A-Z and raises ValueError"""
    from diamond import diamond

    with pytest.raises(ValueError):
        diamond("ß")


def test_rejection_message_is_exact() -> None:
    """Test 17: Invalid input is rejected with exactly 'Input must be a single letter A-Z'"""
    from diamond import diamond

    with pytest.raises(ValueError) as excinfo:
        diamond("42")
    assert str(excinfo.value) == "Input must be a single letter A-Z"
