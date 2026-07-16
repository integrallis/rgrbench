"""Stringify Decorator Tests - An4ik Python TDD Port

Demonstrates decorator that converts function results to strings through TDD
"""


def test_add_returns_string() -> None:
    """Test 1: add function should return string when decorated

    From An4ik example: Functions decorated with @stringify should return strings
    """
    from decorator_examples import add

    # WHEN calling add
    result = add(5, 6)

    # THEN result should be a string
    assert isinstance(result, str), f"add should return string, got {type(result)}"


def test_add_does_right_calculation() -> None:
    """Test 2: add function should still calculate correctly

    From An4ik example: Decorated functions should preserve their logic
    """
    from decorator_examples import add

    # WHEN calling add
    result = add(5, 6)

    # THEN result should be correct string representation
    assert int(result) == 11, f"add(5, 6) should be '11', got '{result}'"


def test_multiply_returns_string() -> None:
    """Test 3: multiply function should return string when decorated

    From An4ik example: Multiple functions can use the same decorator
    """
    from decorator_examples import multiply

    # WHEN calling multiply
    result = multiply(5, 6)

    # THEN result should be a string
    assert isinstance(result, str), f"multiply should return string, got {type(result)}"


def test_add_returns_exact_string_result() -> None:
    """Test 4: add returns the exact string form of the sum"""
    from decorator_examples import add

    # WHEN calling add
    result = add(5, 6)

    # THEN the result is exactly the string "11"
    assert result == "11", f"add(5, 6) should be '11', got {result!r}"


def test_multiply_returns_exact_string_result() -> None:
    """Test 5: multiply returns the exact string form of the product"""
    from decorator_examples import multiply

    # WHEN calling multiply
    result = multiply(5, 6)

    # THEN the result is exactly the string "30"
    assert result == "30", f"multiply(5, 6) should be '30', got {result!r}"


def test_stringify_converts_any_result_to_its_str_form() -> None:
    """Test 6: stringify applied inside a test converts results via str()

    Applying the decorator directly pins its semantics: the wrapper forwards
    positional and keyword arguments and returns str(result).
    """
    from decorator_examples import stringify

    @stringify
    def echo(value: object, *, repeat: int = 1) -> object:
        return [value] * repeat if repeat != 1 else value

    # THEN results of any type come back as their str() form
    assert echo(None) == "None"
    assert echo(3.5) == "3.5"
    assert echo(1, repeat=2) == "[1, 1]"


def test_stringify_preserves_function_metadata() -> None:
    """Test 7: stringify uses functools.wraps to keep name and docstring"""
    from decorator_examples import add, multiply

    assert add.__name__ == "add"
    assert add.__doc__ == "Add two numbers."
    assert multiply.__name__ == "multiply"
    assert multiply.__doc__ == "Multiply two numbers."
