"""Bank Account kata.

A simple bank account that opens with a balance of zero and supports deposits,
withdrawals, balance retrieval and a printable statement. Transaction dates are
injected by the caller as ``datetime.date`` values; the system clock is never read.

Rules:

- ``deposit`` adds funds; ``withdraw`` removes funds. Each records a transaction with
  its date and amount.
- Amounts must be positive: zero and negative amounts are rejected with
  ValueError("Amount must be positive").
- No overdraft: withdrawing more than the current balance is rejected with
  ValueError("Cannot withdraw more than current balance").
- ``balance`` returns the current balance.
- ``statement`` returns the transaction history, oldest first, one line per
  transaction with a running balance, formatted as::

      Date       | Amount  | Balance
      2026-01-15 |  500.00 |  500.00
      2026-01-20 | -100.00 |  400.00
      2026-01-25 |  200.00 |  600.00

  Dates are ISO formatted; withdrawals appear as negative amounts; amount and balance
  are right-aligned to seven characters with two decimal places.

Kata catalogued at tddbuddy.com/katas/bank-account; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from __future__ import annotations

from datetime import date

_STATEMENT_HEADER = "Date       | Amount  | Balance"


class BankAccount:
    """A bank account with injected transaction dates and no overdraft."""

    def __init__(self) -> None:
        self._balance = 0.0
        self._transactions: list[tuple[date, float, float]] = []

    @property
    def balance(self) -> float:
        """The current account balance."""
        return self._balance

    def deposit(self, amount: float, on: date) -> None:
        """Add ``amount`` to the account, recorded against the date ``on``."""
        self._require_positive(amount)
        self._balance += amount
        self._transactions.append((on, amount, self._balance))

    def withdraw(self, amount: float, on: date) -> None:
        """Remove ``amount`` from the account, recorded against the date ``on``."""
        self._require_positive(amount)
        if amount > self._balance:
            raise ValueError("Cannot withdraw more than current balance")
        self._balance -= amount
        self._transactions.append((on, -amount, self._balance))

    def statement(self) -> str:
        """Return the formatted statement: header plus one line per transaction."""
        lines = [_STATEMENT_HEADER]
        for on, amount, running_balance in self._transactions:
            lines.append(f"{on.isoformat()} | {amount:>7.2f} | {running_balance:>7.2f}")
        return "\n".join(lines)

    @staticmethod
    def _require_positive(amount: float) -> None:
        if amount <= 0:
            raise ValueError("Amount must be positive")
