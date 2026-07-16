"""Money class for multi-currency calculations"""

from typing import Protocol


class Expression(Protocol):
    """Expression interface for money operations"""

    def plus(self, addend: "Expression") -> "Expression":
        """Add another expression"""
        ...

    def times(self, multiplier: int) -> "Expression":
        """Multiply by a factor"""
        ...

    def reduce(self, bank: "Bank", to: str) -> "Money":
        """Reduce to a specific currency"""
        ...


class Bank:
    """Bank handles currency conversion"""

    def __init__(self) -> None:
        self.rates: dict[tuple[str, str], int] = {}

    def add_rate(self, from_currency: str, to_currency: str, rate: int) -> None:
        """Add an exchange rate"""
        self.rates[(from_currency, to_currency)] = rate

    def reduce(self, source: "Expression | Money", to: str) -> "Money":
        """Reduce an expression to a given currency"""
        return source.reduce(self, to)


class Money:
    """Represents money in a specific currency"""

    def __init__(self, amount: int, currency_code: str) -> None:
        self.amount = amount
        self._currency = currency_code

    @staticmethod
    def dollar(amount: int) -> "Money":
        """Create a dollar amount"""
        return Money(amount, "USD")

    @staticmethod
    def franc(amount: int) -> "Money":
        """Create a franc amount"""
        return Money(amount, "CHF")

    def times(self, multiplier: int) -> "Money":
        """Multiply money by a factor"""
        return Money(self.amount * multiplier, self._currency)

    def equals(self, other: "Money") -> bool:
        """Check if two money amounts are equal"""
        return self.amount == other.amount and self._currency == other._currency

    def currency(self) -> str:
        """Get the currency code"""
        return self._currency

    def plus(self, addend: "Expression") -> "Expression":
        """Add two money amounts"""
        return Sum(self, addend)

    def reduce(self, bank: "Bank", to: str) -> "Money":
        """Reduce this money to a specific currency"""
        if self._currency == to:
            return self
        pair = (self._currency, to)
        if pair not in bank.rates:
            raise KeyError(f"no exchange rate registered for {self._currency}->{to}")
        return Money(self.amount // bank.rates[pair], to)


class Sum:
    """Represents the sum of two expressions"""

    def __init__(self, augend: Expression, addend: Expression) -> None:
        self.augend = augend
        self.addend = addend

    def plus(self, addend: Expression) -> Expression:
        """Add another expression to this sum"""
        return Sum(self, addend)

    def times(self, multiplier: int) -> Expression:
        """Multiply this sum by a factor"""
        return Sum(self.augend.times(multiplier), self.addend.times(multiplier))

    def reduce(self, bank: Bank, to: str) -> Money:
        """Reduce this sum to a specific currency"""
        amount = (
            self.augend.reduce(bank, to).amount + self.addend.reduce(bank, to).amount
        )
        return Money(amount, to)
