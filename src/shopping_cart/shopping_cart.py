"""Shopping cart with line-item management and stacked discount strategies.

The cart supports adding items (name, unit price, quantity), removing them,
and updating quantities, where updating to zero removes the line. Each line
reports a subtotal and the cart reports an overall total. Discounts follow
the strategy pattern in two tiers. Item-level offers attach to a single
line and reshape its subtotal: "buy X get Y free" makes Y units of every
X+Y-unit group free, and bulk pricing swaps in a special unit price once a
minimum quantity is reached; a line can carry at most one offer. Cart-level
discounts — percentage off, or a fixed amount off (never taking the amount
below zero) — apply after item offers, in the order they were registered.
Special cases: an item may carry limited stock or a maximum quantity per
order, and requests beyond either limit are rejected; an item may be marked
non-combinable with discounts, in which case offers may not attach to it
and cart-level discounts skip its subtotal entirely.

Kata catalogued at tddbuddy.com/katas/shopping-cart; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


class InsufficientStockError(Exception):
    """The requested quantity exceeds the item's available stock."""


class MaxQuantityExceededError(Exception):
    """The requested quantity exceeds the item's per-order maximum."""


class ItemOffer(ABC):
    """Item-level discount strategy that reshapes one line's subtotal."""

    def __init__(self, item_name: str) -> None:
        if not item_name:
            raise ValueError("item name must not be empty")
        self.item_name = item_name

    @abstractmethod
    def subtotal(self, quantity: int, unit_price: float) -> float:
        """Amount charged for the line under this offer."""


