"""Calculator TDD Example - Ported from TDD Ebook
TDD implementation following the narrative from Grzegorz Gałęzowski's book
"""


def test_should_display_0_when_created() -> None:
    """Test 1: Calculator should display 0 on creation

    From the book: "In our case, 'turning on' is creating a calculator."
    This forms the sentence: "Calculator should display 0 when created"
    """
    from calculator_tdd_ebook.calculator import Calculator

    # GIVEN
    calculator = Calculator()

    # WHEN
    displayed_result = calculator.display()

    # THEN
    assert displayed_result == Calculator.INITIAL_VALUE


def test_should_display_entered_digits() -> None:
    """Test 2: Calculator should display entered digits

    From the book: Using constrained non-determinism to make the test more abstract
    and using DigitKeys enum to prevent invalid input like calculator.enter(123)
    """
    from calculator_tdd_ebook.any import Any
    from calculator_tdd_ebook.calculator import Calculator
    from calculator_tdd_ebook.digit_keys import DigitKeys

    # GIVEN
    calculator = Calculator()
    non_zero_digit = Any.other_than(DigitKeys.ZERO)
    any_digit1 = Any.of(DigitKeys)
    any_digit2 = Any.of(DigitKeys)

    # WHEN
    calculator.enter(non_zero_digit)
    calculator.enter(any_digit1)
    calculator.enter(any_digit2)

    # THEN
    assert calculator.display() == Any.string_consisting_of(
        non_zero_digit, any_digit1, any_digit2
    )


def test_should_display_only_one_zero_digit_if_it_is_the_only_entered_digit_even_if_it_is_entered_multiple_times() -> (
    None
):
    """Test 3: Calculator should display only one zero digit if it is the only entered digit even if it is entered multiple times

    From the book: This is a variation of the previous Statement dealing with the special case of zero
    """
    from calculator_tdd_ebook.any import Any
    from calculator_tdd_ebook.calculator import Calculator
    from calculator_tdd_ebook.digit_keys import DigitKeys

    # GIVEN
    calculator = Calculator()

    # WHEN
    calculator.enter(DigitKeys.ZERO)
    calculator.enter(DigitKeys.ZERO)
    calculator.enter(DigitKeys.ZERO)

    # THEN
    assert calculator.display() == Any.string_consisting_of(DigitKeys.ZERO)


def test_any_other_than_never_returns_the_excluded_digit() -> None:
    """Test 4: Any.other_than generates a digit key other than the excluded one

    Constrained non-determinism must never produce the excluded value,
    otherwise Statements relying on it (like Test 2) would be meaningless.
    """
    from calculator_tdd_ebook.any import Any
    from calculator_tdd_ebook.digit_keys import DigitKeys

    for excluded_digit in DigitKeys:
        # WHEN
        generated_digit = Any.other_than(excluded_digit)

        # THEN
        assert isinstance(generated_digit, DigitKeys)
        assert generated_digit != excluded_digit


def test_any_other_than_rejects_unsupported_types() -> None:
    """Test 5: Any.other_than raises NotImplementedError naming the unsupported type"""
    import pytest

    from calculator_tdd_ebook.any import Any

    # WHEN / THEN
    with pytest.raises(NotImplementedError) as excinfo:
        Any.other_than("not a digit key")

    assert str(excinfo.value) == "other_than not implemented for <class 'str'>"


def test_nonzero_digit_replaces_leading_zero() -> None:
    """Entering 0 then 5 displays "5", not "05" (calculator display semantics)"""
    from calculator_tdd_ebook.calculator import Calculator
    from calculator_tdd_ebook.digit_keys import DigitKeys

    calculator = Calculator()
    calculator.enter(DigitKeys.ZERO)
    calculator.enter(DigitKeys.FIVE)
    assert calculator.display() == "5"


def test_zero_after_nonzero_digits_is_kept() -> None:
    """Entering 1 then 0 then 5 displays "105" — interior zeros are significant"""
    from calculator_tdd_ebook.calculator import Calculator
    from calculator_tdd_ebook.digit_keys import DigitKeys

    calculator = Calculator()
    calculator.enter(DigitKeys.ONE)
    calculator.enter(DigitKeys.ZERO)
    calculator.enter(DigitKeys.FIVE)
    assert calculator.display() == "105"
