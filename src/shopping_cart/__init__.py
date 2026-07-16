"""Shopping Cart kata: line items, quantity limits, and stacked discount strategies.

Kata catalogued at tddbuddy.com/katas/shopping-cart; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from shopping_cart.shopping_cart import (
    BulkPrice,
    BuyXGetYFree,
    CartDiscount,
    FixedAmountDiscount,
    InsufficientStockError,
    ItemOffer,
    MaxQuantityExceededError,
    PercentageDiscount,
    ShoppingCart,
)

__all__ = [
    "BulkPrice",
    "BuyXGetYFree",
    "CartDiscount",
    "FixedAmountDiscount",
    "InsufficientStockError",
    "ItemOffer",
    "MaxQuantityExceededError",
    "PercentageDiscount",
    "ShoppingCart",
]
