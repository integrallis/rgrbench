"""Stringify Decorator Implementation

Demonstrates decorator that converts function results to strings through TDD
"""

from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def stringify(func: Callable[..., Any]) -> Callable[..., str]:
    """Decorator that converts function result to string."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> str:
        result = func(*args, **kwargs)
        return str(result)

    return wrapper


@stringify
def add(x: int, y: int) -> int:
    """Add two numbers."""
    return x + y


@stringify
def multiply(x: int, y: int) -> int:
    """Multiply two numbers."""
    return x * y
