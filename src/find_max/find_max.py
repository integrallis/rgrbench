"""Find Max Functions - Python Argument Handling Patterns

Demonstrates various Python argument handling techniques through TDD
"""

from collections.abc import Callable


def get_max(a: int, b: int) -> int:
    """Returns max number among a and b."""
    return max(a, b)


def get_max_without_arguments() -> None:
    """Raise TypeError exception with message as an argument."""
    raise TypeError("Function requires arguments")


def get_max_with_one_argument(a: int) -> int:
    """Returns that value."""
    return a


def get_max_with_many_arguments(*args: int) -> int:
    """Return the largest number among args."""
    return max(args)


def get_max_with_one_or_more_arguments(first: int, *args: int) -> int:
    """Returns the largest number among first and args."""
    return max((first, *args))


def get_max_bounded(*args: int, low: int, high: int) -> int:
    """Returns the largest number among args bounded by low & high."""
    # Filter args to be within bounds
    bounded_args = [arg for arg in args if low <= arg <= high]
    if not bounded_args:
        return low  # Return low if no args are within bounds
    return max(bounded_args)


def make_max(*, low: int, high: int) -> Callable[..., int]:
    """Returns an inner function object which takes at least one argument
    and return largest number among its arguments, but bounded by low & high.
    """

    def bounded_max(*args: int) -> int:
        return get_max_bounded(*args, low=low, high=high)

    return bounded_max
