"""
Port of C# StringCalculator TestCalculator.cs
First test: empty string returns 0
"""

import pytest

from string_calculator.calculator import Calculator


def test_add_return_zero_when_supplied_empty_string() -> None:
    """Port of TestCase('') - empty string returns 0"""
    result = Calculator.add("")
    assert result == 0


def test_add_return_zero_when_supplied_null() -> None:
    """Port of TestCase(null) - None returns 0"""
    result = Calculator.add(None)
    assert result == 0


def test_add_return_number_when_supplied_single_1() -> None:
    """Port of TestCase('1', 1) - single '1' returns 1"""
    result = Calculator.add("1")
    assert result == 1


def test_add_return_sum_when_supplied_two_numbers() -> None:
    """Port of TestCase('0,1', 1) - '0,1' returns 1"""
    result = Calculator.add("0,1")
    assert result == 1


def test_add_return_zero_when_supplied_single_0() -> None:
    """Port of TestCase('0', 0) - single '0' returns 0"""
    result = Calculator.add("0")
    assert result == 0


def test_add_return_number_when_supplied_single_2() -> None:
    """Port of TestCase('2', 2) - single '2' returns 2"""
    result = Calculator.add("2")
    assert result == 2


def test_add_return_number_when_supplied_single_3() -> None:
    """Port of TestCase('3', 3) - single '3' returns 3"""
    result = Calculator.add("3")
    assert result == 3


def test_add_return_sum_when_supplied_multiple_numbers_with_555() -> None:
    """Port of TestCase('0,1,2,3,4,555', 565) - sum of multiple numbers"""
    result = Calculator.add("0,1,2,3,4,555")
    assert result == 565


def test_add_return_sum_with_newline_delimiter() -> None:
    """Port of TestCase('3\\n2', 5) - newline as delimiter"""
    result = Calculator.add("3\n2")
    assert result == 5


def test_add_return_sum_with_mixed_delimiters_1() -> None:
    """Port of TestCase('1\\n2,3', 6) - mixed newline and comma"""
    result = Calculator.add("1\n2,3")
    assert result == 6


def test_add_return_sum_with_mixed_delimiters_2() -> None:
    """Port of TestCase('1\\n2\\n3,4,5', 15) - multiple mixed delimiters"""
    result = Calculator.add("1\n2\n3,4,5")
    assert result == 15


# Port of AddReturnSumWhenSuppliedMultipleNumbersInString test cases
def test_add_return_sum_0_1() -> None:
    """Port of TestCase('0,1', 1)"""
    result = Calculator.add("0,1")
    assert result == 1


def test_add_return_sum_0_1_1() -> None:
    """Port of TestCase('0,1,1', 2)"""
    result = Calculator.add("0,1,1")
    assert result == 2


def test_add_return_sum_0_2() -> None:
    """Port of TestCase('0,2', 2)"""
    result = Calculator.add("0,2")
    assert result == 2


def test_add_return_sum_0_2_2() -> None:
    """Port of TestCase('0,2,2', 4)"""
    result = Calculator.add("0,2,2")
    assert result == 4


def test_add_return_sum_0_3() -> None:
    """Port of TestCase('0,3', 3)"""
    result = Calculator.add("0,3")
    assert result == 3


def test_add_return_sum_0_3_2() -> None:
    """Port of TestCase('0,3,2', 5)"""
    result = Calculator.add("0,3,2")
    assert result == 5


def test_add_return_sum_0_3_3() -> None:
    """Port of TestCase('0,3,3', 6)"""
    result = Calculator.add("0,3,3")
    assert result == 6


# Port of AddReturnSumByIgnoringMoreThanThousandWhenSuppliedMultipleNumbersInString
def test_add_ignore_numbers_greater_than_1000() -> None:
    """Port of TestCase('0,3,1001', 3) - ignore numbers > 1000"""
    result = Calculator.add("0,3,1001")
    assert result == 3


def test_add_include_1000_exactly() -> None:
    """Port of TestCase('0,3,1000', 1003) - include 1000 exactly"""
    result = Calculator.add("0,3,1000")
    assert result == 1003


# Port of AddWhenGivenDefinedDelimiterUsesThatDelimiter
def test_add_with_custom_delimiter_star() -> None:
    """Port of TestCase('//*\n1*2', 3) - custom delimiter '*'"""
    result = Calculator.add("//*\n1*2")
    assert result == 3


def test_add_with_custom_delimiter_semicolon() -> None:
    """Port of TestCase('//;\n1;2', 3) - custom delimiter ';'"""
    result = Calculator.add("//;\n1;2")
    assert result == 3


def test_add_with_custom_delimiter_semicolon_multiple() -> None:
    """Port of TestCase('//;\n1;2;3;4;5;6;7;8;9;10', 55) - custom delimiter with multiple numbers"""
    result = Calculator.add("//;\n1;2;3;4;5;6;7;8;9;10")
    assert result == 55


# Port of AddThrowArgumentExceptionWhenSuppliedStringDoesNotMeetRule
def test_add_throw_exception_for_negative_number() -> None:
    """Port of TestCase('1,-1', -1) - should throw exception for negative numbers"""
    with pytest.raises(ValueError) as exc_info:
        Calculator.add("1,-1")
    assert (
        str(exc_info.value)
        == "string contains [-1], which does not meet rule. entered number should not negative."
    )


def test_add_throw_exception_for_negative_with_custom_delimiter() -> None:
    """Test negative number with custom delimiter to cover line 17"""
    with pytest.raises(ValueError) as exc_info:
        Calculator.add("//;\n1;-2")
    assert (
        str(exc_info.value)
        == "string contains [-2], which does not meet rule. entered number should not negative."
    )


def test_add_throw_exception_for_single_negative_number() -> None:
    """Test single negative number to cover line 35"""
    with pytest.raises(ValueError) as exc_info:
        Calculator.add("-5")
    assert (
        str(exc_info.value)
        == "string contains [-5], which does not meet rule. entered number should not negative."
    )


def test_add_include_single_number_1000_exactly() -> None:
    """A single number of exactly 1000 is included in the sum"""
    result = Calculator.add("1000")
    assert result == 1000


def test_add_ignore_single_number_greater_than_1000() -> None:
    """A single number greater than 1000 is ignored, yielding 0"""
    result = Calculator.add("1001")
    assert result == 0


def test_add_with_custom_delimiter_and_zero() -> None:
    """Zero is a valid non-negative number with a custom delimiter"""
    result = Calculator.add("//;\n0;5")
    assert result == 5


def test_add_with_custom_delimiter_include_1000_exactly() -> None:
    """A number of exactly 1000 is included in the sum with a custom delimiter"""
    result = Calculator.add("//;\n1000;3")
    assert result == 1003


def test_add_with_custom_delimiter_ignore_numbers_greater_than_1000() -> None:
    """Numbers greater than 1000 are ignored with a custom delimiter"""
    result = Calculator.add("//;\n1001;3")
    assert result == 3


def test_add_with_custom_delimiter_and_trailing_newline() -> None:
    """The delimiter definition ends at the first newline; a trailing newline
    after the numbers is treated as insignificant whitespace"""
    result = Calculator.add("//;\n1;2\n")
    assert result == 3
