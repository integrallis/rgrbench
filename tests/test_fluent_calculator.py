"""Fluent Calculator Kata - chainable seed/plus/minus with undo, redo, and save
The calculator accepts only integers and never raises; invalid calls leave the chain unchanged.
"""


def test_seed_sets_the_starting_value() -> None:
    """Test 1: Seeding then asking for the result returns the seed"""
    from fluent_calculator import Calculator

    assert Calculator().seed(10).result() == 10


def test_chained_additions() -> None:
    """Test 2: Seed(10).Plus(5).Plus(5).Result() -> 20"""
    from fluent_calculator import Calculator

    assert Calculator().seed(10).plus(5).plus(5).result() == 20


def test_subtraction() -> None:
    """Test 3: Minus subtracts from the running value"""
    from fluent_calculator import Calculator

    assert Calculator().seed(10).minus(4).result() == 6


def test_mixed_addition_and_subtraction() -> None:
    """Test 4: Plus and minus combine along the chain"""
    from fluent_calculator import Calculator

    assert Calculator().seed(10).plus(5).minus(2).result() == 13


def test_second_seed_is_ignored() -> None:
    """Test 5: After the first seed, additional seed calls are ignored"""
    from fluent_calculator import Calculator

    assert Calculator().seed(10).seed(100).plus(1).result() == 11


def test_operations_before_seed_are_ignored() -> None:
    """Test 6: Plus and minus before seeding leave the chain unchanged"""
    from fluent_calculator import Calculator

    assert Calculator().plus(5).minus(3).seed(10).result() == 10


def test_result_without_seed_is_zero() -> None:
    """Test 7: An unseeded calculator reports 0 without raising"""
    from fluent_calculator import Calculator

    assert Calculator().result() == 0


def test_undo_reverts_the_last_operation() -> None:
    """Test 8: Undo reverts the most recent plus"""
    from fluent_calculator import Calculator

    assert Calculator().seed(10).plus(5).undo().result() == 10


def test_multiple_undos_step_back_through_history() -> None:
    """Test 9: Each undo reverts one more operation"""
    from fluent_calculator import Calculator

    assert Calculator().seed(10).plus(5).minus(2).undo().undo().result() == 10


def test_undo_never_reverts_past_the_seed() -> None:
    """Test 10: Undo with no operations left is a no-op"""
    from fluent_calculator import Calculator

    assert Calculator().seed(10).plus(5).undo().undo().undo().result() == 10


def test_undo_on_unseeded_calculator_is_a_no_op() -> None:
    """Test 11: Undo before seeding leaves the chain unchanged"""
    from fluent_calculator import Calculator

    assert Calculator().undo().seed(7).result() == 7


def test_redo_restores_an_undone_operation() -> None:
    """Test 12: Redo reapplies the operation that undo reverted"""
    from fluent_calculator import Calculator

    assert Calculator().seed(10).plus(5).undo().redo().result() == 15


def test_undo_undo_redo_example() -> None:
    """Test 13: Seed(10).Plus(5).Minus(2).Undo().Undo().Redo().Result() -> 15"""
    from fluent_calculator import Calculator

    assert Calculator().seed(10).plus(5).minus(2).undo().undo().redo().result() == 15


def test_redo_with_nothing_undone_is_a_no_op() -> None:
    """Test 14: Redo with an empty redo history leaves the chain unchanged"""
    from fluent_calculator import Calculator

    assert Calculator().seed(10).plus(5).redo().result() == 15


def test_new_operation_clears_the_redo_history() -> None:
    """Test 15: An operation after undo invalidates the redo stack"""
    from fluent_calculator import Calculator

    assert Calculator().seed(10).plus(5).undo().plus(3).redo().result() == 13


def test_non_integer_operands_are_ignored() -> None:
    """Test 16: Non-integer plus/minus arguments leave the chain unchanged"""
    from fluent_calculator import Calculator

    assert Calculator().seed(10).plus(2.5).minus("3").result() == 10


def test_non_integer_seed_is_ignored() -> None:
    """Test 17: A non-integer seed is ignored; a later integer seed applies"""
    from fluent_calculator import Calculator

    assert Calculator().seed("ten").seed(10).result() == 10


def test_negative_integers_are_valid() -> None:
    """Test 18: Negative integers seed and combine like any other integer"""
    from fluent_calculator import Calculator

    assert Calculator().seed(-5).plus(3).result() == -2
    assert Calculator().seed(0).minus(7).result() == -7


def test_every_method_returns_the_same_calculator() -> None:
    """Test 19: The fluent API chains by returning the calculator instance"""
    from fluent_calculator import Calculator

    calculator = Calculator()
    assert calculator.seed(1) is calculator
    assert calculator.plus(1) is calculator
    assert calculator.minus(1) is calculator
    assert calculator.undo() is calculator
    assert calculator.redo() is calculator
    assert calculator.save() is calculator


def test_save_makes_undo_and_redo_no_ops() -> None:
    """Test 20: After save, undo and redo no longer change the value"""
    from fluent_calculator import Calculator

    assert Calculator().seed(10).plus(5).save().undo().result() == 15
    assert Calculator().seed(10).plus(5).undo().save().redo().result() == 10


def test_operations_after_save_build_fresh_history() -> None:
    """Test 21: New operations after save are allowed and undoable"""
    from fluent_calculator import Calculator

    assert Calculator().seed(10).plus(5).save().plus(3).result() == 18
    assert Calculator().seed(10).plus(5).save().plus(3).undo().result() == 15


def test_undo_after_redo_returns_to_the_pre_redo_value() -> None:
    """Test 22: A redone operation can be undone again, restoring the earlier value"""
    from fluent_calculator import Calculator

    assert Calculator().seed(10).plus(5).undo().redo().undo().result() == 10
