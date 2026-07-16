"""Event Sourcing Kata - bank account state replayed from an event stream
Commands validate against replayed state; projections and temporal queries derive from events.
"""


def test_open_and_deposit() -> None:
    """Test 1: Open, deposit $100 -> balance $100"""
    from event_sourcing import Bank

    bank = Bank()
    bank.open_account("acc-1", "Alice", timestamp=1)
    bank.deposit("acc-1", 100, timestamp=2)
    assert bank.balance("acc-1") == 100


def test_deposits_accumulate() -> None:
    """Test 2: Open, deposit $100, deposit $50 -> balance $150"""
    from event_sourcing import Bank

    bank = Bank()
    bank.open_account("acc-1", "Alice", timestamp=1)
    bank.deposit("acc-1", 100, timestamp=2)
    bank.deposit("acc-1", 50, timestamp=3)
    assert bank.balance("acc-1") == 150


def test_withdrawal_reduces_balance() -> None:
    """Test 3: Open, deposit $100, withdraw $30 -> balance $70"""
    from event_sourcing import Bank

    bank = Bank()
    bank.open_account("acc-1", "Alice", timestamp=1)
    bank.deposit("acc-1", 100, timestamp=2)
    bank.withdraw("acc-1", 30, timestamp=3)
    assert bank.balance("acc-1") == 70


def test_withdrawing_entire_balance() -> None:
    """Test 4: Open, deposit $100, withdraw $100 -> balance $0"""
    from event_sourcing import Bank

    bank = Bank()
    bank.open_account("acc-1", "Alice", timestamp=1)
    bank.deposit("acc-1", 100, timestamp=2)
    bank.withdraw("acc-1", 100, timestamp=3)
    assert bank.balance("acc-1") == 0


def test_overdraw_is_rejected() -> None:
    """Test 5: Withdrawing more than the balance raises insufficient funds"""
    import pytest

    from event_sourcing import Bank

    bank = Bank()
    bank.open_account("acc-1", "Alice", timestamp=1)
    bank.deposit("acc-1", 100, timestamp=2)
    with pytest.raises(ValueError) as excinfo:
        bank.withdraw("acc-1", 150, timestamp=3)
    assert str(excinfo.value) == "insufficient funds"
    assert bank.balance("acc-1") == 100


def test_deposit_without_open_is_rejected() -> None:
    """Test 6: Depositing to an unopened account raises account not found"""
    import pytest

    from event_sourcing import Bank

    bank = Bank()
    with pytest.raises(ValueError) as excinfo:
        bank.deposit("acc-1", 100, timestamp=1)
    assert str(excinfo.value) == "account not found"


def test_withdraw_without_open_is_rejected() -> None:
    """Test 7: Withdrawing from an unopened account raises account not found"""
    import pytest

    from event_sourcing import Bank

    bank = Bank()
    with pytest.raises(ValueError, match="account not found"):
        bank.withdraw("acc-1", 100, timestamp=1)


def test_close_with_nonzero_balance_is_rejected() -> None:
    """Test 8: Open, deposit $100, close -> error: balance must be zero"""
    import pytest

    from event_sourcing import Bank

    bank = Bank()
    bank.open_account("acc-1", "Alice", timestamp=1)
    bank.deposit("acc-1", 100, timestamp=2)
    with pytest.raises(ValueError) as excinfo:
        bank.close_account("acc-1", timestamp=3)
    assert str(excinfo.value) == "balance must be zero"


def test_close_with_zero_balance_succeeds() -> None:
    """Test 9: Open, deposit $100, withdraw $100, close -> account is closed"""
    from event_sourcing import Bank

    bank = Bank()
    bank.open_account("acc-1", "Alice", timestamp=1)
    bank.deposit("acc-1", 100, timestamp=2)
    bank.withdraw("acc-1", 100, timestamp=3)
    bank.close_account("acc-1", timestamp=4)
    assert bank.account_summary("acc-1").status == "closed"


def test_closed_account_rejects_deposits() -> None:
    """Test 10: Depositing to a closed account raises account is closed"""
    import pytest

    from event_sourcing import Bank

    bank = Bank()
    bank.open_account("acc-1", "Alice", timestamp=1)
    bank.close_account("acc-1", timestamp=2)
    with pytest.raises(ValueError) as excinfo:
        bank.deposit("acc-1", 100, timestamp=3)
    assert str(excinfo.value) == "account is closed"


