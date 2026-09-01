from data_structures_visual_lab.domain.data_structures import (
    AVLTree,
    DynamicArray,
    Graph,
    HashTable,
    LinkedList,
    MinHeap,
    Queue,
    Stack,
    TwoThreeTree,
)
from data_structures_visual_lab.domain.algorithms import binary_search
from data_structures_visual_lab.domain.algorithms import bfs
from data_structures_visual_lab.domain.algorithms import bubble_sort
from data_structures_visual_lab.domain.algorithms import connected_components
from data_structures_visual_lab.domain.algorithms import dfs
from data_structures_visual_lab.domain.algorithms import dijkstra
from data_structures_visual_lab.domain.algorithms import heap_sort
from data_structures_visual_lab.domain.algorithms import merge_sort
from data_structures_visual_lab.domain.algorithms import quick_sort
from data_structures_visual_lab.events import EventType, Step
from data_structures_visual_lab.visualization import build_algorithm_visualization_state, build_visualization_state


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


def test_hash_table_visualization_state_includes_bucket_chains_and_collision_data() -> None:
    table = HashTable(bucket_count=4)
    table.insert(1, 10)
    _ok, steps = table.insert_with_steps(5, 50)

    state = build_visualization_state("Hash Table", table, steps[-1])

    assert state.size == 2
    assert state.bucket_count == 4
    assert state.bucket_index == 1
    assert state.collision
    assert len(state.buckets) == 4
    assert state.buckets[1].highlighted
    assert state.buckets[1].collision
    assert [(entry.key, entry.value) for entry in state.buckets[1].entries] == [(1, 10), (5, 50)]
    assert [entry.key for entry in state.buckets[1].entries if entry.highlighted] == [5]


def test_hash_table_visualization_state_highlights_all_duplicate_matches() -> None:
    table = HashTable(bucket_count=4)
    table.insert(1, 10)
    table.insert(5, 50)
    table.insert(1, 99)
    _values, steps = table.search_with_steps(1)

    state = build_visualization_state("Hash Table", table, steps[-1])

    assert state.bucket_index == 1
    assert [(entry.key, entry.value) for entry in state.buckets[1].entries] == [(1, 10), (5, 50), (1, 99)]
    assert [(entry.key, entry.value) for entry in state.buckets[1].entries if entry.highlighted] == [(1, 10), (1, 99)]


def test_binary_search_visualization_state_highlights_range_indices_and_discard() -> None:
    result = binary_search((1, 3, 5, 7, 9), 9)
    discard_step = [step for step in result.steps if step.state.metadata.get("discarded_range") == (0, 2)][0]

    state = build_algorithm_visualization_state("Binary Search", discard_step)

    assert state.structure_name == "Binary Search"
    assert state.target == 9
    assert state.low_index == 3
    assert state.high_index == 4
    assert state.mid_index == 2
    assert state.discarded_range == (0, 2)
    assert [element.index for element in state.values if element.moved] == [0, 1, 2]
    assert [element.index for element in state.values if element.highlighted] == [3, 4]


def test_sort_visualization_state_highlights_swaps_and_sorted_suffix() -> None:
    result = bubble_sort((3, 1, 2))
    swap_step = [step for step in result.steps if step.event_type.name == "SWAP"][0]

    state = build_algorithm_visualization_state("Bubble Sort", swap_step)

    assert [element.index for element in state.values if element.highlighted] == [0, 1]
    assert [element.index for element in state.values if element.moved] == []


def test_sort_visualization_empty_state_prompts_for_array_only() -> None:
    state = build_algorithm_visualization_state("Merge Sort")

    assert state.message == "Enter an integer array, then run the algorithm."


def test_merge_sort_visualization_state_includes_split_and_merge_ranges() -> None:
    result = merge_sort((3, 1, 2))
    split_step = [step for step in result.steps if step.state.metadata.get("split_index") == 1][0]
    merged_step = [step for step in result.steps if step.state.metadata.get("completed_range") == (0, 2)][0]

    split_state = build_algorithm_visualization_state("Merge Sort", split_step)
    merged_state = build_algorithm_visualization_state("Merge Sort", merged_step)

    assert split_state.split_index == 1
    assert split_state.merge_ranges == ((0, 1), (2, 2))
    assert [element.index for element in split_state.values if element.highlighted] == [0, 1, 2]
    assert [element.index for element in split_state.values if element.moved] == [0, 1, 2]
    assert merged_state.completed_range == (0, 2)
    assert [element.value for element in merged_state.values] == [1, 2, 3]


def test_quick_sort_visualization_state_includes_pivot_and_partitions() -> None:
    result = quick_sort((3, 1, 2))
    pivot_step = [step for step in result.steps if step.state.metadata.get("final_pivot_index") == 1][0]

    state = build_algorithm_visualization_state("Quick Sort", pivot_step)

    assert state.pivot_index == 1
    assert state.pivot_value == 2
    assert state.left_partition_range == (0, 0)
    assert state.right_partition_range == (2, 2)
    assert [element.index for element in state.values if element.highlighted] == [1, 2]
    assert [element.index for element in state.values if element.moved] == [0, 1, 2]


