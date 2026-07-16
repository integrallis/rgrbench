"""Roman Numerals Kata - Test-Driven Development
Porting from JavaScript implementation
"""

import pytest

from roman_numerals.converter import to_roman

# Test data from the JavaScript implementation
TEST_CASES = [
    (1, "I"),
    (2, "II"),
    (3, "III"),
    (4, "IV"),
    (5, "V"),
    (6, "VI"),
    (7, "VII"),
    (8, "VIII"),
    (9, "IX"),
    (10, "X"),
    (11, "XI"),
    (14, "XIV"),
    (15, "XV"),
    (19, "XIX"),
    (20, "XX"),
    (27, "XXVII"),
    (30, "XXX"),
    (40, "XL"),
    (49, "XLIX"),
    (50, "L"),
    (87, "LXXXVII"),
    (90, "XC"),
    (100, "C"),
    (239, "CCXXXIX"),
    (400, "CD"),
    (444, "CDXLIV"),
    (500, "D"),
    (692, "DCXCII"),
    (900, "CM"),
    (999, "CMXCIX"),
    (1000, "M"),
    (2016, "MMXVI"),
]


@pytest.mark.parametrize("number,expected", TEST_CASES)
def test_to_roman(number: int, expected: str) -> None:
    """Test converting numbers to Roman numerals"""
    assert to_roman(number) == expected
