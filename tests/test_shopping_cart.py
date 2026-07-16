"""Tests for the Shopping Cart kata."""


def test_added_item_reports_its_subtotal() -> None:
    """Test 1: A line's subtotal is unit price times quantity"""
    from shopping_cart import ShoppingCart

    cart = ShoppingCart()
    cart.add_item("widget", 19.99, quantity=3)

    assert cart.item_subtotal("widget") == 59.97
    assert cart.quantity_of("widget") == 3


def test_adding_the_same_item_again_accumulates_quantity() -> None:
    """Test 2: Re-adding an item tops up its quantity on the same line"""
    from shopping_cart import ShoppingCart

    cart = ShoppingCart()
    cart.add_item("widget", 10.0, quantity=2)
    cart.add_item("widget", 10.0, quantity=3)

    assert cart.quantity_of("widget") == 5
    assert cart.item_subtotal("widget") == 50.0


def test_cart_total_sums_all_line_subtotals() -> None:
    """Test 3: The total is the sum of every line's subtotal"""
    from shopping_cart import ShoppingCart

    cart = ShoppingCart()
    cart.add_item("widget", 10.0, quantity=2)
    cart.add_item("gadget", 7.5, quantity=4)

    assert cart.total() == 50.0


def test_empty_cart_totals_zero() -> None:
    """Test 4: An empty cart totals 0.0"""
    from shopping_cart import ShoppingCart

    cart = ShoppingCart()

    assert cart.total() == 0.0
    assert cart.subtotal() == 0.0
    assert cart.quantity_of("anything") == 0


def test_removed_item_no_longer_counts() -> None:
    """Test 5: Removing an item drops its line from the total"""
    from shopping_cart import ShoppingCart

    cart = ShoppingCart()
    cart.add_item("widget", 10.0, quantity=2)
    cart.add_item("gadget", 5.0, quantity=1)

    cart.remove_item("widget")

    assert cart.quantity_of("widget") == 0
    assert cart.total() == 5.0


def test_operations_on_missing_items_are_rejected() -> None:
    """Test 6: Removing, updating, or pricing an absent item raises ValueError"""
    import pytest

    from shopping_cart import ShoppingCart

    cart = ShoppingCart()

    with pytest.raises(ValueError) as excinfo:
        cart.remove_item("ghost")
    assert str(excinfo.value) == "item [ghost] is not in the cart"

    with pytest.raises(ValueError) as excinfo:
        cart.update_quantity("ghost", 2)
    assert str(excinfo.value) == "item [ghost] is not in the cart"

    with pytest.raises(ValueError) as excinfo:
        cart.item_subtotal("ghost")
    assert str(excinfo.value) == "item [ghost] is not in the cart"


def test_update_quantity_reprices_the_line() -> None:
    """Test 7: Updating a quantity changes the line subtotal"""
    from shopping_cart import ShoppingCart

    cart = ShoppingCart()
    cart.add_item("widget", 10.0, quantity=2)

    cart.update_quantity("widget", 7)

    assert cart.quantity_of("widget") == 7
    assert cart.item_subtotal("widget") == 70.0


def test_updating_quantity_to_zero_removes_the_line() -> None:
    """Test 8: Setting quantity to zero removes the item"""
    from shopping_cart import ShoppingCart

    cart = ShoppingCart()
    cart.add_item("widget", 10.0, quantity=2)

    cart.update_quantity("widget", 0)

    assert cart.quantity_of("widget") == 0
    assert cart.total() == 0.0


def test_invalid_add_arguments_are_rejected() -> None:
    """Test 9: Empty names, negative prices, and non-positive quantities raise"""
    import pytest

    from shopping_cart import ShoppingCart

    cart = ShoppingCart()

    with pytest.raises(ValueError) as excinfo:
        cart.add_item("", 10.0)
    assert str(excinfo.value) == "item name must not be empty"

    with pytest.raises(ValueError) as excinfo:
        cart.add_item("widget", -0.5)
    assert str(excinfo.value) == "unit_price must be non-negative, got [-0.5]"

    with pytest.raises(ValueError) as excinfo:
        cart.add_item("widget", 10.0, quantity=0)
    assert str(excinfo.value) == "quantity must be at least 1, got [0]"


def test_negative_quantity_update_is_rejected() -> None:
    """Test 10: update_quantity refuses negative values"""
    import pytest

    from shopping_cart import ShoppingCart

    cart = ShoppingCart()
    cart.add_item("widget", 10.0, quantity=2)

    with pytest.raises(ValueError) as excinfo:
        cart.update_quantity("widget", -1)
    assert str(excinfo.value) == "quantity must be non-negative, got [-1]"


