# Build-a-robot quoting and purchasing

## Overview
A build-your-own-robot shop assembles custom robots from parts sold by competing suppliers. Every robot needs one choice in each of five part categories — head, body, arms, movement, and power — and each supplier publishes a price list covering only some of the recognized options. The shop quotes a configuration by sourcing every part at the lowest available price, places orders with the winning suppliers when a robot is purchased, and stamps each finished robot with a unique serial name drawn from a supplied randomness source. The recognized options per category are: head — standard vision, infrared vision, night vision; body — square, round, triangular, rectangular; arms — hands, pinchers, boxing gloves; movement — wheels, legs, tracks; power — solar, rechargeable battery, biomass.

## User Stories

### US-1: Registering a healthy supplier pool
As a shop owner, I want the supplier pool validated up front, so that quoting always has real competition to draw on.

- AC-1.1: Fewer than three suppliers is rejected with the exact message "at least 3 suppliers are required, got [N]" where N is the count supplied.
- AC-1.2: Two suppliers sharing a name are rejected with the exact message "duplicate supplier name [NAME]".

### US-2: Quoting a robot at the lowest cost
As a customer, I want each part sourced from whoever sells it cheapest, so that my robot costs as little as possible.

- AC-2.1: For every category in the configuration, the quoted part comes from the supplier offering the lowest price for the chosen option, and each quoted part records its category, winning supplier, and price.
- AC-2.2: The quoted total is the sum of the chosen parts' prices.
- AC-2.3: When two suppliers tie on price, the supplier registered first wins the part.
- AC-2.4: A configuration can be quoted even when no single supplier stocks every chosen part.

### US-3: Validating robot configurations
As a shop owner, I want malformed orders refused with precise reasons, so that only buildable robots reach purchasing.

- AC-3.1: A configuration must cover exactly the five categories head, body, arms, movement, and power; omitting one is rejected with the exact message "missing part category [CATEGORY]".
- AC-3.2: A category outside those five is rejected with the exact message "unknown part category [CATEGORY]".
- AC-3.3: A choice that is not a recognized option for its category is rejected with the exact message "invalid CATEGORY option [OPTION]".
- AC-3.4: A recognized option that no supplier in the pool carries fails with a dedicated part-unavailability error and the exact message "no supplier carries [OPTION]".

### US-4: Purchasing robots and tracking supplier orders
As a shop owner, I want purchasing to follow the quote and leave an audit trail, so that supplier orders match what customers were charged.

- AC-4.1: A purchased robot carries the same sourced parts and the same total as quoting the identical configuration.
- AC-4.2: Purchasing records an order with each winning supplier for exactly the parts bought from it, each with its option and price, listed in the category order head, body, arms, movement, power.
- AC-4.3: Quoting alone records no orders with any supplier.
- AC-4.4: Asking for the order history of a supplier not in the pool is rejected with the exact message "unknown supplier [NAME]".

### US-5: Stamping unique serial names
As a shop owner, I want every robot given a reproducible serial name, so that units are identifiable and production runs are auditable.

- AC-5.1: Every purchased robot's name is exactly two uppercase letters followed by three digits.
- AC-5.2: Names never repeat within a factory, even across long production runs.
- AC-5.3: Names are drawn from the randomness source supplied to the factory, so two factories given identically seeded sources stamp identical name sequences.

## Traceability
```json
{
  "test_factory_requires_at_least_three_suppliers": ["AC-1.1"],
  "test_duplicate_supplier_names_are_rejected": ["AC-1.2"],
  "test_costing_picks_the_cheapest_supplier_for_each_part": ["AC-2.1"],
  "test_quote_total_is_the_sum_of_the_cheapest_parts": ["AC-2.2"],
  "test_price_ties_go_to_the_supplier_listed_first": ["AC-2.3"],
  "test_costing_works_when_no_single_supplier_carries_everything": ["AC-2.4"],
  "test_part_carried_by_no_supplier_is_unavailable": ["AC-3.4"],
  "test_missing_part_category_is_rejected": ["AC-3.1"],
  "test_unknown_part_category_is_rejected": ["AC-3.2"],
  "test_invalid_option_for_a_category_is_rejected": ["AC-3.3"],
  "test_purchased_robot_matches_its_quote": ["AC-4.1"],
  "test_purchasing_places_orders_with_the_respective_suppliers": ["AC-4.2"],
  "test_costing_alone_places_no_orders": ["AC-4.3"],
  "test_orders_for_unknown_supplier_is_rejected": ["AC-4.4"],
  "test_robot_names_are_two_uppercase_letters_and_three_digits": ["AC-5.1"],
  "test_robot_names_are_unique_within_a_factory": ["AC-5.2"],
  "test_same_seed_reproduces_the_same_name_sequence": ["AC-5.3"],
  "test_every_name_in_a_production_run_keeps_the_serial_format": ["AC-5.1"],
  "test_names_stay_unique_across_a_long_production_run": ["AC-5.2"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
