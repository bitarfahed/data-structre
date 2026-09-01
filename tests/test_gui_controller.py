from data_structures_visual_lab.events import EventType
from data_structures_visual_lab.gui.controller import StructureKey, VisualLabController


def test_controller_lists_structures_and_operations() -> None:
    controller = VisualLabController()

    assert controller.structure_keys() == (
        StructureKey.STACK,
        StructureKey.QUEUE,
        StructureKey.LINKED_LIST,
        StructureKey.DYNAMIC_ARRAY,
        StructureKey.AVL_TREE,
        StructureKey.MIN_HEAP,
        StructureKey.HASH_TABLE,
        StructureKey.TWO_THREE_TREE,
        StructureKey.GRAPH,
        StructureKey.BINARY_SEARCH,
        StructureKey.BUBBLE_SORT,
        StructureKey.SELECTION_SORT,
        StructureKey.INSERTION_SORT,
        StructureKey.MERGE_SORT,
        StructureKey.QUICK_SORT,
        StructureKey.HEAP_SORT,
    )
    assert [operation.key for operation in controller.operations_for(StructureKey.STACK)] == [
        "push",
        "pop",
    ]
    assert [operation.key for operation in controller.operations_for(StructureKey.QUEUE)] == [
        "enqueue",
        "dequeue",
    ]
    assert [operation.key for operation in controller.operations_for(StructureKey.LINKED_LIST)] == [
        "push",
        "pop",
        "change_value",
    ]
    assert [operation.key for operation in controller.operations_for(StructureKey.DYNAMIC_ARRAY)] == [
        "add",
        "delete",
    ]
    assert [operation.key for operation in controller.operations_for(StructureKey.AVL_TREE)] == [
        "insert",
        "balance",
        "search",
        "delete",
        "min",
        "max",
    ]
    assert [operation.key for operation in controller.operations_for(StructureKey.MIN_HEAP)] == [
        "add_raw",
        "sift_up",
        "extract_raw",
        "heapify_down",
        "peek_min",
    ]
    assert [operation.key for operation in controller.operations_for(StructureKey.HASH_TABLE)] == [
        "insert",
        "search",
        "delete",
    ]
    assert [operation.key for operation in controller.operations_for(StructureKey.TWO_THREE_TREE)] == [
        "insert_raw",
        "repair",
        "search",
    ]
    assert [operation.key for operation in controller.operations_for(StructureKey.GRAPH)] == [
        "add_vertex",
        "remove_vertex",
        "add_edge",
        "remove_edge",
        "bfs",
    ]
    assert [operation.key for operation in controller.operations_for(StructureKey.BINARY_SEARCH)] == [
        "load_array",
        "search",
    ]
    for structure_key in (
        StructureKey.BUBBLE_SORT,
        StructureKey.SELECTION_SORT,
        StructureKey.INSERTION_SORT,
        StructureKey.MERGE_SORT,
        StructureKey.QUICK_SORT,
        StructureKey.HEAP_SORT,
    ):
        assert [operation.key for operation in controller.operations_for(structure_key)] == ["sort"]


def test_controller_rejects_invalid_value_input_without_mutating_structure() -> None:
    controller = VisualLabController()

    result = controller.run_operation(StructureKey.STACK, "push", value_text="abc")

    assert not result.ok
    assert result.message == "Value must be an integer."
    assert result.steps == []
    assert controller.snapshot(StructureKey.STACK).size == 0


def test_controller_rejects_negative_index_input() -> None:
    controller = VisualLabController()

    result = controller.run_operation(StructureKey.DYNAMIC_ARRAY, "delete", index_text="-1")

    assert not result.ok
    assert result.message == "Index must be greater than or equal to 0."
    assert result.steps == []


def test_controller_runs_stack_operation_and_exposes_steps() -> None:
    controller = VisualLabController()

    result = controller.run_operation(StructureKey.STACK, "push", value_text="7")

    assert result.ok
    assert [step.event_type for step in result.steps] == [
        EventType.ADD,
        EventType.COMPLETE,
    ]
    assert controller.snapshot(StructureKey.STACK).values[0].value == 7


def test_controller_runs_linked_list_default_index_operation() -> None:
    controller = VisualLabController()

    controller.run_operation(StructureKey.LINKED_LIST, "push", value_text="2")
    result = controller.run_operation(StructureKey.LINKED_LIST, "push", value_text="1")

    assert result.ok
    assert [element.value for element in controller.snapshot(StructureKey.LINKED_LIST).values] == [
        1,
        2,
    ]


def test_controller_runs_dynamic_array_delete_with_required_index() -> None:
    controller = VisualLabController()

    controller.run_operation(StructureKey.DYNAMIC_ARRAY, "add", value_text="1")
    controller.run_operation(StructureKey.DYNAMIC_ARRAY, "add", value_text="2")
    result = controller.run_operation(StructureKey.DYNAMIC_ARRAY, "delete", index_text="0")

    assert result.ok
    assert [element.value for element in controller.snapshot(StructureKey.DYNAMIC_ARRAY).values[:1]] == [2]