def test_percentage_discount_reduces_the_total() -> None:
    """Test 11: A 10% discount on 59.97 leaves 53.97"""
    from shopping_cart import PercentageDiscount, ShoppingCart

    cart = ShoppingCart()
    cart.add_item("widget", 19.99, quantity=3)
    cart.add_discount(PercentageDiscount(10))

    assert cart.total() == 53.97


def test_percentage_discount_bounds_are_enforced() -> None:
    """Test 12: Percentages must be greater than 0 and at most 100"""
    import pytest

    from shopping_cart import PercentageDiscount

    for bad in (0, -5, 101):
        with pytest.raises(ValueError) as excinfo:
            PercentageDiscount(bad)
        assert (
            str(excinfo.value)
            == f"percent must be greater than 0 and at most 100, got [{bad}]"
        )


def test_fixed_amount_discount_reduces_the_total() -> None:
    """Test 13: A 15.00 discount on 100.00 leaves 85.00"""
    from shopping_cart import FixedAmountDiscount, ShoppingCart

    cart = ShoppingCart()
    cart.add_item("gadget", 25.0, quantity=4)
    cart.add_discount(FixedAmountDiscount(15.0))

    assert cart.total() == 85.0


def test_fixed_amount_discount_never_drops_the_total_below_zero() -> None:
    """Test 14: A discount larger than the subtotal clamps the total at 0.00"""
    from shopping_cart import FixedAmountDiscount, ShoppingCart

    cart = ShoppingCart()
    cart.add_item("widget", 5.0, quantity=1)
    cart.add_discount(FixedAmountDiscount(20.0))

    assert cart.total() == 0.0


def test_non_positive_fixed_discount_is_rejected() -> None:
    """Test 15: A fixed discount amount must be positive"""
    import pytest

    from shopping_cart import FixedAmountDiscount

    with pytest.raises(ValueError) as excinfo:
        FixedAmountDiscount(0)
    assert str(excinfo.value) == "amount must be positive, got [0]"


def test_cart_discounts_apply_in_registration_order_fixed_first() -> None:
    """Test 16: On 100.00, fixed 10 then 50% yields (100-10)*0.5 = 45.00"""
    from shopping_cart import FixedAmountDiscount, PercentageDiscount, ShoppingCart

    cart = ShoppingCart()
    cart.add_item("gadget", 25.0, quantity=4)
    cart.add_discount(FixedAmountDiscount(10.0))
    cart.add_discount(PercentageDiscount(50))

    assert cart.total() == 45.0


def test_cart_discounts_apply_in_registration_order_percentage_first() -> None:
    """Test 17: On 100.00, 50% then fixed 10 yields 100*0.5-10 = 40.00"""
    from shopping_cart import FixedAmountDiscount, PercentageDiscount, ShoppingCart

    cart = ShoppingCart()
    cart.add_item("gadget", 25.0, quantity=4)
    cart.add_discount(PercentageDiscount(50))
    cart.add_discount(FixedAmountDiscount(10.0))

    assert cart.total() == 40.0


def test_buy_x_get_y_free_prices_only_the_paid_units() -> None:
    """Test 18: Buy 2 get 1 free on 6 units charges for 4"""
    from shopping_cart import BuyXGetYFree, ShoppingCart

    cart = ShoppingCart()
    cart.add_item("cola", 2.0, quantity=6)
    cart.add_offer(BuyXGetYFree("cola", buy=2, get=1))

    assert cart.item_subtotal("cola") == 8.0
    assert cart.total() == 8.0


def test_buy_x_get_y_free_remainder_units_are_paid() -> None:
    """Test 19: Buy 2 get 1 free charges 2 of 2 units and 4 of 5 units"""
    from shopping_cart import BuyXGetYFree, ShoppingCart

    cart = ShoppingCart()
    cart.add_item("cola", 2.0, quantity=2)
    cart.add_offer(BuyXGetYFree("cola", buy=2, get=1))

    assert cart.item_subtotal("cola") == 4.0

    cart.update_quantity("cola", 5)  # one full group free + 2 paid remainder
    assert cart.item_subtotal("cola") == 8.0


def test_buy_x_get_y_free_parameters_must_be_positive() -> None:
    """Test 20: Buy and get counts below one are rejected"""
    import pytest

    from shopping_cart import BuyXGetYFree

    with pytest.raises(ValueError) as excinfo:
        BuyXGetYFree("cola", buy=0, get=1)
    assert str(excinfo.value) == "buy must be at least 1, got [0]"

    with pytest.raises(ValueError) as excinfo:
        BuyXGetYFree("cola", buy=2, get=0)
    assert str(excinfo.value) == "get must be at least 1, got [0]"


