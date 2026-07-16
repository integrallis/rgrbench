# Bookshop series discount pricing

## Overview
A bookshop sells a five-title book series at a base price of 8.00 euros per copy. Baskets
mixing distinct titles earn a discount that grows with the number of different titles in a
set, and a basket's price is computed by grouping its copies into sets in whatever way
yields the lowest total — a greedy grouping is not good enough.

## User Stories

### US-1: Charge the base price
As a bookseller, I want plain baskets charged at the base price, so that undiscounted sales are correct.

- AC-1.1: An empty basket costs 0.00.
- AC-1.2: A single copy costs the base price of 8.00, whichever of the five titles it is.
- AC-1.3: Multiple copies of the same title never form a discounted set; each costs the full base price.

### US-2: Discount sets of distinct titles
As a bookseller, I want sets of different titles discounted by size, so that customers are rewarded for buying across the series.

- AC-2.1: A set of distinct titles is discounted on its combined base price by 5% for two titles, 10% for three, 20% for four, and 25% for all five (worked examples: two distinct titles cost 15.20, three cost 21.60, four cost 25.60, the full series costs 30.00).

### US-3: Price mixed baskets optimally
As a bookseller, I want baskets with repeated titles grouped for the lowest total, so that customers always get the best applicable price.

- AC-3.1: A basket's price is the cheapest possible partition of its copies into discounted sets and full-price singles (worked examples: a distinct pair plus a duplicate copy costs 15.20 + 8.00 = 23.20; a full series plus one extra copy costs 38.00; two of every title costs 60.00).
- AC-3.2: Grouping is globally optimal rather than greedy: when two four-title sets beat a five-set plus a three-set, the two four-sets win (worked example: two copies each of three titles plus one each of the other two costs 51.20, not 51.60; doubling that basket costs 102.40).
- AC-3.3: The price depends only on how many copies of each title the basket holds, never on the order the copies were listed.
- AC-3.4: Large baskets are priced correctly and in reasonable time (worked example: five complete series — 25 copies — cost 150.00).

### US-4: Reject unknown titles and report in euros
As a bookseller, I want unknown titles refused and prices returned as amounts, so that the till stays reliable.

- AC-4.1: A basket containing anything other than one of the five series titles is rejected as an error whose message is "unknown book: <title>".
- AC-4.2: Prices are reported as numeric amounts in euros.

## Traceability
```json
{
  "test_empty_basket_costs_nothing": ["AC-1.1"],
  "test_single_book_costs_eight_euros": ["AC-1.2"],
  "test_each_title_alone_costs_the_same": ["AC-1.2"],
  "test_two_copies_of_the_same_title_get_no_discount": ["AC-1.3"],
  "test_three_copies_of_the_same_title_get_no_discount": ["AC-1.3"],
  "test_two_different_titles_get_five_percent_off": ["AC-2.1"],
  "test_three_different_titles_get_ten_percent_off": ["AC-2.1"],
  "test_four_different_titles_get_twenty_percent_off": ["AC-2.1"],
  "test_five_different_titles_get_twenty_five_percent_off": ["AC-2.1"],
  "test_pair_plus_single_combines_discounted_and_full_price": ["AC-3.1"],
  "test_two_full_series_cost_two_five_sets": ["AC-3.1"],
  "test_greedy_grouping_trap_is_avoided": ["AC-3.2"],
  "test_two_greedy_traps_in_one_basket": ["AC-3.2"],
  "test_basket_order_does_not_change_the_price": ["AC-3.3"],
  "test_full_series_plus_one_extra_copy": ["AC-3.1"],
  "test_larger_basket_prices_efficiently_and_correctly": ["AC-3.4"],
  "test_mixed_basket_with_uneven_counts": ["AC-3.1"],
  "test_unknown_books_are_rejected": ["AC-4.1"],
  "test_price_returns_a_float_in_euros": ["AC-4.2"],
  "test_unknown_book_error_names_the_offending_title": ["AC-4.1"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
