"""Sum Example - Basic TDD Example from Kent Beck
Ported from JavaScript implementation
"""


def test_sum_two_numbers() -> None:
    """Test 1: Should sum two numbers and return the result"""
    from sum_example.calculator import sum_numbers

    assert sum_numbers(1, 1) == 2


def test_sum_negative_numbers() -> None:
    """Test 2: Should handle negative numbers"""
    from sum_example.calculator import sum_numbers

    assert sum_numbers(-1, 1) == 0
    assert sum_numbers(-5, -3) == -8


def test_sum_with_zero() -> None:
    """Test 3: Should handle zero correctly"""
    from sum_example.calculator import sum_numbers

    assert sum_numbers(0, 0) == 0
    assert sum_numbers(5, 0) == 5
    assert sum_numbers(0, -5) == -5
