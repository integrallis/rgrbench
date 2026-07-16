"""
Port of C# LCDDigits TestLCDDigits.cs
Complete port with all test cases
"""

from lcd_digits.lcd_digits import LCDDigits


def test_digit_the_number_0() -> None:
    """Port of digit_the_number_0"""
    expect = "._." + "\n" + "|.|" + "\n" + "|_|" + "\n"

    assert LCDDigits.get_digits(0) == expect


def test_digit_the_number_1() -> None:
    """Port of digit_the_number_1"""
    expect = "..." + "\n" + "..|" + "\n" + "..|" + "\n"

    assert LCDDigits.get_digits(1) == expect


def test_digit_the_number_10() -> None:
    """Port of digit_the_number_10"""
    expect = "..." + "._." + "\n" + "..|" + "|.|" + "\n" + "..|" + "|_|" + "\n"

    assert LCDDigits.get_digits(10) == expect


def test_digit_the_number_100() -> None:
    """Port of digit_the_number_100"""
    expect = (
        "..."
        + "._."
        + "._."
        + "\n"
        + "..|"
        + "|.|"
        + "|.|"
        + "\n"
        + "..|"
        + "|_|"
        + "|_|"
        + "\n"
    )

    assert LCDDigits.get_digits(100) == expect
