"""Non-visual controller logic for the visual lab GUI."""

from dataclasses import dataclass
from enum import Enum

from data_structures_visual_lab.domain.data_structures import AVLTree, DynamicArray, LinkedList, MinHeap, Queue, Stack
from data_structures_visual_lab.events import Step
from data_structures_visual_lab.visualization.state import VisualizationState, build_visualization_state


class StructureKey(str, Enum):
    """Supported structures."""

    STACK = "Stack"
    QUEUE = "Queue"
    LINKED_LIST = "Linked List"
    DYNAMIC_ARRAY = "Dynamic Array"
    AVL_TREE = "AVL Tree"
    MIN_HEAP = "Min-Heap"


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
    StructureKey.AVL_TREE: (
        "An AVL tree is a binary search tree that tracks height and balance factor. "
        "Here, insert first behaves like a normal BST insert, then Balance restores AVL validity."
    ),
    StructureKey.MIN_HEAP: (
        "A min-heap stores values in a complete binary tree where each parent is less than or equal to its children. "
        "Here, raw add and raw extract are separated from the repair steps."
    ),
}

OPERATIONS: dict[StructureKey, tuple[OperationSpec, ...]] = {
    StructureKey.STACK: (
        OperationSpec("push", "push(value)", needs_value=True),
        OperationSpec("pop", "pop()"),
    ),
    StructureKey.QUEUE: (
        OperationSpec("enqueue", "enqueue(value)", needs_value=True),
        OperationSpec("dequeue", "dequeue()"),
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
    ),
    StructureKey.DYNAMIC_ARRAY: (
        OperationSpec("add", "add(value)", needs_value=True),
        OperationSpec("delete", "delete(index)", needs_index=True, index_required=True),
    ),
    StructureKey.AVL_TREE: (
        OperationSpec("insert", "insert(value)", needs_value=True),
        OperationSpec("balance", "balance()"),
        OperationSpec("search", "search(value)", needs_value=True),
        OperationSpec("delete", "delete(value)", needs_value=True),
        OperationSpec("min", "min()"),
        OperationSpec("max", "max()"),
    ),
    StructureKey.MIN_HEAP: (
        OperationSpec("add_raw", "add_raw(value)", needs_value=True),
        OperationSpec("sift_up", "sift_up()"),
        OperationSpec("extract_raw", "extract_raw()"),
        OperationSpec("heapify_down", "heapify_down()"),
        OperationSpec("peek_min", "peek_min()"),
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
            StructureKey.AVL_TREE: AVLTree(),
            StructureKey.MIN_HEAP: MinHeap(),
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

    def reset_structure(self, structure_key: StructureKey) -> None:
        """Replace the selected structure with a new empty instance."""
        if structure_key is StructureKey.STACK:
            self._structures[structure_key] = Stack()
        elif structure_key is StructureKey.QUEUE:
            self._structures[structure_key] = Queue()
        elif structure_key is StructureKey.LINKED_LIST:
            self._structures[structure_key] = LinkedList()
        elif structure_key is StructureKey.DYNAMIC_ARRAY:
            self._structures[structure_key] = DynamicArray()
        elif structure_key is StructureKey.AVL_TREE:
            self._structures[structure_key] = AVLTree()
        else:
            self._structures[structure_key] = MinHeap()

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

        if isinstance(structure, AVLTree):
            if operation_key == "insert":
                ok, steps = structure.insert_with_steps(_require_int(value))
                return OperationResult(ok, steps[-1].message, steps)
            if operation_key == "balance":
                ok, steps = structure.balance_with_steps()
                return OperationResult(ok, steps[-1].message, steps)
            if operation_key == "search":
                ok, steps = structure.search_with_steps(_require_int(value))
                return OperationResult(ok, steps[-1].message, steps)
            if operation_key == "delete":
                ok, steps = structure.delete_with_steps(_require_int(value))
                return OperationResult(ok, steps[-1].message, steps)
            if operation_key == "min":
                result, steps = structure.min_with_steps()
                return OperationResult(result is not None, steps[-1].message, steps)
            result, steps = structure.max_with_steps()
            return OperationResult(result is not None, steps[-1].message, steps)

        if isinstance(structure, MinHeap):
            if operation_key == "add_raw":
                ok, steps = structure.add_raw_with_steps(_require_int(value))
                return OperationResult(ok, steps[-1].message, steps)
            if operation_key == "sift_up":
                ok, steps = structure.sift_up_with_steps()
                return OperationResult(ok, steps[-1].message, steps)
            if operation_key == "extract_raw":
                result, steps = structure.extract_raw_with_steps()
                return OperationResult(result is not None, steps[-1].message, steps)
            if operation_key == "heapify_down":
                ok, steps = structure.heapify_down_with_steps()
                return OperationResult(ok, steps[-1].message, steps)
            result, steps = structure.peek_min_with_steps()
            return OperationResult(result is not None, steps[-1].message, steps)

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
