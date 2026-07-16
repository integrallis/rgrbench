"""Fibonacci - Dynamic Programming Implementation
Ported from Python implementation by An4ik
"""


def test_first_fibonacci_number() -> None:
    """Test 1: The first Fibonacci number is 0"""
    from fibonacci.dynamic import Fibonacci

    fib = Fibonacci()
    assert fib.get_number(1) == 0


def test_second_fibonacci_number() -> None:
    """Test 2: The second Fibonacci number is 1"""
    from fibonacci.dynamic import Fibonacci

    fib = Fibonacci()
    assert fib.get_number(2) == 1


def test_third_fibonacci_number() -> None:
    """Test 3: The third Fibonacci number is 1"""
    from fibonacci.dynamic import Fibonacci

    fib = Fibonacci()
    assert fib.get_number(3) == 1


def test_larger_fibonacci_numbers() -> None:
    """Test 4: Larger Fibonacci numbers"""
    from fibonacci.dynamic import Fibonacci

    fib = Fibonacci()
    assert fib.get_number(10) == 34
    assert fib.get_number(15) == 377


def test_negative_number_raises_error() -> None:
    """Test 5: Negative numbers raise TypeError"""
    import pytest

    from fibonacci.dynamic import Fibonacci

    fib = Fibonacci()
    with pytest.raises(TypeError):
        fib.get_number(-1)


def test_number_below_one_raises_error_with_message() -> None:
    """Test 6: Numbers below 1 raise TypeError explaining the sequence starts from 1"""
    import pytest

    from fibonacci.dynamic import Fibonacci

    fib = Fibonacci()
    with pytest.raises(TypeError) as excinfo:
        fib.get_number(0)
    assert str(excinfo.value) == "Fibonacci numbers start from 1"