def test_bulk_price_applies_at_and_above_the_threshold() -> None:
    """Test 21: Three or more soaps at 4.00 reprice to 2.50 each"""
    from shopping_cart import BulkPrice, ShoppingCart

    cart = ShoppingCart()
    cart.add_item("soap", 4.0, quantity=3)
    cart.add_offer(BulkPrice("soap", min_quantity=3, unit_price=2.5))

    assert cart.item_subtotal("soap") == 7.5

    cart.update_quantity("soap", 5)
    assert cart.item_subtotal("soap") == 12.5


def test_bulk_price_does_not_apply_below_the_threshold() -> None:
    """Test 22: Two soaps stay at the regular 4.00 unit price"""
    from shopping_cart import BulkPrice, ShoppingCart

    cart = ShoppingCart()
    cart.add_item("soap", 4.0, quantity=2)
    cart.add_offer(BulkPrice("soap", min_quantity=3, unit_price=2.5))

    assert cart.item_subtotal("soap") == 8.0


def test_bulk_price_parameters_are_validated() -> None:
    """Test 23: Bulk threshold below two and negative bulk price are rejected"""
    import pytest

    from shopping_cart import BulkPrice

    with pytest.raises(ValueError) as excinfo:
        BulkPrice("soap", min_quantity=1, unit_price=2.5)
    assert str(excinfo.value) == "min_quantity must be at least 2, got [1]"

    with pytest.raises(ValueError) as excinfo:
        BulkPrice("soap", min_quantity=3, unit_price=-1.0)
    assert str(excinfo.value) == "unit_price must be non-negative, got [-1.0]"


def test_limited_stock_caps_the_quantity() -> None:
    """Test 24: Requests beyond an item's stock raise InsufficientStockError"""
    import pytest

    from shopping_cart import InsufficientStockError, ShoppingCart

    cart = ShoppingCart()

    with pytest.raises(InsufficientStockError) as excinfo:
        cart.add_item("rare", 99.0, quantity=6, stock=5)
    assert str(excinfo.value) == "only [5] of [rare] in stock, requested [6]"

    cart.add_item("rare", 99.0, quantity=4, stock=5)
    with pytest.raises(InsufficientStockError) as excinfo:
        cart.add_item("rare", 99.0, quantity=2)
    assert str(excinfo.value) == "only [5] of [rare] in stock, requested [6]"

    with pytest.raises(InsufficientStockError) as excinfo:
        cart.update_quantity("rare", 6)
    assert str(excinfo.value) == "only [5] of [rare] in stock, requested [6]"
    assert cart.quantity_of("rare") == 4


def test_maximum_quantity_per_order_is_enforced() -> None:
    """Test 25: Requests beyond an item's per-order cap raise MaxQuantityExceededError"""
    import pytest

    from shopping_cart import MaxQuantityExceededError, ShoppingCart

    cart = ShoppingCart()
    cart.add_item("sale-item", 1.0, quantity=2, max_quantity=3)

    with pytest.raises(MaxQuantityExceededError) as excinfo:
        cart.add_item("sale-item", 1.0, quantity=2)
    assert str(excinfo.value) == "maximum [3] of [sale-item] per order, requested [4]"

    with pytest.raises(MaxQuantityExceededError) as excinfo:
        cart.update_quantity("sale-item", 4)
    assert str(excinfo.value) == "maximum [3] of [sale-item] per order, requested [4]"

    cart.update_quantity("sale-item", 3)
    assert cart.quantity_of("sale-item") == 3


def test_non_combinable_items_are_skipped_by_cart_discounts() -> None:
    """Test 26: A 10% discount leaves a non-discountable line untouched"""
    from shopping_cart import PercentageDiscount, ShoppingCart

    cart = ShoppingCart()
    cart.add_item("gift card", 50.0, quantity=1, discountable=False)
    cart.add_item("toy", 30.0, quantity=1)
    cart.add_discount(PercentageDiscount(10))

    assert cart.total() == 77.0  # 30 * 0.9 + 50