def test_closed_account_rejects_withdrawals() -> None:
    """Test 11: Withdrawing from a closed account raises account is closed"""
    import pytest

    from event_sourcing import Bank

    bank = Bank()
    bank.open_account("acc-1", "Alice", timestamp=1)
    bank.close_account("acc-1", timestamp=2)
    with pytest.raises(ValueError, match="account is closed"):
        bank.withdraw("acc-1", 100, timestamp=3)


def test_deposit_amount_must_be_positive() -> None:
    """Test 12: Zero and negative deposits are rejected"""
    import pytest

    from event_sourcing import Bank

    bank = Bank()
    bank.open_account("acc-1", "Alice", timestamp=1)
    with pytest.raises(ValueError) as excinfo:
        bank.deposit("acc-1", 0, timestamp=2)
    assert str(excinfo.value) == "deposit amount must be positive"
    with pytest.raises(ValueError, match="deposit amount must be positive"):
        bank.deposit("acc-1", -50, timestamp=2)


def test_withdrawal_amount_must_be_positive() -> None:
    """Test 13: Zero and negative withdrawals are rejected"""
    import pytest

    from event_sourcing import Bank

    bank = Bank()
    bank.open_account("acc-1", "Alice", timestamp=1)
    bank.deposit("acc-1", 100, timestamp=2)
    with pytest.raises(ValueError) as excinfo:
        bank.withdraw("acc-1", 0, timestamp=3)
    assert str(excinfo.value) == "withdrawal amount must be positive"
    with pytest.raises(ValueError, match="withdrawal amount must be positive"):
        bank.withdraw("acc-1", -10, timestamp=3)


def test_opening_the_same_account_twice_is_rejected() -> None:
    """Test 14: An account id may only be opened once"""
    import pytest

    from event_sourcing import Bank

    bank = Bank()
    bank.open_account("acc-1", "Alice", timestamp=1)
    with pytest.raises(ValueError) as excinfo:
        bank.open_account("acc-1", "Bob", timestamp=2)
    assert str(excinfo.value) == "account already exists"


def test_commands_record_events_in_order() -> None:
    """Test 15: Each command appends its event, in order, with its payload"""
    from event_sourcing import AccountOpened, Bank, MoneyDeposited, MoneyWithdrawn

    bank = Bank()
    bank.open_account("acc-1", "Alice", timestamp=1)
    bank.deposit("acc-1", 100, timestamp=2)
    bank.withdraw("acc-1", 30, timestamp=3)
    assert bank.events == (
        AccountOpened("acc-1", "Alice", 1),
        MoneyDeposited("acc-1", 100, 2),
        MoneyWithdrawn("acc-1", 30, 3),
    )


def test_state_rebuilds_from_an_event_stream() -> None:
    """Test 16: A bank rehydrated from recorded events reports the same balance"""
    from event_sourcing import AccountOpened, Bank, MoneyDeposited, MoneyWithdrawn

    events = [
        AccountOpened("acc-1", "Alice", 1),
        MoneyDeposited("acc-1", 100, 2),
        MoneyWithdrawn("acc-1", 30, 3),
    ]
    rehydrated = Bank(events)
    assert rehydrated.balance("acc-1") == 70
    assert rehydrated.account_summary("acc-1").status == "open"


def test_balance_at_timestamp() -> None:
    """Test 17: Balance at T2, after the first deposit of three events, is $100"""
    from event_sourcing import Bank

    bank = Bank()
    bank.open_account("acc-1", "Alice", timestamp=1)
    bank.deposit("acc-1", 100, timestamp=2)
    bank.deposit("acc-1", 50, timestamp=3)
    assert bank.balance_at("acc-1", timestamp=2) == 100
    assert bank.balance_at("acc-1", timestamp=3) == 150


def test_balance_at_timestamp_before_account_opened() -> None:
    """Test 18: A temporal query before the account opened finds no account"""
    import pytest

    from event_sourcing import Bank

    bank = Bank()
    bank.open_account("acc-1", "Alice", timestamp=5)
    bank.deposit("acc-1", 100, timestamp=6)
    with pytest.raises(ValueError) as excinfo:
        bank.balance_at("acc-1", timestamp=4)
    assert str(excinfo.value) == "account not found"