def test_heap_sort_visualization_state_includes_active_heap_and_sorted_suffix() -> None:
    result = heap_sort((3, 1, 2))
    root_swap = [step for step in result.steps if step.state.metadata.get("root_to_end_swap") is True][0]

    state = build_algorithm_visualization_state("Heap Sort", root_swap)

    assert state.active_heap_range == (0, 1)
    assert state.sorted_suffix_start == 2
    assert [element.index for element in state.values if element.highlighted] == [0, 2]
    assert [element.index for element in state.values if element.moved] == [0, 1, 2]


def test_two_three_visualization_state_includes_multikey_nodes_and_repair_data() -> None:
    tree = TwoThreeTree()
    tree.insert_raw(10)
    tree.insert_raw(5)
    _ok, steps = tree.insert_raw_with_steps(15)

    state = build_visualization_state("2-3 Tree", tree, steps[-1])

    assert state.size == 3
    assert not state.tree_valid
    assert state.repair_pending
    assert state.invalid_node_id == state.multi_key_tree_nodes[0].id
    assert state.multi_key_tree_edges == ()
    assert state.multi_key_tree_nodes[0].keys == (5, 10, 15)
    assert state.multi_key_tree_nodes[0].overflowing
    assert state.multi_key_tree_nodes[0].highlighted
    assert state.multi_key_tree_nodes[0].highlighted_key == 15


def test_graph_visualization_state_includes_nodes_edges_weights_and_type() -> None:
    graph = Graph(directed=True)
    graph.add_vertex(1)
    graph.add_vertex(2)
    _ok, steps = graph.add_edge_with_steps(1, 2, weight=5)

    state = build_visualization_state("Graph", graph, steps[-1])

    assert state.graph_type == "directed"
    assert [node.value for node in state.graph_nodes] == [1, 2]
    assert [node.value for node in state.graph_nodes if node.highlighted] == [1, 2]
    assert [(edge.source, edge.destination, edge.weight, edge.directed) for edge in state.graph_edges] == [
        (1, 2, 5, True)
    ]
    assert state.graph_edges[0].highlighted
    assert state.adjacency == {1: ((2, 5),), 2: ()}


def test_graph_visualization_state_includes_bfs_queue_and_order() -> None:
    graph = Graph()
    for vertex in (1, 2, 3):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    result = bfs(graph, 1)
    discover_step = [step for step in result.steps if step.message == "Discovered vertex 2; enqueue it."][0]

    state = build_visualization_state("Graph", graph, discover_step)

    assert state.current_vertex == 2
    assert state.frontier == "queue"
    assert state.queue == (2,)
    assert state.visited_vertices == (1, 2)
    assert state.traversal_order == (1,)
    assert state.examined_edge == (1, 2)
    assert [node.value for node in state.graph_nodes if node.current] == [2]
    assert [node.value for node in state.graph_nodes if node.visited] == [1, 2]
    assert [(edge.source, edge.destination) for edge in state.graph_edges if edge.highlighted] == [(1, 2)]


def test_graph_visualization_state_includes_dijkstra_distances_queue_and_path() -> None:
    graph = Graph()
    for vertex in (1, 2, 3):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2, 4)
    graph.add_edge(1, 3, 1)
    graph.add_edge(3, 2, 2)
    result = dijkstra(graph, 1, 2)
    update_step = [step for step in result.steps if step.message == "Update vertex 3: distance becomes 1."][0]
    complete_step = result.steps[-1]

    update_state = build_visualization_state("Graph", graph, update_step)
    complete_state = build_visualization_state("Graph", graph, complete_step)

    assert update_state.current_vertex == 3
    assert update_state.distances == {1: 0, 2: 4, 3: 1}
    assert update_state.priority_queue == ((1, 3), (4, 2))
    assert update_state.examined_edge == (1, 3)
    assert [node.value for node in update_state.graph_nodes if node.current] == [3]
    assert complete_state.shortest_path == (1, 3, 2)
    assert [node.value for node in complete_state.graph_nodes if node.path] == [1, 2, 3]


def test_graph_visualization_state_includes_connected_components() -> None:
    graph = Graph()
    for vertex in (1, 2, 3):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2)
    result = connected_components(graph)
    final_step = result.steps[-1]

    state = build_visualization_state("Graph", graph, final_step)

    assert state.completed_components == ((1, 2), (3,))
    assert state.component_count == 2
    assert [node.value for node in state.graph_nodes if node.component_id == 1] == [1, 2]
    assert [node.value for node in state.graph_nodes if node.component_id == 2] == [3]


def test_graph_visualization_state_includes_dfs_stack_and_order() -> None:
    graph = Graph()
    for vertex in (1, 2, 3):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    result = dfs(graph, 1)
    discover_step = [step for step in result.steps if step.message == "Discovered vertex 2; push it onto the stack."][0]

    state = build_visualization_state("Graph", graph, discover_step)

    assert state.current_vertex == 2
    assert state.frontier == "stack"
    assert state.stack == (2,)
    assert state.queue == ()
    assert state.visited_vertices == (1, 2)
    assert state.traversal_order == (1,)
    assert state.examined_edge == (1, 2)
    assert [node.value for node in state.graph_nodes if node.current] == [2]
    assert [node.value for node in state.graph_nodes if node.visited] == [1, 2]
    assert [(edge.source, edge.destination) for edge in state.graph_edges if edge.highlighted] == [(1, 2)]
