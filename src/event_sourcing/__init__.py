"""Event Sourcing kata: bank accounts whose state is replayed from events.

Four event types record the account lifecycle: AccountOpened,
MoneyDeposited, MoneyWithdrawn, and AccountClosed, each carrying an
injected timestamp. Commands validate against state rebuilt by
replaying the event stream: an account must be opened before any other
operation, deposit and withdrawal amounts must be positive, a
withdrawal may not exceed the balance, closed accounts reject deposits
and withdrawals, and an account may only close with a zero balance.
Projections derive the current balance (deposits minus withdrawals), a
transaction history with running balances, and an account summary
(owner, balance, transaction count, open/closed status). Temporal
queries report the balance as of a timestamp and the transactions
within an inclusive timestamp range.

Kata catalogued at tddbuddy.com/katas/event-sourcing; implementation
and tests original (MIT), machine-authored from the specification,
2026.
"""

from event_sourcing.bank import (
    AccountClosed,
    AccountOpened,
    AccountSummary,
    Bank,
    MoneyDeposited,
    MoneyWithdrawn,
    Transaction,
)

__all__ = [
    "AccountClosed",
    "AccountOpened",
    "AccountSummary",
    "Bank",
    "MoneyDeposited",
    "MoneyWithdrawn",
    "Transaction",
]
