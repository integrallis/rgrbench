"""
Money Example - Test-Driven Development by Kent Beck
Implementing multi-currency money with proper TDD
"""


def test_multiplication() -> None:
    """Test 1: $5 * 2 = $10"""
    from money.money import Money

    five = Money.dollar(5)
    product = five.times(2)
    assert product.equals(Money.dollar(10))


def test_equality() -> None:
    """Test 2: Money equality"""
    from money.money import Money

    assert Money.dollar(5).equals(Money.dollar(5))
    assert not Money.dollar(5).equals(Money.dollar(6))


def test_privacy() -> None:
    """Test 3: Amount should be private (immutable)"""
    from money.money import Money

    five = Money.dollar(5)
    five.times(2)
    assert five.equals(Money.dollar(5))


def test_franc_multiplication() -> None:
    """Test 4: Franc multiplication"""
    from money.money import Money

    five = Money.franc(5)
    assert Money.franc(10).equals(five.times(2))
    assert Money.franc(15).equals(five.times(3))


def test_common_currency_equality() -> None:
    """Test 5: Equality for same currency"""
    from money.money import Money

    assert Money.franc(5).equals(Money.franc(5))
    assert not Money.franc(5).equals(Money.franc(6))


def test_different_currency_inequality() -> None:
    """Test 6: Different currencies are not equal"""
    from money.money import Money

    assert not Money.franc(5).equals(Money.dollar(5))


def test_currency() -> None:
    """Test 7: Currency is accessible"""
    from money.money import Money

    assert Money.dollar(1).currency() == "USD"
    assert Money.franc(1).currency() == "CHF"


def test_simple_addition() -> None:
    """Test 8: Simple addition of same currency"""
    from money.money import Bank, Money

    five = Money.dollar(5)
    sum_expr = five.plus(five)
    bank = Bank()
    reduced = bank.reduce(sum_expr, "USD")
    assert reduced.equals(Money.dollar(10))


def test_reduce_money() -> None:
    """Test 9: Reduce money through bank"""
    from money.money import Bank, Money

    bank = Bank()
    result = bank.reduce(Money.dollar(1), "USD")
    assert result.equals(Money.dollar(1))

    # Test currency conversion path
    bank.add_rate("CHF", "USD", 2)
    result = bank.reduce(Money.franc(2), "USD")
    assert result.equals(Money.dollar(1))


def test_mixed_addition() -> None:
    """Test 10: Mixed currency addition with exchange"""
    from money.money import Bank, Money

    bank = Bank()
    bank.add_rate("CHF", "USD", 2)
    result = bank.reduce(Money.franc(2), "USD")
    assert result.equals(Money.dollar(1))


def test_sum_plus_money() -> None:
    """Test 11: Sum plus Money operation"""
    from money.money import Bank, Money, Sum

    five_bucks = Money.dollar(5)
    ten_francs = Money.franc(10)
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)
    sum_expr = Sum(five_bucks, ten_francs).plus(five_bucks)
    result = bank.reduce(sum_expr, "USD")
    assert result.equals(Money.dollar(15))


def test_sum_times() -> None:
    """Test 12: Sum times operation"""
    from money.money import Bank, Money, Sum

    five_bucks = Money.dollar(5)
    ten_francs = Money.franc(10)
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)
    sum_expr = Sum(five_bucks, ten_francs).times(2)
    result = bank.reduce(sum_expr, "USD")
    assert result.equals(Money.dollar(20))


def test_reduce_money_truncates_fractional_conversion() -> None:
    """Test 13: Conversion uses integer division, truncating fractions"""
    from money.money import Bank, Money

    bank = Bank()
    bank.add_rate("CHF", "USD", 2)
    result = bank.reduce(Money.franc(5), "USD")
    assert result.equals(Money.dollar(2))


def test_reduce_money_without_registered_rate() -> None:
    """Test 14: Reducing with no registered rate raises"""
    import pytest

    from money.money import Bank, Money

    bank = Bank()
    with pytest.raises(KeyError, match="USD->CHF"):
        bank.reduce(Money.dollar(10), "CHF")
