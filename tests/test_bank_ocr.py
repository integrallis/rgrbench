"""Bank OCR kata tests.

Entries are three 27-character lines of ASCII-art digits (3x3 cells of pipes and
underscores). Covers parsing, the mod-11 checksum, ILL/ERR classification, and
single-segment error correction with unique, ambiguous and unfixable outcomes.

The glyph rows below are transcribed from the kata's digit reference and used to
build entries independently of the implementation.
"""

import pytest

_TOP = {
    "0": " _ ",
    "1": "   ",
    "2": " _ ",
    "3": " _ ",
    "4": "   ",
    "5": " _ ",
    "6": " _ ",
    "7": " _ ",
    "8": " _ ",
    "9": " _ ",
}
_MIDDLE = {
    "0": "| |",
    "1": "  |",
    "2": " _|",
    "3": " _|",
    "4": "|_|",
    "5": "|_ ",
    "6": "|_ ",
    "7": "  |",
    "8": "|_|",
    "9": "|_|",
}
_BOTTOM = {
    "0": "|_|",
    "1": "  |",
    "2": "|_ ",
    "3": " _|",
    "4": "  |",
    "5": " _|",
    "6": "|_|",
    "7": "  |",
    "8": "|_|",
    "9": " _|",
}


def entry_for(digits: str) -> str:
    """Render a 9-digit string as a three-line OCR entry."""
    return "\n".join(
        "".join(row[digit] for digit in digits) for row in (_TOP, _MIDDLE, _BOTTOM)
    )


def blank_out(entry: str, line: int, column: int) -> str:
    """Replace one character of an entry with a space (remove one segment)."""
    lines = entry.split("\n")
    lines[line] = lines[line][:column] + " " + lines[line][column + 1 :]
    return "\n".join(lines)


def test_parses_all_zeros() -> None:
    """Test 1: nine zero cells parse to '000000000'."""
    from bank_ocr import parse_entry

    assert parse_entry(entry_for("000000000")) == "000000000"


def test_parses_all_ones() -> None:
    """Test 2: nine one cells parse to '111111111'."""
    from bank_ocr import parse_entry

    assert parse_entry(entry_for("111111111")) == "111111111"


def test_parses_ascending_digits() -> None:
    """Test 3: the canonical '123456789' entry parses correctly."""
    from bank_ocr import parse_entry

    assert parse_entry(entry_for("123456789")) == "123456789"


@pytest.mark.parametrize("digit", list("0123456789"))
def test_parses_each_digit(digit: str) -> None:
    """Test 4: every digit glyph is recognised (entry of nine repeats)."""
    from bank_ocr import parse_entry

    assert parse_entry(entry_for(digit * 9)) == digit * 9


def test_unreadable_cell_parses_as_question_mark() -> None:
    """Test 5: a cell matching no digit is reported as '?' in its position."""
    from bank_ocr import parse_entry

    corrupted = blank_out(entry_for("123456789"), line=1, column=2)

    assert parse_entry(corrupted) == "?23456789"


def test_parse_rejects_wrong_line_count() -> None:
    """Test 6: an entry without exactly three lines raises ValueError."""
    from bank_ocr import parse_entry

    with pytest.raises(ValueError, match="entry must have exactly three lines"):
        parse_entry(" _ \n| |")


def test_parse_tolerates_trailing_blank_line() -> None:
    """Test 7: a trailing newline (blank fourth line) is accepted."""
    from bank_ocr import parse_entry

    assert parse_entry(entry_for("000000000") + "\n") == "000000000"


def test_checksum_accepts_spec_example() -> None:
    """Test 8: 345882865 satisfies (d1*9 + ... + d9*1) mod 11 == 0."""
    from bank_ocr import checksum_valid

    assert checksum_valid("345882865") is True


def test_checksum_accepts_ascending_digits() -> None:
    """Test 9: 123456789 has weighted sum 165 = 15 * 11, so it is valid."""
    from bank_ocr import checksum_valid

    assert checksum_valid("123456789") is True


def test_checksum_accepts_all_zeros() -> None:
    """Test 10: 000000000 has weighted sum 0, which is divisible by 11."""
    from bank_ocr import checksum_valid

    assert checksum_valid("000000000") is True


def test_checksum_rejects_all_ones() -> None:
    """Test 11: 111111111 has weighted sum 45, and 45 mod 11 == 1."""
    from bank_ocr import checksum_valid

    assert checksum_valid("111111111") is False


def test_checksum_rejects_non_digit_and_wrong_length() -> None:
    """Test 12: strings with '?' or the wrong length are never valid."""
    from bank_ocr import checksum_valid

    assert checksum_valid("34588286?") is False
    assert checksum_valid("12345678") is False
    assert checksum_valid("1234567890") is False


def test_status_of_valid_entry_is_number_only() -> None:
    """Test 13: a readable entry passing the checksum is reported as-is."""
    from bank_ocr import account_status

    assert account_status(entry_for("345882865")) == "345882865"


def test_status_of_checksum_failure_is_err() -> None:
    """Test 14: a readable entry failing the checksum gains ' ERR'."""
    from bank_ocr import account_status

    assert account_status(entry_for("111111111")) == "111111111 ERR"


