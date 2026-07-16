"""
Tests for the Heavy Metal Bake Sale kata (tddbuddy.com/katas/heavy-metal-bake-sale).
Items: B = Brownie $0.75, M = Muffin $1.00, C = Cake Pop $1.35, W = Water $1.50.
"""

import pytest


def test_total_for_a_single_brownie() -> None:
    """Test 1: A single brownie totals $0.75"""
    from heavy_metal_bake_sale import BakeSale

    assert BakeSale().total("B") == "$0.75"


@pytest.mark.parametrize(
    "code,expected_total",
    [("B", "$0.75"), ("M", "$1.00"), ("C", "$1.35"), ("W", "$1.50")],
)
def test_each_item_is_priced_per_the_inventory_table(
    code: str, expected_total: str
) -> None:
    """Test 2: Each item code totals its listed price"""
    from heavy_metal_bake_sale import BakeSale

    assert BakeSale().total(code) == expected_total


def test_total_for_brownie_cake_pop_and_water() -> None:
    """Test 3: Order B,C,W totals $3.60 per the price table (0.75 + 1.35 + 1.50);
    the upstream example's $3.50 contradicts the table and is treated as a typo"""
    from heavy_metal_bake_sale import BakeSale

    assert BakeSale().total("B,C,W") == "$3.60"


def test_total_for_cake_pop_and_muffin() -> None:
    """Test 4: Order C,M totals $2.35 (spec example)"""
    from heavy_metal_bake_sale import BakeSale

    assert BakeSale().total("C,M") == "$2.35"


def test_total_tolerates_spaces_around_codes() -> None:
    """Test 5: Whitespace around comma-delimited codes is ignored"""
    from heavy_metal_bake_sale import BakeSale

    assert BakeSale().total(" B , C , W ") == "$3.60"


def test_total_with_repeated_items() -> None:
    """Test 6: Repeated codes are summed (B,B,M = $2.50)"""
    from heavy_metal_bake_sale import BakeSale

    assert BakeSale().total("B,B,M") == "$2.50"


def test_paying_the_exact_amount_gives_zero_change() -> None:
    """Test 7: Paying $0.75 for a brownie returns change of $0.00 (spec example)"""
    from heavy_metal_bake_sale import BakeSale

    assert BakeSale().pay("B", "0.75") == "$0.00"


def test_overpaying_returns_the_difference_as_change() -> None:
    """Test 8: Paying $4.00 for B,C,W ($3.60 per the price table) returns $0.40 change"""
    from heavy_metal_bake_sale import BakeSale

    assert BakeSale().pay("B,C,W", "4.00") == "$0.40"


def test_underpaying_is_refused_with_not_enough_money() -> None:
    """Test 9: Paying $2.00 for C,M ($2.35) raises 'Not enough money' (spec example)"""
    from heavy_metal_bake_sale import BakeSale, NotEnoughMoneyError

    with pytest.raises(NotEnoughMoneyError, match="Not enough money"):
        BakeSale().pay("C,M", "2.00")


def test_underpaying_leaves_stock_untouched() -> None:
    """Test 10: A refused payment does not consume any stock"""
    from heavy_metal_bake_sale import BakeSale, NotEnoughMoneyError

    sale = BakeSale({"C": 5, "M": 5})
    with pytest.raises(NotEnoughMoneyError):
        sale.pay("C,M", "2.00")
    assert sale.stock_of("C") == 5
    assert sale.stock_of("M") == 5


def test_out_of_stock_item_is_reported_by_name_when_totalling() -> None:
    """Test 11: Ordering water with none left raises 'Water is out of stock' (spec example)"""
    from heavy_metal_bake_sale import BakeSale, OutOfStockError

    sale = BakeSale({"B": 48, "M": 36, "C": 24, "W": 0})
    with pytest.raises(OutOfStockError, match="Water is out of stock"):
        sale.total("W")