def test_fixed_discount_cannot_eat_into_non_combinable_items() -> None:
    """Test 27: Clamping applies to the discountable portion only"""
    from shopping_cart import FixedAmountDiscount, ShoppingCart

    cart = ShoppingCart()
    cart.add_item("gift card", 50.0, quantity=1, discountable=False)
    cart.add_item("toy", 5.0, quantity=1)
    cart.add_discount(FixedAmountDiscount(20.0))

    assert cart.total() == 50.0  # toy portion clamps at 0, gift card intact


def test_offer_attachment_rules_are_enforced() -> None:
    """Test 28: Offers reject absent items, non-combinable items, and doubling up"""
    import pytest

    from shopping_cart import BulkPrice, BuyXGetYFree, ShoppingCart

    cart = ShoppingCart()

    with pytest.raises(ValueError) as excinfo:
        cart.add_offer(BuyXGetYFree("ghost", buy=2, get=1))
    assert str(excinfo.value) == "item [ghost] is not in the cart"

    cart.add_item("gift card", 50.0, quantity=1, discountable=False)
    with pytest.raises(ValueError) as excinfo:
        cart.add_offer(BuyXGetYFree("gift card", buy=2, get=1))
    assert str(excinfo.value) == "item [gift card] cannot be combined with discounts"

    cart.add_item("cola", 2.0, quantity=6)
    cart.add_offer(BuyXGetYFree("cola", buy=2, get=1))
    with pytest.raises(ValueError) as excinfo:
        cart.add_offer(BulkPrice("cola", min_quantity=3, unit_price=1.5))
    assert str(excinfo.value) == "item [cola] already has an offer"


def test_item_offers_apply_before_cart_level_discounts() -> None:
    """Test 29: Buy 2 get 1 free reshapes the line, then the percentage applies"""
    from shopping_cart import BuyXGetYFree, PercentageDiscount, ShoppingCart

    cart = ShoppingCart()
    cart.add_item("cola", 2.0, quantity=6)  # offer prices this at 8.00
    cart.add_offer(BuyXGetYFree("cola", buy=2, get=1))
    cart.add_discount(PercentageDiscount(50))

    assert cart.total() == 4.0


def test_offer_with_empty_item_name_is_rejected() -> None:
    """Test 30: An offer's item name must not be empty"""
    import pytest

    from shopping_cart import BulkPrice, BuyXGetYFree

    with pytest.raises(ValueError) as excinfo:
        BuyXGetYFree("", buy=2, get=1)
    assert str(excinfo.value) == "item name must not be empty"

    with pytest.raises(ValueError) as excinfo:
        BulkPrice("", min_quantity=3, unit_price=2.5)
    assert str(excinfo.value) == "item name must not be empty"


def test_buy_one_get_one_free_is_a_valid_offer() -> None:
    """Test 31: Buy 1 get 1 free on 4 units charges for 2"""
    from shopping_cart import BuyXGetYFree, ShoppingCart

    cart = ShoppingCart()
    cart.add_item("cola", 2.0, quantity=4)
    cart.add_offer(BuyXGetYFree("cola", buy=1, get=1))

    assert cart.item_subtotal("cola") == 4.0


def test_buy_x_get_many_free_counts_free_units_in_partial_groups() -> None:
    """Test 32: Buy 1 get 2 free on 5 units charges for 2 - a full group plus one paid, one free"""
    from shopping_cart import BuyXGetYFree, ShoppingCart

    cart = ShoppingCart()
    cart.add_item("cola", 2.0, quantity=5)
    cart.add_offer(BuyXGetYFree("cola", buy=1, get=2))

    assert cart.item_subtotal("cola") == 4.0


def test_bulk_price_boundary_values_are_accepted() -> None:
    """Test 33: A bulk threshold of two and a bulk price of zero are valid"""
    from shopping_cart import BulkPrice, ShoppingCart

    cart = ShoppingCart()
    cart.add_item("soap", 4.0, quantity=2)
    cart.add_offer(BulkPrice("soap", min_quantity=2, unit_price=0.0))

    assert cart.item_subtotal("soap") == 0.0


def test_one_percent_discount_is_valid() -> None:
    """Test 34: A 1% discount on 100.00 leaves 99.00"""
    from shopping_cart import PercentageDiscount, ShoppingCart

    cart = ShoppingCart()
    cart.add_item("gadget", 25.0, quantity=4)
    cart.add_discount(PercentageDiscount(1))

    assert cart.total() == 99.0


def test_hundred_percent_discount_zeroes_the_total() -> None:
    """Test 35: A 100% discount takes the total to 0.00"""
    from shopping_cart import PercentageDiscount, ShoppingCart

    cart = ShoppingCart()
    cart.add_item("gadget", 25.0, quantity=4)
    cart.add_discount(PercentageDiscount(100))

    assert cart.total() == 0.0