def test_status_of_unreadable_entry_is_ill() -> None:
    """Test 15: an entry with an unreadable cell gains ' ILL'."""
    from bank_ocr import account_status

    corrupted = blank_out(entry_for("123456789"), line=1, column=2)

    assert account_status(corrupted) == "?23456789 ILL"


def test_fix_leaves_valid_entry_unchanged() -> None:
    """Test 16: error correction reports a valid entry as its number."""
    from bank_ocr import fix_entry

    assert fix_entry(entry_for("123456789")) == "123456789"


def test_fix_all_ones_to_711111111() -> None:
    """Test 17: 111111111 (sum 45 = 1 mod 11) is uniquely fixed by 1->7 at
    position 1 (adds 6*9 = 54, giving 99 = 9 * 11)."""
    from bank_ocr import fix_entry

    assert fix_entry(entry_for("111111111")) == "711111111"


def test_fix_all_sevens_to_777777177() -> None:
    """Test 18: 777777777 (sum 315 = 7 mod 11) is uniquely fixed by 7->1 at
    position 7 (subtracts 6*3 = 18, giving 297 = 27 * 11)."""
    from bank_ocr import fix_entry

    assert fix_entry(entry_for("777777777")) == "777777177"


def test_fix_200000000_to_200800000() -> None:
    """Test 19: 200000000 (sum 18 = 7 mod 11) is uniquely fixed by 0->8 at
    position 4 (adds 8*6 = 48, giving 66 = 6 * 11)."""
    from bank_ocr import fix_entry

    assert fix_entry(entry_for("200000000")) == "200800000"


def test_fix_all_threes_to_333393333() -> None:
    """Test 20: 333333333 (sum 135 = 3 mod 11) is uniquely fixed by 3->9 at
    position 5 (adds 6*5 = 30, giving 165 = 15 * 11)."""
    from bank_ocr import fix_entry

    assert fix_entry(entry_for("333333333")) == "333393333"


def test_fix_all_eights_is_ambiguous() -> None:
    """Test 21: 888888888 (sum 360 = 8 mod 11) has three one-segment fixes
    (8->6 at position 6, 8->0 at position 9, 8->9 at position 7)."""
    from bank_ocr import fix_entry

    assert fix_entry(entry_for("888888888")) == (
        "888888888 AMB ['888886888', '888888880', '888888988']"
    )


def test_fix_all_fives_is_ambiguous() -> None:
    """Test 22: 555555555 (sum 225 = 5 mod 11) has two one-segment fixes
    (5->6 at position 4, 5->9 at position 3)."""
    from bank_ocr import fix_entry

    assert fix_entry(entry_for("555555555")) == (
        "555555555 AMB ['555655555', '559555555']"
    )


def test_fix_490067715_is_ambiguous() -> None:
    """Test 23: 490067715 (sum 194 = 7 mod 11) has three one-segment fixes
    (7->1 at position 7, 5->9 at position 9, 0->8 at position 4)."""
    from bank_ocr import fix_entry

    assert fix_entry(entry_for("490067715")) == (
        "490067715 AMB ['490067115', '490067719', '490867715']"
    )


def test_fix_recovers_single_unreadable_cell() -> None:
    """Test 24: '?23456789' with the '1' cell missing its pipe segment has the
    unique one-segment completion '123456789', which is valid."""
    from bank_ocr import fix_entry

    corrupted = blank_out(entry_for("123456789"), line=1, column=2)

    assert fix_entry(corrupted) == "123456789"


def test_fix_cannot_recover_two_unreadable_cells() -> None:
    """Test 25: with two unreadable cells no single-cell change helps, so the
    ILL classification is reported."""
    from bank_ocr import fix_entry

    corrupted = blank_out(entry_for("123456789"), line=1, column=2)
    corrupted = blank_out(corrupted, line=2, column=3)

    assert fix_entry(corrupted) == "??3456789 ILL"


def test_fix_reports_err_when_no_candidate_exists() -> None:
    """Test 26: 222222222 fails the checksum (90 = 2 mod 11) and the '2' glyph
    is not one segment away from any other digit, so ' ERR' is reported."""
    from bank_ocr import fix_entry

    assert fix_entry(entry_for("222222222")) == "222222222 ERR"


def test_parse_rejects_wrong_line_count_with_exact_message() -> None:
    """Test 27: the wrong-line-count ValueError carries exactly the specified
    message 'entry must have exactly three lines'."""
    from bank_ocr import parse_entry

    with pytest.raises(ValueError) as excinfo:
        parse_entry(" _ \n| |")
    assert str(excinfo.value) == "entry must have exactly three lines"


def test_parse_pads_short_lines_with_trailing_spaces() -> None:
    """Test 28: lines shorter than 27 characters are padded on the right, so an
    entry whose trailing spaces were stripped still reads the same digits."""
    from bank_ocr import parse_entry

    entry = entry_for("711111111")
    stripped = "\n".join(line.rstrip() for line in entry.split("\n"))

    assert parse_entry(stripped) == "711111111"
