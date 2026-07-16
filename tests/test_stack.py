"""Stack Kata - Test-Driven Development
Porting from Java implementation
"""


def test_new_stack_is_empty() -> None:
    """Test 1: New stack should be empty"""
    from stack.stack import Stack

    stack = Stack()
    assert stack.is_empty()


def test_push_then_pop() -> None:
    """Test 2: After push and pop, stack is empty"""
    from stack.stack import Stack

    stack = Stack()
    stack.push(42)
    stack.pop()
    assert stack.is_empty()


def test_push_twice_pop_once() -> None:
    """Test 3: After two pushes and one pop, stack is not empty"""
    from stack.stack import Stack

    stack = Stack()
    stack.push(42)
    stack.push(99)
    stack.pop()
    assert not stack.is_empty()


def test_pop_empty_stack_throws() -> None:
    """Test 4: Popping empty stack throws EmptyStackError"""
    import pytest

    from stack.stack import EmptyStackError, Stack

    stack = Stack()
    with pytest.raises(EmptyStackError):
        stack.pop()


def test_push_to_full_stack_throws() -> None:
    """Test 5: Pushing to full stack throws FullStackError"""
    import pytest

    from stack.stack import FullStackError, Stack

    stack = Stack(capacity=2)
    stack.push(42)
    stack.push(99)
    with pytest.raises(FullStackError):
        stack.push(13)


def test_stack_with_negative_size_throws() -> None:
    """Test 6: Creating stack with negative capacity throws ValueError"""
    import pytest

    from stack.stack import Stack

    with pytest.raises(ValueError):
        Stack(capacity=-1)


def test_stack_with_zero_capacity() -> None:
    """Test 7: Stack with zero capacity throws on first push"""
    import pytest

    from stack.stack import FullStackError, Stack

    stack = Stack(capacity=0)
    with pytest.raises(FullStackError):
        stack.push(42)


def test_pop_returns_pushed_items_in_lifo_order() -> None:
    """Test 8: Pop returns pushed items in last-in-first-out order"""
    from stack.stack import Stack

    stack = Stack()
    stack.push(42)
    stack.push(99)
    assert stack.pop() == 99
    assert stack.pop() == 42


def test_pop_empty_stack_error_message() -> None:
    """Test 9: Popping empty stack reports 'Cannot pop from empty stack'"""
    import pytest

    from stack.stack import EmptyStackError, Stack

    stack = Stack()
    with pytest.raises(EmptyStackError) as exc_info:
        stack.pop()
    assert str(exc_info.value) == "Cannot pop from empty stack"


def test_push_to_full_stack_error_message() -> None:
    """Test 10: Pushing to full stack reports 'Stack is full'"""
    import pytest

    from stack.stack import FullStackError, Stack

    stack = Stack(capacity=1)
    stack.push(42)
    with pytest.raises(FullStackError) as exc_info:
        stack.push(99)
    assert str(exc_info.value) == "Stack is full"


def test_negative_capacity_error_message() -> None:
    """Test 11: Negative capacity reports 'Capacity cannot be negative'"""
    import pytest

    from stack.stack import Stack

    with pytest.raises(ValueError) as exc_info:
        Stack(capacity=-1)
    assert str(exc_info.value) == "Capacity cannot be negative"
