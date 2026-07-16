# Coin change maker

## Overview
A change maker that breaks an amount of money in cents into coins using the denominations 25, 10, 5 and 1. It dispenses the fewest coins by always choosing the largest denomination that still fits, and lists the coins from largest to smallest.

## User Stories

### US-1: Make change with the fewest coins
As a cashier, I want an amount broken into coins greedily from the largest denomination down, so that customers receive as few coins as possible.

- AC-1.1: An amount equal to a single denomination is served as exactly that one coin: 25 yields one 25.
- AC-1.2: Amounts requiring repeats of one denomination use it repeatedly: 50 yields two 25s.
- AC-1.3: Mixed amounts are served largest denomination first: 41 yields 25, 10, 5, 1 in that order.

### US-2: No change due
As a cashier, I want a zero amount to produce no coins, so that exact payments dispense nothing.

- AC-2.1: An amount of zero yields an empty collection of coins.

## Traceability
```json
{
  "test_single_coin_change": ["AC-1.1"],
  "test_multiple_coins": ["AC-1.2"],
  "test_greedy_algorithm": ["AC-1.3"],
  "test_zero_amount": ["AC-2.1"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
