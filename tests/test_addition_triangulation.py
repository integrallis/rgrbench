"""Addition Class - TDD Ebook Triangulation Example
Demonstrates the three implementation approaches from the Triangulation chapter
"""


def test_should_add_two_numbers_together() -> None:
    """Test 1: Addition should add two numbers together

    From the book: Simple example to demonstrate triangulation approaches.
    Starting with "Type the obvious implementation" approach.
    """
    from addition_triangulation.addition import Addition

    # GIVEN
    addition = Addition()

    # WHEN
    sum_result = addition.of(3, 5)

    # THEN
    assert sum_result == 8


def test_should_add_two_numbers_together_with_constrained_non_determinism() -> None:
    """Test 2: Addition with constrained non-determinism

    From the book: Using constrained non-determinism enforces using
    the "type the obvious implementation" approach.
    """
    from addition_triangulation.addition import Addition

    # GIVEN
    a = 4  # Any.integer() - simplified for this example
    b = 7  # Any.integer() - simplified for this example
    addition = Addition()

    # WHEN
    sum_result = addition.of(a, b)

    # THEN
    assert sum_result == a + b