class BuyXGetYFree(ItemOffer):
    """Every group of buy+get units includes get free units."""

    def __init__(self, item_name: str, buy: int, get: int) -> None:
        super().__init__(item_name)
        if buy < 1:
            raise ValueError(f"buy must be at least 1, got [{buy}]")
        if get < 1:
            raise ValueError(f"get must be at least 1, got [{get}]")
        self.buy = buy
        self.get = get

    def subtotal(self, quantity: int, unit_price: float) -> float:
        group = self.buy + self.get
        free = (quantity // group) * self.get + max(0, quantity % group - self.buy)
        return (quantity - free) * unit_price


class BulkPrice(ItemOffer):
    """A special unit price once the line reaches a minimum quantity."""

    def __init__(self, item_name: str, min_quantity: int, unit_price: float) -> None:
        super().__init__(item_name)
        if min_quantity < 2:
            raise ValueError(f"min_quantity must be at least 2, got [{min_quantity}]")
        if unit_price < 0:
            raise ValueError(f"unit_price must be non-negative, got [{unit_price}]")
        self.min_quantity = min_quantity
        self.unit_price = unit_price

    def subtotal(self, quantity: int, unit_price: float) -> float:
        if quantity >= self.min_quantity:
            return quantity * self.unit_price
        return quantity * unit_price


class CartDiscount(ABC):
    """Cart-level discount strategy applied to the discountable subtotal."""

    @abstractmethod
    def apply(self, amount: float) -> float:
        """Return the amount after this discount."""


class PercentageDiscount(CartDiscount):
    """Takes a percentage off the discountable subtotal."""

    def __init__(self, percent: float) -> None:
        if not 0 < percent <= 100:
            raise ValueError(
                f"percent must be greater than 0 and at most 100, got [{percent}]"
            )
        self.percent = percent

    def apply(self, amount: float) -> float:
        return amount * (100.0 - self.percent) / 100.0


class FixedAmountDiscount(CartDiscount):
    """Takes a fixed amount off, never dropping below zero."""

    def __init__(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError(f"amount must be positive, got [{amount}]")
        self.amount = amount

    def apply(self, amount: float) -> float:
        return max(0.0, amount - self.amount)


@dataclass
class _LineItem:
    """One cart line: pricing, quantity, limits, and an optional offer."""

    name: str
    unit_price: float
    quantity: int
    stock: int | None
    max_quantity: int | None
    discountable: bool
    offer: ItemOffer | None = None


class ShoppingCart:
    """Holds line items, enforces quantity limits, and prices the order."""

    def __init__(self) -> None:
        self._items: dict[str, _LineItem] = {}
        self._discounts: list[CartDiscount] = []

    def add_item(
        self,
        name: str,
        unit_price: float,
        quantity: int = 1,
        *,
        stock: int | None = None,
        max_quantity: int | None = None,
        discountable: bool = True,
    ) -> None:
        """Add an item, or top up its quantity if it is already in the cart.

        A repeated add keeps the price, limits, and discountability from the
        first add; the combined quantity is checked against the limits.
        """
        if not name:
            raise ValueError("item name must not be empty")
        if unit_price < 0:
            raise ValueError(f"unit_price must be non-negative, got [{unit_price}]")
        if quantity < 1:
            raise ValueError(f"quantity must be at least 1, got [{quantity}]")
        if stock is not None and stock < 0:
            raise ValueError(f"stock must be non-negative, got [{stock}]")
        if max_quantity is not None and max_quantity < 1:
            raise ValueError(f"max_quantity must be at least 1, got [{max_quantity}]")
        existing = self._items.get(name)
        if existing is None:
            self._check_limits(name, quantity, stock, max_quantity)
            self._items[name] = _LineItem(
                name=name,
                unit_price=float(unit_price),
                quantity=quantity,
                stock=stock,
                max_quantity=max_quantity,
                discountable=discountable,
            )
        else:
            combined = existing.quantity + quantity
            self._check_limits(name, combined, existing.stock, existing.max_quantity)
            existing.quantity = combined

    def remove_item(self, name: str) -> None:
        """Remove the named line from the cart."""
        self._require(name)
        del self._items[name]

    def update_quantity(self, name: str, quantity: int) -> None:
        """Set a line's quantity; zero removes the line."""
        item = self._require(name)
        if quantity < 0:
            raise ValueError(f"quantity must be non-negative, got [{quantity}]")
        if quantity == 0:
            del self._items[name]
            return
        self._check_limits(name, quantity, item.stock, item.max_quantity)
        item.quantity = quantity

    def quantity_of(self, name: str) -> int:
        """Quantity of the named item currently in the cart (0 if absent)."""
        item = self._items.get(name)
        return 0 if item is None else item.quantity

    def add_offer(self, offer: ItemOffer) -> None:
        """Attach an item-level offer to its line (one offer per line)."""
        item = self._items.get(offer.item_name)
        if item is None:
            raise ValueError(f"item [{offer.item_name}] is not in the cart")
        if not item.discountable:
            raise ValueError(
                f"item [{offer.item_name}] cannot be combined with discounts"
            )
        if item.offer is not None:
            raise ValueError(f"item [{offer.item_name}] already has an offer")
        item.offer = offer

    def add_discount(self, discount: CartDiscount) -> None:
        """Register a cart-level discount; discounts apply in registration order."""
        self._discounts.append(discount)

    def item_subtotal(self, name: str) -> float:
        """The line's subtotal after any item-level offer, rounded to cents."""
        return round(self._line_subtotal(self._require(name)), 2)

    def subtotal(self) -> float:
        """Sum of line subtotals before cart-level discounts, rounded to cents."""
        return round(sum(self._line_subtotal(item) for item in self._items.values()), 2)

    def total(self) -> float:
        """The order total after item offers and cart-level discounts.

        Cart-level discounts apply, in registration order, only to the
        subtotal of discountable lines; non-combinable lines are added on
        top unchanged.
        """
        discountable = sum(
            self._line_subtotal(item)
            for item in self._items.values()
            if item.discountable
        )
        exempt = sum(
            self._line_subtotal(item)
            for item in self._items.values()
            if not item.discountable
        )
        for discount in self._discounts:
            discountable = discount.apply(discountable)
        return round(discountable + exempt, 2)

    def _require(self, name: str) -> _LineItem:
        item = self._items.get(name)
        if item is None:
            raise ValueError(f"item [{name}] is not in the cart")
        return item

    @staticmethod
    def _line_subtotal(item: _LineItem) -> float:
        if item.offer is not None:
            return item.offer.subtotal(item.quantity, item.unit_price)
        return item.quantity * item.unit_price

    @staticmethod
    def _check_limits(
        name: str, requested: int, stock: int | None, max_quantity: int | None
    ) -> None:
        if stock is not None and requested > stock:
            raise InsufficientStockError(
                f"only [{stock}] of [{name}] in stock, requested [{requested}]"
            )
        if max_quantity is not None and requested > max_quantity:
            raise MaxQuantityExceededError(
                f"maximum [{max_quantity}] of [{name}] per order, "
                f"requested [{requested}]"
            )