def test_controller_requires_index_when_operation_needs_it() -> None:
    controller = VisualLabController()

    result = controller.run_operation(StructureKey.LINKED_LIST, "change_value", value_text="9")

    assert not result.ok
    assert result.message == "Enter an integer index."


def test_controller_supports_multiple_operations_without_resetting_structure() -> None:
    controller = VisualLabController()

    controller.run_operation(StructureKey.QUEUE, "enqueue", value_text="1")
    controller.run_operation(StructureKey.QUEUE, "enqueue", value_text="2")
    first = controller.run_operation(StructureKey.QUEUE, "dequeue")
    controller.run_operation(StructureKey.QUEUE, "enqueue", value_text="3")

    assert first.ok
    assert [element.value for element in controller.snapshot(StructureKey.QUEUE).values] == [2, 3]


def test_dynamic_array_resize_steps_include_capacity_change_metadata() -> None:
    controller = VisualLabController()

    controller.run_operation(StructureKey.DYNAMIC_ARRAY, "add", value_text="1")
    result = controller.run_operation(StructureKey.DYNAMIC_ARRAY, "add", value_text="2")

    resize_steps = [step for step in result.steps if step.event_type is EventType.RESIZE]
    assert resize_steps
    assert resize_steps[0].metadata["old_capacity"] == 1
    assert resize_steps[0].metadata["new_capacity"] == 2
    assert resize_steps[0].metadata["state"] == [1]


def test_controller_reset_replaces_selected_structure_with_empty_instance() -> None:
    controller = VisualLabController()

    controller.run_operation(StructureKey.DYNAMIC_ARRAY, "add", value_text="1")
    controller.run_operation(StructureKey.DYNAMIC_ARRAY, "add", value_text="2")
    assert controller.snapshot(StructureKey.DYNAMIC_ARRAY).size == 2
    assert controller.snapshot(StructureKey.DYNAMIC_ARRAY).capacity == 2

    controller.reset_structure(StructureKey.DYNAMIC_ARRAY)
    snapshot = controller.snapshot(StructureKey.DYNAMIC_ARRAY)

    assert snapshot.size == 0
    assert snapshot.capacity == 1
    assert list(snapshot.values) == [snapshot.values[0]]
    assert snapshot.values[0].value is None

    controller.run_operation(StructureKey.DYNAMIC_ARRAY, "add", value_text="9")
    snapshot = controller.snapshot(StructureKey.DYNAMIC_ARRAY)
    assert snapshot.size == 1
    assert snapshot.capacity == 1
    assert snapshot.values[0].value == 9


def test_controller_reset_clears_each_round_1_structure() -> None:
    controller = VisualLabController()

    controller.run_operation(StructureKey.STACK, "push", value_text="1")
    controller.run_operation(StructureKey.QUEUE, "enqueue", value_text="2")
    controller.run_operation(StructureKey.LINKED_LIST, "push", value_text="3")
    controller.run_operation(StructureKey.DYNAMIC_ARRAY, "add", value_text="4")
    controller.run_operation(StructureKey.AVL_TREE, "insert", value_text="5")
    controller.run_operation(StructureKey.MIN_HEAP, "add_raw", value_text="6")
    controller.run_operation(StructureKey.HASH_TABLE, "insert", value_text="7", index_text="1")
    controller.run_operation(StructureKey.TWO_THREE_TREE, "insert_raw", value_text="8")

    for structure_key in controller.structure_keys():
        controller.reset_structure(structure_key)
        snapshot = controller.snapshot(structure_key)
        assert snapshot.size == 0
        assert all(element.value is None for element in snapshot.values)
        assert snapshot.tree_nodes == ()
        assert snapshot.multi_key_tree_nodes == ()


def test_controller_runs_avl_insert_and_marks_pending_rebalance() -> None:
    controller = VisualLabController()

    controller.run_operation(StructureKey.AVL_TREE, "insert", value_text="30")
    controller.run_operation(StructureKey.AVL_TREE, "insert", value_text="20")
    result = controller.run_operation(StructureKey.AVL_TREE, "insert", value_text="10")
    snapshot = controller.snapshot(StructureKey.AVL_TREE, result.steps[-1])

    assert result.ok
    assert snapshot.rebalance_pending
    assert not snapshot.balanced
    assert [node.value for node in snapshot.tree_nodes] == [10, 20, 30]
    assert [node.value for node in snapshot.tree_nodes if node.unbalanced] == [30]


def test_controller_blocks_avl_insert_while_rebalance_is_pending() -> None:
    controller = VisualLabController()

    controller.run_operation(StructureKey.AVL_TREE, "insert", value_text="30")
    controller.run_operation(StructureKey.AVL_TREE, "insert", value_text="20")
    controller.run_operation(StructureKey.AVL_TREE, "insert", value_text="10")
    result = controller.run_operation(StructureKey.AVL_TREE, "insert", value_text="5")

    assert not result.ok
    assert result.message == "AVL insert blocked because rebalance is pending."
    assert [node.value for node in controller.snapshot(StructureKey.AVL_TREE).tree_nodes] == [10, 20, 30]


