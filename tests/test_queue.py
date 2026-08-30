import pytest

from data_structures_visual_lab.domain.data_structures.queue import Queue


def test_queue_enqueue_stores_integer_values() -> None:
    queue = Queue()

    queue.enqueue(10)
    queue.enqueue(-3)

    assert queue.to_list() == [10, -3]
    assert len(queue) == 2
    assert not queue.is_empty()


def test_queue_dequeue_uses_fifo_order() -> None:
    queue = Queue()

    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)

    assert queue.dequeue() == 1
    assert queue.dequeue() == 2
    assert queue.dequeue() == 3
    assert queue.is_empty()


def test_queue_dequeue_empty_returns_none() -> None:
    queue = Queue()

    assert queue.dequeue() is None
    assert queue.dequeue() is None
    assert queue.to_list() == []


def test_queue_allows_duplicate_values() -> None:
    queue = Queue()

    queue.enqueue(7)
    queue.enqueue(7)
    queue.enqueue(7)

    assert queue.to_list() == [7, 7, 7]
    assert [queue.dequeue(), queue.dequeue(), queue.dequeue()] == [7, 7, 7]


@pytest.mark.parametrize("value", ["1", 1.5, None, False])
def test_queue_rejects_non_integer_input(value: object) -> None:
    queue = Queue()

    with pytest.raises(TypeError, match="integers"):
        queue.enqueue(value)  # type: ignore[arg-type]

    assert queue.is_empty()


def test_queue_repeated_operations_keep_expected_state() -> None:
    queue = Queue()

    assert queue.dequeue() is None
    queue.enqueue(4)
    queue.enqueue(5)
    assert queue.dequeue() == 4
    queue.enqueue(6)
    assert queue.to_list() == [5, 6]
    assert queue.dequeue() == 5
    assert queue.dequeue() == 6
    assert queue.dequeue() is None


def test_queue_display_representation() -> None:
    queue = Queue()
    queue.enqueue(2)
    queue.enqueue(9)

    assert queue.display() == "Queue(front -> back): [2, 9]"
    assert str(queue) == queue.display()
