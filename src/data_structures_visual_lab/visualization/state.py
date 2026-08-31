"""GUI-independent visualization state helpers."""

from dataclasses import dataclass

from data_structures_visual_lab.domain.data_structures import (
    AVLNode,
    AVLTree,
    DynamicArray,
    HashTable,
    LinkedList,
    MinHeap,
    Queue,
    Stack,
)
from data_structures_visual_lab.events import EventType, Step


@dataclass(frozen=True)
class VisualElement:
    """One value-bearing item to render."""

    index: int
    value: int | None
    highlighted: bool = False
    moved: bool = False


@dataclass(frozen=True)
class VisualTreeNode:
    """One tree node to render."""

    id: int
    value: int
    depth: int
    order: int
    height: int | None = None
    balance_factor: int | None = None
    array_index: int | None = None
    highlighted: bool = False
    unbalanced: bool = False


@dataclass(frozen=True)
class VisualHashEntry:
    """One hash-table entry to render."""

    key: int
    value: int
    entry_index: int
    highlighted: bool = False


@dataclass(frozen=True)
class VisualBucket:
    """One hash-table bucket chain to render."""

    index: int
    entries: tuple[VisualHashEntry, ...]
    highlighted: bool = False
    collision: bool = False


@dataclass(frozen=True)
class VisualizationState:
    """A structure snapshot plus the current operation message."""

    structure_name: str
    values: tuple[VisualElement, ...]
    message: str
    size: int
    capacity: int | None = None
    event_type: EventType | None = None
    metadata: dict[str, object] | None = None
    tree_nodes: tuple[VisualTreeNode, ...] = ()
    tree_edges: tuple[tuple[int, int], ...] = ()
    balanced: bool | None = None
    rebalance_pending: bool = False
    heap_valid: bool | None = None
    repair_pending: bool = False
    repair_index: int | None = None
    repair_kind: str | None = None
    buckets: tuple[VisualBucket, ...] = ()
    bucket_count: int | None = None
    bucket_index: int | None = None
    collision: bool = False


def build_visualization_state(
    structure_name: str,
    structure: Stack | Queue | LinkedList | DynamicArray | AVLTree | MinHeap | HashTable,
    step: Step | None = None,
) -> VisualizationState:
    """Build a renderer-friendly state from a domain structure and optional step."""
    metadata = step.metadata if step is not None else {}
    highlight_indexes = _highlight_indexes(metadata)
    moved_indexes = _moved_indexes(metadata)
    message = step.message if step is not None else str(structure)

    if isinstance(structure, AVLTree):
        highlight_values = _highlight_values(metadata)
        unbalanced_values = set(structure.unbalanced_values())
        nodes, edges = _tree_nodes_and_edges(
            structure.root,
            highlight_values,
            unbalanced_values,
        )
        return VisualizationState(
            structure_name=structure_name,
            values=(),
            message=message,
            size=len(structure),
            event_type=step.event_type if step is not None else None,
            metadata=metadata,
            tree_nodes=nodes,
            tree_edges=edges,
            balanced=structure.is_balanced(),
            rebalance_pending=structure.rebalance_pending,
        )

    if isinstance(structure, MinHeap):
        values = _values_from_metadata(metadata, structure.to_list())
        highlight_indexes = _heap_highlight_indexes(metadata)
        nodes, edges = _heap_nodes_and_edges(values, highlight_indexes)
        elements = tuple(
            VisualElement(
                index=index,
                value=value,
                highlighted=index in highlight_indexes,
            )
            for index, value in enumerate(values)
        )
        return VisualizationState(
            structure_name=structure_name,
            values=elements,
            message=message,
            size=len(values),
            event_type=step.event_type if step is not None else None,
            metadata=metadata,
            tree_nodes=nodes,
            tree_edges=edges,
            heap_valid=structure.is_valid_heap(),
            repair_pending=structure.repair_pending,
            repair_index=structure.repair_index,
            repair_kind=structure.repair_kind,
        )

    if isinstance(structure, HashTable):
        bucket_index = _int_or_none(metadata.get("bucket_index"))
        entry_index = _int_or_none(metadata.get("entry_index"))
        collision = metadata.get("collision") is True
        buckets = _hash_buckets(
            structure.bucket_contents(),
            bucket_index=bucket_index,
            entry_index=entry_index,
            collision=collision,
        )
        return VisualizationState(
            structure_name=structure_name,
            values=(),
            message=message,
            size=structure.size,
            event_type=step.event_type if step is not None else None,
            metadata=metadata,
            buckets=buckets,
            bucket_count=structure.bucket_count,
            bucket_index=bucket_index,
            collision=collision,
        )

    if isinstance(structure, DynamicArray):
        values = _values_from_metadata(metadata, structure.to_list())
        capacity = _capacity_from_metadata(metadata, structure.capacity)
        elements = tuple(
            VisualElement(
                index=index,
                value=values[index] if index < len(values) else None,
                highlighted=index in highlight_indexes,
                moved=index in moved_indexes,
            )
            for index in range(capacity)
        )
        return VisualizationState(
            structure_name=structure_name,
            values=elements,
            message=message,
            size=len(values),
            capacity=capacity,
            event_type=step.event_type if step is not None else None,
            metadata=metadata,
        )

    values = _values_from_metadata(metadata, structure.to_list())
    elements = tuple(
        VisualElement(
            index=index,
            value=value,
            highlighted=index in highlight_indexes,
            moved=index in moved_indexes,
        )
        for index, value in enumerate(values)
    )
    return VisualizationState(
        structure_name=structure_name,
        values=elements,
        message=message,
        size=len(values),
        event_type=step.event_type if step is not None else None,
        metadata=metadata,
    )


