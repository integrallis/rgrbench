# Retail shopping cart with discounts, offers, and purchase limits

## Overview
An online-store shopping cart tracks the items a shopper intends to buy — each as a named line with a unit price and a quantity — and prices the order. Storewide discounts, per-item promotional offers, stock availability, and per-order quantity caps all shape the final total, and every reported amount is rounded to cents.

## User Stories

### US-1: Managing the items in the cart
As a shopper, I want to add, adjust, and remove items, so that the cart mirrors what I intend to buy.

- AC-1.1: Adding an item creates a line with its name, unit price, and quantity, and the line's quantity can be read back.
- AC-1.2: Adding an item already in the cart tops up the quantity on the existing line.
- AC-1.3: Adding without stating a quantity puts one unit in the cart.
- AC-1.4: Removing an item drops its line entirely: its quantity reads zero and it no longer contributes to the total.
- AC-1.5: Changing a line's quantity reprices that line accordingly.
- AC-1.6: Setting a quantity to zero removes the line; setting it to one keeps the line as a normal update.
- AC-1.7: The quantity of an item never added reads zero.

### US-2: Pricing the order
As a shopper, I want accurate totals, so that I know exactly what I will pay.

- AC-2.1: A line's subtotal is its unit price times its quantity, rounded to cents.
- AC-2.2: The cart total is the sum of the line subtotals, after any offers and discounts.
- AC-2.3: An empty cart totals 0.0, with a pre-discount sum of 0.0.
- AC-2.4: The cart also reports its pre-discount sum: all lines added together, rounded to cents.
- AC-2.5: A unit price of zero is allowed and subtotals to zero.

### US-3: Rejecting invalid line operations
As a store owner, I want malformed cart operations refused with precise messages, so that pricing mistakes surface at the source.

- AC-3.1: An empty item name is rejected with the exact message "item name must not be empty".
- AC-3.2: A negative unit price is rejected with the exact message "unit_price must be non-negative, got [P]" where P is the offending price.
- AC-3.3: Adding fewer than one unit is rejected with the exact message "quantity must be at least 1, got [Q]" where Q is the offending quantity.
- AC-3.4: Changing a quantity to a negative value is rejected with the exact message "quantity must be non-negative, got [Q]".
- AC-3.5: Removing, requantifying, or asking the subtotal of an item not in the cart is rejected with the exact message "item [NAME] is not in the cart".

### US-4: Applying storewide discounts
As a store owner, I want cart-level discounts, so that promotions reduce what shoppers pay.

- AC-4.1: A percentage discount reduces the total by that percentage — 10% off 59.97 leaves 53.97; 1% and 100% are both valid, with 100% taking the total to 0.0.
- AC-4.2: A percentage must be greater than zero and at most one hundred, rejected otherwise with the exact message "percent must be greater than 0 and at most 100, got [X]".
- AC-4.3: A fixed-amount discount subtracts its amount from the total — 15.00 off 100.00 leaves 85.00; amounts under one unit of currency, such as 0.75, are valid.
- AC-4.4: A fixed-amount discount never takes the total below zero.
- AC-4.5: A fixed-amount discount must be positive, rejected otherwise with the exact message "amount must be positive, got [X]".
- AC-4.6: Discounts apply in the order they were registered: on 100.00, a fixed 10.00 then 50% yields 45.00, while 50% then a fixed 10.00 yields 40.00.
- AC-4.7: Lines marked as not discountable are skipped by percentage discounts: 10% off alongside a 50.00 non-discountable line and a 30.00 regular line totals 77.00.
- AC-4.8: Fixed-amount discounts deplete only the discountable portion of the cart, clamping that portion at zero without eating into non-discountable lines.

### US-5: Attaching promotional offers to items
As a store owner, I want per-item offers, so that multi-buy promotions price lines automatically.

- AC-5.1: A buy-X-get-Y-free offer groups a line's units into batches of X plus Y where the first X units of each batch are paid and the rest are free, including in a final partial batch: buy two get one free charges 4 of 6 units and 4 of 5 units; buy one get one free charges 2 of 4 units; buy one get two free charges 2 of 5 units.
- AC-5.2: The buy and get counts must each be at least one, rejected otherwise with the exact messages "buy must be at least 1, got [X]" and "get must be at least 1, got [X]".
- AC-5.3: A bulk-price offer reprices every unit of a line to the bulk unit price once the quantity reaches the threshold; below the threshold the regular price stands.
- AC-5.4: A bulk threshold below two is rejected with the exact message "min_quantity must be at least 2, got [X]", and a negative bulk price with the exact message "unit_price must be non-negative, got [X]"; a threshold of exactly two and a bulk price of zero are valid.
- AC-5.5: An offer attaches only to an item already in the cart (otherwise "item [NAME] is not in the cart"), never to a non-discountable item (otherwise "item [NAME] cannot be combined with discounts"), and an item carries at most one offer (otherwise "item [NAME] already has an offer").
- AC-5.6: An offer's item name must not be empty, rejected with the exact message "item name must not be empty".
- AC-5.7: Offers reshape line subtotals first; cart-level discounts then apply to the reshaped amounts.

