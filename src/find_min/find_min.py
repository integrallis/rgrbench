"""Find Min Functions - Python Argument Handling Patterns

Demonstrates various Python argument handling techniques through TDD - min operations
"""

from collections.abc import Callable


def get_min(a: int, b: int) -> int:
    """Returns min number among a and b."""
    return min(a, b)


def get_min_without_arguments() -> None:
    """Raise TypeError exception with message as an argument."""
    raise TypeError("Function requires arguments")


def get_min_with_one_argument(a: int) -> int:
    """Returns that value."""
    return a


def get_min_with_many_arguments(*args: int) -> int:
    """Return the smallest number among args."""
    return min(args)


def get_min_with_one_or_more_arguments(first: int, *args: int) -> int:
    """Returns the smallest number among first and args."""
    return min((first, *args))


def get_min_bounded(*args: int, low: int, high: int) -> int:
    """Returns the smallest number among args bounded by low & high."""
    # Filter args to be within bounds
    bounded_args = [arg for arg in args if low <= arg <= high]
    if not bounded_args:
        return high  # Return high if no args are within bounds
    return min(bounded_args)


def make_min(*, low: int, high: int) -> Callable[..., int]:
    """Returns an inner function object which takes at least one argument
    and return smallest number among its arguments, but bounded by low & high.
    """

    def bounded_min(*args: int) -> int:
        return get_min_bounded(*args, low=low, high=high)

    return bounded_min
