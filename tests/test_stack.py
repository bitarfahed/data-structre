import pytest

from data_structures_visual_lab.domain.data_structures.stack import Stack


def test_stack_push_stores_integer_values() -> None:
    stack = Stack()

    stack.push(10)
    stack.push(-3)

    assert stack.to_list() == [10, -3]
    assert len(stack) == 2
    assert not stack.is_empty()


def test_stack_pop_uses_lifo_order() -> None:
    stack = Stack()

    stack.push(1)
    stack.push(2)
    stack.push(3)

    assert stack.pop() == 3
    assert stack.pop() == 2
    assert stack.pop() == 1
    assert stack.is_empty()


def test_stack_pop_empty_returns_none() -> None:
    stack = Stack()

    assert stack.pop() is None
    assert stack.pop() is None
    assert stack.to_list() == []


def test_stack_allows_duplicate_values() -> None:
    stack = Stack()

    stack.push(7)
    stack.push(7)
    stack.push(7)

    assert stack.to_list() == [7, 7, 7]
    assert [stack.pop(), stack.pop(), stack.pop()] == [7, 7, 7]


@pytest.mark.parametrize("value", ["1", 1.5, None, True])
def test_stack_rejects_non_integer_input(value: object) -> None:
    stack = Stack()

    with pytest.raises(TypeError, match="integers"):
        stack.push(value)  # type: ignore[arg-type]

    assert stack.is_empty()


def test_stack_repeated_operations_keep_expected_state() -> None:
    stack = Stack()

    assert stack.pop() is None
    stack.push(4)
    stack.push(5)
    assert stack.pop() == 5
    stack.push(6)
    assert stack.to_list() == [4, 6]
    assert stack.pop() == 6
    assert stack.pop() == 4
    assert stack.pop() is None


def test_stack_display_representation() -> None:
    stack = Stack()
    stack.push(2)
    stack.push(9)

    assert stack.display() == "Stack(bottom -> top): [2, 9]"
    assert str(stack) == stack.display()
