"""Heavy Metal Bake Sale kata.

A band's bake-sale till: a shopper hands over a comma-separated list of item
codes (B = Brownie $0.75, M = Muffin $1.00, C = Cake Pop $1.35, W = Water
$1.50) drawn from a starting inventory of 48 brownies, 36 muffins, 24 cake
pops and 30 bottles of water. When every requested item is in stock the till
quotes the total due; if any item has run out the sale is refused with
"<Item> is out of stock". Payment at or above the total completes the sale,
consumes stock, and yields the change (possibly $0.00); a short payment is
refused with "Not enough money" and leaves stock untouched. Amounts are
displayed as dollar strings with two decimals.

Divergence note: the upstream page shows an example transaction "B,C,W ->
$3.50", which contradicts its own price table (0.75 + 1.35 + 1.50 = 3.60).
The price table is taken as authoritative here, so B,C,W totals $3.60; the
page's other three examples agree with the table.

Kata catalogued at tddbuddy.com/katas/heavy-metal-bake-sale; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from collections import Counter
from collections.abc import Mapping
from decimal import Decimal

ITEMS: dict[str, tuple[str, Decimal]] = {
    "B": ("Brownie", Decimal("0.75")),
    "M": ("Muffin", Decimal("1.00")),
    "C": ("Cake Pop", Decimal("1.35")),
    "W": ("Water", Decimal("1.50")),
}

DEFAULT_STOCK: dict[str, int] = {"B": 48, "M": 36, "C": 24, "W": 30}


class OutOfStockError(Exception):
    """Raised when an ordered item is not available in sufficient quantity."""


class NotEnoughMoneyError(Exception):
    """Raised when the payment does not cover the order total."""


def format_money(amount: Decimal) -> str:
    """Format ``amount`` as a dollar string with two decimal places."""
    return f"${amount.quantize(Decimal('0.01'))}"


class BakeSale:
    """Till for the bake sale: quotes totals and completes cash sales."""

    def __init__(self, stock: Mapping[str, int] | None = None) -> None:
        self._stock: dict[str, int] = dict(DEFAULT_STOCK if stock is None else stock)

    def stock_of(self, code: str) -> int:
        """Return the remaining quantity of the item with ``code``."""
        return self._stock.get(code, 0)

    def total(self, order: str) -> str:
        """Return the amount due for ``order`` as a dollar string.

        Raises OutOfStockError when any requested item is unavailable.
        """
        codes = self._parse(order)
        self._check_stock(codes)
        return format_money(self._sum(codes))

    def pay(self, order: str, amount_paid: Decimal | str) -> str:
        """Complete the sale of ``order`` and return the change due.

        Raises OutOfStockError when any item is unavailable and
        NotEnoughMoneyError when the payment is below the total; stock is
        only decremented on a completed sale.
        """
        codes = self._parse(order)
        self._check_stock(codes)
        due = self._sum(codes)
        paid = Decimal(amount_paid)
        if paid < due:
            raise NotEnoughMoneyError("Not enough money")
        for code in codes:
            self._stock[code] -= 1
        return format_money(paid - due)

    @staticmethod
    def _parse(order: str) -> list[str]:
        codes = [part.strip() for part in order.split(",") if part.strip()]
        for code in codes:
            if code not in ITEMS:
                raise ValueError(f"Unknown item code: {code}")
        return codes

    def _check_stock(self, codes: list[str]) -> None:
        for code, quantity in Counter(codes).items():
            if self._stock.get(code, 0) < quantity:
                raise OutOfStockError(f"{ITEMS[code][0]} is out of stock")

    @staticmethod
    def _sum(codes: list[str]) -> Decimal:
        return sum((ITEMS[code][1] for code in codes), Decimal("0.00"))
