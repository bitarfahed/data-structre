"""Non-visual controller logic for the visual lab GUI."""

from dataclasses import dataclass, replace
from enum import Enum

from data_structures_visual_lab.domain.algorithms import (
    AlgorithmStep,
    bfs,
    binary_search,
    bubble_sort,
    heap_sort,
    insertion_sort,
    merge_sort,
    parse_integer_array_text,
    quick_sort,
    selection_sort,
    validate_ascending_sorted,
)
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
from data_structures_visual_lab.events import Step
from data_structures_visual_lab.visualization.state import (
    VisualizationState,
    build_algorithm_visualization_state,
    build_visualization_state,
)


class StructureKey(str, Enum):
    """Supported structures."""

    STACK = "Stack"
    QUEUE = "Queue"
    LINKED_LIST = "Linked List"
    DYNAMIC_ARRAY = "Dynamic Array"
    AVL_TREE = "AVL Tree"
    MIN_HEAP = "Min-Heap"
    HASH_TABLE = "Hash Table"
    TWO_THREE_TREE = "2-3 Tree"
    GRAPH = "Graph"
    BINARY_SEARCH = "Binary Search"
    BUBBLE_SORT = "Bubble Sort"
    SELECTION_SORT = "Selection Sort"
    INSERTION_SORT = "Insertion Sort"
    MERGE_SORT = "Merge Sort"
    QUICK_SORT = "Quick Sort"
    HEAP_SORT = "Heap Sort"


@dataclass(frozen=True)
class OperationSpec:
    """A user-facing operation description."""

    key: str
    label: str
    needs_value: bool = False
    needs_index: bool = False
    index_required: bool = False
    value_label: str = "Value"
    index_label: str = "Index"
    index_allows_negative: bool = False
    index_input_kind: str = "integer"


