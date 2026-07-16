"""Bank Account kata tests.

Account opens at zero; deposits and withdrawals take injected dates; amounts must be
positive; no overdraft; the statement lists transactions chronologically with a
running balance in the format given by the kata.
"""

import pytest


def test_new_account_has_zero_balance() -> None:
    """Test 1: an account is created with an initial balance of 0."""
    from bank_account import BankAccount

    account = BankAccount()

    assert account.balance == 0


def test_deposit_adds_funds() -> None:
    """Test 2: depositing increases the balance by the deposited amount."""
    from datetime import date

    from bank_account import BankAccount

    account = BankAccount()

    account.deposit(500.00, date(2026, 1, 15))

    assert account.balance == 500.00


def test_multiple_deposits_accumulate() -> None:
    """Test 3: successive deposits are summed into the balance."""
    from datetime import date

    from bank_account import BankAccount

    account = BankAccount()

    account.deposit(500.00, date(2026, 1, 15))
    account.deposit(200.00, date(2026, 1, 25))

    assert account.balance == 700.00


def test_withdraw_removes_funds() -> None:
    """Test 4: withdrawing decreases the balance by the withdrawn amount."""
    from datetime import date

    from bank_account import BankAccount

    account = BankAccount()
    account.deposit(500.00, date(2026, 1, 15))

    account.withdraw(100.00, date(2026, 1, 20))

    assert account.balance == 400.00


def test_withdraw_entire_balance_leaves_zero() -> None:
    """Test 5: withdrawing exactly the current balance is allowed and leaves 0."""
    from datetime import date

    from bank_account import BankAccount

    account = BankAccount()
    account.deposit(250.00, date(2026, 2, 1))

    account.withdraw(250.00, date(2026, 2, 2))

    assert account.balance == 0


def test_deposit_rejects_negative_amount() -> None:
    """Test 6: a negative deposit is rejected with 'Amount must be positive'."""
    from datetime import date

    from bank_account import BankAccount

    account = BankAccount()

    with pytest.raises(ValueError) as exc_info:
        account.deposit(-50.00, date(2026, 1, 15))
    assert str(exc_info.value) == "Amount must be positive"


def test_deposit_rejects_zero_amount() -> None:
    """Test 7: a zero deposit is rejected with 'Amount must be positive'."""
    from datetime import date

    from bank_account import BankAccount

    account = BankAccount()

    with pytest.raises(ValueError, match="Amount must be positive"):
        account.deposit(0, date(2026, 1, 15))


def test_withdraw_rejects_negative_amount() -> None:
    """Test 8: a negative withdrawal is rejected with 'Amount must be positive'."""
    from datetime import date

    from bank_account import BankAccount

    account = BankAccount()
    account.deposit(100.00, date(2026, 1, 15))

    with pytest.raises(ValueError, match="Amount must be positive"):
        account.withdraw(-10.00, date(2026, 1, 16))


def test_withdraw_rejects_zero_amount() -> None:
    """Test 9: a zero withdrawal is rejected with 'Amount must be positive'."""
    from datetime import date

    from bank_account import BankAccount

    account = BankAccount()
    account.deposit(100.00, date(2026, 1, 15))

    with pytest.raises(ValueError, match="Amount must be positive"):
        account.withdraw(0, date(2026, 1, 16))


def test_withdraw_more_than_balance_is_rejected() -> None:
    """Test 10: overdrafts are rejected with 'Cannot withdraw more than current
    balance'."""
    from datetime import date

    from bank_account import BankAccount

    account = BankAccount()
    account.deposit(100.00, date(2026, 1, 15))

    with pytest.raises(ValueError) as exc_info:
        account.withdraw(100.01, date(2026, 1, 16))
    assert str(exc_info.value) == "Cannot withdraw more than current balance"


def test_withdraw_from_empty_account_is_rejected() -> None:
    """Test 11: any withdrawal from a fresh account is an overdraft."""
    from datetime import date

    from bank_account import BankAccount

    account = BankAccount()

    with pytest.raises(ValueError, match="Cannot withdraw more than current balance"):
        account.withdraw(1.00, date(2026, 1, 15))


def test_rejected_operations_do_not_change_state() -> None:
    """Test 12: rejected deposits and withdrawals leave balance and statement
    untouched."""
    from datetime import date

    from bank_account import BankAccount

    account = BankAccount()
    account.deposit(100.00, date(2026, 1, 15))
    statement_before = account.statement()

    for operation in (
        lambda: account.deposit(-5.00, date(2026, 1, 16)),
        lambda: account.deposit(0, date(2026, 1, 16)),
        lambda: account.withdraw(-5.00, date(2026, 1, 16)),
        lambda: account.withdraw(200.00, date(2026, 1, 16)),
    ):
        with pytest.raises(ValueError):
            operation()

    assert account.balance == 100.00
    assert account.statement() == statement_before


def test_statement_of_new_account_is_header_only() -> None:
    """Test 13: with no transactions the statement is just the header line."""
    from bank_account import BankAccount

    account = BankAccount()

    assert account.statement() == "Date       | Amount  | Balance"


def test_statement_single_deposit_line_format() -> None:
    """Test 14: a deposit line shows ISO date, amount and running balance
    right-aligned to seven characters with two decimals."""
    from datetime import date

    from bank_account import BankAccount

    account = BankAccount()
    account.deposit(500.00, date(2026, 1, 15))

    assert account.statement() == (
        "Date       | Amount  | Balance\n2026-01-15 |  500.00 |  500.00"
    )


def test_statement_matches_kata_example() -> None:
    """Test 15: the statement reproduces the kata's example block exactly."""
    from datetime import date

    from bank_account import BankAccount

    account = BankAccount()
    account.deposit(500.00, date(2026, 1, 15))
    account.withdraw(100.00, date(2026, 1, 20))
    account.deposit(200.00, date(2026, 1, 25))

    assert account.statement() == (
        "Date       | Amount  | Balance\n"
        "2026-01-15 |  500.00 |  500.00\n"
        "2026-01-20 | -100.00 |  400.00\n"
        "2026-01-25 |  200.00 |  600.00"
    )


def test_statement_shows_withdrawals_as_negative_amounts() -> None:
    """Test 16: withdrawal lines carry a negative amount with the running
    balance reduced."""
    from datetime import date

    from bank_account import BankAccount

    account = BankAccount()
    account.deposit(80.00, date(2026, 3, 1))
    account.withdraw(30.00, date(2026, 3, 2))

    assert account.statement().splitlines()[2] == "2026-03-02 |  -30.00 |   50.00"


def test_statement_lists_transactions_in_chronological_order() -> None:
    """Test 17: transactions appear oldest first, in the order they were made,
    with the running balance after each one."""
    from datetime import date

    from bank_account import BankAccount

    account = BankAccount()
    account.deposit(10.00, date(2026, 4, 1))
    account.deposit(20.00, date(2026, 4, 2))
    account.withdraw(5.00, date(2026, 4, 3))

    lines = account.statement().splitlines()

    assert lines[1].startswith("2026-04-01")
    assert lines[2].startswith("2026-04-02")
    assert lines[3].startswith("2026-04-03")
    assert lines[3].endswith("  25.00")
