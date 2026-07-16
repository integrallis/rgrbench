"""Supermarket Pricing kata - checkout total with layered pricing rules.

A checkout scans items and reports the running total. Unit prices: A 50,
B 30, C 20, D 15. Multi-buy specials, independent of scan order: three
A for 130 and two B for 45. Item C is buy-one-get-one-free, so every
second C in a pair is free. Bananas (1.99 per kilogram) and Apples
(3.49 per kilogram) are weighed items; each weighed line is rounded to
the nearest cent, half up. A combo prices one D plus one C together at
25; each disjoint {D, C} pair forms one qualifying set, the combo applies
once per set before the per-item offers, and combo items do not count
towards other offers. Totals are exact decimals.

Kata catalogued at tddbuddy.com/katas/supermarket-pricing; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from decimal import ROUND_HALF_UP, Decimal

_UNIT_PRICES: dict[str, Decimal] = {
    "A": Decimal(50),
    "B": Decimal(30),
    "C": Decimal(20),
    "D": Decimal(15),
}

_MULTI_BUY: dict[str, tuple[int, Decimal]] = {
    "A": (3, Decimal(130)),
    "B": (2, Decimal(45)),
}

_BOGOF_ITEMS = frozenset({"C"})

_PER_KILO_PRICES: dict[str, Decimal] = {
    "Bananas": Decimal("1.99"),
    "Apples": Decimal("3.49"),
}

_COMBO_ITEMS = ("D", "C")
_COMBO_PRICE = Decimal(25)

_CENT = Decimal("0.01")


class Checkout:
    """Accumulates scanned items and computes the discounted total."""

    def __init__(self) -> None:
        self._counts: dict[str, int] = {}
        self._weighed_lines: list[Decimal] = []

    def scan(self, item: str) -> None:
        """Add one unit-priced item to the basket."""
        if item not in _UNIT_PRICES:
            raise ValueError(f"Unknown item: {item}")
        self._counts[item] = self._counts.get(item, 0) + 1

    def scan_weighed(self, item: str, kilograms: Decimal | str | float) -> None:
        """Add a weighed item; its line price is rounded to the nearest cent."""
        if item not in _PER_KILO_PRICES:
            raise ValueError(f"Unknown item: {item}")
        weight = Decimal(str(kilograms))
        if weight <= 0:
            raise ValueError("weight must be positive")
        line = (_PER_KILO_PRICES[item] * weight).quantize(_CENT, rounding=ROUND_HALF_UP)
        self._weighed_lines.append(line)

    def total(self) -> Decimal:
        """Return the basket total with all pricing rules applied."""
        counts = dict(self._counts)
        total = self._apply_combo(counts)
        for item, count in counts.items():
            total += self._price_item(item, count)
        return total + sum(self._weighed_lines, Decimal(0))

    @staticmethod
    def _apply_combo(counts: dict[str, int]) -> Decimal:
        first, second = _COMBO_ITEMS
        sets = min(counts.get(first, 0), counts.get(second, 0))
        if sets:
            counts[first] -= sets
            counts[second] -= sets
        return sets * _COMBO_PRICE

    @staticmethod
    def _price_item(item: str, count: int) -> Decimal:
        unit = _UNIT_PRICES[item]
        if item in _MULTI_BUY:
            size, deal_price = _MULTI_BUY[item]
            return (count // size) * deal_price + (count % size) * unit
        if item in _BOGOF_ITEMS:
            paid = count - count // 2
            return paid * unit
        return count * unit