def test_controller_runs_avl_balance_and_reenables_insertion() -> None:
    controller = VisualLabController()

    controller.run_operation(StructureKey.AVL_TREE, "insert", value_text="30")
    controller.run_operation(StructureKey.AVL_TREE, "insert", value_text="20")
    controller.run_operation(StructureKey.AVL_TREE, "insert", value_text="10")
    balance_result = controller.run_operation(StructureKey.AVL_TREE, "balance")
    insert_result = controller.run_operation(StructureKey.AVL_TREE, "insert", value_text="5")

    assert balance_result.ok
    assert insert_result.ok
    snapshot = controller.snapshot(StructureKey.AVL_TREE)
    assert snapshot.balanced
    assert not snapshot.rebalance_pending
    assert [node.value for node in snapshot.tree_nodes] == [5, 10, 20, 30]


def test_controller_runs_avl_search_min_max_and_delete() -> None:
    controller = VisualLabController()

    for value in ("20", "10", "30"):
        controller.run_operation(StructureKey.AVL_TREE, "insert", value_text=value)

    found = controller.run_operation(StructureKey.AVL_TREE, "search", value_text="10")
    missing = controller.run_operation(StructureKey.AVL_TREE, "search", value_text="99")
    minimum = controller.run_operation(StructureKey.AVL_TREE, "min")
    maximum = controller.run_operation(StructureKey.AVL_TREE, "max")
    deleted = controller.run_operation(StructureKey.AVL_TREE, "delete", value_text="20")

    assert found.ok
    assert found.message == "AVL search found 10."
    assert not missing.ok
    assert missing.message == "AVL search did not find 99."
    assert minimum.ok
    assert minimum.message == "AVL minimum is 10."
    assert maximum.ok
    assert maximum.message == "AVL maximum is 30."
    assert deleted.ok
    assert [node.value for node in controller.snapshot(StructureKey.AVL_TREE).tree_nodes] == [10, 30]


def test_controller_rejects_invalid_avl_value_input() -> None:
    controller = VisualLabController()

    result = controller.run_operation(StructureKey.AVL_TREE, "insert", value_text="abc")

    assert not result.ok
    assert result.message == "Value must be an integer."
    assert controller.snapshot(StructureKey.AVL_TREE).size == 0


def test_controller_reset_clears_avl_pending_rebalance_state() -> None:
    controller = VisualLabController()

    controller.run_operation(StructureKey.AVL_TREE, "insert", value_text="30")
    controller.run_operation(StructureKey.AVL_TREE, "insert", value_text="20")
    controller.run_operation(StructureKey.AVL_TREE, "insert", value_text="10")
    assert controller.snapshot(StructureKey.AVL_TREE).rebalance_pending

    controller.reset_structure(StructureKey.AVL_TREE)
    snapshot = controller.snapshot(StructureKey.AVL_TREE)

    assert snapshot.size == 0
    assert snapshot.tree_nodes == ()
    assert snapshot.balanced
    assert not snapshot.rebalance_pending


def test_controller_runs_two_three_insert_raw_and_marks_pending_repair() -> None:
    controller = VisualLabController()

    controller.run_operation(StructureKey.TWO_THREE_TREE, "insert_raw", value_text="10")
    controller.run_operation(StructureKey.TWO_THREE_TREE, "insert_raw", value_text="5")
    result = controller.run_operation(StructureKey.TWO_THREE_TREE, "insert_raw", value_text="15")
    snapshot = controller.snapshot(StructureKey.TWO_THREE_TREE, result.steps[-1])

    assert result.ok
    assert result.message == "Raw insert complete. Repair required before another insert."
    assert not snapshot.tree_valid
    assert snapshot.repair_pending
    assert len(snapshot.multi_key_tree_nodes) == 1
    assert snapshot.multi_key_tree_nodes[0].keys == (5, 10, 15)
    assert snapshot.multi_key_tree_nodes[0].overflowing
    assert snapshot.multi_key_tree_nodes[0].highlighted


def test_controller_blocks_two_three_insert_while_repair_is_pending() -> None:
    controller = VisualLabController()

    controller.run_operation(StructureKey.TWO_THREE_TREE, "insert_raw", value_text="10")
    controller.run_operation(StructureKey.TWO_THREE_TREE, "insert_raw", value_text="5")
    controller.run_operation(StructureKey.TWO_THREE_TREE, "insert_raw", value_text="15")
    result = controller.run_operation(StructureKey.TWO_THREE_TREE, "insert_raw", value_text="20")

    assert not result.ok
    assert result.message == "2-3 Tree insert blocked because repair is pending."
    assert controller.snapshot(StructureKey.TWO_THREE_TREE).size == 3


