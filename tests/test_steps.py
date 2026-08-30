from data_structures_visual_lab.domain.data_structures import DynamicArray, LinkedList, Queue, Stack
from data_structures_visual_lab.events import EventType, Step


def event_types(steps: list[Step]) -> list[EventType]:
    return [step.event_type for step in steps]


def test_step_contains_event_type_message_and_metadata() -> None:
    step = Step(EventType.ADD, "Added a value.", {"value": 3})

    assert step.event_type is EventType.ADD
    assert step.message == "Added a value."
    assert step.metadata == {"value": 3}


def test_stack_push_and_pop_expose_steps_without_changing_behavior() -> None:
    stack = Stack()

    push_steps = stack.push_with_steps(4)
    value, pop_steps = stack.pop_with_steps()
    empty_value, empty_steps = stack.pop_with_steps()

    assert event_types(push_steps) == [EventType.ADD, EventType.COMPLETE]
    assert value == 4
    assert event_types(pop_steps) == [
        EventType.VISIT,
        EventType.REMOVE,
        EventType.COMPLETE,
    ]
    assert empty_value is None
    assert event_types(empty_steps) == [EventType.COMPLETE]
    assert stack.is_empty()


def test_queue_enqueue_and_dequeue_expose_steps_without_changing_behavior() -> None:
    queue = Queue()

    enqueue_steps = queue.enqueue_with_steps(1)
    queue.enqueue(2)
    value, dequeue_steps = queue.dequeue_with_steps()

    assert event_types(enqueue_steps) == [EventType.ADD, EventType.COMPLETE]
    assert value == 1
    assert event_types(dequeue_steps) == [
        EventType.VISIT,
        EventType.REMOVE,
        EventType.COMPLETE,
    ]
    assert queue.to_list() == [2]


def test_linked_list_push_exposes_traversal_and_reference_update_steps() -> None:
    linked_list = LinkedList()
    linked_list.push(1)
    linked_list.push(3, index=1)

    success, steps = linked_list.push_with_steps(2, index=1)

    assert success
    assert EventType.COMPARE in event_types(steps)
    assert EventType.VISIT in event_types(steps)
    assert EventType.ADD in event_types(steps)
    assert EventType.UPDATE in event_types(steps)
    assert steps[-1].event_type is EventType.COMPLETE
    assert steps[-1].metadata["state"] == [1, 2, 3]
    assert linked_list.to_list() == [1, 2, 3]


def test_linked_list_pop_exposes_traversal_remove_and_reference_update_steps() -> None:
    linked_list = LinkedList()
    linked_list.push(1)
    linked_list.push(2, index=1)
    linked_list.push(3, index=2)

    value, steps = linked_list.pop_with_steps(1)

    assert value == 2
    assert EventType.COMPARE in event_types(steps)
    assert EventType.VISIT in event_types(steps)
    assert EventType.REMOVE in event_types(steps)
    assert EventType.UPDATE in event_types(steps)
    assert steps[-1].metadata["state"] == [1, 3]


def test_linked_list_change_value_exposes_update_steps() -> None:
    linked_list = LinkedList()
    linked_list.push(1)
    linked_list.push(2, index=1)

    success, steps = linked_list.change_value_with_steps(1, 9)

    assert success
    assert EventType.MOVE in event_types(steps)
    assert EventType.UPDATE in event_types(steps)
    assert steps[-1].event_type is EventType.COMPLETE
    assert linked_list.to_list() == [1, 9]


def test_linked_list_invalid_step_operations_are_safe() -> None:
    linked_list = LinkedList()

    push_success, push_steps = linked_list.push_with_steps(5, index=1)
    popped, pop_steps = linked_list.pop_with_steps()
    update_success, update_steps = linked_list.change_value_with_steps(0, 9)

    assert not push_success
    assert popped is None
    assert not update_success
    assert push_steps[-1].event_type is EventType.COMPLETE
    assert pop_steps[-1].event_type is EventType.COMPLETE
    assert update_steps[-1].event_type is EventType.COMPLETE
    assert linked_list.is_empty()


def test_dynamic_array_add_exposes_growth_resize_step() -> None:
    array = DynamicArray(initial_capacity=2)
    array.add(1)
    array.add(2)

    steps = array.add_with_steps(3)

    assert event_types(steps) == [
        EventType.RESIZE,
        EventType.ADD,
        EventType.COMPLETE,
    ]
    assert steps[0].metadata["old_capacity"] == 2
    assert steps[0].metadata["new_capacity"] == 4
    assert steps[0].metadata["state"] == [1, 2]
    assert steps[-1].metadata["state"] == [1, 2, 3]
    assert array.capacity == 4


def test_dynamic_array_delete_exposes_move_and_shrink_resize_steps() -> None:
    array = DynamicArray(initial_capacity=2)
    for value in range(8):
        array.add(value)

    for _ in range(5):
        array.delete(0)

    value, steps = array.delete_with_steps(0)

    assert value == 5
    assert EventType.COMPARE in event_types(steps)
    assert EventType.REMOVE in event_types(steps)
    assert EventType.MOVE in event_types(steps)
    assert EventType.RESIZE in event_types(steps)
    assert steps[-1].metadata["state"] == [6, 7]
    assert steps[-1].metadata["capacity"] == 4


def test_dynamic_array_invalid_delete_step_is_safe() -> None:
    array = DynamicArray()

    value, steps = array.delete_with_steps(0)

    assert value is None
    assert event_types(steps) == [EventType.COMPARE, EventType.COMPLETE]
    assert array.is_empty()
