"""Change Calculator - Test-Driven Development
Porting from JavaScript implementation
"""


def test_single_coin_change() -> None:
    """Test 1: Single coin exact change"""
    from change_calculator.calculator import ChangeCalculator

    calc = ChangeCalculator()
    result = calc.calculate_change(25)
    assert result == [25]


def test_multiple_coins() -> None:
    """Test 2: Multiple coins of same denomination"""
    from change_calculator.calculator import ChangeCalculator

    calc = ChangeCalculator()
    result = calc.calculate_change(50)
    assert result == [25, 25]


def test_greedy_algorithm() -> None:
    """Test 3: Greedy algorithm with mixed denominations"""
    from change_calculator.calculator import ChangeCalculator

    calc = ChangeCalculator()
    result = calc.calculate_change(41)
    assert result == [25, 10, 5, 1]


def test_zero_amount() -> None:
    """Test 4: Zero amount returns empty list"""
    from change_calculator.calculator import ChangeCalculator

    calc = ChangeCalculator()
    result = calc.calculate_change(0)
    assert result == []