def test_controller_runs_two_three_repair_and_reenables_insert() -> None:
    controller = VisualLabController()

    controller.run_operation(StructureKey.TWO_THREE_TREE, "insert_raw", value_text="10")
    controller.run_operation(StructureKey.TWO_THREE_TREE, "insert_raw", value_text="5")
    controller.run_operation(StructureKey.TWO_THREE_TREE, "insert_raw", value_text="15")
    repair_result = controller.run_operation(StructureKey.TWO_THREE_TREE, "repair")
    insert_result = controller.run_operation(StructureKey.TWO_THREE_TREE, "insert_raw", value_text="20")

    assert repair_result.ok
    assert repair_result.message == "2-3 Tree repair complete. Tree is valid."
    assert insert_result.ok
    snapshot = controller.snapshot(StructureKey.TWO_THREE_TREE)
    assert snapshot.tree_valid
    assert not snapshot.repair_pending
    assert [node.keys for node in snapshot.multi_key_tree_nodes] == [(10,), (5,), (15, 20)]


def test_controller_runs_two_three_recursive_repair_and_search() -> None:
    controller = VisualLabController()
    for value in ("10", "5", "15", "12", "11", "20", "25"):
        controller.run_operation(StructureKey.TWO_THREE_TREE, "insert_raw", value_text=value)
        if controller.snapshot(StructureKey.TWO_THREE_TREE).repair_pending:
            controller.run_operation(StructureKey.TWO_THREE_TREE, "repair")

    found = controller.run_operation(StructureKey.TWO_THREE_TREE, "search", value_text="11")
    missing = controller.run_operation(StructureKey.TWO_THREE_TREE, "search", value_text="99")
    snapshot = controller.snapshot(StructureKey.TWO_THREE_TREE, found.steps[-1])

    assert found.ok
    assert found.message == "2-3 Tree search found 11."
    assert not missing.ok
    assert missing.message == "2-3 Tree search did not find 99."
    assert snapshot.tree_valid
    assert not snapshot.repair_pending
    assert [node.keys for node in snapshot.multi_key_tree_nodes if node.depth == 0] == [(12,)]


def test_controller_rejects_invalid_two_three_value_input() -> None:
    controller = VisualLabController()

    result = controller.run_operation(StructureKey.TWO_THREE_TREE, "insert_raw", value_text="abc")

    assert not result.ok
    assert result.message == "Value must be an integer."
    assert controller.snapshot(StructureKey.TWO_THREE_TREE).size == 0


def test_controller_reset_clears_two_three_repair_state() -> None:
    controller = VisualLabController()

    controller.run_operation(StructureKey.TWO_THREE_TREE, "insert_raw", value_text="10")
    controller.run_operation(StructureKey.TWO_THREE_TREE, "insert_raw", value_text="5")
    controller.run_operation(StructureKey.TWO_THREE_TREE, "insert_raw", value_text="15")
    assert controller.snapshot(StructureKey.TWO_THREE_TREE).repair_pending

    controller.reset_structure(StructureKey.TWO_THREE_TREE)
    snapshot = controller.snapshot(StructureKey.TWO_THREE_TREE)

    assert snapshot.size == 0
    assert snapshot.multi_key_tree_nodes == ()
    assert snapshot.tree_valid
    assert not snapshot.repair_pending


def test_controller_runs_graph_builder_operations() -> None:
    controller = VisualLabController()

    first_vertex = controller.run_graph_operation("add_vertex", vertex_text="1")
    second_vertex = controller.run_graph_operation("add_vertex", vertex_text="2")
    edge_result = controller.run_graph_operation("add_edge", source_text="1", destination_text="2", weight_text="7")
    snapshot = controller.snapshot(StructureKey.GRAPH, edge_result.steps[-1])

    assert first_vertex.ok
    assert second_vertex.ok
    assert edge_result.ok
    assert edge_result.message == "Added edge 1 -> 2 with weight 7."
    assert snapshot.graph_type == "undirected"
    assert [node.value for node in snapshot.graph_nodes] == [1, 2]
    assert [(edge.source, edge.destination, edge.weight, edge.directed) for edge in snapshot.graph_edges] == [
        (1, 2, 7, False)
    ]
    assert snapshot.graph_edges[0].highlighted


def test_controller_graph_directed_mode_preserves_edge_direction() -> None:
    controller = VisualLabController()

    controller.set_graph_directed(True)
    controller.run_graph_operation("add_vertex", vertex_text="1")
    controller.run_graph_operation("add_vertex", vertex_text="2")
    controller.run_graph_operation("add_edge", source_text="1", destination_text="2")
    snapshot = controller.snapshot(StructureKey.GRAPH)

    assert controller.graph_directed()
    assert snapshot.graph_type == "directed"
    assert [(edge.source, edge.destination, edge.directed) for edge in snapshot.graph_edges] == [(1, 2, True)]
    assert snapshot.adjacency == {1: ((2, 1),), 2: ()}


