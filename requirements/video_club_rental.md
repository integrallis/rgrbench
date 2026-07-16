# Video club rental billing

## Overview
A video rental club charges customers per rented movie according to the movie's
pricing category and how many days it was kept, and rewards renters with frequent
renter points. The system prices individual rentals, accumulates a customer's
rentals into totals, and prints a plain-text statement listing every rental with its
charge, the amount owed, and the points earned.

## User Stories

### US-1: Price a rental by category and length
As a club clerk, I want each rental priced from the movie's category and the days kept, so that customers are charged the club's published rates.

- AC-1.1: A regular movie costs 2.0 for a rental of up to two days, plus 1.5 for each day beyond the second: three days cost 3.5 and five days cost 6.5.
- AC-1.2: A new release costs 3.0 per day rented: one day costs 3.0 and three days cost 9.0.
- AC-1.3: A children's movie costs 1.5 for a rental of up to three days, plus 1.5 for each day beyond the third: four days cost 3.0 and six days cost 6.0.
- AC-1.4: A rental must last at least one day; zero or negative day counts are rejected with an error whose message reads "days_rented must be at least 1".

### US-2: Award frequent renter points
As a club owner, I want rentals to earn loyalty points, so that regular customers are rewarded and encouraged to return.

- AC-2.1: Every rental earns one frequent renter point, regardless of category or length.
- AC-2.2: A new release kept more than one day earns one bonus point, for two points in total; keeping it longer earns no further points.

### US-3: Keep a customer's rental account
As a club clerk, I want a customer's rentals accumulated in one place, so that the amount owed and the points earned can be totalled at the counter.

- AC-3.1: A customer's total charge and total frequent renter points are the sums over all recorded rentals; for a three-day regular, a two-day new release, and a four-day children's rental together, the totals are 12.5 owed and 4 points.
- AC-3.2: A customer lists the rentals recorded so far, in the order they were added.

### US-4: Print a rental statement
As a club clerk, I want a printable statement of a customer's rentals, so that the customer sees each charge and the totals at a glance.

- AC-4.1: The statement opens with the line "Rental Record for <customer name>".
- AC-4.2: Each rental appears on its own line in rental order, indented by a tab, as the movie title, a tab, and the rental's charge.
- AC-4.3: The statement closes with the lines "Amount owed is <total charge>" and "You earned <total points> frequent renter points".
- AC-4.4: A customer with no rentals still gets a statement: no rental lines, an amount owed of 0.0, and 0 points.
- AC-4.5: Charges are printed with a decimal point; whole amounts carry a trailing ".0" (a charge of two prints as "2.0").

### US-5: Describe the movie catalogue
As a club owner, I want every movie carrying a title and one of the club's pricing categories, so that pricing is unambiguous for every tape on the shelf.

- AC-5.1: A movie exposes its title and its pricing category.
- AC-5.2: There are exactly three pricing categories, named REGULAR, NEW_RELEASE, and CHILDRENS.

## Traceability
```json
{
  "test_regular_movie_base_charge": ["AC-1.1"],
  "test_regular_movie_two_days_still_base_charge": ["AC-1.1"],
  "test_regular_movie_charges_extra_after_two_days": ["AC-1.1"],
  "test_new_release_charges_per_day": ["AC-1.2"],
  "test_childrens_movie_base_charge": ["AC-1.3"],
  "test_childrens_movie_charges_extra_after_three_days": ["AC-1.3"],
  "test_every_rental_earns_one_point": ["AC-2.1"],
  "test_one_day_new_release_earns_one_point": ["AC-2.1"],
  "test_multi_day_new_release_earns_bonus_point": ["AC-2.2"],
  "test_rental_must_last_at_least_one_day": ["AC-1.4"],
  "test_customer_totals_sum_over_rentals": ["AC-3.1"],
  "test_customer_lists_recorded_rentals": ["AC-3.2"],
  "test_statement_with_no_rentals": ["AC-4.4"],
  "test_statement_with_single_rental": ["AC-4.1", "AC-4.2", "AC-4.3"],
  "test_statement_with_multiple_rentals": ["AC-4.2", "AC-4.3"],
  "test_statement_renders_whole_amounts_with_decimal_point": ["AC-4.5"],
  "test_movie_carries_title_and_price_code": ["AC-5.1"],
  "test_price_codes_are_three_distinct_categories": ["AC-5.2"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
