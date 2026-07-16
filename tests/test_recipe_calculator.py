"""Recipe Calculator kata: scale a recipe's ingredient quantities by a factor.

Kata catalogued at tddbuddy.com/katas/recipe-calculator; implementation and
tests original (MIT), machine-authored from the specification, 2026.
"""


def test_empty_recipe_scales_to_empty_recipe() -> None:
    """Test 1: Scaling an empty recipe yields an empty recipe"""
    from recipe_calculator import scale

    assert scale({}, 2) == {}


def test_single_ingredient_doubles() -> None:
    """Test 2: A single ingredient is multiplied by the factor"""
    from recipe_calculator import scale

    assert scale({"flour": 200}, 2) == {"flour": 400}


def test_multiple_ingredients_stay_in_proportion() -> None:
    """Test 3: Every ingredient in a multi-ingredient recipe is scaled alike"""
    from recipe_calculator import scale

    recipe = {"flour": 200, "sugar": 100, "butter": 50}
    assert scale(recipe, 3) == {"flour": 600, "sugar": 300, "butter": 150}


def test_identity_factor_returns_unchanged_quantities() -> None:
    """Test 4: A factor of 1 leaves all quantities unchanged"""
    from recipe_calculator import scale

    recipe = {"milk": 250.0, "eggs": 2.0}
    assert scale(recipe, 1) == {"milk": 250.0, "eggs": 2.0}


def test_zero_factor_zeroes_all_quantities() -> None:
    """Test 5: A factor of 0 zeroes every quantity"""
    from recipe_calculator import scale

    assert scale({"milk": 250, "eggs": 2}, 0) == {"milk": 0, "eggs": 0}


def test_fractional_factor_halves_quantities() -> None:
    """Test 6: A factor of 0.5 halves every quantity"""
    from recipe_calculator import scale

    assert scale({"flour": 300, "salt": 5}, 0.5) == {"flour": 150, "salt": 2.5}


def test_fractional_quantities_are_supported() -> None:
    """Test 7: Fractional ingredient quantities scale to fractional results"""
    from recipe_calculator import scale

    assert scale({"vanilla": 1.5}, 1.5) == {"vanilla": 2.25}


def test_rounding_absorbs_floating_point_noise() -> None:
    """Test 8: 0.1 scaled by 3 is exactly 0.3 after rounding"""
    from recipe_calculator import scale

    assert scale({"yeast": 0.1}, 3) == {"yeast": 0.3}


def test_results_are_rounded_to_two_decimals_by_default() -> None:
    """Test 9: Default precision is two decimal places"""
    from recipe_calculator import scale

    assert scale({"flour": 1}, 1 / 3) == {"flour": 0.33}


def test_precision_is_configurable() -> None:
    """Test 10: An explicit precision controls the rounding"""
    from recipe_calculator import scale

    assert scale({"flour": 1}, 1 / 3, precision=4) == {"flour": 0.3333}


def test_negative_factor_is_rejected() -> None:
    """Test 11: A negative factor raises a meaningful ValueError"""
    import pytest

    from recipe_calculator import scale

    with pytest.raises(ValueError, match="scaling factor must be non-negative"):
        scale({"flour": 200}, -1)


def test_negative_quantity_is_rejected() -> None:
    """Test 12: A negative ingredient quantity raises ValueError"""
    import pytest

    from recipe_calculator import scale

    with pytest.raises(ValueError, match="must have a positive quantity"):
        scale({"flour": -200}, 2)


def test_zero_quantity_is_rejected() -> None:
    """Test 13: A zero ingredient quantity raises ValueError"""
    import pytest

    from recipe_calculator import scale

    with pytest.raises(ValueError, match="must have a positive quantity"):
        scale({"flour": 0}, 2)


def test_error_message_names_the_offending_ingredient() -> None:
    """Test 14: The validation error identifies which ingredient is invalid"""
    import pytest

    from recipe_calculator import scale

    with pytest.raises(ValueError, match="'sugar'"):
        scale({"flour": 200, "sugar": -1}, 2)


def test_input_recipe_is_not_mutated() -> None:
    """Test 15: Scaling returns a new mapping and leaves the input untouched"""
    from recipe_calculator import scale

    recipe = {"flour": 200.0, "sugar": 100.0}
    result = scale(recipe, 2)
    assert recipe == {"flour": 200.0, "sugar": 100.0}
    assert result is not recipe


def test_ingredient_names_are_preserved() -> None:
    """Test 16: The scaled recipe contains exactly the original ingredients"""
    from recipe_calculator import scale

    recipe = {"flour": 200, "sugar": 100, "butter": 50, "eggs": 2}
    assert set(scale(recipe, 2.5)) == set(recipe)


def test_large_scaling_factor() -> None:
    """Test 17: Scaling for a crowd multiplies quantities faithfully"""
    from recipe_calculator import scale

    assert scale({"rice": 90, "stock": 240}, 12) == {"rice": 1080, "stock": 2880}
