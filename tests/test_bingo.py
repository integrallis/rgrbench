"""Bingo Kata - card state, marking called numbers, and win detection
Columns B/I/N/G/O cover 1-15, 16-30, 31-45, 46-60, 61-75; the centre space is free.
"""

# Sample card, column-major: B, I, N (four numbers, centre free), G, O.
# Grid rows: [1,16,31,46,61] [2,17,32,47,62] [3,18,FREE,48,63] [4,19,33,49,64] [5,20,34,50,65]
CARD_NUMBERS = [
    1, 2, 3, 4, 5,
    16, 17, 18, 19, 20,
    31, 32, 33, 34,
    46, 47, 48, 49, 50,
    61, 62, 63, 64, 65,
]


def test_column_letter_for_range_starts() -> None:
    """Test 1: The lowest number of each column range maps to its letter"""
    from bingo import column_letter

    assert column_letter(1) == "B"
    assert column_letter(16) == "I"
    assert column_letter(31) == "N"
    assert column_letter(46) == "G"
    assert column_letter(61) == "O"


def test_column_letter_for_range_ends() -> None:
    """Test 2: The highest number of each column range maps to its letter"""
    from bingo import column_letter

    assert column_letter(15) == "B"
    assert column_letter(30) == "I"
    assert column_letter(45) == "N"
    assert column_letter(60) == "G"
    assert column_letter(75) == "O"


def test_column_letter_rejects_numbers_outside_one_to_seventy_five() -> None:
    """Test 3: Numbers outside 1-75 are not valid bingo calls"""
    import pytest

    from bingo import column_letter

    with pytest.raises(ValueError, match="between 1 and 75"):
        column_letter(0)
    with pytest.raises(ValueError, match="between 1 and 75"):
        column_letter(76)


def test_card_places_numbers_column_major() -> None:
    """Test 4: Card numbers fill the grid column by column (B, I, N, G, O)"""
    from bingo import BingoCard

    card = BingoCard(CARD_NUMBERS)
    assert card.number_at(0, 0) == 1
    assert card.number_at(4, 0) == 5
    assert card.number_at(0, 1) == 16
    assert card.number_at(1, 2) == 32
    assert card.number_at(3, 2) == 33
    assert card.number_at(0, 3) == 46
    assert card.number_at(4, 4) == 65


def test_centre_space_is_free_and_pre_marked() -> None:
    """Test 5: The centre of the N column holds no number and starts marked"""
    from bingo import BingoCard

    card = BingoCard(CARD_NUMBERS)
    assert card.number_at(2, 2) is None
    assert card.is_marked(2, 2) is True


def test_all_numbered_spaces_start_unmarked() -> None:
    """Test 6: Every space except the free centre starts unmarked"""
    from bingo import BingoCard

    card = BingoCard(CARD_NUMBERS)
    for row in range(5):
        for column in range(5):
            if (row, column) == (2, 2):
                continue
            assert card.is_marked(row, column) is False


def test_card_requires_exactly_twenty_four_numbers() -> None:
    """Test 7: A card holds 25 spaces, so 24 numbers plus the free space"""
    import pytest

    from bingo import BingoCard

    with pytest.raises(ValueError, match="exactly 24 numbers"):
        BingoCard(CARD_NUMBERS[:-1])


def test_card_numbers_must_be_unique() -> None:
    """Test 8: A card contains 24 unique numbers"""
    import pytest

    from bingo import BingoCard

    duplicated = CARD_NUMBERS[:-1] + [CARD_NUMBERS[0]]
    with pytest.raises(ValueError, match=r"^card numbers must be unique$"):
        BingoCard(duplicated)


def test_card_numbers_must_fit_their_column_range() -> None:
    """Test 9: A number outside its column's range is rejected"""
    import pytest

    from bingo import BingoCard

    invalid = list(CARD_NUMBERS)
    invalid[0] = 21  # 21 belongs to column I, not column B
    with pytest.raises(ValueError, match="not valid for column B"):
        BingoCard(invalid)