def test_controller_graph_validation_messages_are_clear() -> None:
    controller = VisualLabController()

    controller.run_graph_operation("add_vertex", vertex_text="1")
    duplicate_vertex = controller.run_graph_operation("add_vertex", vertex_text="1")
    missing_destination = controller.run_graph_operation("add_edge", source_text="1", destination_text="2")
    self_loop = controller.run_graph_operation("add_edge", source_text="1", destination_text="1")
    invalid_weight = controller.run_graph_operation("add_edge", source_text="1", destination_text="2", weight_text="bad")
    negative_weight = controller.run_graph_operation("add_edge", source_text="1", destination_text="2", weight_text="-1")
    invalid_vertex = controller.run_graph_operation("add_vertex", vertex_text="bad")

    assert not duplicate_vertex.ok
    assert duplicate_vertex.message == "Add vertex skipped because vertex 1 already exists."
    assert not missing_destination.ok
    assert missing_destination.message == "Add edge skipped because destination vertex 2 does not exist."
    assert not self_loop.ok
    assert self_loop.message == "Add edge skipped because self-loops are not supported."
    assert not invalid_weight.ok
    assert invalid_weight.message == "Weight must be an integer."
    assert not negative_weight.ok
    assert negative_weight.message == "Weight must be greater than or equal to 0."
    assert not invalid_vertex.ok
    assert invalid_vertex.message == "Vertex must be an integer."


def test_controller_graph_restart_preserves_selected_type() -> None:
    controller = VisualLabController()
    controller.set_graph_directed(True)
    controller.run_graph_operation("add_vertex", vertex_text="1")
    controller.run_graph_operation("add_vertex", vertex_text="2")
    controller.run_graph_operation("add_edge", source_text="1", destination_text="2")

    controller.reset_structure(StructureKey.GRAPH)
    snapshot = controller.snapshot(StructureKey.GRAPH)

    assert controller.graph_directed()
    assert snapshot.graph_type == "directed"
    assert snapshot.graph_nodes == ()
    assert snapshot.graph_edges == ()


def test_controller_runs_graph_bfs_from_start_vertex() -> None:
    controller = VisualLabController()
    for vertex in ("1", "2", "3", "4"):
        controller.run_graph_operation("add_vertex", vertex_text=vertex)
    controller.run_graph_operation("add_edge", source_text="1", destination_text="2")
    controller.run_graph_operation("add_edge", source_text="1", destination_text="3")

    result = controller.run_graph_operation("bfs", vertex_text="1")
    snapshot = controller.snapshot(StructureKey.GRAPH, result.steps[-1])

    assert result.ok
    assert result.message == "BFS complete. Traversal order: [1, 2, 3]."
    assert snapshot.traversal_order == (1, 2, 3)
    assert snapshot.visited_vertices == (1, 2, 3)
    assert [node.value for node in snapshot.graph_nodes if node.visited] == [1, 2, 3]


def test_controller_rejects_invalid_or_missing_graph_bfs_start() -> None:
    controller = VisualLabController()

    empty = controller.run_graph_operation("bfs", vertex_text="1")
    invalid = controller.run_graph_operation("bfs", vertex_text="bad")
    controller.run_graph_operation("add_vertex", vertex_text="1")
    missing = controller.run_graph_operation("bfs", vertex_text="9")

    assert not empty.ok
    assert empty.message == "BFS skipped because the graph is empty."
    assert not invalid.ok
    assert invalid.message == "Start must be an integer."
    assert not missing.ok
    assert missing.message == "BFS start vertex 9 does not exist."


def test_controller_runs_min_heap_add_raw_and_marks_pending_repair() -> None:
    controller = VisualLabController()

    controller.run_operation(StructureKey.MIN_HEAP, "add_raw", value_text="10")
    controller.run_operation(StructureKey.MIN_HEAP, "add_raw", value_text="20")
    result = controller.run_operation(StructureKey.MIN_HEAP, "add_raw", value_text="5")
    snapshot = controller.snapshot(StructureKey.MIN_HEAP, result.steps[-1])

    assert result.ok
    assert result.message == "Raw add complete. Sift Up required before another add or extract."
    assert not snapshot.heap_valid
    assert snapshot.repair_pending
    assert snapshot.repair_kind == "sift_up"
    assert snapshot.repair_index == 2
    assert [element.value for element in snapshot.values] == [10, 20, 5]
    assert [node.array_index for node in snapshot.tree_nodes if node.highlighted] == [2]


def test_controller_blocks_min_heap_mutations_while_repair_is_pending() -> None:
    controller = VisualLabController()

    controller.run_operation(StructureKey.MIN_HEAP, "add_raw", value_text="10")
    controller.run_operation(StructureKey.MIN_HEAP, "add_raw", value_text="20")
    controller.run_operation(StructureKey.MIN_HEAP, "add_raw", value_text="5")

    add_result = controller.run_operation(StructureKey.MIN_HEAP, "add_raw", value_text="1")
    extract_result = controller.run_operation(StructureKey.MIN_HEAP, "extract_raw")

    assert not add_result.ok
    assert add_result.message == "Min-Heap add blocked because repair is pending."
    assert not extract_result.ok
    assert extract_result.message == "Min-Heap extract blocked because repair is pending."
    assert [element.value for element in controller.snapshot(StructureKey.MIN_HEAP).values] == [10, 20, 5]


