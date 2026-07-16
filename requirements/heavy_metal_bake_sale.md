# Bake sale checkout

## Overview
A checkout for a bake sale stand. The stand sells four goods, each ordered by a one-letter
code: B for a Brownie at $0.75, M for a Muffin at $1.00, C for a Cake Pop at $1.35, and W
for a Water at $1.50. Customers place comma-delimited orders; the checkout quotes totals,
takes payment and returns change, and tracks the remaining stock of each item, refusing
orders it cannot fill.

## User Stories

### US-1: Quote an order's total
As a cashier, I want the total of a comma-delimited order, so that I can tell the customer what they owe.

- AC-1.1: Each item code is priced from the table: B (Brownie) $0.75, M (Muffin) $1.00, C (Cake Pop) $1.35, W (Water) $1.50.
- AC-1.2: An order is a comma-delimited list of item codes; its total is the sum of the item prices, reported in dollars and cents with a leading dollar sign (worked examples: B, C, W totals $3.60; C, M totals $2.35).
- AC-1.3: Whitespace around the comma-delimited codes is ignored.
- AC-1.4: A code counts once per appearance, so repeated items are summed (worked example: B, B, M totals $2.50).
- AC-1.5: An order containing no items totals $0.00.
- AC-1.6: Quoting a total is not a sale and leaves stock untouched.

### US-2: Take payment and give change
As a cashier, I want payments checked against the total, so that customers get correct change and short payments are refused.

- AC-2.1: Paying exactly the total returns change of $0.00.
- AC-2.2: Overpaying returns the difference as change (worked example: paying $4.00 for a $3.60 order returns $0.40).
- AC-2.3: Paying less than the total is refused with exactly the message "Not enough money".
- AC-2.4: A refused payment consumes no stock.
- AC-2.5: A completed sale removes one unit of stock for each code in the order.

### US-3: Track and enforce stock
As a stand organizer, I want stock tracked and exhausted items refused, so that we never sell what we do not have.

- AC-3.1: By default the stand opens with 48 Brownies, 36 Muffins, 24 Cake Pops, and 30 Waters; a custom starting inventory can be supplied instead, and the remaining stock of any item can be queried at any time.
- AC-3.2: An order asking for more units of an item than remain — including any order for an item with none left — is refused, whether quoting or paying, with the message "<item name> is out of stock" naming the item in full (worked example: "Water is out of stock").
- AC-3.3: An item absent from the supplied inventory has a stock of zero and ordering it is refused as out of stock.
- AC-3.4: Selling the last unit of an item makes the next order for it out of stock.

### US-4: Reject unknown item codes
As a cashier, I want unknown codes rejected clearly, so that mistyped orders are caught.

- AC-4.1: An order containing an item code not in the price table is rejected as invalid, and the rejection names the offending code.

## Traceability
```json
{
  "test_total_for_a_single_brownie": ["AC-1.1", "AC-1.2"],
  "test_each_item_is_priced_per_the_inventory_table": ["AC-1.1"],
  "test_total_for_brownie_cake_pop_and_water": ["AC-1.2"],
  "test_total_for_cake_pop_and_muffin": ["AC-1.2"],
  "test_total_tolerates_spaces_around_codes": ["AC-1.3"],
  "test_total_with_repeated_items": ["AC-1.4"],
  "test_paying_the_exact_amount_gives_zero_change": ["AC-2.1"],
  "test_overpaying_returns_the_difference_as_change": ["AC-2.2"],
  "test_underpaying_is_refused_with_not_enough_money": ["AC-2.3"],
  "test_underpaying_leaves_stock_untouched": ["AC-2.4"],
  "test_out_of_stock_item_is_reported_by_name_when_totalling": ["AC-3.2"],
  "test_out_of_stock_item_is_reported_by_name_when_paying": ["AC-3.2"],
  "test_ordering_more_than_the_remaining_stock_is_out_of_stock": ["AC-3.2"],
  "test_completed_sale_decrements_stock": ["AC-2.5"],
  "test_quoting_a_total_does_not_decrement_stock": ["AC-1.6"],
  "test_default_inventory_matches_the_specification": ["AC-3.1"],
  "test_repeated_sales_exhaust_stock": ["AC-3.4"],
  "test_unknown_item_code_is_rejected": ["AC-4.1"],
  "test_stock_of_an_unstocked_item_is_zero": ["AC-3.3"],
  "test_ordering_an_unstocked_item_is_out_of_stock": ["AC-3.3"],
  "test_short_payment_refusal_message_is_exact": ["AC-2.3"],
  "test_unknown_item_code_is_named_in_the_error": ["AC-4.1"],
  "test_total_of_an_empty_order_is_zero_dollars": ["AC-1.5"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
