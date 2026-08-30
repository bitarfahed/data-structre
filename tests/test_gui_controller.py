from dsa_visual_lab.events import EventType
from dsa_visual_lab.gui.controller import StructureKey, VisualLabController


def test_controller_lists_round_1_structures_and_operations() -> None:
    controller = VisualLabController()

    assert controller.structure_keys() == (
        StructureKey.STACK,
        StructureKey.QUEUE,
        StructureKey.LINKED_LIST,
        StructureKey.DYNAMIC_ARRAY,
    )
    assert [operation.key for operation in controller.operations_for(StructureKey.STACK)] == [
        "push",
        "pop",
    ]
    assert [operation.key for operation in controller.operations_for(StructureKey.LINKED_LIST)] == [
        "push",
        "pop",
        "change_value",
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
