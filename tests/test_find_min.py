"""Find Min Functions - An4ik Python TDD Port

Demonstrates Python argument handling patterns through TDD - minimum operations
"""


def test_get_min_should_return_smaller_of_two_numbers() -> None:
    """Test 1: get_min should return the smaller of two numbers

    From An4ik example: Basic min comparison between two numbers
    """
    from find_min import get_min

    # GIVEN
    a, b = 1, 34

    # WHEN
    result = get_min(a, b)

    # THEN
    assert result == 1


def test_get_min_without_arguments_should_raise_type_error() -> None:
    """Test 2: get_min_without_arguments should raise TypeError

    From An4ik example: Function should raise TypeError when called
    """
    import pytest

    from find_min import get_min_without_arguments

    # WHEN/THEN
    with pytest.raises(TypeError):
        get_min_without_arguments()


def test_get_min_with_one_argument_should_return_that_value() -> None:
    """Test 3: get_min_with_one_argument should return that value

    From An4ik example: Function with single argument returns that argument
    """
    from find_min import get_min_with_one_argument

    # GIVEN
    value = 123

    # WHEN
    result = get_min_with_one_argument(value)

    # THEN
    assert result == 123


def test_get_min_with_many_arguments_should_return_smallest() -> None:
    """Test 4: get_min_with_many_arguments should return the smallest among args

    From An4ik example: Function with *args returns minimum value
    """
    from find_min import get_min_with_many_arguments

    # GIVEN
    args = (1, 2, 3, 4)

    # WHEN
    result = get_min_with_many_arguments(*args)

    # THEN
    assert result == 1


def test_get_min_with_one_or_more_arguments_should_return_smallest() -> None:
    """Test 5: get_min_with_one_or_more_arguments should return smallest among first and args

    From An4ik example: Function with required first + *args parameters
    """
    from find_min import get_min_with_one_or_more_arguments

    # GIVEN
    first = 124
    array = [1123, 1421, 12]

    # WHEN
    result = get_min_with_one_or_more_arguments(first, *array)

    # THEN
    assert result == 12


def test_get_min_bounded_should_return_smallest_within_bounds() -> None:
    """Test 6: get_min_bounded should return smallest number bounded by low & high

    From An4ik example: Function with *args and keyword-only parameters
    """
    from find_min import get_min_bounded

    # GIVEN
    args = (-54, 45, 23)
    kwargs = {"low": 0, "high": 127}

    # WHEN
    result = get_min_bounded(*args, **kwargs)

    # THEN
    assert result == 23


def test_make_min_should_return_callable_bounded_function() -> None:
    """Test 7: make_min should return a callable function that bounds results

    From An4ik example: Factory function that returns a closure
    """
    from find_min import make_min

    # GIVEN
    low, high = 0, 255

    # WHEN
    bounded_min = make_min(low=low, high=high)

    # THEN
    assert callable(bounded_min)

    # AND WHEN called with args outside bounds
    result = bounded_min(-5, 12, 13)

    # THEN returns min within bounds
    assert result == 12


def test_get_min_bounded_with_no_valid_args_should_return_high() -> None:
    """Test edge case: get_min_bounded with no args within bounds returns high

    Edge case for 100% test coverage
    """
    from find_min import get_min_bounded

    # GIVEN args all outside bounds
    args = (-100, -200, 300, 400)
    kwargs = {"low": 0, "high": 127}

    # WHEN
    result = get_min_bounded(*args, **kwargs)

    # THEN returns high when no args are within bounds
    assert result == 127


def test_get_min_without_arguments_should_raise_with_exact_message() -> None:
    """get_min_without_arguments raises TypeError carrying the documented message

    The message is part of the contract: "Function requires arguments"
    (exact casing, no decoration).
    """
    import pytest

    from find_min import get_min_without_arguments

    # WHEN/THEN
    with pytest.raises(TypeError) as exc_info:
        get_min_without_arguments()

    # THEN the exception message matches exactly
    assert str(exc_info.value) == "Function requires arguments"


def test_get_min_with_one_or_more_arguments_when_first_is_smallest() -> None:
    """get_min_with_one_or_more_arguments must consider the required first param

    The first positional argument participates in the comparison, so the
    result is first when it is smaller than everything in args.
    """
    from find_min import get_min_with_one_or_more_arguments

    # GIVEN first smaller than every value in args
    first = 3
    array = [10, 20]

    # WHEN
    result = get_min_with_one_or_more_arguments(first, *array)

    # THEN
    assert result == 3


def test_get_min_with_many_arguments_handles_duplicates_and_negatives() -> None:
    """get_min_with_many_arguments handles duplicate and negative values"""
    from find_min import get_min_with_many_arguments

    # WHEN
    result = get_min_with_many_arguments(-5, -5, 0, 3, -2)

    # THEN
    assert result == -5


def test_get_min_with_many_arguments_with_no_arguments_raises_value_error() -> None:
    """get_min_with_many_arguments with an empty argument list raises ValueError

    min() of an empty sequence raises ValueError; this pins the empty-args
    behavior of the *args variant.
    """
    import pytest

    from find_min import get_min_with_many_arguments

    # WHEN/THEN
    with pytest.raises(ValueError):
        get_min_with_many_arguments()


def test_get_min_bounded_includes_value_equal_to_low() -> None:
    """get_min_bounded bounds are inclusive: a value equal to low is a candidate"""
    from find_min import get_min_bounded

    # GIVEN one arg exactly at the low bound and one inside the range
    result = get_min_bounded(0, 50, low=0, high=127)

    # THEN the value at the low bound is the minimum
    assert result == 0


def test_get_min_bounded_includes_value_equal_to_high() -> None:
    """get_min_bounded bounds are inclusive: a value equal to high is a candidate"""
    from find_min import get_min_bounded

    # GIVEN the only in-range arg sits exactly at the high bound
    result = get_min_bounded(127, 200, low=0, high=127)

    # THEN it is returned
    assert result == 127


def test_get_min_with_exactly_one_argument() -> None:
    """One argument is valid per the function's contract and returns that argument"""
    from find_min.find_min import get_min_with_one_or_more_arguments

    assert get_min_with_one_or_more_arguments(7) == 7
