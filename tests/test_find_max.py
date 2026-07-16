"""Find Max Functions - An4ik Python TDD Port

Demonstrates Python argument handling patterns through TDD
"""


def test_get_max_should_return_larger_of_two_numbers() -> None:
    """Test 1: get_max should return the larger of two numbers

    From An4ik example: Basic max comparison between two numbers
    """
    from find_max import get_max

    # GIVEN
    a, b = 1, 34

    # WHEN
    result = get_max(a, b)

    # THEN
    assert result == 34


def test_get_max_without_arguments_should_raise_type_error() -> None:
    """Test 2: get_max_without_arguments should raise TypeError

    From An4ik example: Function should raise TypeError when called
    """
    import pytest

    from find_max import get_max_without_arguments

    # WHEN/THEN
    with pytest.raises(TypeError):
        get_max_without_arguments()


def test_get_max_with_one_argument_should_return_that_value() -> None:
    """Test 3: get_max_with_one_argument should return that value

    From An4ik example: Function with single argument returns that argument
    """
    from find_max import get_max_with_one_argument

    # GIVEN
    value = 123

    # WHEN
    result = get_max_with_one_argument(value)

    # THEN
    assert result == 123


def test_get_max_with_many_arguments_should_return_largest() -> None:
    """Test 4: get_max_with_many_arguments should return the largest among args

    From An4ik example: Function with *args returns maximum value
    """
    from find_max import get_max_with_many_arguments

    # GIVEN
    args = (1, 2, 3, 4)

    # WHEN
    result = get_max_with_many_arguments(*args)

    # THEN
    assert result == 4


def test_get_max_with_one_or_more_arguments_should_return_largest() -> None:
    """Test 5: get_max_with_one_or_more_arguments should return largest among first and args

    From An4ik example: Function with required first + *args parameters
    """
    from find_max import get_max_with_one_or_more_arguments

    # GIVEN
    first = 12454
    array = [1123, 1421, 12]

    # WHEN
    result = get_max_with_one_or_more_arguments(first, *array)

    # THEN
    assert result == 12454


def test_get_max_bounded_should_return_largest_within_bounds() -> None:
    """Test 6: get_max_bounded should return largest number bounded by low & high

    From An4ik example: Function with *args and keyword-only parameters
    """
    from find_max import get_max_bounded

    # GIVEN
    args = (-54, 45, 140)
    kwargs = {"low": 0, "high": 127}

    # WHEN
    result = get_max_bounded(*args, **kwargs)

    # THEN
    assert result == 45


def test_make_max_should_return_callable_bounded_function() -> None:
    """Test 7: make_max should return a callable function that bounds results

    From An4ik example: Factory function that returns a closure
    """
    from find_max import make_max

    # GIVEN
    low, high = 0, 255

    # WHEN
    bounded_max = make_max(low=low, high=high)

    # THEN
    assert callable(bounded_max)

    # AND WHEN called with args outside bounds
    result = bounded_max(-5, 12, 300)

    # THEN returns max within bounds
    assert result == 12


def test_get_max_bounded_with_no_valid_args_should_return_low() -> None:
    """Test edge case: get_max_bounded with no args within bounds returns low

    Edge case for 100% test coverage
    """
    from find_max import get_max_bounded

    # GIVEN args all outside bounds
    args = (-100, -200, 300, 400)
    kwargs = {"low": 0, "high": 127}

    # WHEN
    result = get_max_bounded(*args, **kwargs)

    # THEN returns low when no args are within bounds
    assert result == 0


def test_get_max_without_arguments_should_raise_with_exact_message() -> None:
    """get_max_without_arguments raises TypeError carrying the documented message

    The message is part of the contract: "Function requires arguments"
    (exact casing, no decoration).
    """
    import pytest

    from find_max import get_max_without_arguments

    # WHEN/THEN
    with pytest.raises(TypeError) as exc_info:
        get_max_without_arguments()

    # THEN the exception message matches exactly
    assert str(exc_info.value) == "Function requires arguments"


def test_get_max_bounded_includes_value_equal_to_high() -> None:
    """get_max_bounded bounds are inclusive: a value equal to high is a candidate"""
    from find_max import get_max_bounded

    # GIVEN one arg exactly at the high bound and one inside the range
    result = get_max_bounded(127, 50, low=0, high=127)

    # THEN the value at the high bound is the maximum
    assert result == 127


def test_get_max_bounded_includes_value_equal_to_low() -> None:
    """get_max_bounded bounds are inclusive: a value equal to low is a candidate"""
    from find_max import get_max_bounded

    # GIVEN the only in-range arg sits exactly at the low bound
    result = get_max_bounded(0, -10, low=0, high=127)

    # THEN it is returned
    assert result == 0


def test_get_max_with_many_arguments_handles_duplicates_and_negatives() -> None:
    """get_max_with_many_arguments handles duplicate and negative values"""
    from find_max import get_max_with_many_arguments

    # WHEN
    result = get_max_with_many_arguments(-5, -5, -1, -30)

    # THEN
    assert result == -1


def test_get_max_with_many_arguments_with_no_arguments_raises_value_error() -> None:
    """get_max_with_many_arguments with an empty argument list raises ValueError

    max() of an empty sequence raises ValueError; this pins the empty-args
    behavior of the *args variant.
    """
    import pytest

    from find_max import get_max_with_many_arguments

    # WHEN/THEN
    with pytest.raises(ValueError):
        get_max_with_many_arguments()


def test_get_max_with_exactly_one_argument() -> None:
    """One argument is valid per the function's contract and returns that argument"""
    from find_max.find_max import get_max_with_one_or_more_arguments

    assert get_max_with_one_or_more_arguments(7) == 7
