import pytest

from data_structures_visual_lab.domain.data_structures.linked_list import LinkedList, Node


def test_node_accepts_integer_value_and_reference() -> None:
    tail = Node(2)
    head = Node(1, tail)

    assert head.value == 1
    assert head.next is tail
    assert tail.next is None


def test_push_inserts_at_beginning() -> None:
    linked_list = LinkedList()

    assert linked_list.push(2)
    assert linked_list.push(1, index=0)

    assert linked_list.to_list() == [1, 2]
    assert linked_list.head is not None
    assert linked_list.head.value == 1
    assert linked_list.head.next is not None
    assert linked_list.head.next.value == 2


def test_push_inserts_at_middle() -> None:
    linked_list = LinkedList()
    linked_list.push(1)
    linked_list.push(3, index=1)

    assert linked_list.push(2, index=1)

    assert linked_list.to_list() == [1, 2, 3]


def test_push_inserts_at_end() -> None:
    linked_list = LinkedList()
    linked_list.push(1)
    linked_list.push(2, index=1)

    assert linked_list.push(3, index=2)

    assert linked_list.to_list() == [1, 2, 3]
    assert len(linked_list) == 3


def test_push_default_index_inserts_at_beginning() -> None:
    linked_list = LinkedList()

    linked_list.push(3)
    linked_list.push(2)
    linked_list.push(1)

    assert linked_list.to_list() == [1, 2, 3]


def test_pop_removes_from_beginning() -> None:
    linked_list = LinkedList()
    linked_list.push(3)
    linked_list.push(2)
    linked_list.push(1)

    assert linked_list.pop(0) == 1

    assert linked_list.to_list() == [2, 3]
    assert linked_list.head is not None
    assert linked_list.head.value == 2


def test_pop_removes_from_middle() -> None:
    linked_list = LinkedList()
    linked_list.push(1)
    linked_list.push(2, index=1)
    linked_list.push(3, index=2)

    assert linked_list.pop(1) == 2

    assert linked_list.to_list() == [1, 3]
    assert linked_list.head is not None
    assert linked_list.head.next is not None
    assert linked_list.head.next.value == 3


def test_pop_removes_from_end() -> None:
    linked_list = LinkedList()
    linked_list.push(1)
    linked_list.push(2, index=1)
    linked_list.push(3, index=2)

    assert linked_list.pop(2) == 3

    assert linked_list.to_list() == [1, 2]
    assert linked_list.head is not None
    assert linked_list.head.next is not None
    assert linked_list.head.next.next is None


def test_pop_default_index_removes_beginning() -> None:
    linked_list = LinkedList()
    linked_list.push(2)
    linked_list.push(1)

    assert linked_list.pop() == 1
    assert linked_list.to_list() == [2]


def test_change_value_updates_existing_node() -> None:
    linked_list = LinkedList()
    linked_list.push(1)
    linked_list.push(2, index=1)
    linked_list.push(3, index=2)

    assert linked_list.change_value(1, 9)

    assert linked_list.to_list() == [1, 9, 3]


def test_change_value_rejects_invalid_index_without_changes() -> None:
    linked_list = LinkedList()
    linked_list.push(1)

    assert not linked_list.change_value(1, 9)
    assert not linked_list.change_value(-1, 9)

    assert linked_list.to_list() == [1]


def test_empty_list_operations_are_safe() -> None:
    linked_list = LinkedList()

    assert linked_list.pop() is None
    assert linked_list.pop(3) is None
    assert not linked_list.change_value(0, 5)
    assert linked_list.display() == "LinkedList(head -> tail): empty"
    assert linked_list.is_empty()


def test_invalid_and_negative_indices_are_rejected_safely() -> None:
    linked_list = LinkedList()
    linked_list.push(1)
    linked_list.push(2, index=1)

    assert not linked_list.push(0, index=-1)
    assert not linked_list.push(3, index=3)
    assert linked_list.pop(-1) is None
    assert linked_list.pop(2) is None

    assert linked_list.to_list() == [1, 2]


@pytest.mark.parametrize("value", ["1", 1.5, None, True])
def test_linked_list_rejects_non_integer_values(value: object) -> None:
    linked_list = LinkedList()

    with pytest.raises(TypeError, match="integers"):
        linked_list.push(value)  # type: ignore[arg-type]

    assert linked_list.is_empty()


@pytest.mark.parametrize("value", ["1", 1.5, None, False])
def test_change_value_rejects_non_integer_values(value: object) -> None:
    linked_list = LinkedList()
    linked_list.push(1)

    with pytest.raises(TypeError, match="integers"):
        linked_list.change_value(0, value)  # type: ignore[arg-type]

    assert linked_list.to_list() == [1]


@pytest.mark.parametrize("index", ["0", 1.5, None, True])
def test_linked_list_rejects_non_integer_indices(index: object) -> None:
    linked_list = LinkedList()
    linked_list.push(1)

    with pytest.raises(TypeError, match="indices"):
        linked_list.push(2, index=index)  # type: ignore[arg-type]

    with pytest.raises(TypeError, match="indices"):
        linked_list.pop(index)  # type: ignore[arg-type]

    with pytest.raises(TypeError, match="indices"):
        linked_list.change_value(index, 2)  # type: ignore[arg-type]


def test_linked_list_allows_duplicate_values() -> None:
    linked_list = LinkedList()

    linked_list.push(7)
    linked_list.push(7, index=1)
    linked_list.push(7, index=2)

    assert linked_list.to_list() == [7, 7, 7]
    assert [linked_list.pop(), linked_list.pop(), linked_list.pop()] == [7, 7, 7]


def test_node_reference_structure_after_mixed_operations() -> None:
    linked_list = LinkedList()
    linked_list.push(10)
    linked_list.push(30, index=1)
    linked_list.push(20, index=1)
    linked_list.pop(0)
    linked_list.push(40, index=2)

    first = linked_list.head
    assert first is not None
    second = first.next
    assert second is not None
    third = second.next
    assert third is not None

    assert first.value == 20
    assert second.value == 30
    assert third.value == 40
    assert third.next is None
    assert linked_list.to_list() == [20, 30, 40]


def test_display_representation() -> None:
    linked_list = LinkedList()
    linked_list.push(3)
    linked_list.push(2)
    linked_list.push(1)

    assert linked_list.display() == "LinkedList(head -> tail): 1 -> 2 -> 3"
    assert str(linked_list) == linked_list.display()
