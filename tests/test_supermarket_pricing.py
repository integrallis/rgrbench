"""
Tests for Supermarket Pricing kata - checkout total with layered pricing rules
"""

import pytest


def test_empty_basket_totals_zero() -> None:
    """Test 1: Scanning nothing totals 0"""
    from supermarket_pricing import Checkout

    assert Checkout().total() == 0


def test_single_item_uses_unit_price() -> None:
    """Test 2: A single A costs its unit price of 50"""
    from supermarket_pricing import Checkout

    checkout = Checkout()
    checkout.scan("A")
    assert checkout.total() == 50


def test_two_different_items_add_up() -> None:
    """Test 3: A and B cost 50 + 30 = 80"""
    from supermarket_pricing import Checkout

    checkout = Checkout()
    checkout.scan("A")
    checkout.scan("B")
    assert checkout.total() == 80


def test_unit_prices_for_all_items() -> None:
    """Test 4: Unit prices are A 50, B 30, C 20, D 15"""
    from supermarket_pricing import Checkout

    for item, price in [("A", 50), ("B", 30), ("C", 20), ("D", 15)]:
        checkout = Checkout()
        checkout.scan(item)
        assert checkout.total() == price


def test_three_a_multi_buy() -> None:
    """Test 5: Three A cost the 130 deal price instead of 150"""
    from supermarket_pricing import Checkout

    checkout = Checkout()
    for _ in range(3):
        checkout.scan("A")
    assert checkout.total() == 130


def test_fourth_a_at_unit_price() -> None:
    """Test 6: Four A cost the deal plus one unit: 130 + 50 = 180"""
    from supermarket_pricing import Checkout

    checkout = Checkout()
    for _ in range(4):
        checkout.scan("A")
    assert checkout.total() == 180


def test_two_b_multi_buy() -> None:
    """Test 7: Two B cost the 45 deal price instead of 60"""
    from supermarket_pricing import Checkout

    checkout = Checkout()
    checkout.scan("B")
    checkout.scan("B")
    assert checkout.total() == 45


def test_third_b_at_unit_price() -> None:
    """Test 8: Three B cost the deal plus one unit: 45 + 30 = 75"""
    from supermarket_pricing import Checkout

    checkout = Checkout()
    for _ in range(3):
        checkout.scan("B")
    assert checkout.total() == 75


def test_scan_order_does_not_matter() -> None:
    """Test 9: A,B,A,B,A totals 175 in any scan order"""
    from supermarket_pricing import Checkout

    for order in [["A", "B", "A", "B", "A"], ["B", "A", "A", "B", "A"]]:
        checkout = Checkout()
        for item in order:
            checkout.scan(item)
        assert checkout.total() == 175


def test_bogof_pair_of_c() -> None:
    """Test 10: Two C cost 20 - the second one is free"""
    from supermarket_pricing import Checkout

    checkout = Checkout()
    checkout.scan("C")
    checkout.scan("C")
    assert checkout.total() == 20


def test_bogof_odd_c_pays_for_the_odd_one() -> None:
    """Test 11: Three C cost 40 - two paid, one free"""
    from supermarket_pricing import Checkout

    checkout = Checkout()
    for _ in range(3):
        checkout.scan("C")
    assert checkout.total() == 40


def test_no_special_for_d() -> None:
    """Test 12: Two D cost plain unit price, 30"""
    from supermarket_pricing import Checkout

    checkout = Checkout()
    checkout.scan("D")
    checkout.scan("D")
    assert checkout.total() == 30


def test_combo_d_plus_c() -> None:
    """Test 13: D and C together cost the 25 combo price"""
    from supermarket_pricing import Checkout

    checkout = Checkout()
    checkout.scan("D")
    checkout.scan("C")
    assert checkout.total() == 25


def test_combo_applies_once_per_qualifying_set() -> None:
    """Test 14: D,C,D is one combo plus one unit D: 25 + 15 = 40"""
    from supermarket_pricing import Checkout

    checkout = Checkout()
    for item in ["D", "C", "D"]:
        checkout.scan(item)
    assert checkout.total() == 40


def test_each_disjoint_pair_gets_the_combo() -> None:
    """Test 15: D,C,D,C forms two qualifying sets: 25 + 25 = 50"""
    from supermarket_pricing import Checkout

    checkout = Checkout()
    for item in ["D", "C", "D", "C"]:
        checkout.scan(item)
    assert checkout.total() == 50


def test_weighed_bananas_rounded_to_cent() -> None:
    """Test 16: Half a kilogram of Bananas costs 1.00 (0.995 rounds half up)"""
    from decimal import Decimal

    from supermarket_pricing import Checkout

    checkout = Checkout()
    checkout.scan_weighed("Bananas", "0.5")
    assert checkout.total() == Decimal("1.00")


def test_weighed_apples() -> None:
    """Test 17: Two kilograms of Apples cost 6.98"""
    from decimal import Decimal

    from supermarket_pricing import Checkout

    checkout = Checkout()
    checkout.scan_weighed("Apples", 2)
    assert checkout.total() == Decimal("6.98")


def test_weighed_line_rounds_half_up() -> None:
    """Test 18: 1.5 kg of Bananas is 2.985, rounded half up to 2.99"""
    from decimal import Decimal

    from supermarket_pricing import Checkout

    checkout = Checkout()
    checkout.scan_weighed("Bananas", "1.5")
    assert checkout.total() == Decimal("2.99")


def test_mixed_basket_combines_all_rules() -> None:
    """Test 19: Multi-buys plus a weighed item: 130 + 45 + 1.00 = 176.00"""
    from decimal import Decimal

    from supermarket_pricing import Checkout

    checkout = Checkout()
    for item in ["A", "A", "A", "B", "B"]:
        checkout.scan(item)
    checkout.scan_weighed("Bananas", "0.5")
    assert checkout.total() == Decimal("176.00")


def test_unknown_item_is_rejected() -> None:
    """Test 20: Scanning an unknown item raises with the item named"""
    from supermarket_pricing import Checkout

    with pytest.raises(ValueError, match="Unknown item: X"):
        Checkout().scan("X")


def test_unknown_weighed_item_is_rejected() -> None:
    """Test 21: Weighing an unknown item raises with the item named"""
    from supermarket_pricing import Checkout

    with pytest.raises(ValueError, match="Unknown item: Grapes"):
        Checkout().scan_weighed("Grapes", 1)


def test_non_positive_weight_is_rejected() -> None:
    """Test 22: A weighed item needs a positive weight"""
    from supermarket_pricing import Checkout

    with pytest.raises(ValueError, match="weight must be positive"):
        Checkout().scan_weighed("Bananas", 0)


def test_negative_weight_is_rejected_with_the_exact_message() -> None:
    """Test 23: A negative weight raises exactly 'weight must be positive'"""
    from supermarket_pricing import Checkout

    with pytest.raises(ValueError) as excinfo:
        Checkout().scan_weighed("Bananas", "-0.5")
    assert str(excinfo.value) == "weight must be positive"
