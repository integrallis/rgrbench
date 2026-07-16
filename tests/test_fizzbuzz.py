"""
Port of C# FizzBuzzKata TestFizzBuzz.cs
Complete port with all test cases
"""

import pytest

from fizzbuzz_kata.fizzbuzz import FizzBuzz


def test_can_test_fizz() -> None:
    """Port of CanTestFizz - tests full sequence generation"""
    expected_result = (
        "1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz 16 17 Fizz 19 Buzz "
        "Fizz 22 23 Fizz Buzz 26 Fizz 28 29 FizzBuzz 31 32 Fizz 34 Buzz Fizz 37 38 Fizz Buzz "
        "41 Fizz 43 44 FizzBuzz 46 47 Fizz 49 Buzz Fizz 52 53 Fizz Buzz 56 Fizz 58 59 FizzBuzz "
        "61 62 Fizz 64 Buzz Fizz 67 68 Fizz Buzz 71 Fizz 73 74 FizzBuzz 76 77 Fizz 79 Buzz "
        "Fizz 82 83 Fizz Buzz 86 Fizz 88 89 FizzBuzz 91 92 Fizz 94 Buzz Fizz 97 98 Fizz Buzz"
    )
    assert FizzBuzz.print_fizz_buzz() == expected_result


def test_can_test_single_number_1() -> None:
    """Port of TestCase(1, '1')"""
    result = FizzBuzz.print_fizz_buzz(1)
    assert result == "1"


def test_can_test_single_number_3() -> None:
    """Port of TestCase(3, 'Fizz')"""
    result = FizzBuzz.print_fizz_buzz(3)
    assert result == "Fizz"


def test_can_test_single_number_5() -> None:
    """Port of TestCase(5, 'Buzz')"""
    result = FizzBuzz.print_fizz_buzz(5)
    assert result == "Buzz"


def test_can_test_single_number_15() -> None:
    """Port of TestCase(15, 'FizzBuzz')"""
    result = FizzBuzz.print_fizz_buzz(15)
    assert result == "FizzBuzz"


def test_can_test_single_number_30() -> None:
    """Port of TestCase(30, 'FizzBuzz')"""
    result = FizzBuzz.print_fizz_buzz(30)
    assert result == "FizzBuzz"


def test_can_test_single_number_100() -> None:
    """Upper boundary: 100 is a valid input and is divisible by 5"""
    result = FizzBuzz.print_fizz_buzz(100)
    assert result == "Buzz"


def test_can_throw_argument_exception_when_number_is_negative_1() -> None:
    """Port of TestCase(-1) - should throw exception"""
    with pytest.raises(ValueError) as exc_info:
        FizzBuzz.print_fizz_buzz(-1)
    assert (
        str(exc_info.value)
        == "entered number is [-1], which does not meet rule, entered number should be between 1 to 100."
    )


def test_can_throw_argument_exception_when_number_is_101() -> None:
    """Port of TestCase(101) - should throw exception"""
    with pytest.raises(ValueError) as exc_info:
        FizzBuzz.print_fizz_buzz(101)
    assert (
        str(exc_info.value)
        == "entered number is [101], which does not meet rule, entered number should be between 1 to 100."
    )


def test_can_throw_argument_exception_when_number_is_0() -> None:
    """Port of TestCase(0) - should throw exception"""
    with pytest.raises(ValueError) as exc_info:
        FizzBuzz.print_fizz_buzz(0)
    assert (
        str(exc_info.value)
        == "entered number is [0], which does not meet rule, entered number should be between 1 to 100."
    )