def test_controller_runs_min_heap_sift_up_and_reenables_mutations() -> None:
    controller = VisualLabController()

    controller.run_operation(StructureKey.MIN_HEAP, "add_raw", value_text="10")
    controller.run_operation(StructureKey.MIN_HEAP, "add_raw", value_text="20")
    controller.run_operation(StructureKey.MIN_HEAP, "add_raw", value_text="5")
    sift_result = controller.run_operation(StructureKey.MIN_HEAP, "sift_up")
    add_result = controller.run_operation(StructureKey.MIN_HEAP, "add_raw", value_text="5")
    second_sift_result = controller.run_operation(StructureKey.MIN_HEAP, "sift_up")

    assert sift_result.ok
    assert add_result.ok
    assert second_sift_result.ok
    snapshot = controller.snapshot(StructureKey.MIN_HEAP)
    assert snapshot.heap_valid
    assert not snapshot.repair_pending
    assert [element.value for element in snapshot.values].count(5) == 2


def test_controller_runs_hash_table_insert_and_reports_collision() -> None:
    controller = VisualLabController()

    controller.run_operation(StructureKey.HASH_TABLE, "insert", value_text="10", index_text="1")
    result = controller.run_operation(StructureKey.HASH_TABLE, "insert", value_text="50", index_text="9")
    snapshot = controller.snapshot(StructureKey.HASH_TABLE, result.steps[-1])

    assert result.ok
    assert result.message == "Inserted key 9 with value 50."
    assert snapshot.bucket_count == 8
    assert snapshot.bucket_index == 1
    assert snapshot.collision
    assert snapshot.buckets[1].collision
    assert [(entry.key, entry.value) for entry in snapshot.buckets[1].entries] == [(1, 10), (9, 50)]
    assert [entry.key for entry in snapshot.buckets[1].entries if entry.highlighted] == [9]


def test_controller_runs_hash_table_duplicate_key_insert() -> None:
    controller = VisualLabController()

    controller.run_operation(StructureKey.HASH_TABLE, "insert", value_text="10", index_text="1")
    result = controller.run_operation(StructureKey.HASH_TABLE, "insert", value_text="99", index_text="1")

    assert result.ok
    assert result.message == "Inserted key 1 with value 99."
    snapshot = controller.snapshot(StructureKey.HASH_TABLE, result.steps[-1])
    assert [(entry.key, entry.value) for entry in snapshot.buckets[1].entries] == [(1, 10), (1, 99)]
    assert snapshot.collision
    assert [entry.entry_index for entry in snapshot.buckets[1].entries if entry.highlighted] == [1]


def test_controller_runs_hash_table_search_and_delete() -> None:
    controller = VisualLabController()

    controller.run_operation(StructureKey.HASH_TABLE, "insert", value_text="10", index_text="1")
    controller.run_operation(StructureKey.HASH_TABLE, "insert", value_text="20", index_text="1")
    controller.run_operation(StructureKey.HASH_TABLE, "insert", value_text="90", index_text="9")
    found = controller.run_operation(StructureKey.HASH_TABLE, "search", index_text="1")
    found_snapshot = controller.snapshot(StructureKey.HASH_TABLE, found.steps[-1])
    missing = controller.run_operation(StructureKey.HASH_TABLE, "search", index_text="2")
    deleted = controller.run_operation(StructureKey.HASH_TABLE, "delete", index_text="1")
    missing_delete = controller.run_operation(StructureKey.HASH_TABLE, "delete", index_text="1")

    assert found.ok
    assert found.message == "Found key 1 with values [10, 20]."
    assert [entry.value for entry in found_snapshot.buckets[1].entries if entry.highlighted] == [10, 20]
    assert not missing.ok
    assert missing.message == "Key 2 was not found."
    assert deleted.ok
    assert deleted.message == "Deleted 2 entries for key 1."
    assert not missing_delete.ok
    assert missing_delete.message == "Delete skipped because key 1 was not found."
    snapshot = controller.snapshot(StructureKey.HASH_TABLE)
    assert snapshot.size == 1
    assert [(entry.key, entry.value) for entry in snapshot.buckets[1].entries] == [(9, 90)]


def test_controller_accepts_negative_integer_hash_keys() -> None:
    controller = VisualLabController()

    result = controller.run_operation(StructureKey.HASH_TABLE, "insert", value_text="7", index_text="-1")

    assert result.ok
    snapshot = controller.snapshot(StructureKey.HASH_TABLE, result.steps[-1])
    assert snapshot.bucket_index == 7
    assert snapshot.buckets[7].entries[0].key == -1


def test_controller_rejects_invalid_hash_table_inputs() -> None:
    controller = VisualLabController()

    missing_key = controller.run_operation(StructureKey.HASH_TABLE, "search")
    invalid_key = controller.run_operation(StructureKey.HASH_TABLE, "insert", value_text="1", index_text="abc")
    invalid_value = controller.run_operation(StructureKey.HASH_TABLE, "insert", value_text="abc", index_text="1")

    assert not missing_key.ok
    assert missing_key.message == "Enter an integer key."
    assert not invalid_key.ok
    assert invalid_key.message == "Key must be an integer."
    assert not invalid_value.ok
    assert invalid_value.message == "Value must be an integer."
    assert controller.snapshot(StructureKey.HASH_TABLE).size == 0


