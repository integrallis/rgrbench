# Personal bank account with printable statement

## Overview
A personal bank account that opens with a zero balance and accepts dated deposits and withdrawals. Amounts must be positive, the account can never be overdrawn, and rejected operations leave the account untouched. On request the account prints a statement: a fixed header followed by one line per transaction in chronological order, each showing the date, the signed amount, and the running balance.

## User Stories

### US-1: Deposits build the balance
As an account holder, I want to deposit money on a given date, so that my balance grows by what I pay in.

- AC-1.1: A newly opened account has a balance of 0.
- AC-1.2: A deposit increases the balance by exactly the deposited amount.
- AC-1.3: Successive deposits accumulate into the balance.

### US-2: Withdrawals draw down the balance
As an account holder, I want to withdraw money on a given date, so that I can take out funds I own.

- AC-2.1: A withdrawal decreases the balance by exactly the withdrawn amount.
- AC-2.2: Withdrawing exactly the current balance is allowed and leaves the balance at 0.

### US-3: Invalid operations are rejected without side effects
As an account holder, I want impossible transactions refused cleanly, so that my account state stays correct.

- AC-3.1: A deposit of zero or a negative amount is rejected with an error whose message is exactly "Amount must be positive".
- AC-3.2: A withdrawal of zero or a negative amount is rejected with the same "Amount must be positive" error.
- AC-3.3: A withdrawal greater than the current balance is rejected with an error whose message is exactly "Cannot withdraw more than current balance"; any withdrawal from an account holding 0 falls under this rule.
- AC-3.4: A rejected deposit or withdrawal changes nothing: the balance and the printed statement are the same afterwards as before.

### US-4: Printable statement
As an account holder, I want a statement of my transactions, so that I can review my account history.

- AC-4.1: With no transactions, the statement is exactly the single header line "Date       | Amount  | Balance".
- AC-4.2: Each transaction adds one line under the header showing the ISO-formatted date, the transaction amount, and the running balance after it; the amount and balance columns are right-aligned to seven characters with two decimal places.
- AC-4.3: Withdrawals appear as negative amounts with the running balance reduced accordingly.
- AC-4.4: Transactions are listed oldest first, in the order they were made, each with the running balance at that point.
- AC-4.5: The canonical worked example — deposit 500.00 on 15 January 2026, withdraw 100.00 on 20 January 2026, deposit 200.00 on 25 January 2026 — produces exactly:

```text
Date       | Amount  | Balance
2026-01-15 |  500.00 |  500.00
2026-01-20 | -100.00 |  400.00
2026-01-25 |  200.00 |  600.00
```

## Traceability
```json
{
  "test_new_account_has_zero_balance": ["AC-1.1"],
  "test_deposit_adds_funds": ["AC-1.2"],
  "test_multiple_deposits_accumulate": ["AC-1.3"],
  "test_withdraw_removes_funds": ["AC-2.1"],
  "test_withdraw_entire_balance_leaves_zero": ["AC-2.2"],
  "test_deposit_rejects_negative_amount": ["AC-3.1"],
  "test_deposit_rejects_zero_amount": ["AC-3.1"],
  "test_withdraw_rejects_negative_amount": ["AC-3.2"],
  "test_withdraw_rejects_zero_amount": ["AC-3.2"],
  "test_withdraw_more_than_balance_is_rejected": ["AC-3.3"],
  "test_withdraw_from_empty_account_is_rejected": ["AC-3.3"],
  "test_rejected_operations_do_not_change_state": ["AC-3.4"],
  "test_statement_of_new_account_is_header_only": ["AC-4.1"],
  "test_statement_single_deposit_line_format": ["AC-4.2"],
  "test_statement_matches_kata_example": ["AC-4.5"],
  "test_statement_shows_withdrawals_as_negative_amounts": ["AC-4.3"],
  "test_statement_lists_transactions_in_chronological_order": ["AC-4.4"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