def test_fixed_discounts_smaller_than_one_are_valid() -> None:
    """Test 36: A 0.75 discount on 10.00 leaves 9.25"""
    from shopping_cart import FixedAmountDiscount, ShoppingCart

    cart = ShoppingCart()
    cart.add_item("widget", 5.0, quantity=2)
    cart.add_discount(FixedAmountDiscount(0.75))

    assert cart.total() == 9.25


def test_default_quantity_is_one() -> None:
    """Test 37: Adding without a quantity puts one unit in the cart"""
    from shopping_cart import ShoppingCart

    cart = ShoppingCart()
    cart.add_item("widget", 10.0)

    assert cart.quantity_of("widget") == 1
    assert cart.item_subtotal("widget") == 10.0


def test_zero_priced_items_are_allowed() -> None:
    """Test 38: A unit price of zero is non-negative and subtotals to zero"""
    from shopping_cart import ShoppingCart

    cart = ShoppingCart()
    cart.add_item("freebie", 0.0, quantity=3)

    assert cart.item_subtotal("freebie") == 0.0


def test_zero_stock_is_a_valid_limit_but_admits_nothing() -> None:
    """Test 39: Zero stock is a valid limit; any request exceeds it"""
    import pytest

    from shopping_cart import InsufficientStockError, ShoppingCart

    cart = ShoppingCart()

    with pytest.raises(InsufficientStockError) as excinfo:
        cart.add_item("gone", 5.0, quantity=1, stock=0)
    assert str(excinfo.value) == "only [0] of [gone] in stock, requested [1]"


def test_negative_stock_is_rejected() -> None:
    """Test 40: A negative stock value raises with the value named"""
    import pytest

    from shopping_cart import ShoppingCart

    cart = ShoppingCart()

    with pytest.raises(ValueError) as excinfo:
        cart.add_item("widget", 10.0, stock=-1)
    assert str(excinfo.value) == "stock must be non-negative, got [-1]"


def test_max_quantity_of_one_is_valid() -> None:
    """Test 41: A per-order cap of one admits a single unit"""
    from shopping_cart import ShoppingCart

    cart = ShoppingCart()
    cart.add_item("limited", 9.99, quantity=1, max_quantity=1)

    assert cart.quantity_of("limited") == 1


def test_non_positive_max_quantity_is_rejected() -> None:
    """Test 42: A per-order cap below one raises with the value named"""
    import pytest

    from shopping_cart import ShoppingCart

    cart = ShoppingCart()

    with pytest.raises(ValueError) as excinfo:
        cart.add_item("widget", 10.0, max_quantity=0)
    assert str(excinfo.value) == "max_quantity must be at least 1, got [0]"


def test_first_add_beyond_the_per_order_cap_is_rejected() -> None:
    """Test 43: The per-order cap applies to the very first add"""
    import pytest

    from shopping_cart import MaxQuantityExceededError, ShoppingCart

    cart = ShoppingCart()

    with pytest.raises(MaxQuantityExceededError) as excinfo:
        cart.add_item("sale-item", 1.0, quantity=5, max_quantity=3)
    assert str(excinfo.value) == "maximum [3] of [sale-item] per order, requested [5]"
    assert cart.quantity_of("sale-item") == 0


def test_updating_quantity_to_one_keeps_the_line() -> None:
    """Test 44: Only zero removes the line; one is a normal update"""
    from shopping_cart import ShoppingCart

    cart = ShoppingCart()
    cart.add_item("widget", 10.0, quantity=3)

    cart.update_quantity("widget", 1)

    assert cart.quantity_of("widget") == 1
    assert cart.item_subtotal("widget") == 10.0


def test_subtotal_sums_lines_and_rounds_to_cents() -> None:
    """Test 45: Subtotal reports the pre-discount sum rounded to cents"""
    from shopping_cart import ShoppingCart

    cart = ShoppingCart()
    cart.add_item("widget", 19.99, quantity=3)
    cart.add_item("sliver", 0.554, quantity=1)

    assert cart.subtotal() == 60.52  # 59.97 + 0.554 = 60.524, to cents
    assert cart.item_subtotal("sliver") == 0.55


def test_buying_exactly_the_stock_is_allowed() -> None:
    """Test 46: A request equal to the available stock succeeds"""
    from shopping_cart import ShoppingCart

    cart = ShoppingCart()
    cart.add_item("rare", 99.0, quantity=5, stock=5)

    assert cart.quantity_of("rare") == 5