def test_controller_reset_clears_hash_table_entries() -> None:
    controller = VisualLabController()

    controller.run_operation(StructureKey.HASH_TABLE, "insert", value_text="10", index_text="1")
    controller.run_operation(StructureKey.HASH_TABLE, "insert", value_text="50", index_text="9")
    assert controller.snapshot(StructureKey.HASH_TABLE).size == 2

    controller.reset_structure(StructureKey.HASH_TABLE)
    snapshot = controller.snapshot(StructureKey.HASH_TABLE)

    assert snapshot.size == 0
    assert snapshot.bucket_count == 8
    assert all(not bucket.entries for bucket in snapshot.buckets)


def test_controller_runs_min_heap_extract_raw_and_heapify_down() -> None:
    controller = VisualLabController()
    for value in ("1", "3", "2", "8", "9", "4"):
        controller.run_operation(StructureKey.MIN_HEAP, "add_raw", value_text=value)
        if controller.snapshot(StructureKey.MIN_HEAP).repair_pending:
            controller.run_operation(StructureKey.MIN_HEAP, "sift_up")

    extract_result = controller.run_operation(StructureKey.MIN_HEAP, "extract_raw")
    extract_snapshot = controller.snapshot(StructureKey.MIN_HEAP, extract_result.steps[-1])
    heapify_result = controller.run_operation(StructureKey.MIN_HEAP, "heapify_down")

    assert extract_result.ok
    assert extract_result.message == "Extracted 1. Heapify Down required before another add or extract."
    assert not extract_snapshot.heap_valid
    assert extract_snapshot.repair_kind == "heapify_down"
    assert heapify_result.ok
    snapshot = controller.snapshot(StructureKey.MIN_HEAP)
    assert snapshot.heap_valid
    assert not snapshot.repair_pending
    assert [element.value for element in snapshot.values][0] == 2


def test_controller_runs_min_heap_peek_min_and_empty_peek() -> None:
    controller = VisualLabController()

    empty = controller.run_operation(StructureKey.MIN_HEAP, "peek_min")
    controller.run_operation(StructureKey.MIN_HEAP, "add_raw", value_text="7")
    controller.run_operation(StructureKey.MIN_HEAP, "add_raw", value_text="3")
    controller.run_operation(StructureKey.MIN_HEAP, "sift_up")
    result = controller.run_operation(StructureKey.MIN_HEAP, "peek_min")

    assert not empty.ok
    assert empty.message == "Min-Heap peek skipped because the heap is empty."
    assert result.ok
    assert result.message == "Min-Heap minimum is 3."
    snapshot = controller.snapshot(StructureKey.MIN_HEAP, result.steps[-1])
    assert [node.array_index for node in snapshot.tree_nodes if node.highlighted] == [0]


def test_controller_rejects_invalid_min_heap_value_input() -> None:
    controller = VisualLabController()

    result = controller.run_operation(StructureKey.MIN_HEAP, "add_raw", value_text="abc")

    assert not result.ok
    assert result.message == "Value must be an integer."
    assert controller.snapshot(StructureKey.MIN_HEAP).size == 0


def test_controller_reset_clears_min_heap_repair_state() -> None:
    controller = VisualLabController()

    controller.run_operation(StructureKey.MIN_HEAP, "add_raw", value_text="10")
    controller.run_operation(StructureKey.MIN_HEAP, "add_raw", value_text="20")
    controller.run_operation(StructureKey.MIN_HEAP, "add_raw", value_text="5")
    assert controller.snapshot(StructureKey.MIN_HEAP).repair_pending

    controller.reset_structure(StructureKey.MIN_HEAP)
    snapshot = controller.snapshot(StructureKey.MIN_HEAP)

    assert snapshot.size == 0
    assert snapshot.values == ()
    assert snapshot.tree_nodes == ()
    assert snapshot.heap_valid
    assert not snapshot.repair_pending


def test_controller_loads_binary_search_array_and_exposes_it_to_visualization() -> None:
    controller = VisualLabController()

    result = controller.run_operation(
        StructureKey.BINARY_SEARCH,
        "load_array",
        index_text="1, 3, 5, 7, 9",
    )

    assert result.ok
    assert result.message == "Loaded array with 5 values."
    assert controller.binary_search_array_loaded()
    assert controller.binary_search_array() == (1, 3, 5, 7, 9)
    assert [element.value for element in controller.snapshot(StructureKey.BINARY_SEARCH).values] == [1, 3, 5, 7, 9]


def test_controller_binary_search_uses_loaded_array_and_target() -> None:
    controller = VisualLabController()

    controller.run_operation(
        StructureKey.BINARY_SEARCH,
        "load_array",
        index_text="2, 4, 8, 11, 19",
    )
    result = controller.run_operation(
        StructureKey.BINARY_SEARCH,
        "search",
        value_text="11",
    )

    assert result.ok
    assert result.message == "Found target 11 at index 3."
    assert result.steps[0].state.values == (2, 4, 8, 11, 19)  # type: ignore[union-attr]
    assert result.steps[-1].state.found_index == 3  # type: ignore[union-attr]