def test_marking_a_called_number_on_the_card() -> None:
    """Test 10: Calling a number on the card marks its space and reports a hit"""
    from bingo import BingoCard

    card = BingoCard(CARD_NUMBERS)
    assert card.mark(17) is True
    assert card.is_marked(1, 1) is True


def test_marking_a_called_number_not_on_the_card() -> None:
    """Test 11: Calling a valid number absent from the card marks nothing"""
    from bingo import BingoCard

    card = BingoCard(CARD_NUMBERS)
    assert card.mark(15) is False
    for row in range(5):
        for column in range(5):
            if (row, column) == (2, 2):
                continue
            assert card.is_marked(row, column) is False


def test_marking_rejects_numbers_outside_one_to_seventy_five() -> None:
    """Test 12: Calls outside 1-75 are invalid"""
    import pytest

    from bingo import BingoCard

    card = BingoCard(CARD_NUMBERS)
    with pytest.raises(ValueError, match="between 1 and 75"):
        card.mark(0)
    with pytest.raises(ValueError, match="between 1 and 75"):
        card.mark(76)


def test_new_card_has_no_bingo() -> None:
    """Test 13: A freshly dealt card has no completed line"""
    from bingo import BingoCard

    card = BingoCard(CARD_NUMBERS)
    assert card.has_bingo() is False


def test_horizontal_line_is_bingo() -> None:
    """Test 14: Five marked spaces across a row form a bingo"""
    from bingo import BingoCard

    card = BingoCard(CARD_NUMBERS)
    for number in (2, 17, 32, 47, 62):  # second row
        card.mark(number)
    assert card.has_bingo() is True


def test_middle_row_needs_only_four_marks() -> None:
    """Test 15: The free centre completes the middle row with four calls"""
    from bingo import BingoCard

    card = BingoCard(CARD_NUMBERS)
    for number in (3, 18, 48, 63):  # middle row around the free space
        card.mark(number)
    assert card.has_bingo() is True


def test_vertical_line_is_bingo() -> None:
    """Test 16: Five marked spaces down a column form a bingo"""
    from bingo import BingoCard

    card = BingoCard(CARD_NUMBERS)
    for number in (1, 2, 3, 4, 5):  # B column
        card.mark(number)
    assert card.has_bingo() is True


def test_n_column_needs_only_four_marks() -> None:
    """Test 17: The free centre completes the N column with four calls"""
    from bingo import BingoCard

    card = BingoCard(CARD_NUMBERS)
    for number in (31, 32, 33, 34):  # N column around the free space
        card.mark(number)
    assert card.has_bingo() is True


def test_diagonal_line_is_bingo() -> None:
    """Test 18: The top-left to bottom-right diagonal through the free space"""
    from bingo import BingoCard

    card = BingoCard(CARD_NUMBERS)
    for number in (1, 17, 49, 65):
        card.mark(number)
    assert card.has_bingo() is True


def test_anti_diagonal_line_is_bingo() -> None:
    """Test 19: The top-right to bottom-left diagonal through the free space"""
    from bingo import BingoCard

    card = BingoCard(CARD_NUMBERS)
    for number in (61, 47, 19, 5):
        card.mark(number)
    assert card.has_bingo() is True


def test_four_marks_in_a_row_are_not_bingo() -> None:
    """Test 20: An incomplete row is not a bingo"""
    from bingo import BingoCard

    card = BingoCard(CARD_NUMBERS)
    for number in (2, 17, 32, 47):  # second row minus its last space
        card.mark(number)
    assert card.has_bingo() is False


def test_scattered_marks_are_not_bingo() -> None:
    """Test 21: Marks that never complete a line are not a bingo"""
    from bingo import BingoCard

    card = BingoCard(CARD_NUMBERS)
    for number in (1, 17, 33, 50, 62):
        card.mark(number)
    assert card.has_bingo() is False


def test_marking_accepts_the_boundary_calls_one_and_seventy_five() -> None:
    """Test 22: The boundary calls 1 and 75 are valid"""
    from bingo import BingoCard

    card = BingoCard(CARD_NUMBERS)
    assert card.mark(1) is True
    assert card.mark(75) is False  # a valid call absent from this card
