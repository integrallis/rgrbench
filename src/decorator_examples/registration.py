"""Registration Decorator Implementation

Demonstrates decorator pattern for function registration through TDD
"""

from collections.abc import Callable

registered: set[Callable[[], None]] = set()


def register(
    is_active: bool = True,
) -> Callable[[Callable[[], None]], Callable[[], None]]:
    """
    Registers/unregisters subjects.

    Depends on is_active param add/remove from registered subjects.
    :param is_active: Flag of subject

    :return: decorate function object
    """

    def decorate(func: Callable[[], None]) -> Callable[[], None]:
        # Set status attribute based on is_active
        func.status = "active" if is_active else "inactive"  # type: ignore

        # Add to registered set if active
        if is_active:
            registered.add(func)

        return func

    return decorate


@register()
def subject_1() -> None:
    """Do nothing."""
    pass


@register(is_active=False)
def subject_2() -> None:
    """Do nothing."""
    pass


@register()
def subject_3() -> None:
    """Do nothing."""
    pass