def test_transaction_history_with_running_balances() -> None:
    """Test 19: History lists every deposit and withdrawal with its running balance"""
    from event_sourcing import Bank, Transaction

    bank = Bank()
    bank.open_account("acc-1", "Alice", timestamp=1)
    bank.deposit("acc-1", 100, timestamp=2)
    bank.withdraw("acc-1", 30, timestamp=3)
    bank.deposit("acc-1", 5, timestamp=4)
    assert bank.transaction_history("acc-1") == [
        Transaction("deposit", 100, 2, 100),
        Transaction("withdrawal", 30, 3, 70),
        Transaction("deposit", 5, 4, 75),
    ]


def test_transactions_filtered_by_date_range() -> None:
    """Test 20: A date-range query returns transactions within the inclusive bounds"""
    from event_sourcing import Bank, Transaction

    bank = Bank()
    bank.open_account("acc-1", "Alice", timestamp=1)
    bank.deposit("acc-1", 100, timestamp=2)
    bank.withdraw("acc-1", 30, timestamp=5)
    bank.deposit("acc-1", 5, timestamp=9)
    assert bank.transactions_between("acc-1", start=2, end=5) == [
        Transaction("deposit", 100, 2, 100),
        Transaction("withdrawal", 30, 5, 70),
    ]
    assert bank.transactions_between("acc-1", start=6, end=8) == []


def test_account_summary_projection() -> None:
    """Test 21: The summary reports owner, balance, transaction count, and status"""
    from event_sourcing import Bank

    bank = Bank()
    bank.open_account("acc-1", "Alice", timestamp=1)
    bank.deposit("acc-1", 100, timestamp=2)
    bank.withdraw("acc-1", 30, timestamp=3)
    summary = bank.account_summary("acc-1")
    assert summary.owner_name == "Alice"
    assert summary.balance == 70
    assert summary.transaction_count == 2
    assert summary.status == "open"


def test_accounts_are_independent() -> None:
    """Test 22: Events for one account never affect another's balance"""
    from event_sourcing import Bank

    bank = Bank()
    bank.open_account("acc-1", "Alice", timestamp=1)
    bank.open_account("acc-2", "Bob", timestamp=2)
    bank.deposit("acc-1", 100, timestamp=3)
    bank.deposit("acc-2", 25, timestamp=4)
    bank.withdraw("acc-1", 40, timestamp=5)
    assert bank.balance("acc-1") == 60
    assert bank.balance("acc-2") == 25


def test_one_dollar_movements_are_accepted() -> None:
    """Test 23: A deposit or withdrawal of exactly $1 is valid"""
    from event_sourcing import Bank

    bank = Bank()
    bank.open_account("acc-1", "Alice", timestamp=1)
    bank.deposit("acc-1", 1, timestamp=2)
    assert bank.balance("acc-1") == 1
    bank.withdraw("acc-1", 1, timestamp=3)
    assert bank.balance("acc-1") == 0


def test_closing_records_the_event_with_its_timestamp() -> None:
    """Test 24: Closing an account appends an AccountClosed event carrying the
    command's timestamp"""
    from event_sourcing import AccountClosed, AccountOpened, Bank

    bank = Bank()
    bank.open_account("acc-1", "Alice", timestamp=1)
    bank.close_account("acc-1", timestamp=2)
    assert bank.events == (
        AccountOpened("acc-1", "Alice", 1),
        AccountClosed("acc-1", 2),
    )


def test_balance_at_considers_every_event_up_to_the_timestamp() -> None:
    """Test 25: A temporal query filters by timestamp across the whole stream,
    even when recorded events carry out-of-order timestamps"""
    from event_sourcing import AccountOpened, Bank, MoneyDeposited

    events = [
        AccountOpened("acc-1", "Alice", 1),
        MoneyDeposited("acc-1", 100, 10),
        MoneyDeposited("acc-1", 50, 5),
    ]
    bank = Bank(events)
    assert bank.balance_at("acc-1", timestamp=5) == 50
    assert bank.balance_at("acc-1", timestamp=10) == 150


def test_replaying_a_stream_without_an_opening_event_is_rejected() -> None:
    """Test 26: Querying a stream whose account was never opened raises
    account not found"""
    import pytest

    from event_sourcing import Bank, MoneyDeposited

    bank = Bank([MoneyDeposited("acc-1", 100, 1)])
    with pytest.raises(ValueError) as excinfo:
        bank.balance("acc-1")
    assert str(excinfo.value) == "account not found"