@dataclass(frozen=True)
class OperationResult:
    """The result of running one GUI operation."""

    ok: bool
    message: str
    steps: list[Step | AlgorithmStep]


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
    StructureKey.HASH_TABLE: (
        "A hash table maps integer keys to integer values by calculating a bucket index. "
        "This version uses separate chaining when keys repeat or multiple keys land in the same bucket."
    ),
    StructureKey.TWO_THREE_TREE: (
        "A 2-3 tree keeps all leaves at the same depth. Each node normally stores one or two keys, "
        "and this version separates raw leaf insertion from split and promotion repair."
    ),
    StructureKey.GRAPH: (
        "A graph stores vertices and weighted edges. This builder supports directed and undirected graphs "
        "using an adjacency list."
    ),
    StructureKey.BINARY_SEARCH: (
        "Binary Search repeatedly checks the middle of an ascending sorted array, then discards the half "
        "that cannot contain the target."
    ),
    StructureKey.BUBBLE_SORT: (
        "Bubble Sort repeatedly compares neighboring values and swaps them when they are out of order."
    ),
    StructureKey.SELECTION_SORT: (
        "Selection Sort repeatedly finds the minimum value in the unsorted suffix and swaps it into place."
    ),
    StructureKey.INSERTION_SORT: (
        "Insertion Sort grows a sorted prefix by shifting larger values and inserting the current value."
    ),
    StructureKey.MERGE_SORT: (
        "Merge Sort recursively splits an array into smaller ranges, then merges those ranges back in sorted order."
    ),
    StructureKey.QUICK_SORT: (
        "Quick Sort partitions an array around a pivot, then recursively sorts the left and right partitions."
    ),
    StructureKey.HEAP_SORT: (
        "Heap Sort builds a Max-Heap, then repeatedly moves the largest root value into the sorted suffix."
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
    StructureKey.HASH_TABLE: (
        OperationSpec(
            "insert",
            "insert(key, value)",
            needs_value=True,
            needs_index=True,
            index_required=True,
            index_label="Key",
            index_allows_negative=True,
        ),
        OperationSpec(
            "search",
            "search(key)",
            needs_index=True,
            index_required=True,
            index_label="Key",
            index_allows_negative=True,
        ),
        OperationSpec(
            "delete",
            "delete(key)",
            needs_index=True,
            index_required=True,
            index_label="Key",
            index_allows_negative=True,
        ),
    ),
    StructureKey.TWO_THREE_TREE: (
        OperationSpec("insert_raw", "insert_raw(value)", needs_value=True),
        OperationSpec("repair", "repair()"),
        OperationSpec("search", "search(value)", needs_value=True),
    ),
    StructureKey.GRAPH: (
        OperationSpec("add_vertex", "Add Vertex", needs_value=True, value_label="Vertex"),
        OperationSpec("remove_vertex", "Remove Vertex", needs_value=True, value_label="Vertex"),
        OperationSpec(
            "add_edge",
            "Add Edge",
            needs_value=True,
            needs_index=True,
            index_required=True,
            value_label="Destination",
            index_label="Source",
        ),
        OperationSpec(
            "remove_edge",
            "Remove Edge",
            needs_value=True,
            needs_index=True,
            index_required=True,
            value_label="Destination",
            index_label="Source",
        ),
        OperationSpec("bfs", "BFS", needs_value=True, value_label="Start"),
    ),
    StructureKey.BINARY_SEARCH: (
        OperationSpec(
            "load_array",
            "Load Array",
            needs_index=True,
            index_label="Array",
            index_input_kind="array",
        ),
        OperationSpec(
            "search",
            "Search",
            needs_value=True,
            value_label="Target",
        ),
    ),
    StructureKey.BUBBLE_SORT: (
        OperationSpec("sort", "sort(array)", needs_index=True, index_required=True, index_label="Array", index_input_kind="array"),
    ),
    StructureKey.SELECTION_SORT: (
        OperationSpec("sort", "sort(array)", needs_index=True, index_required=True, index_label="Array", index_input_kind="array"),
    ),
    StructureKey.INSERTION_SORT: (
        OperationSpec("sort", "sort(array)", needs_index=True, index_required=True, index_label="Array", index_input_kind="array"),
    ),
    StructureKey.MERGE_SORT: (
        OperationSpec("sort", "sort(array)", needs_index=True, index_required=True, index_label="Array", index_input_kind="array"),
    ),
    StructureKey.QUICK_SORT: (
        OperationSpec("sort", "sort(array)", needs_index=True, index_required=True, index_label="Array", index_input_kind="array"),
    ),
    StructureKey.HEAP_SORT: (
        OperationSpec("sort", "sort(array)", needs_index=True, index_required=True, index_label="Array", index_input_kind="array"),
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
            StructureKey.HASH_TABLE: HashTable(),
            StructureKey.TWO_THREE_TREE: TwoThreeTree(),
            StructureKey.GRAPH: Graph(),
        }
        self._binary_search_array: tuple[int, ...] = ()
        self._binary_search_array_loaded = False

    def structure_keys(self) -> tuple[StructureKey, ...]:
        return tuple(StructureKey)

    def explanation_for(self, structure_key: StructureKey) -> str:
        return STRUCTURE_EXPLANATIONS[structure_key]

    def operations_for(self, structure_key: StructureKey) -> tuple[OperationSpec, ...]:
        return OPERATIONS[structure_key]

    def category_for(self, structure_key: StructureKey) -> str:
        if structure_key is StructureKey.BINARY_SEARCH:
            return "Algorithms / Searching"
        if structure_key in {
            StructureKey.BUBBLE_SORT,
            StructureKey.SELECTION_SORT,
            StructureKey.INSERTION_SORT,
            StructureKey.MERGE_SORT,
            StructureKey.QUICK_SORT,
            StructureKey.HEAP_SORT,
        }:
            return "Algorithms / Sorting"
        return "Structures"

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
        if _is_algorithm_key(structure_key):
            if structure_key is StructureKey.BINARY_SEARCH and self._binary_search_array_loaded:
                state = build_algorithm_visualization_state(structure_key.value, values=self._binary_search_array)
                return replace(state, message="Loaded array. Enter a target, then search.")
            return build_algorithm_visualization_state(structure_key.value)
        return build_visualization_state(
            structure_key.value,
            self._structures[structure_key],
            step,
        )

    def binary_search_array_loaded(self) -> bool:
        """Return whether Binary Search has a validated loaded array."""
        return self._binary_search_array_loaded

    def binary_search_array(self) -> tuple[int, ...]:
        """Return the current loaded Binary Search array."""
        return self._binary_search_array

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
        elif structure_key is StructureKey.MIN_HEAP:
            self._structures[structure_key] = MinHeap()
        elif structure_key is StructureKey.HASH_TABLE:
            self._structures[structure_key] = HashTable()
        elif structure_key is StructureKey.TWO_THREE_TREE:
            self._structures[structure_key] = TwoThreeTree()
        elif structure_key is StructureKey.GRAPH:
            current = self._structures[structure_key]
            self._structures[structure_key] = Graph(directed=current.directed)
        elif structure_key is StructureKey.BINARY_SEARCH:
            self._binary_search_array = ()
            self._binary_search_array_loaded = False

    def set_graph_directed(self, directed: bool) -> None:
        """Create a new empty graph using the selected graph type."""
        self._structures[StructureKey.GRAPH] = Graph(directed=directed)

    def graph_directed(self) -> bool:
        """Return the selected graph direction mode."""
        graph = self._structures[StructureKey.GRAPH]
        return graph.directed

    def run_graph_operation(
        self,
        operation_key: str,
        vertex_text: str = "",
        source_text: str = "",
        destination_text: str = "",
        weight_text: str = "",
    ) -> OperationResult:
        """Run a graph operation with graph-specific input fields."""
        graph = self._structures[StructureKey.GRAPH]
        try:
            if operation_key == "add_vertex":
                vertex = self._parse_required_integer(vertex_text, "Vertex")
                if isinstance(vertex, str):
                    return OperationResult(False, vertex, [])
                ok, steps = graph.add_vertex_with_steps(vertex)
                return OperationResult(ok, steps[-1].message, steps)
            if operation_key == "remove_vertex":
                vertex = self._parse_required_integer(vertex_text, "Vertex")
                if isinstance(vertex, str):
                    return OperationResult(False, vertex, [])
                ok, steps = graph.remove_vertex_with_steps(vertex)
                return OperationResult(ok, steps[-1].message, steps)
            if operation_key == "bfs":
                start = self._parse_required_integer(vertex_text, "Start")
                if isinstance(start, str):
                    return OperationResult(False, start, [])
                result = bfs(graph, start)
                return OperationResult(result.ok, result.message, result.steps)

            source = self._parse_required_integer(source_text, "Source")
            destination = self._parse_required_integer(destination_text, "Destination")
            if isinstance(source, str):
                return OperationResult(False, source, [])
            if isinstance(destination, str):
                return OperationResult(False, destination, [])

            if operation_key == "add_edge":
                weight = self._parse_optional_weight(weight_text)
                if isinstance(weight, str):
                    return OperationResult(False, weight, [])
                ok, steps = graph.add_edge_with_steps(source, destination, weight)
                return OperationResult(ok, steps[-1].message, steps)
            if operation_key == "remove_edge":
                ok, steps = graph.remove_edge_with_steps(source, destination)
                return OperationResult(ok, steps[-1].message, steps)
        except (TypeError, ValueError) as error:
            return OperationResult(False, str(error), [])

        return OperationResult(False, f"Unsupported graph operation: {operation_key}", [])

    def run_operation(
        self,
        structure_key: StructureKey,
        operation_key: str,
        value_text: str = "",
        index_text: str = "",
    ) -> OperationResult:
        operation = self.operation_for(structure_key, operation_key)
        value = self._parse_value(value_text) if operation.needs_value else None
        index = None
        if operation.needs_index:
            if operation.index_input_kind == "array":
                index = self._parse_array(index_text)
            else:
                index = self._parse_index(
                    index_text,
                    operation.index_required,
                    operation.index_label,
                    operation.index_allows_negative,
                )

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
        index: int | tuple[int, ...] | None,
    ) -> OperationResult:
        if structure_key is StructureKey.BINARY_SEARCH:
            if operation_key == "load_array":
                array = _require_array(index)
                validation = validate_ascending_sorted(array)
                if not validation.ok:
                    return OperationResult(False, validation.message, [])
                self._binary_search_array = validation.values
                self._binary_search_array_loaded = True
                return OperationResult(True, f"Loaded array with {len(validation.values)} values.", [])
            if not self._binary_search_array_loaded:
                return OperationResult(False, "Load an ascending sorted array before searching.", [])
            result = binary_search(self._binary_search_array, _require_int(value))
            return OperationResult(result.ok, result.message, result.steps)
        if structure_key is StructureKey.BUBBLE_SORT:
            result = bubble_sort(_require_array(index))
            return OperationResult(result.ok, result.message, result.steps)
        if structure_key is StructureKey.SELECTION_SORT:
            result = selection_sort(_require_array(index))
            return OperationResult(result.ok, result.message, result.steps)
        if structure_key is StructureKey.INSERTION_SORT:
            result = insertion_sort(_require_array(index))
            return OperationResult(result.ok, result.message, result.steps)
        if structure_key is StructureKey.MERGE_SORT:
            result = merge_sort(_require_array(index))
            return OperationResult(result.ok, result.message, result.steps)
        if structure_key is StructureKey.QUICK_SORT:
            result = quick_sort(_require_array(index))
            return OperationResult(result.ok, result.message, result.steps)
        if structure_key is StructureKey.HEAP_SORT:
            result = heap_sort(_require_array(index))
            return OperationResult(result.ok, result.message, result.steps)

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

        if isinstance(structure, HashTable):
            if operation_key == "insert":
                ok, steps = structure.insert_with_steps(_require_int(index), _require_int(value))
                return OperationResult(ok, steps[-1].message, steps)
            if operation_key == "search":
                result, steps = structure.search_with_steps(_require_int(index))
                return OperationResult(bool(result), steps[-1].message, steps)
            ok, steps = structure.delete_with_steps(_require_int(index))
            return OperationResult(ok, steps[-1].message, steps)

        if isinstance(structure, TwoThreeTree):
            if operation_key == "insert_raw":
                ok, steps = structure.insert_raw_with_steps(_require_int(value))
                return OperationResult(ok, steps[-1].message, steps)
            if operation_key == "repair":
                ok, steps = structure.repair_with_steps()
                return OperationResult(ok, steps[-1].message, steps)
            ok, steps = structure.search_with_steps(_require_int(value))
            return OperationResult(ok, steps[-1].message, steps)

        if isinstance(structure, Graph):
            if operation_key == "add_vertex":
                ok, steps = structure.add_vertex_with_steps(_require_int(value))
                return OperationResult(ok, steps[-1].message, steps)
            if operation_key == "remove_vertex":
                ok, steps = structure.remove_vertex_with_steps(_require_int(value))
                return OperationResult(ok, steps[-1].message, steps)
            if operation_key == "add_edge":
                ok, steps = structure.add_edge_with_steps(_require_int(index), _require_int(value))
                return OperationResult(ok, steps[-1].message, steps)
            ok, steps = structure.remove_edge_with_steps(_require_int(index), _require_int(value))
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
    def _parse_index(index_text: str, required: bool, label: str, allows_negative: bool) -> int | str | None:
        text = index_text.strip()
        if not text and not required:
            return None
        if not text:
            return f"Enter an integer {label.lower()}."
        parsed = _parse_integer(text, f"{label} must be an integer.")
        if isinstance(parsed, str):
            return parsed
        if parsed < 0 and not allows_negative:
            return f"{label} must be greater than or equal to 0."
        return parsed

    @staticmethod
    def _parse_array(array_text: str) -> tuple[int, ...] | str:
        result = parse_integer_array_text(array_text)
        if not result.ok:
            return result.message
        return result.values

    @staticmethod
    def _parse_required_integer(text: str, label: str) -> int | str:
        stripped = text.strip()
        if not stripped:
            return f"Enter an integer {label.lower()}."
        return _parse_integer(stripped, f"{label} must be an integer.")

    @staticmethod
    def _parse_optional_weight(text: str) -> int | str:
        stripped = text.strip()
        if not stripped:
            return 1
        parsed = _parse_integer(stripped, "Weight must be an integer.")
        if isinstance(parsed, str):
            return parsed
        if parsed < 0:
            return "Weight must be greater than or equal to 0."
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


def _require_array(value: int | tuple[int, ...] | None) -> tuple[int, ...]:
    if not isinstance(value, tuple):
        raise TypeError("Expected an integer array.")
    return value


def _is_algorithm_key(structure_key: StructureKey) -> bool:
    return structure_key in {
        StructureKey.BINARY_SEARCH,
        StructureKey.BUBBLE_SORT,
        StructureKey.SELECTION_SORT,
        StructureKey.INSERTION_SORT,
        StructureKey.MERGE_SORT,
        StructureKey.QUICK_SORT,
        StructureKey.HEAP_SORT,
    }
