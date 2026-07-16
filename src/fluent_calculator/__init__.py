"""Fluent Calculator kata: chainable integer arithmetic with undo/redo.

Every method returns the calculator so calls chain. seed(value) sets
the starting value; only the first seed counts and later seeds are
ignored. plus(value) and minus(value) add and subtract integers. The
calculator never raises: operations before seeding, non-integer
arguments, and undo/redo with nothing to revert or restore all leave
the chain unchanged. undo() reverts the most recent operation (never
past the seed), redo() restores an undone operation, and a new
operation after an undo clears the redo history. save() persists the
current state, turning undo and redo into no-ops until new operations
build fresh history. result() returns the current value, or 0 when the
calculator was never seeded.

Kata catalogued at tddbuddy.com/katas/fluent-calc; implementation and
tests original (MIT), machine-authored from the specification, 2026.
"""

from fluent_calculator.calculator import Calculator

__all__ = ["Calculator"]
