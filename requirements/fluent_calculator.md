# Chainable calculator with undo, redo, and save

## Overview
A pocket calculator with a fluent, chainable interface. The user seeds it with a starting
value, chains additions and subtractions, and asks for the running result at any point.
The calculator accepts only whole numbers and never raises an error: any invalid call
simply leaves the chain unchanged. A history of operations supports stepping backwards
(undo) and forwards again (redo), and the current state can be sealed (save) so that the
history can no longer be replayed.

## User Stories

### US-1: Chain arithmetic fluently
As a user, I want to seed a value and chain additions and subtractions in one expression, so that I can compute a running total without intermediate variables.

- AC-1.1: Seeding the calculator sets its starting value; asking for the result immediately afterwards reports that value.
- AC-1.2: Each addition increases the running value by its operand; additions chain and accumulate (worked example: seed 10, add 5, add 5 gives 20).
- AC-1.3: Each subtraction decreases the running value by its operand.
- AC-1.4: Additions and subtractions combine freely along a single chain.
- AC-1.5: Every call — seeding, adding, subtracting, undoing, redoing, saving — hands back the same calculator, so calls chain fluently.

### US-2: Invalid input never breaks the chain
As a user, I want invalid calls to be silently ignored, so that a chain never fails partway through.

- AC-2.1: Only the first seed counts; any later seed is ignored.
- AC-2.2: Additions and subtractions made before the calculator is seeded are ignored.
- AC-2.3: An unseeded calculator reports a result of 0 without raising.
- AC-2.4: Additions and subtractions with non-whole-number operands (fractions, text) are ignored.
- AC-2.5: A non-whole-number seed is ignored, and a later valid seed still applies.
- AC-2.6: Negative whole numbers are valid seeds and operands and combine like any other whole number.

### US-3: Undo operations
As a user, I want to undo operations one at a time, so that I can step back through my calculation history.

- AC-3.1: Undo reverts the most recent addition or subtraction, restoring the prior value.
- AC-3.2: Repeated undos step back through the history one operation at a time.
- AC-3.3: Undo never reverts past the seed; with no operations left to revert it changes nothing.
- AC-3.4: Undo on an unseeded calculator changes nothing, and a later seed still applies.

### US-4: Redo undone operations
As a user, I want to reapply operations I have undone, so that stepping back is not irreversible.

- AC-4.1: Redo reapplies the operation most recently reverted by undo (worked example: seed 10, add 5, subtract 2, undo, undo, redo gives 15).
- AC-4.2: Redo with nothing undone changes nothing.
- AC-4.3: Performing a new operation after an undo discards the redo history; a subsequent redo changes nothing.
- AC-4.4: A redone operation can be undone again, restoring the earlier value.

### US-5: Save to seal the history
As a user, I want to save the calculator's state, so that the history before the save can no longer be replayed.

- AC-5.1: After a save, undo and redo no longer change the value — neither operations made before the save nor undos pending at the save can be replayed.
- AC-5.2: New operations after a save are accepted and build a fresh history that can itself be undone.

## Traceability
```json
{
  "test_seed_sets_the_starting_value": ["AC-1.1"],
  "test_chained_additions": ["AC-1.2"],
  "test_subtraction": ["AC-1.3"],
  "test_mixed_addition_and_subtraction": ["AC-1.4"],
  "test_second_seed_is_ignored": ["AC-2.1"],
  "test_operations_before_seed_are_ignored": ["AC-2.2"],
  "test_result_without_seed_is_zero": ["AC-2.3"],
  "test_undo_reverts_the_last_operation": ["AC-3.1"],
  "test_multiple_undos_step_back_through_history": ["AC-3.2"],
  "test_undo_never_reverts_past_the_seed": ["AC-3.3"],
  "test_undo_on_unseeded_calculator_is_a_no_op": ["AC-3.4"],
  "test_redo_restores_an_undone_operation": ["AC-4.1"],
  "test_undo_undo_redo_example": ["AC-3.2", "AC-4.1"],
  "test_redo_with_nothing_undone_is_a_no_op": ["AC-4.2"],
  "test_new_operation_clears_the_redo_history": ["AC-4.3"],
  "test_non_integer_operands_are_ignored": ["AC-2.4"],
  "test_non_integer_seed_is_ignored": ["AC-2.5"],
  "test_negative_integers_are_valid": ["AC-2.6"],
  "test_every_method_returns_the_same_calculator": ["AC-1.5"],
  "test_save_makes_undo_and_redo_no_ops": ["AC-5.1"],
  "test_operations_after_save_build_fresh_history": ["AC-5.2"],
  "test_undo_after_redo_returns_to_the_pre_redo_value": ["AC-4.4"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
