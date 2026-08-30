from dsa_visual_lab.domain.data_structures import DynamicArray, LinkedList, Queue, Stack
from dsa_visual_lab.events import EventType, Step
from dsa_visual_lab.visualization import build_visualization_state


def test_stack_visualization_state_marks_highlighted_index() -> None:
    stack = Stack()
    stack.push(4)
    stack.push(5)
    step = Step(EventType.VISIT, "Visit top.", {"index": 1})

    state = build_visualization_state("Stack", stack, step)

    assert state.message == "Visit top."
    assert state.event_type is EventType.VISIT
    assert state.metadata == {"index": 1}
    assert [element.value for element in state.values] == [4, 5]
    assert not state.values[0].highlighted
    assert state.values[1].highlighted


def test_stack_pop_step_visualization_uses_step_snapshot() -> None:
    stack = Stack()
    stack.push(1)
    stack.push(2)
    _value, steps = stack.pop_with_steps()

    state = build_visualization_state("Stack", stack, steps[0])

    assert [element.value for element in state.values] == [1, 2]
    assert state.values[1].highlighted


def test_queue_visualization_state_uses_front_to_back_values() -> None:
    queue = Queue()
    queue.enqueue(1)
    queue.enqueue(2)

    state = build_visualization_state("Queue", queue)

    assert [element.value for element in state.values] == [1, 2]
    assert state.size == 2


def test_linked_list_visualization_state_uses_head_to_tail_values() -> None:
    linked_list = LinkedList()
    linked_list.push(2)
    linked_list.push(1)

    state = build_visualization_state("Linked List", linked_list)

    assert [element.value for element in state.values] == [1, 2]
    assert state.capacity is None


def test_dynamic_array_visualization_state_includes_empty_capacity_cells() -> None:
    array = DynamicArray(initial_capacity=4)
    array.add(8)
    step = Step(EventType.RESIZE, "Capacity changed.", {"from_index": 0, "to_index": 1})

    state = build_visualization_state("Dynamic Array", array, step)

    assert state.size == 1
    assert state.capacity == 4
    assert [element.value for element in state.values] == [8, None, None, None]
    assert state.values[0].moved
    assert state.values[1].moved
