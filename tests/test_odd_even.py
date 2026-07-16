"""
Port of C# OddEvenKata TestOddEven.cs
Complete port with all test cases
"""

from odd_even_kata.odd_even import OddEven


# Port of CanPrintOddEven test cases
def test_can_print_odd_even_1_50() -> None:
    """Port of TestCase(1, 50)"""
    result = OddEven.print_odd_even(1, 50)
    assert result is not None


def test_can_print_odd_even_1_100() -> None:
    """Port of TestCase(1, 100)"""
    result = OddEven.print_odd_even(1, 100)
    assert result is not None


def test_can_print_odd_even_5_150() -> None:
    """Port of TestCase(5, 150)"""
    result = OddEven.print_odd_even(5, 150)
    assert result is not None


# Port of CanPrintOddEvenForSingleNumber test cases
def test_can_print_odd_even_for_single_number_1() -> None:
    """Port of TestCase(1, 'Odd')"""
    result = OddEven.print_single_odd_even(1)
    assert result == "Odd"


def test_can_print_odd_even_for_single_number_3() -> None:
    """Port of TestCase(3, '3')"""
    result = OddEven.print_single_odd_even(3)
    assert result == "3"


def test_can_print_odd_even_for_single_number_5() -> None:
    """Port of TestCase(5, '5')"""
    result = OddEven.print_single_odd_even(5)
    assert result == "5"


def test_can_print_odd_even_for_single_number_4() -> None:
    """Port of TestCase(4, 'Even')"""
    result = OddEven.print_single_odd_even(4)
    assert result == "Even"


def test_can_print_odd_even_for_single_number_9() -> None:
    """Port of TestCase(9, 'Odd')"""
    result = OddEven.print_single_odd_even(9)
    assert result == "Odd"


def test_can_print_odd_even_for_single_number_10() -> None:
    """Port of TestCase(10, 'Even')"""
    result = OddEven.print_single_odd_even(10)
    assert result == "Even"


# Range test cases with exact expected output
def test_print_odd_even_range_1_10() -> None:
    """Odds print 'Odd', evens print 'Even', odd primes print themselves"""
    result = OddEven.print_odd_even(1, 10)
    assert result == "Odd Even 3 Even 5 Even 7 Even Odd Even"


def test_print_odd_even_negative_start_begins_at_1() -> None:
    """A negative start number is clamped so the range begins at 1"""
    result = OddEven.print_odd_even(-5, 3)
    assert result == "Odd Even 3"


def test_print_odd_even_start_zero_includes_zero() -> None:
    """A start of 0 is not clamped; 0 prints as itself"""
    result = OddEven.print_odd_even(0, 2)
    assert result == "0 Odd Even"


def test_print_odd_even_empty_range_returns_empty_string() -> None:
    """When the start number exceeds the last number the result is empty"""
    result = OddEven.print_odd_even(5, 3)
    assert result == ""


# Single-number classification boundary test cases
def test_can_print_odd_even_for_single_number_2() -> None:
    """2 is reported as 'Even'; the even label takes precedence over primality"""
    result = OddEven.print_single_odd_even(2)
    assert result == "Even"


def test_can_print_odd_even_for_single_number_11() -> None:
    """11 is an odd prime, so it prints as itself"""
    result = OddEven.print_single_odd_even(11)
    assert result == "11"


def test_can_print_odd_even_for_single_number_25() -> None:
    """25 = 5 * 5 is an odd composite, so it prints 'Odd'"""
    result = OddEven.print_single_odd_even(25)
    assert result == "Odd"


def test_can_print_odd_even_for_single_number_0() -> None:
    """0 is neither odd, even (per the kata), nor prime, so it prints as itself"""
    result = OddEven.print_single_odd_even(0)
    assert result == "0"


def test_can_print_odd_even_for_single_number_negative_4() -> None:
    """Negative even numbers are not labeled 'Even'; they print as themselves"""
    result = OddEven.print_single_odd_even(-4)
    assert result == "-4"
