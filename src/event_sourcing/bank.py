"""Event-sourced bank: events, command validation, and projections."""

from collections.abc import Iterable
from dataclasses import dataclass, field


@dataclass(frozen=True)
class AccountOpened:
    account_id: str
    owner_name: str
    timestamp: int


@dataclass(frozen=True)
class MoneyDeposited:
    account_id: str
    amount: int
    timestamp: int


@dataclass(frozen=True)
class MoneyWithdrawn:
    account_id: str
    amount: int
    timestamp: int


@dataclass(frozen=True)
class AccountClosed:
    account_id: str
    timestamp: int


Event = AccountOpened | MoneyDeposited | MoneyWithdrawn | AccountClosed


@dataclass(frozen=True)
class Transaction:
    """One deposit or withdrawal with the running balance after it."""

    kind: str  # "deposit" or "withdrawal"
    amount: int
    timestamp: int
    balance: int


@dataclass(frozen=True)
class AccountSummary:
    """Projection of an account's headline figures."""

    owner_name: str
    balance: int
    transaction_count: int
    status: str  # "open" or "closed"


@dataclass
class _AccountState:
    """State rebuilt by replaying an account's events."""

    owner_name: str
    balance: int = 0
    closed: bool = False
    transactions: list[Transaction] = field(default_factory=list)


class Bank:
    """Command handler and event store; all state derives from event replay."""

    def __init__(self, events: Iterable[Event] = ()) -> None:
        self._events: list[Event] = list(events)

    @property
    def events(self) -> tuple[Event, ...]:
        """The recorded event stream, in order."""
        return tuple(self._events)

    def open_account(self, account_id: str, owner_name: str, timestamp: int) -> None:
        """Record an AccountOpened event for a new account id."""
        if self._replay(account_id) is not None:
            raise ValueError("account already exists")
        self._events.append(AccountOpened(account_id, owner_name, timestamp))

    def deposit(self, account_id: str, amount: int, timestamp: int) -> None:
        """Record a MoneyDeposited event after validating the command."""
        self._require_open(account_id)
        if amount <= 0:
            raise ValueError("deposit amount must be positive")
        self._events.append(MoneyDeposited(account_id, amount, timestamp))

    def withdraw(self, account_id: str, amount: int, timestamp: int) -> None:
        """Record a MoneyWithdrawn event after validating the command."""
        state = self._require_open(account_id)
        if amount <= 0:
            raise ValueError("withdrawal amount must be positive")
        if amount > state.balance:
            raise ValueError("insufficient funds")
        self._events.append(MoneyWithdrawn(account_id, amount, timestamp))

    def close_account(self, account_id: str, timestamp: int) -> None:
        """Record an AccountClosed event; only zero-balance accounts may close."""
        state = self._require_open(account_id)
        if state.balance != 0:
            raise ValueError("balance must be zero")
        self._events.append(AccountClosed(account_id, timestamp))

    def balance(self, account_id: str) -> int:
        """Current balance: replayed deposits minus withdrawals."""
        return self._require_existing(account_id).balance

    def balance_at(self, account_id: str, timestamp: int) -> int:
        """Balance considering only events at or before the timestamp."""
        state = self._replay(account_id, up_to=timestamp)
        if state is None:
            raise ValueError("account not found")
        return state.balance

    def transaction_history(self, account_id: str) -> list[Transaction]:
        """All deposits and withdrawals with running balances, in order."""
        return list(self._require_existing(account_id).transactions)

    def transactions_between(self, account_id: str, start: int, end: int) -> list[Transaction]:
        """Transactions whose timestamps fall within [start, end]."""
        history = self._require_existing(account_id).transactions
        return [entry for entry in history if start <= entry.timestamp <= end]

    def account_summary(self, account_id: str) -> AccountSummary:
        """Owner name, balance, transaction count, and open/closed status."""
        state = self._require_existing(account_id)
        return AccountSummary(
            owner_name=state.owner_name,
            balance=state.balance,
            transaction_count=len(state.transactions),
            status="closed" if state.closed else "open",
        )

    def _require_existing(self, account_id: str) -> _AccountState:
        state = self._replay(account_id)
        if state is None:
            raise ValueError("account not found")
        return state

    def _require_open(self, account_id: str) -> _AccountState:
        state = self._require_existing(account_id)
        if state.closed:
            raise ValueError("account is closed")
        return state

    def _replay(self, account_id: str, up_to: int | None = None) -> _AccountState | None:
        state: _AccountState | None = None
        for event in self._events:
            if event.account_id != account_id:
                continue
            if up_to is not None and event.timestamp > up_to:
                continue
            state = self._apply(state, event)
        return state

    @staticmethod
    def _apply(state: _AccountState | None, event: Event) -> _AccountState:
        if isinstance(event, AccountOpened):
            return _AccountState(owner_name=event.owner_name)
        if state is None:
            raise ValueError("account not found")
        if isinstance(event, MoneyDeposited):
            state.balance += event.amount
            state.transactions.append(
                Transaction("deposit", event.amount, event.timestamp, state.balance)
            )
        elif isinstance(event, MoneyWithdrawn):
            state.balance -= event.amount
            state.transactions.append(
                Transaction("withdrawal", event.amount, event.timestamp, state.balance)
            )
        else:
            state.closed = True
        return state
