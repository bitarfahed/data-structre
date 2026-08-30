import pytest

from data_structures_visual_lab.domain.data_structures.min_heap import MinHeap


def assert_min_heap_invariant(heap: MinHeap) -> None:
    values = heap.to_list()
    for index, value in enumerate(values):
        left_index = 2 * index + 1
        right_index = 2 * index + 2
        if left_index < len(values):
            assert value <= values[left_index]
        if right_index < len(values):
            assert value <= values[right_index]


def add_and_repair(heap: MinHeap, values: list[int]) -> None:
    for value in values:
        assert heap.add_raw(value)
        if heap.repair_pending:
            assert heap.sift_up()


def extract_and_repair(heap: MinHeap) -> int | None:
    value = heap.extract_raw()
    if heap.repair_pending:
        assert heap.heapify_down()
    return value


def test_add_raw_appends_without_repairing_heap_order() -> None:
    heap = MinHeap()
    add_and_repair(heap, [10, 20])

    assert heap.add_raw(5)

    assert heap.to_list() == [10, 20, 5]
    assert not heap.is_valid_heap()
    assert heap.repair_pending
    assert heap.repair_index == 2
    assert heap.repair_value == 5
    assert heap.repair_kind == "sift_up"


def test_sift_up_repairs_raw_insertion() -> None:
    heap = MinHeap()
    add_and_repair(heap, [10, 20])
    heap.add_raw(5)

    assert heap.sift_up()

    assert heap.to_list() == [5, 20, 10]
    assert heap.is_valid_heap()
    assert not heap.repair_pending
    assert heap.repair_index is None
    assert heap.repair_value is None


def test_raw_insertion_that_preserves_heap_order_does_not_require_repair() -> None:
    heap = MinHeap()

    assert heap.add_raw(3)
    assert heap.add_raw(8)

    assert heap.to_list() == [3, 8]
    assert heap.is_valid_heap()
    assert not heap.repair_pending
    assert not heap.sift_up()


def test_add_raw_is_blocked_while_repair_is_pending() -> None:
    heap = MinHeap()
    add_and_repair(heap, [10, 20])
    heap.add_raw(5)

    assert not heap.add_raw(1)
    assert heap.to_list() == [10, 20, 5]


def test_extract_raw_removes_root_and_replaces_it_without_heapifying() -> None:
    heap = MinHeap()
    add_and_repair(heap, [1, 3, 2, 8, 9, 4])

    result = heap.extract_raw()

    assert result == 1
    assert heap.to_list() == [4, 3, 2, 8, 9]
    assert not heap.is_valid_heap()
    assert heap.repair_pending
    assert heap.repair_index == 0
    assert heap.repair_value == 4
    assert heap.repair_kind == "heapify_down"


def test_heapify_down_repairs_raw_extraction() -> None:
    heap = MinHeap()
    add_and_repair(heap, [1, 3, 2, 8, 9, 4])
    heap.extract_raw()

    assert heap.heapify_down()

    assert heap.to_list() == [2, 3, 4, 8, 9]
    assert heap.is_valid_heap()
    assert not heap.repair_pending
    assert_min_heap_invariant(heap)


def test_extract_raw_is_blocked_while_repair_is_pending() -> None:
    heap = MinHeap()
    add_and_repair(heap, [10, 20])
    heap.add_raw(5)

    assert heap.extract_raw() is None
    assert heap.to_list() == [10, 20, 5]


def test_heapify_down_does_not_clear_pending_sift_up_repair() -> None:
    heap = MinHeap()
    add_and_repair(heap, [10, 20])
    heap.add_raw(5)

    assert not heap.heapify_down()

    assert heap.repair_pending
    assert heap.repair_kind == "sift_up"
    assert not heap.is_valid_heap()


def test_sift_up_does_not_clear_pending_heapify_down_repair() -> None:
    heap = MinHeap()
    add_and_repair(heap, [1, 3, 2, 8, 9, 4])
    heap.extract_raw()

    assert not heap.sift_up()

    assert heap.repair_pending
    assert heap.repair_kind == "heapify_down"
    assert not heap.is_valid_heap()


def test_extract_raw_without_violation_does_not_require_heapify_down() -> None:
    heap = MinHeap()
    add_and_repair(heap, [1, 2])

    assert heap.extract_raw() == 1

    assert heap.to_list() == [2]
    assert heap.is_valid_heap()
    assert not heap.repair_pending
    assert not heap.heapify_down()


def test_empty_heap_behavior_is_safe() -> None:
    heap = MinHeap()

    assert heap.peek_min() is None
    assert heap.extract_raw() is None
    assert not heap.sift_up()
    assert not heap.heapify_down()
    assert heap.to_list() == []
    assert heap.size == 0
    assert heap.is_valid_heap()


@pytest.mark.parametrize("value", ["1", 1.5, None, True])
def test_add_raw_rejects_non_integer_values(value: object) -> None:
    heap = MinHeap()

    with pytest.raises(TypeError, match="integers"):
        heap.add_raw(value)  # type: ignore[arg-type]


def test_duplicate_values_are_allowed() -> None:
    heap = MinHeap()

    add_and_repair(heap, [4, 4, 2, 2])

    assert heap.to_list().count(4) == 2
    assert heap.to_list().count(2) == 2
    assert heap.peek_min() == 2
    assert_min_heap_invariant(heap)


def test_repeated_add_and_repair_cycles_keep_heap_valid() -> None:
    heap = MinHeap()

    add_and_repair(heap, [9, 5, 7, 1, 3, 2, 8, 4])

    assert heap.peek_min() == 1
    assert heap.size == 8
    assert not heap.repair_pending
    assert_min_heap_invariant(heap)


def test_repeated_extract_and_repair_cycles_return_values_in_sorted_order() -> None:
    heap = MinHeap()
    add_and_repair(heap, [9, 5, 7, 1, 3, 2, 8, 4])

    extracted = [extract_and_repair(heap) for _ in range(8)]

    assert extracted == [1, 2, 3, 4, 5, 7, 8, 9]
    assert heap.to_list() == []
    assert heap.peek_min() is None
    assert_min_heap_invariant(heap)


def test_correct_minimum_value_after_repairs() -> None:
    heap = MinHeap()

    add_and_repair(heap, [6, 10, 1, 12, 3])

    assert heap.peek_min() == 1
    assert extract_and_repair(heap) == 1
    assert heap.peek_min() == 3


def test_display_representation() -> None:
    heap = MinHeap()
    add_and_repair(heap, [3, 1])

    assert heap.display() == "MinHeap(array order): [1, 3]"
    assert str(heap) == heap.display()
    assert repr(heap) == "MinHeap([1, 3])"
