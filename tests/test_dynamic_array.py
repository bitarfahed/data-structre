import pytest

from data_structures_visual_lab.domain.data_structures.dynamic_array import DynamicArray


def test_add_stores_integer_values_in_order() -> None:
    array = DynamicArray()

    array.add(10)
    array.add(-3)

    assert array.to_list() == [10, -3]
    assert array.size == 2
    assert len(array) == 2
    assert not array.is_empty()


def test_add_grows_capacity_when_size_reaches_capacity() -> None:
    array = DynamicArray(initial_capacity=2)

    array.add(1)
    array.add(2)
    assert array.capacity == 2

    array.add(3)

    assert array.capacity == 4
    assert array.to_list() == [1, 2, 3]


def test_delete_shrinks_capacity_after_size_reaches_quarter_capacity() -> None:
    array = DynamicArray(initial_capacity=2)
    for value in range(8):
        array.add(value)

    assert array.capacity == 8

    assert array.delete(0) == 0
    assert array.delete(0) == 1
    assert array.delete(0) == 2
    assert array.delete(0) == 3
    assert array.delete(0) == 4
    assert array.delete(0) == 5

    assert array.size == 2
    assert array.capacity == 4
    assert array.to_list() == [6, 7]


def test_delete_never_shrinks_below_initial_minimum_capacity() -> None:
    array = DynamicArray(initial_capacity=4)
    for value in range(5):
        array.add(value)

    assert array.capacity == 8

    for _ in range(5):
        array.delete(0)

    assert array.size == 0
    assert array.capacity == 4
    assert array.minimum_capacity == 4
    assert array.to_list() == []


def test_values_are_preserved_across_growth_and_shrink() -> None:
    array = DynamicArray(initial_capacity=2)
    for value in [5, 6, 7, 8, 9]:
        array.add(value)

    assert array.capacity == 8
    assert array.to_list() == [5, 6, 7, 8, 9]

    assert array.delete(1) == 6
    assert array.delete(2) == 8
    assert array.delete(0) == 5

    assert array.to_list() == [7, 9]
    assert array.capacity == 4


def test_delete_from_beginning_middle_and_end() -> None:
    array = DynamicArray()
    for value in [1, 2, 3, 4]:
        array.add(value)

    assert array.delete(0) == 1
    assert array.to_list() == [2, 3, 4]

    assert array.delete(1) == 3
    assert array.to_list() == [2, 4]

    assert array.delete(1) == 4
    assert array.to_list() == [2]


def test_invalid_and_negative_delete_indices_are_safe() -> None:
    array = DynamicArray()
    array.add(1)
    array.add(2)

    assert array.delete(-1) is None
    assert array.delete(2) is None
    assert array.delete(99) is None

    assert array.to_list() == [1, 2]
    assert array.size == 2


def test_delete_from_empty_array_is_safe() -> None:
    array = DynamicArray()

    assert array.delete(0) is None
    assert array.delete(4) is None
    assert array.delete(-1) is None
    assert array.is_empty()
    assert array.capacity == array.minimum_capacity


@pytest.mark.parametrize("value", ["1", 1.5, None, True])
def test_add_rejects_non_integer_input(value: object) -> None:
    array = DynamicArray()

    with pytest.raises(TypeError, match="integers"):
        array.add(value)  # type: ignore[arg-type]

    assert array.is_empty()


@pytest.mark.parametrize("index", ["0", 1.5, None, False])
def test_delete_rejects_non_integer_indices(index: object) -> None:
    array = DynamicArray()
    array.add(1)

    with pytest.raises(TypeError, match="indices"):
        array.delete(index)  # type: ignore[arg-type]

    assert array.to_list() == [1]


def test_duplicate_values_are_allowed() -> None:
    array = DynamicArray(initial_capacity=2)

    array.add(7)
    array.add(7)
    array.add(7)

    assert array.to_list() == [7, 7, 7]
    assert [array.delete(0), array.delete(0), array.delete(0)] == [7, 7, 7]


def test_size_and_capacity_after_repeated_operations() -> None:
    array = DynamicArray(initial_capacity=2)

    for value in range(10):
        array.add(value)

    assert array.size == 10
    assert array.capacity == 16

    for _ in range(7):
        array.delete(0)

    assert array.size == 3
    assert array.capacity == 8
    assert array.to_list() == [7, 8, 9]

    array.add(10)
    array.add(11)

    assert array.size == 5
    assert array.capacity == 8
    assert array.to_list() == [7, 8, 9, 10, 11]


def test_display_representation() -> None:
    array = DynamicArray(initial_capacity=2)
    array.add(2)
    array.add(9)

    assert array.display() == "DynamicArray(size=2, capacity=2): [2, 9]"
    assert str(array) == array.display()


def test_initial_capacity_must_be_positive_integer() -> None:
    with pytest.raises(ValueError, match="at least 1"):
        DynamicArray(initial_capacity=0)

    with pytest.raises(TypeError, match="integer"):
        DynamicArray(initial_capacity=True)  # type: ignore[arg-type]
