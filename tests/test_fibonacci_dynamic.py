"""Fibonacci Dynamic Programming - An4ik Python TDD Port

Demonstrates memoized fibonacci implementation through TDD
"""


def test_the_first_number_should_be_zero() -> None:
    """Test 1: The first fibonacci number should be 0

    From An4ik example: F(1) = 0 (using 1-based indexing)
    """
    from fibonacci_dynamic import Fibonacci

    # GIVEN
    fib = Fibonacci()

    # WHEN
    result = fib.get_number(1)

    # THEN
    assert result == 0, f"The first number is 0, not {result}"


def test_the_second_number_should_be_one() -> None:
    """Test 2: The second fibonacci number should be 1

    From An4ik example: F(2) = 1 (using 1-based indexing)
    """
    from fibonacci_dynamic import Fibonacci

    # GIVEN
    fib = Fibonacci()

    # WHEN
    result = fib.get_number(2)

    # THEN
    assert result == 1, f"The second number is 1, not {result}"


def test_the_third_number_should_be_one() -> None:
    """Test 3: The third fibonacci number should be 1

    From An4ik example: F(3) = 1 (using 1-based indexing)
    """
    from fibonacci_dynamic import Fibonacci

    # GIVEN
    fib = Fibonacci()

    # WHEN
    result = fib.get_number(3)

    # THEN
    assert result == 1, f"The third number is 1, not {result}"


def test_long_argument_should_calculate_with_memoization() -> None:
    """Test 4: Test with longer argument that requires dynamic programming

    From An4ik example: F(6) = 5 (using 1-based indexing)
    This forces implementation of memoized fibonacci algorithm for efficiency.
    """
    from fibonacci_dynamic import Fibonacci

    # GIVEN
    fib = Fibonacci()

    # WHEN
    result = fib.get_number(6)

    # THEN
    assert result == 5, f"The sixth number is 5, not {result}"


def test_negative_number_should_raise_exception() -> None:
    """Test 5: Negative number should raise ValueError

    From An4ik example: F(n) for n < 1 should raise ValueError
    Tests input validation for invalid fibonacci sequence index.
    """
    import pytest

    from fibonacci_dynamic import Fibonacci

    # GIVEN
    fib = Fibonacci()

    # WHEN/THEN
    with pytest.raises(
        ValueError, match="Fibonacci sequence is not defined for negative numbers"
    ):
        fib.get_number(-1)


def test_negative_number_error_message() -> None:
    """Test 6: The validation error carries the exact expected message

    From An4ik example: the ValueError message is part of the observable
    contract for invalid fibonacci sequence indexes.
    """
    import pytest

    from fibonacci_dynamic import Fibonacci

    # GIVEN
    fib = Fibonacci()

    # WHEN/THEN
    with pytest.raises(ValueError) as exc_info:
        fib.get_number(-1)
    assert (
        str(exc_info.value) == "Fibonacci sequence is not defined for negative numbers"
    )