def _highlight_indexes(metadata: dict[str, object]) -> set[int]:
    indexes: set[int] = set()
    for key in ("index", "from_index", "to_index", "previous_index", "inserted_index"):
        value = metadata.get(key)
        if type(value) is int:
            indexes.add(value)
    return indexes


def _heap_highlight_indexes(metadata: dict[str, object]) -> set[int]:
    indexes = _highlight_indexes(metadata)
    value = metadata.get("repair_index")
    if type(value) is int:
        indexes.add(value)
    listed_indexes = metadata.get("highlight_indexes")
    if isinstance(listed_indexes, list):
        indexes.update(index for index in listed_indexes if type(index) is int)
    return indexes


def _values_from_metadata(
    metadata: dict[str, object],
    fallback: list[int],
) -> list[int]:
    values = metadata.get("state")
    if isinstance(values, list) and all(type(value) is int for value in values):
        return values
    return fallback


def _capacity_from_metadata(metadata: dict[str, object], fallback: int) -> int:
    capacity = metadata.get("capacity")
    if type(capacity) is int and capacity >= 0:
        return capacity
    new_capacity = metadata.get("new_capacity")
    if type(new_capacity) is int and new_capacity >= 0:
        return new_capacity
    return fallback


def _moved_indexes(metadata: dict[str, object]) -> set[int]:
    indexes: set[int] = set()
    for key in ("from_index", "to_index"):
        value = metadata.get(key)
        if type(value) is int:
            indexes.add(value)
    return indexes


def _highlight_values(metadata: dict[str, object]) -> set[int]:
    values: set[int] = set()
    for key in ("value", "inserted_value", "deleted_value", "result_value", "old_root_value", "new_root_value"):
        value = metadata.get(key)
        if type(value) is int:
            values.add(value)

    listed_values = metadata.get("highlight_values")
    if isinstance(listed_values, list):
        values.update(value for value in listed_values if type(value) is int)
    return values


def _tree_nodes_and_edges(
    root: AVLNode | None,
    highlight_values: set[int],
    unbalanced_values: set[int],
) -> tuple[tuple[VisualTreeNode, ...], tuple[tuple[int, int], ...]]:
    nodes: list[VisualTreeNode] = []
    edges: list[tuple[int, int]] = []
    counter = 0
    order = 0

    def visit(node: AVLNode | None, depth: int) -> int | None:
        nonlocal counter, order
        if node is None:
            return None

        left_id = visit(node.left, depth + 1)

        node_id = counter
        counter += 1
        current_order = order
        order += 1
        nodes.append(
            VisualTreeNode(
                id=node_id,
                value=node.value,
                depth=depth,
                order=current_order,
                height=node.height,
                balance_factor=node.balance_factor,
                highlighted=node.value in highlight_values,
                unbalanced=node.value in unbalanced_values,
            )
        )
        if left_id is not None:
            edges.append((node_id, left_id))

        right_id = visit(node.right, depth + 1)
        if right_id is not None:
            edges.append((node_id, right_id))
        return node_id

    visit(root, 0)
    return tuple(nodes), tuple(edges)


def _heap_nodes_and_edges(
    values: list[int],
    highlight_indexes: set[int],
) -> tuple[tuple[VisualTreeNode, ...], tuple[tuple[int, int], ...]]:
    nodes = tuple(
        VisualTreeNode(
            id=index,
            value=value,
            depth=_heap_depth(index),
            order=index,
            array_index=index,
            highlighted=index in highlight_indexes,
        )
        for index, value in enumerate(values)
    )
    edges = []
    for index in range(len(values)):
        left_index = 2 * index + 1
        right_index = 2 * index + 2
        if left_index < len(values):
            edges.append((index, left_index))
        if right_index < len(values):
            edges.append((index, right_index))
    return nodes, tuple(edges)


def _heap_depth(index: int) -> int:
    depth = 0
    while index > 0:
        index = (index - 1) // 2
        depth += 1
    return depth


def _hash_buckets(
    bucket_contents: list[list[tuple[int, int]]],
    bucket_index: int | None,
    entry_index: int | None,
    collision: bool,
) -> tuple[VisualBucket, ...]:
    buckets: list[VisualBucket] = []
    for current_bucket_index, bucket in enumerate(bucket_contents):
        highlighted_bucket = current_bucket_index == bucket_index
        entries = tuple(
            VisualHashEntry(
                key=key,
                value=value,
                entry_index=current_entry_index,
                highlighted=highlighted_bucket and current_entry_index == entry_index,
            )
            for current_entry_index, (key, value) in enumerate(bucket)
        )
        buckets.append(
            VisualBucket(
                index=current_bucket_index,
                entries=entries,
                highlighted=highlighted_bucket,
                collision=highlighted_bucket and collision,
            )
        )
    return tuple(buckets)


def _int_or_none(value: object) -> int | None:
    return value if type(value) is int else None