### US-6: Enforcing purchase limits
As a store owner, I want stock and per-order caps enforced, so that shoppers cannot buy more than is available or permitted.

- AC-6.1: A request that would exceed an item's stated stock — on the first add, an accumulating add, or a quantity change — fails with a dedicated insufficient-stock error carrying the exact message "only [S] of [NAME] in stock, requested [R]", and leaves the cart unchanged.
- AC-6.2: Buying exactly the stated stock succeeds, and a stock of zero is a valid limit that admits nothing.
- AC-6.3: A negative stock is rejected with the exact message "stock must be non-negative, got [X]".
- AC-6.4: A request that would exceed an item's per-order cap — including the very first add — fails with a dedicated maximum-quantity error carrying the exact message "maximum [M] of [NAME] per order, requested [R]", and leaves the cart unchanged.
- AC-6.5: A per-order cap of one is valid, and changing the quantity to exactly the cap succeeds.
- AC-6.6: A per-order cap below one is rejected with the exact message "max_quantity must be at least 1, got [X]".

## Traceability
```json
{
  "test_added_item_reports_its_subtotal": ["AC-1.1", "AC-2.1"],
  "test_adding_the_same_item_again_accumulates_quantity": ["AC-1.2"],
  "test_cart_total_sums_all_line_subtotals": ["AC-2.2"],
  "test_empty_cart_totals_zero": ["AC-2.3", "AC-1.7"],
  "test_removed_item_no_longer_counts": ["AC-1.4"],
  "test_operations_on_missing_items_are_rejected": ["AC-3.5"],
  "test_update_quantity_reprices_the_line": ["AC-1.5"],
  "test_updating_quantity_to_zero_removes_the_line": ["AC-1.6"],
  "test_invalid_add_arguments_are_rejected": ["AC-3.1", "AC-3.2", "AC-3.3"],
  "test_negative_quantity_update_is_rejected": ["AC-3.4"],
  "test_percentage_discount_reduces_the_total": ["AC-4.1"],
  "test_percentage_discount_bounds_are_enforced": ["AC-4.2"],
  "test_fixed_amount_discount_reduces_the_total": ["AC-4.3"],
  "test_fixed_amount_discount_never_drops_the_total_below_zero": ["AC-4.4"],
  "test_non_positive_fixed_discount_is_rejected": ["AC-4.5"],
  "test_cart_discounts_apply_in_registration_order_fixed_first": ["AC-4.6"],
  "test_cart_discounts_apply_in_registration_order_percentage_first": ["AC-4.6"],
  "test_buy_x_get_y_free_prices_only_the_paid_units": ["AC-5.1"],
  "test_buy_x_get_y_free_remainder_units_are_paid": ["AC-5.1"],
  "test_buy_x_get_y_free_parameters_must_be_positive": ["AC-5.2"],
  "test_bulk_price_applies_at_and_above_the_threshold": ["AC-5.3"],
  "test_bulk_price_does_not_apply_below_the_threshold": ["AC-5.3"],
  "test_bulk_price_parameters_are_validated": ["AC-5.4"],
  "test_limited_stock_caps_the_quantity": ["AC-6.1"],
  "test_maximum_quantity_per_order_is_enforced": ["AC-6.4", "AC-6.5"],
  "test_non_combinable_items_are_skipped_by_cart_discounts": ["AC-4.7"],
  "test_fixed_discount_cannot_eat_into_non_combinable_items": ["AC-4.8"],
  "test_offer_attachment_rules_are_enforced": ["AC-5.5"],
  "test_item_offers_apply_before_cart_level_discounts": ["AC-5.7"],
  "test_offer_with_empty_item_name_is_rejected": ["AC-5.6"],
  "test_buy_one_get_one_free_is_a_valid_offer": ["AC-5.1"],
  "test_buy_x_get_many_free_counts_free_units_in_partial_groups": ["AC-5.1"],
  "test_bulk_price_boundary_values_are_accepted": ["AC-5.4"],
  "test_one_percent_discount_is_valid": ["AC-4.1"],
  "test_hundred_percent_discount_zeroes_the_total": ["AC-4.1"],
  "test_fixed_discounts_smaller_than_one_are_valid": ["AC-4.3"],
  "test_default_quantity_is_one": ["AC-1.3"],
  "test_zero_priced_items_are_allowed": ["AC-2.5"],
  "test_zero_stock_is_a_valid_limit_but_admits_nothing": ["AC-6.2"],
  "test_negative_stock_is_rejected": ["AC-6.3"],
  "test_max_quantity_of_one_is_valid": ["AC-6.5"],
  "test_non_positive_max_quantity_is_rejected": ["AC-6.6"],
  "test_first_add_beyond_the_per_order_cap_is_rejected": ["AC-6.4"],
  "test_updating_quantity_to_one_keeps_the_line": ["AC-1.6"],
  "test_subtotal_sums_lines_and_rounds_to_cents": ["AC-2.4", "AC-2.1"],
  "test_buying_exactly_the_stock_is_allowed": ["AC-6.2"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
