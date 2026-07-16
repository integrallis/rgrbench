"""Recipe Calculator kata.

Scale a recipe, given as a mapping of ingredient names to quantities, by a
numeric factor. Every quantity is multiplied by the factor, keeping all
ingredients in proportion, and results are rounded to a fixed number of
decimal places so binary floating-point noise does not leak into quantities.
A factor of 1 leaves quantities unchanged, a factor of 0 zeroes them, and the
input mapping is never mutated. Negative factors are rejected, as are
ingredients whose quantities are zero or negative.

Kata catalogued at tddbuddy.com/katas/recipe-calculator; implementation and
tests original (MIT), machine-authored from the specification, 2026.
"""


def scale(
    recipe: dict[str, float], factor: float, precision: int = 2
) -> dict[str, float]:
    """Return a new recipe with every quantity multiplied by ``factor``."""
    if factor < 0:
        raise ValueError(f"scaling factor must be non-negative, got {factor}")
    for name, quantity in recipe.items():
        if quantity <= 0:
            raise ValueError(
                f"ingredient {name!r} must have a positive quantity, got {quantity}"
            )
    return {
        name: round(quantity * factor, precision) for name, quantity in recipe.items()
    }
