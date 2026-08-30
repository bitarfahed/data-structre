"""Non-visual controller logic for the Round 1 GUI."""

from dataclasses import dataclass
from enum import Enum

from dsa_visual_lab.domain.data_structures import DynamicArray, LinkedList, Queue, Stack
from dsa_visual_lab.events import EventType, Step
from dsa_visual_lab.visualization.state import VisualizationState, build_visualization_state


class StructureKey(str, Enum):
    """Supported Round 1 structures."""

    STACK = "Stack"
    QUEUE = "Queue"
    LINKED_LIST = "Linked List"
    DYNAMIC_ARRAY = "Dynamic Array"


@dataclass(frozen=True)
class OperationSpec:
    """A user-facing operation description."""

    key: str
    label: str
    needs_value: bool = False
    needs_index: bool = False
    index_required: bool = False


@dataclass(frozen=True)
class OperationResult:
    """The result of running one GUI operation."""

    ok: bool
    message: str
    steps: list[Step]


STRUCTURE_EXPLANATIONS: dict[StructureKey, str] = {
    StructureKey.STACK: "A stack stores values in last-in, first-out order. The newest value is removed first.",
    StructureKey.QUEUE: "A queue stores values in first-in, first-out order. The oldest value is removed first.",
    StructureKey.LINKED_LIST: "A singly linked list stores values in nodes. Each node points to the next node.",
    StructureKey.DYNAMIC_ARRAY: "A dynamic array stores values in indexed cells and resizes when it needs more or less space.",
}

OPERATIONS: dict[StructureKey, tuple[OperationSpec, ...]] = {
    StructureKey.STACK: (
        OperationSpec("push", "push(value)", needs_value=True),
        OperationSpec("pop", "pop()"),
        OperationSpec("display", "display()"),
    ),
    StructureKey.QUEUE: (
        OperationSpec("enqueue", "enqueue(value)", needs_value=True),
        OperationSpec("dequeue", "dequeue()"),
        OperationSpec("display", "display()"),
    ),
    StructureKey.LINKED_LIST: (
        OperationSpec("push", "push(value, index=0)", needs_value=True, needs_index=True),
        OperationSpec("pop", "pop(index=0)", needs_index=True),
        OperationSpec(
            "change_value",
            "change_value(index, value)",
            needs_value=True,
            needs_index=True,
            index_required=True,
        ),
        OperationSpec("display", "display()"),
    ),
    StructureKey.DYNAMIC_ARRAY: (
        OperationSpec("add", "add(value)", needs_value=True),
        OperationSpec("delete", "delete(index)", needs_index=True, index_required=True),
        OperationSpec("display", "display()"),
    ),
}


class VisualLabController:
    """Owns domain objects and exposes operation results for the GUI."""

    def __init__(self) -> None:
        self._structures = {
            StructureKey.STACK: Stack(),
            StructureKey.QUEUE: Queue(),
            StructureKey.LINKED_LIST: LinkedList(),
            StructureKey.DYNAMIC_ARRAY: DynamicArray(),
        }

    def structure_keys(self) -> tuple[StructureKey, ...]:
        return tuple(StructureKey)

    def explanation_for(self, structure_key: StructureKey) -> str:
        return STRUCTURE_EXPLANATIONS[structure_key]

    def operations_for(self, structure_key: StructureKey) -> tuple[OperationSpec, ...]:
        return OPERATIONS[structure_key]

    def operation_for(self, structure_key: StructureKey, operation_key: str) -> OperationSpec:
        for operation in self.operations_for(structure_key):
            if operation.key == operation_key:
                return operation
        raise KeyError(f"Unsupported operation: {operation_key}")

    def snapshot(
        self,
        structure_key: StructureKey,
        step: Step | None = None,
    ) -> VisualizationState:
        return build_visualization_state(
            structure_key.value,
            self._structures[structure_key],
            step,
        )

    def run_operation(
        self,
        structure_key: StructureKey,
        operation_key: str,
        value_text: str = "",
        index_text: str = "",
    ) -> OperationResult:
        operation = self.operation_for(structure_key, operation_key)
        value = self._parse_value(value_text) if operation.needs_value else None
        index = self._parse_index(index_text, operation.index_required) if operation.needs_index else None

        if isinstance(value, str):
            return OperationResult(False, value, [])
        if isinstance(index, str):
            return OperationResult(False, index, [])

        try:
            return self._run_validated_operation(structure_key, operation_key, value, index)
        except TypeError as error:
            return OperationResult(False, str(error), [])

    def _run_validated_operation(
        self,
        structure_key: StructureKey,
        operation_key: str,
        value: int | None,
        index: int | None,
    ) -> OperationResult:
        structure = self._structures[structure_key]

        if operation_key == "display":
            step = Step(
                EventType.COMPLETE,
                structure.display(),
                {"size": len(structure), "state": structure.to_list()},
            )
            if isinstance(structure, DynamicArray):
                step = Step(
                    EventType.COMPLETE,
                    structure.display(),
                    {
                        "size": structure.size,
                        "capacity": structure.capacity,
                        "state": structure.to_list(),
                    },
                )
            return OperationResult(True, step.message, [step])

        if isinstance(structure, Stack):
            if operation_key == "push":
                steps = structure.push_with_steps(_require_int(value))
                return OperationResult(True, steps[-1].message, steps)
            result, steps = structure.pop_with_steps()
            return OperationResult(result is not None, steps[-1].message, steps)

        if isinstance(structure, Queue):
            if operation_key == "enqueue":
                steps = structure.enqueue_with_steps(_require_int(value))
                return OperationResult(True, steps[-1].message, steps)
            result, steps = structure.dequeue_with_steps()
            return OperationResult(result is not None, steps[-1].message, steps)

        if isinstance(structure, LinkedList):
            if operation_key == "push":
                ok, steps = structure.push_with_steps(_require_int(value), index or 0)
                return OperationResult(ok, steps[-1].message, steps)
            if operation_key == "pop":
                result, steps = structure.pop_with_steps(index or 0)
                return OperationResult(result is not None, steps[-1].message, steps)
            ok, steps = structure.change_value_with_steps(_require_int(index), _require_int(value))
            return OperationResult(ok, steps[-1].message, steps)

        if operation_key == "add":
            steps = structure.add_with_steps(_require_int(value))
            return OperationResult(True, steps[-1].message, steps)

        result, steps = structure.delete_with_steps(_require_int(index))
        return OperationResult(result is not None, steps[-1].message, steps)

    @staticmethod
    def _parse_value(value_text: str) -> int | str:
        text = value_text.strip()
        if not text:
            return "Enter an integer value."
        return _parse_integer(text, "Value must be an integer.")

    @staticmethod
    def _parse_index(index_text: str, required: bool) -> int | str | None:
        text = index_text.strip()
        if not text and not required:
            return None
        if not text:
            return "Enter an integer index."
        parsed = _parse_integer(text, "Index must be an integer.")
        if isinstance(parsed, str):
            return parsed
        if parsed < 0:
            return "Index must be greater than or equal to 0."
        return parsed


def _parse_integer(text: str, error_message: str) -> int | str:
    try:
        value = int(text)
    except ValueError:
        return error_message
    return value


def _require_int(value: int | None) -> int:
    if value is None:
        raise TypeError("Expected an integer.")
    return value
