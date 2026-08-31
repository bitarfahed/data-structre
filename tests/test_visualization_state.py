from data_structures_visual_lab.domain.data_structures import AVLTree, DynamicArray, LinkedList, MinHeap, Queue, Stack
from data_structures_visual_lab.events import EventType, Step
from data_structures_visual_lab.visualization import build_visualization_state


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


def test_avl_visualization_state_includes_nodes_edges_and_balance_data() -> None:
    tree = AVLTree()
    tree.insert(30)
    tree.insert(20)
    _ok, steps = tree.insert_with_steps(10)

    state = build_visualization_state("AVL Tree", tree, steps[-1])

    assert state.values == ()
    assert state.size == 3
    assert not state.balanced
    assert state.rebalance_pending
    assert [node.value for node in state.tree_nodes] == [10, 20, 30]
    assert [(parent, child) for parent, child in state.tree_edges] == [(1, 0), (2, 1)]
    assert [node.value for node in state.tree_nodes if node.unbalanced] == [30]
    assert [node.value for node in state.tree_nodes if node.highlighted] == [10]


def test_min_heap_visualization_state_includes_tree_array_and_repair_data() -> None:
    heap = MinHeap()
    heap.add_raw(10)
    heap.add_raw(20)
    _ok, steps = heap.add_raw_with_steps(5)

    state = build_visualization_state("Min-Heap", heap, steps[-1])

    assert state.size == 3
    assert not state.heap_valid
    assert state.repair_pending
    assert state.repair_kind == "sift_up"
    assert state.repair_index == 2
    assert [element.value for element in state.values] == [10, 20, 5]
    assert [element.index for element in state.values if element.highlighted] == [2]
    assert [node.array_index for node in state.tree_nodes] == [0, 1, 2]
    assert state.tree_edges == ((0, 1), (0, 2))
    assert [node.array_index for node in state.tree_nodes if node.highlighted] == [2]
