# Multi-currency money

## Overview
A small multi-currency accounting model in the style of Kent Beck's money example.
Monetary amounts carry a currency (dollars in USD, francs in CHF), support scalar
multiplication and addition, and compare by value. A bank holds exchange rates and
reduces any monetary expression — a plain amount, a sum, or a scaled sum — to a single
requested currency.

## User Stories

### US-1: Scaling amounts
As a bookkeeper, I want to multiply a monetary amount by a whole-number factor, so that repeated charges can be priced in one step.

- AC-1.1: Multiplying a dollar amount by a factor yields the amount scaled by that
  factor; 5 dollars times 2 equals 10 dollars.
- AC-1.2: Franc amounts scale the same way; 5 francs times 2 equals 10 francs and 5
  francs times 3 equals 15 francs.
- AC-1.3: Multiplication produces a new amount and never alters the original; after
  being multiplied, 5 dollars still equals 5 dollars.

### US-2: Comparing amounts
As a bookkeeper, I want amounts to compare by quantity and currency, so that equal sums of the same money are interchangeable and different currencies are never conflated.

- AC-2.1: Two amounts with the same quantity and the same currency are equal.
- AC-2.2: Two amounts in the same currency with different quantities are not equal.
- AC-2.3: Two amounts with the same quantity but different currencies are not equal.
- AC-2.4: Every amount reports its currency code; dollar amounts report "USD" and franc
  amounts report "CHF".

### US-3: Adding and reducing expressions
As a bookkeeper, I want to add amounts into composite expressions and have a bank reduce them to one currency, so that mixed holdings can be valued consistently.

- AC-3.1: Adding an amount to another yields an expression that the bank reduces to a
  requested currency; 5 dollars plus 5 dollars reduces to 10 dollars.
- AC-3.2: Reducing a plain amount to its own currency yields an equal amount and needs
  no exchange rate.
- AC-3.3: A sum can be extended by adding a further amount, mixing currencies, before
  reduction; 5 dollars plus 10 francs, plus another 5 dollars, reduces to 15 dollars
  when 2 francs exchange for 1 dollar.
- AC-3.4: A sum can be multiplied by a factor before reduction; the sum of 5 dollars and
  10 francs, times 2, reduces to 20 dollars at the same rate.

### US-4: Exchanging currencies
As a bookkeeper, I want the bank to convert between currencies using registered rates, so that reductions across currencies are well defined.

- AC-4.1: An exchange rate is registered for an ordered currency pair; with a rate of 2
  from francs to dollars, 2 francs reduce to 1 dollar.
- AC-4.2: Conversion divides the amount by the rate and truncates any fraction to a
  whole unit; at the 2-to-1 franc-to-dollar rate, 5 francs reduce to 2 dollars.
- AC-4.3: Reducing to a different currency with no registered rate fails with an error
  naming the requested conversion pair, in the form "USD->CHF".

## Traceability
```json
{
  "test_multiplication": ["AC-1.1"],
  "test_equality": ["AC-2.1", "AC-2.2"],
  "test_privacy": ["AC-1.3"],
  "test_franc_multiplication": ["AC-1.2"],
  "test_common_currency_equality": ["AC-2.1", "AC-2.2"],
  "test_different_currency_inequality": ["AC-2.3"],
  "test_currency": ["AC-2.4"],
  "test_simple_addition": ["AC-3.1"],
  "test_reduce_money": ["AC-3.2", "AC-4.1"],
  "test_mixed_addition": ["AC-4.1"],
  "test_sum_plus_money": ["AC-3.3"],
  "test_sum_times": ["AC-3.4"],
  "test_reduce_money_truncates_fractional_conversion": ["AC-4.2"],
  "test_reduce_money_without_registered_rate": ["AC-4.3"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
