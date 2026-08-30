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

    for structure_key in controller.structure_keys():
        controller.reset_structure(structure_key)
        snapshot = controller.snapshot(structure_key)
        assert snapshot.size == 0
        assert all(element.value is None for element in snapshot.values)
        assert snapshot.tree_nodes == ()


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
