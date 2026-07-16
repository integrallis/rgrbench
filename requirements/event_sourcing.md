# Event-sourced bank ledger

## Overview
A bank whose single source of truth is an append-only stream of timestamped events. Commands — opening an account, depositing, withdrawing, and closing — are validated against the state replayed from the stream, and each accepted command appends exactly one event recording the account, the command's payload, and its timestamp. Balances, statements, summaries, and as-of-a-moment queries are all derived by replaying events; a bank can be rehydrated from a previously recorded stream.

## User Stories

### US-1: Manage money in accounts
As an account holder, I want to open an account, deposit money, and withdraw money, so that I can manage my funds.

- AC-1.1: After opening an account and depositing 100, the balance is 100.
- AC-1.2: Deposits accumulate: depositing 100 and then 50 yields a balance of 150.
- AC-1.3: A withdrawal reduces the balance: deposit 100, withdraw 30, balance 70.
- AC-1.4: The entire balance may be withdrawn, leaving a balance of 0.
- AC-1.5: Movements of exactly 1 are valid, for both deposits and withdrawals.
- AC-1.6: Accounts are independent: activity on one account never affects another account's balance.

### US-2: Commands are validated with precise reasons
As a bank operator, I want invalid commands rejected with exact reasons, so that the ledger records only lawful movements.

- AC-2.1: Withdrawing more than the balance is rejected with the exact message "insufficient funds", and the balance is unchanged.
- AC-2.2: Depositing to or withdrawing from an account that was never opened is rejected with the exact message "account not found".
- AC-2.3: An account identifier may be opened only once; opening it again is rejected with the exact message "account already exists".
- AC-2.4: Closing an account with a nonzero balance is rejected with the exact message "balance must be zero".
- AC-2.5: A closed account rejects both deposits and withdrawals with the exact message "account is closed".
- AC-2.6: Deposit amounts must be positive; zero or negative amounts are rejected with the exact message "deposit amount must be positive".
- AC-2.7: Withdrawal amounts must be positive; zero or negative amounts are rejected with the exact message "withdrawal amount must be positive".
- AC-2.8: Closing an account whose balance is zero succeeds, and the account's status becomes "closed".

### US-3: The event stream is the source of truth
As an auditor, I want every accepted command recorded as an event, so that the complete history is replayable.

- AC-3.1: Each accepted command appends exactly one event, in command order, recording the account identifier, the command's payload (owner name for openings, amount for money movements), and the command's timestamp.
- AC-3.2: Closing an account appends an account-closed event carrying the account identifier and the command's timestamp.
- AC-3.3: A bank rehydrated from a previously recorded event stream reports the same balances and the same account status as the original.
- AC-3.4: Querying an account in a stream that never recorded that account's opening is rejected with the exact message "account not found".

### US-4: Query balances as of any moment
As an auditor, I want the balance of an account as of a given timestamp, so that I can reconstruct past states.

- AC-4.1: The balance as of a timestamp reflects every event with a timestamp up to and including that moment (after deposits of 100 at time 2 and 50 at time 3, the balance as of time 2 is 100 and as of time 3 is 150).
- AC-4.2: The as-of filter is applied by timestamp across the whole stream, even when recorded events carry out-of-order timestamps.
- AC-4.3: Asking for a balance as of a moment before the account was opened is rejected with the exact message "account not found".

### US-5: Derive statements and summaries
As an account holder, I want statements and a summary of my account, so that I can review activity at a glance.

- AC-5.1: The transaction history lists every deposit and withdrawal in order, each entry carrying its kind ("deposit" or "withdrawal"), its amount, its timestamp, and the running balance after it.
- AC-5.2: Transactions can be filtered to a timestamp range; both bounds are inclusive, and a range containing no transactions yields an empty list.
- AC-5.3: The account summary reports the owner's name, the current balance, the number of transactions (deposits and withdrawals), and the status, "open" or "closed".

## Traceability
```json
{
  "test_open_and_deposit": ["AC-1.1"],
  "test_deposits_accumulate": ["AC-1.2"],
  "test_withdrawal_reduces_balance": ["AC-1.3"],
  "test_withdrawing_entire_balance": ["AC-1.4"],
  "test_overdraw_is_rejected": ["AC-2.1"],
  "test_deposit_without_open_is_rejected": ["AC-2.2"],
  "test_withdraw_without_open_is_rejected": ["AC-2.2"],
  "test_close_with_nonzero_balance_is_rejected": ["AC-2.4"],
  "test_close_with_zero_balance_succeeds": ["AC-2.8"],
  "test_closed_account_rejects_deposits": ["AC-2.5"],
  "test_closed_account_rejects_withdrawals": ["AC-2.5"],
  "test_deposit_amount_must_be_positive": ["AC-2.6"],
  "test_withdrawal_amount_must_be_positive": ["AC-2.7"],
  "test_opening_the_same_account_twice_is_rejected": ["AC-2.3"],
  "test_commands_record_events_in_order": ["AC-3.1"],
  "test_state_rebuilds_from_an_event_stream": ["AC-3.3"],
  "test_balance_at_timestamp": ["AC-4.1"],
  "test_balance_at_timestamp_before_account_opened": ["AC-4.3"],
  "test_transaction_history_with_running_balances": ["AC-5.1"],
  "test_transactions_filtered_by_date_range": ["AC-5.2"],
  "test_account_summary_projection": ["AC-5.3"],
  "test_accounts_are_independent": ["AC-1.6"],
  "test_one_dollar_movements_are_accepted": ["AC-1.5"],
  "test_closing_records_the_event_with_its_timestamp": ["AC-3.2"],
  "test_balance_at_considers_every_event_up_to_the_timestamp": ["AC-4.2"],
  "test_replaying_a_stream_without_an_opening_event_is_rejected": ["AC-3.4"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
