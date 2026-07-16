# Scaling recipe ingredient quantities

## Overview
A kitchen helper rescales a recipe for a different number of servings. A recipe is a set of named ingredients, each with a positive quantity; scaling multiplies every quantity by a single factor so the recipe stays in proportion, rounds the results to a configurable precision, and hands back a new recipe while leaving the original untouched.

## User Stories

### US-1: Scaling every ingredient in proportion
As a home cook, I want every ingredient multiplied by the same factor, so that a resized recipe tastes the same as the original.

- AC-1.1: Every ingredient's quantity is multiplied by the factor; scaling an empty recipe yields an empty recipe.
- AC-1.2: A factor of one leaves every quantity unchanged, and a factor of zero zeroes every quantity.
- AC-1.3: Fractional factors and fractional quantities are supported: a factor of 0.5 halves quantities, and 1.5 of something scaled by 1.5 gives 2.25.
- AC-1.4: Large factors multiply faithfully, as when catering for a crowd at twelve times the quantities.

### US-2: Rounding results predictably
As a home cook, I want tidy numbers, so that measurements are practical and free of floating-point noise.

- AC-2.1: Results are rounded to two decimal places by default: a third of one unit comes out as 0.33, and 0.1 scaled by three is exactly 0.3.
- AC-2.2: The rounding precision can be chosen explicitly; at four decimal places a third of one unit comes out as 0.3333.

### US-3: Rejecting invalid inputs with helpful errors
As a home cook, I want bad inputs called out clearly, so that mistakes are caught before cooking starts.

- AC-3.1: A negative factor is rejected with an error stating "scaling factor must be non-negative".
- AC-3.2: An ingredient with a zero or negative quantity is rejected with an error stating it "must have a positive quantity".
- AC-3.3: The quantity-validation error names the offending ingredient in quotes, as in 'sugar'.

### US-4: Preserving the original recipe
As a home cook, I want the original recipe preserved, so that I can scale it again later from the source.

- AC-4.1: Scaling returns a new collection; the input recipe is left unmodified.
- AC-4.2: The scaled recipe contains exactly the original ingredient names, no more and no fewer.

## Traceability
```json
{
  "test_empty_recipe_scales_to_empty_recipe": ["AC-1.1"],
  "test_single_ingredient_doubles": ["AC-1.1"],
  "test_multiple_ingredients_stay_in_proportion": ["AC-1.1"],
  "test_identity_factor_returns_unchanged_quantities": ["AC-1.2"],
  "test_zero_factor_zeroes_all_quantities": ["AC-1.2"],
  "test_fractional_factor_halves_quantities": ["AC-1.3"],
  "test_fractional_quantities_are_supported": ["AC-1.3"],
  "test_rounding_absorbs_floating_point_noise": ["AC-2.1"],
  "test_results_are_rounded_to_two_decimals_by_default": ["AC-2.1"],
  "test_precision_is_configurable": ["AC-2.2"],
  "test_negative_factor_is_rejected": ["AC-3.1"],
  "test_negative_quantity_is_rejected": ["AC-3.2"],
  "test_zero_quantity_is_rejected": ["AC-3.2"],
  "test_error_message_names_the_offending_ingredient": ["AC-3.3"],
  "test_input_recipe_is_not_mutated": ["AC-4.1"],
  "test_ingredient_names_are_preserved": ["AC-4.2"],
  "test_large_scaling_factor": ["AC-1.4"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
