# Supermarket checkout pricing

## Overview
A supermarket till prices a basket as items are scanned. Everyday items carry unit prices with layered promotions on top — multi-buy bundles, a buy-one-get-one-free line, and a cross-item combo — while fresh produce is sold by the kilogram and rounded to the cent. The total reflects every applicable rule no matter the order in which items are scanned, and bad scans are refused with clear messages.

## User Stories

### US-1: Charge unit prices
As a shopper, I want each item charged at its listed unit price, so that my total matches the shelf labels.

- AC-1.1: An empty basket totals 0.
- AC-1.2: Unit prices are: A costs 50, B costs 30, C costs 20, D costs 15.
- AC-1.3: Different items in one basket add their prices together (A with B totals 80).
- AC-1.4: Multiple units of an item with no promotion of its own cost the unit price each (two D total 30).

### US-2: Reward quantity with multi-buy bundles
As a store manager, I want bundle deals on selected items, so that shoppers are rewarded for buying in quantity.

- AC-2.1: Three A cost the bundle price of 130 instead of 150.
- AC-2.2: Units of A beyond a complete bundle are charged at unit price (four A total 180).
- AC-2.3: Two B cost the bundle price of 45 instead of 60.
- AC-2.4: Units of B beyond a complete bundle are charged at unit price (three B total 75).
- AC-2.5: The total never depends on the order in which items are scanned (A, B, A, B, A totals 175 in any order).

### US-3: Give every second C free
As a store manager, I want item C on buy-one-get-one-free, so that every second C costs nothing.

- AC-3.1: Every second C in the basket is free (two C total 20).
- AC-3.2: An unpaired C is charged at unit price (three C total 40).

### US-4: Price the D-and-C combo
As a store manager, I want a combined price when D and C are bought together, so that the pairing is promoted.

- AC-4.1: One D together with one C costs the combo price of 25.
- AC-4.2: The combo applies once per disjoint D-and-C pair; leftovers are charged at unit price (D, C and another D total 40; two D with two C total 50).

### US-5: Sell produce by weight
As a shopper buying fresh produce, I want weighed goods priced by the kilogram and rounded to the cent, so that fractional weights are charged fairly.

- AC-5.1: Weighed goods are priced per kilogram: Bananas at 1.99, Apples at 3.49 (two kilograms of Apples cost 6.98).
- AC-5.2: Each weighed line is rounded to the nearest cent, with exact halves rounding up (half a kilogram of Bananas comes to 0.995 and is charged as 1.00; one and a half kilograms comes to 2.985 and is charged as 2.99).
- AC-5.3: Weighed lines combine with all other pricing rules in a single basket, and such totals are expressed to the cent (three A, two B and half a kilogram of Bananas total 176.00).

### US-6: Refuse bad scans
As a till operator, I want invalid scans refused with a clear message, so that mistakes are caught at the till.

- AC-6.1: Scanning an item that is not in the price list is refused with a message naming the item, of the form "Unknown item: X".
- AC-6.2: Weighing an item that is not in the price list is refused the same way (for example "Unknown item: Grapes").
- AC-6.3: A weighed item's weight must be positive; zero or negative weight is refused with the message exactly "weight must be positive".

## Traceability
```json
{
  "test_empty_basket_totals_zero": ["AC-1.1"],
  "test_single_item_uses_unit_price": ["AC-1.2"],
  "test_two_different_items_add_up": ["AC-1.3"],
  "test_unit_prices_for_all_items": ["AC-1.2"],
  "test_three_a_multi_buy": ["AC-2.1"],
  "test_fourth_a_at_unit_price": ["AC-2.2"],
  "test_two_b_multi_buy": ["AC-2.3"],
  "test_third_b_at_unit_price": ["AC-2.4"],
  "test_scan_order_does_not_matter": ["AC-2.5"],
  "test_bogof_pair_of_c": ["AC-3.1"],
  "test_bogof_odd_c_pays_for_the_odd_one": ["AC-3.2"],
  "test_no_special_for_d": ["AC-1.4"],
  "test_combo_d_plus_c": ["AC-4.1"],
  "test_combo_applies_once_per_qualifying_set": ["AC-4.2"],
  "test_each_disjoint_pair_gets_the_combo": ["AC-4.2"],
  "test_weighed_bananas_rounded_to_cent": ["AC-5.1", "AC-5.2"],
  "test_weighed_apples": ["AC-5.1"],
  "test_weighed_line_rounds_half_up": ["AC-5.2"],
  "test_mixed_basket_combines_all_rules": ["AC-5.3"],
  "test_unknown_item_is_rejected": ["AC-6.1"],
  "test_unknown_weighed_item_is_rejected": ["AC-6.2"],
  "test_non_positive_weight_is_rejected": ["AC-6.3"],
  "test_negative_weight_is_rejected_with_the_exact_message": ["AC-6.3"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