def test_out_of_stock_item_is_reported_by_name_when_paying() -> None:
    """Test 12: Paying for an order containing a sold-out muffin raises 'Muffin is out of stock'"""
    from heavy_metal_bake_sale import BakeSale, OutOfStockError

    sale = BakeSale({"B": 1, "M": 0, "C": 1, "W": 1})
    with pytest.raises(OutOfStockError, match="Muffin is out of stock"):
        sale.pay("C,M", "5.00")


def test_ordering_more_than_the_remaining_stock_is_out_of_stock() -> None:
    """Test 13: Ordering two brownies when only one remains raises 'Brownie is out of stock'"""
    from heavy_metal_bake_sale import BakeSale, OutOfStockError

    sale = BakeSale({"B": 1})
    with pytest.raises(OutOfStockError, match="Brownie is out of stock"):
        sale.total("B,B")


def test_completed_sale_decrements_stock() -> None:
    """Test 14: A completed sale consumes one unit per ordered code"""
    from heavy_metal_bake_sale import BakeSale

    sale = BakeSale({"B": 2, "C": 2, "W": 2})
    sale.pay("B,C,W", "4.00")
    assert sale.stock_of("B") == 1
    assert sale.stock_of("C") == 1
    assert sale.stock_of("W") == 1


def test_quoting_a_total_does_not_decrement_stock() -> None:
    """Test 15: Quoting a total is not a sale and leaves stock untouched"""
    from heavy_metal_bake_sale import BakeSale

    sale = BakeSale({"B": 2})
    sale.total("B")
    assert sale.stock_of("B") == 2


def test_default_inventory_matches_the_specification() -> None:
    """Test 16: Default stock is 48 brownies, 36 muffins, 24 cake pops, 30 waters"""
    from heavy_metal_bake_sale import BakeSale

    sale = BakeSale()
    assert sale.stock_of("B") == 48
    assert sale.stock_of("M") == 36
    assert sale.stock_of("C") == 24
    assert sale.stock_of("W") == 30


def test_repeated_sales_exhaust_stock() -> None:
    """Test 17: Selling the last unit makes the next order out of stock"""
    from heavy_metal_bake_sale import BakeSale, OutOfStockError

    sale = BakeSale({"W": 1})
    sale.pay("W", "1.50")
    with pytest.raises(OutOfStockError, match="Water is out of stock"):
        sale.total("W")


def test_unknown_item_code_is_rejected() -> None:
    """Test 18: An unknown item code raises ValueError"""
    from heavy_metal_bake_sale import BakeSale

    with pytest.raises(ValueError):
        BakeSale().total("B,X")


def test_stock_of_an_unstocked_item_is_zero() -> None:
    """Test 19: An item absent from the inventory mapping has a stock of zero"""
    from heavy_metal_bake_sale import BakeSale

    assert BakeSale({"B": 1}).stock_of("W") == 0


def test_ordering_an_unstocked_item_is_out_of_stock() -> None:
    """Test 20: Ordering an item absent from the inventory mapping is refused as out of stock"""
    from heavy_metal_bake_sale import BakeSale, OutOfStockError

    sale = BakeSale({"B": 1})
    with pytest.raises(OutOfStockError, match="Water is out of stock"):
        sale.total("W")


def test_short_payment_refusal_message_is_exact() -> None:
    """Test 21: A short payment is refused with exactly 'Not enough money'"""
    from heavy_metal_bake_sale import BakeSale, NotEnoughMoneyError

    with pytest.raises(NotEnoughMoneyError) as excinfo:
        BakeSale().pay("C,M", "2.00")
    assert str(excinfo.value) == "Not enough money"


def test_unknown_item_code_is_named_in_the_error() -> None:
    """Test 22: The rejection of an unknown item code names the offending code"""
    from heavy_metal_bake_sale import BakeSale

    with pytest.raises(ValueError, match="X"):
        BakeSale().total("B,X")


def test_total_of_an_empty_order_is_zero_dollars() -> None:
    """Test 23: An order containing no items totals $0.00"""
    from heavy_metal_bake_sale import BakeSale

    assert BakeSale().total("") == "$0.00"