def test_controller_binary_search_target_changes_do_not_replace_loaded_array() -> None:
    controller = VisualLabController()

    controller.run_operation(StructureKey.BINARY_SEARCH, "load_array", index_text="1, 3, 5")
    first = controller.run_operation(StructureKey.BINARY_SEARCH, "search", value_text="3")
    second = controller.run_operation(StructureKey.BINARY_SEARCH, "search", value_text="1")

    assert first.ok
    assert second.ok
    assert controller.binary_search_array() == (1, 3, 5)
    assert [element.value for element in controller.snapshot(StructureKey.BINARY_SEARCH).values] == [1, 3, 5]


def test_controller_rejects_unsorted_binary_search_input() -> None:
    controller = VisualLabController()

    controller.run_operation(StructureKey.BINARY_SEARCH, "load_array", index_text="1, 3, 5")
    result = controller.run_operation(
        StructureKey.BINARY_SEARCH,
        "load_array",
        index_text="1, 4, 3",
    )

    assert not result.ok
    assert result.message == "Binary Search requires ascending sorted input."
    assert result.steps == []
    assert controller.binary_search_array() == (1, 3, 5)


def test_controller_rejects_invalid_binary_search_inputs() -> None:
    controller = VisualLabController()

    invalid_array = controller.run_operation(
        StructureKey.BINARY_SEARCH,
        "load_array",
        index_text="1, no",
    )
    controller.run_operation(StructureKey.BINARY_SEARCH, "load_array", index_text="1, 2")
    invalid_target = controller.run_operation(
        StructureKey.BINARY_SEARCH,
        "search",
        value_text="no",
    )

    assert not invalid_array.ok
    assert invalid_array.message == "Array values must be integers."
    assert not invalid_target.ok
    assert invalid_target.message == "Value must be an integer."


def test_controller_rejects_binary_search_before_array_load() -> None:
    controller = VisualLabController()

    result = controller.run_operation(StructureKey.BINARY_SEARCH, "search", value_text="5")

    assert not result.ok
    assert result.message == "Load an ascending sorted array before searching."
    assert result.steps == []


def test_controller_binary_search_allows_loaded_empty_array() -> None:
    controller = VisualLabController()

    loaded = controller.run_operation(StructureKey.BINARY_SEARCH, "load_array", index_text="")
    result = controller.run_operation(StructureKey.BINARY_SEARCH, "search", value_text="5")

    assert loaded.ok
    assert loaded.message == "Loaded array with 0 values."
    assert controller.binary_search_array_loaded()
    assert controller.snapshot(StructureKey.BINARY_SEARCH).message == "Loaded array. Enter a target, then search."
    assert not result.ok
    assert result.message == "Target 5 was not found."


def test_controller_binary_search_restart_clears_loaded_array() -> None:
    controller = VisualLabController()

    controller.run_operation(StructureKey.BINARY_SEARCH, "load_array", index_text="1, 2, 3")
    assert controller.binary_search_array_loaded()

    controller.reset_structure(StructureKey.BINARY_SEARCH)

    assert not controller.binary_search_array_loaded()
    assert controller.binary_search_array() == ()
    assert controller.snapshot(StructureKey.BINARY_SEARCH).values == ()


def test_controller_runs_sorting_algorithms() -> None:
    controller = VisualLabController()

    for structure_key, message in (
        (StructureKey.BUBBLE_SORT, "Bubble Sort complete."),
        (StructureKey.SELECTION_SORT, "Selection Sort complete."),
        (StructureKey.INSERTION_SORT, "Insertion Sort complete."),
        (StructureKey.MERGE_SORT, "Merge Sort complete."),
        (StructureKey.QUICK_SORT, "Quick Sort complete."),
        (StructureKey.HEAP_SORT, "Heap Sort complete."),
    ):
        result = controller.run_operation(structure_key, "sort", index_text="3, 1, 2")

        assert result.ok
        assert result.message == message
        assert result.steps[-1].state.values == (1, 2, 3)  # type: ignore[union-attr]


def test_controller_runs_sorting_algorithms_on_custom_arrays() -> None:
    controller = VisualLabController()

    for structure_key in (
        StructureKey.BUBBLE_SORT,
        StructureKey.SELECTION_SORT,
        StructureKey.INSERTION_SORT,
        StructureKey.MERGE_SORT,
        StructureKey.QUICK_SORT,
        StructureKey.HEAP_SORT,
    ):
        result = controller.run_operation(structure_key, "sort", index_text="8, 3, 7, 1, 5")

        assert result.ok
        assert result.steps[0].state.values == (8, 3, 7, 1, 5)  # type: ignore[union-attr]
        assert result.steps[-1].state.values == (1, 3, 5, 7, 8)  # type: ignore[union-attr]


def test_controller_rejects_invalid_sorting_array_input() -> None:
    controller = VisualLabController()

    result = controller.run_operation(StructureKey.BUBBLE_SORT, "sort", index_text="3, no, 2")

    assert not result.ok
    assert result.message == "Array values must be integers."
    assert result.steps == []
