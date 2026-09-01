"""GUI-independent visualization state helpers."""

from dataclasses import dataclass

from data_structures_visual_lab.domain.data_structures import (
    AVLNode,
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
from data_structures_visual_lab.domain.algorithms import AlgorithmStep
from data_structures_visual_lab.domain.data_structures.two_three_tree import TwoThreeNodeSnapshot
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
class VisualMultiKeyTreeNode:
    """One 2-3 tree node to render."""

    id: int
    keys: tuple[int, ...]
    depth: int
    order: int
    highlighted: bool = False
    highlighted_key: int | None = None
    overflowing: bool = False


@dataclass(frozen=True)
class VisualGraphNode:
    """One graph vertex to render."""

    value: int
    highlighted: bool = False
    visited: bool = False
    current: bool = False
    path: bool = False
    component_id: int | None = None
    cycle: bool = False


@dataclass(frozen=True)
class VisualGraphEdge:
    """One weighted graph edge to render."""

    source: int
    destination: int
    weight: int
    directed: bool
    highlighted: bool = False
    mst: bool = False


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
    multi_key_tree_nodes: tuple[VisualMultiKeyTreeNode, ...] = ()
    multi_key_tree_edges: tuple[tuple[int, int], ...] = ()
    tree_valid: bool | None = None
    invalid_node_id: int | None = None
    low_index: int | None = None
    high_index: int | None = None
    mid_index: int | None = None
    target: int | None = None
    discarded_range: tuple[int, int] | None = None
    found_index: int | None = None
    found: bool | None = None
    sorted_prefix_end: int | None = None
    sorted_suffix_start: int | None = None
    split_index: int | None = None
    merge_ranges: tuple[tuple[int, int], ...] = ()
    completed_range: tuple[int, int] | None = None
    pivot_index: int | None = None
    pivot_value: int | None = None
    left_partition_range: tuple[int, int] | None = None
    right_partition_range: tuple[int, int] | None = None
    active_heap_range: tuple[int, int] | None = None
    graph_type: str | None = None
    graph_nodes: tuple[VisualGraphNode, ...] = ()
    graph_edges: tuple[VisualGraphEdge, ...] = ()
    adjacency: dict[int, tuple[tuple[int, int], ...]] | None = None
    current_vertex: int | None = None
    queue: tuple[int, ...] = ()
    stack: tuple[int, ...] = ()
    frontier: str | None = None
    visited_vertices: tuple[int, ...] = ()
    traversal_order: tuple[int, ...] = ()
    examined_edge: tuple[int, int] | None = None
    distances: dict[int, int | None] | None = None
    priority_queue: tuple[tuple[int, int], ...] = ()
    predecessors: dict[int, int | None] | None = None
    shortest_path: tuple[int, ...] = ()
    current_component: int | None = None
    current_component_vertices: tuple[int, ...] = ()
    completed_components: tuple[tuple[int, ...], ...] = ()
    component_count: int | None = None
    traversal_path: tuple[int, ...] = ()
    cycle_detected: bool = False
    cycle_vertices: tuple[int, ...] = ()
    cycle_edges: tuple[tuple[int, int], ...] = ()
    indegrees: dict[int, int] | None = None
    zero_indegree_queue: tuple[int, ...] = ()
    processed_vertices: tuple[int, ...] = ()
    topological_order: tuple[int, ...] = ()
    topological_sort_possible: bool | None = None
    candidate_edges: tuple[tuple[int, int, int], ...] = ()
    mst_edges: tuple[tuple[int, int, int], ...] = ()
    mst_total_weight: int | None = None
    mst_disconnected: bool = False


def build_algorithm_visualization_state(
    algorithm_name: str,
    step: AlgorithmStep | None = None,
    values: tuple[int, ...] = (),
) -> VisualizationState:
    """Build a renderer-friendly state from an algorithm step."""
    if step is None:
        message = "Enter an integer array and target, then run the algorithm."
        if algorithm_name != "Binary Search":
            message = "Enter an integer array, then run the algorithm."
        elif values:
            message = "Loaded array. Enter a target, then search."
        return VisualizationState(
            structure_name=algorithm_name,
            values=tuple(VisualElement(index=index, value=value) for index, value in enumerate(values)),
            message=message,
            size=len(values),
        )

    metadata = step.state.metadata
    current_indices = set(step.state.current_indices)
    if step.state.swapped_indices is not None:
        current_indices.update(step.state.swapped_indices)
    discarded_range = _range_or_none(metadata.get("discarded_range"))
    sorted_prefix_end = _int_or_none(metadata.get("sorted_prefix_end"))
    sorted_suffix_start = _int_or_none(metadata.get("sorted_suffix_start"))
    completed_range = _range_or_none(metadata.get("completed_range"))
    merge_output_range = _range_or_none(metadata.get("merge_output_range"))
    merge_ranges = step.state.merge_ranges
    left_partition_range = _range_or_none(metadata.get("left_partition_range"))
    right_partition_range = _range_or_none(metadata.get("right_partition_range"))
    active_heap_range = _range_or_none(metadata.get("active_heap_range"))
    elements = tuple(
        VisualElement(
            index=index,
            value=value,
            highlighted=index in current_indices or index == step.state.found_index or index == step.state.pivot_index,
            moved=(
                (discarded_range is not None and discarded_range[0] <= index <= discarded_range[1])
                or _index_in_ranges(index, merge_ranges)
                or (completed_range is not None and completed_range[0] <= index <= completed_range[1])
                or (merge_output_range is not None and merge_output_range[0] <= index <= merge_output_range[1])
                or (left_partition_range is not None and left_partition_range[0] <= index <= left_partition_range[1])
                or (right_partition_range is not None and right_partition_range[0] <= index <= right_partition_range[1])
                or (active_heap_range is not None and active_heap_range[0] <= index <= active_heap_range[1])
                or index in _shift_indexes(metadata)
                or (sorted_prefix_end is not None and index <= sorted_prefix_end)
                or (sorted_suffix_start is not None and index >= sorted_suffix_start)
            ),
        )
        for index, value in enumerate(step.state.values)
    )
    return VisualizationState(
        structure_name=algorithm_name,
        values=elements,
        message=step.message,
        size=len(step.state.values),
        metadata=metadata,
        low_index=_int_or_none(metadata.get("low_index")),
        high_index=_int_or_none(metadata.get("high_index")),
        mid_index=_int_or_none(metadata.get("mid_index")),
        target=_int_or_none(metadata.get("target")),
        discarded_range=discarded_range,
        found_index=step.state.found_index,
        found=step.state.found,
        sorted_prefix_end=sorted_prefix_end,
        sorted_suffix_start=sorted_suffix_start,
        split_index=_int_or_none(metadata.get("split_index")),
        merge_ranges=merge_ranges,
        completed_range=completed_range,
        pivot_index=step.state.pivot_index,
        pivot_value=_int_or_none(metadata.get("pivot_value")),
        left_partition_range=left_partition_range,
        right_partition_range=right_partition_range,
        active_heap_range=active_heap_range,
    )


def build_visualization_state(
    structure_name: str,
    structure: Stack | Queue | LinkedList | DynamicArray | AVLTree | MinHeap | HashTable | TwoThreeTree | Graph,
    step: Step | None = None,
) -> VisualizationState:
    """Build a renderer-friendly state from a domain structure and optional step."""
    metadata = _step_metadata(step)
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
        entry_indexes = _int_list(metadata.get("entry_indexes"))
        collision = metadata.get("collision") is True
        buckets = _hash_buckets(
            structure.bucket_contents(),
            bucket_index=bucket_index,
            entry_index=entry_index,
            entry_indexes=entry_indexes,
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

    if isinstance(structure, TwoThreeTree):
        nodes, edges = _two_three_nodes_and_edges(
            structure.node_snapshots(),
            highlight_node_id=_int_or_none(metadata.get("highlight_node_id")),
            highlight_value=_int_or_none(metadata.get("highlight_value")),
            path_node_ids=_int_list(metadata.get("search_path_node_ids")),
        )
        return VisualizationState(
            structure_name=structure_name,
            values=(),
            message=message,
            size=structure.size,
            event_type=step.event_type if step is not None else None,
            metadata=metadata,
            repair_pending=structure.repair_pending,
            multi_key_tree_nodes=nodes,
            multi_key_tree_edges=edges,
            tree_valid=structure.is_valid(),
            invalid_node_id=structure.invalid_node_id,
        )

    if isinstance(structure, Graph):
        highlight_vertices = _int_list(metadata.get("highlight_vertices"))
        highlight_edges = _edge_set(metadata.get("highlight_edges"))
        visited_vertices = _int_tuple(metadata.get("visited_vertices"))
        traversal_order = _int_tuple(metadata.get("traversal_order"))
        queue = _int_tuple(metadata.get("queue"))
        stack = _int_tuple(metadata.get("stack"))
        frontier = _str_or_none(metadata.get("frontier"))
        current_vertex = _int_or_none(metadata.get("current_vertex"))
        examined_edge = _edge_or_none(metadata.get("examined_edge"))
        shortest_path = _int_tuple(metadata.get("shortest_path"))
        distances = _distance_dict(metadata.get("distances"))
        priority_queue = _priority_queue(metadata.get("priority_queue"))
        predecessors = _predecessor_dict(metadata.get("predecessors"))
        current_component = _int_or_none(metadata.get("current_component"))
        current_component_vertices = _int_tuple(metadata.get("current_component_vertices"))
        completed_components = _components_tuple(metadata.get("completed_components"))
        components = _components_tuple(metadata.get("components"))
        component_count = _int_or_none(metadata.get("component_count"))
        component_by_vertex = _component_by_vertex(completed_components, current_component_vertices, current_component)
        traversal_path = _int_tuple(metadata.get("traversal_path"))
        cycle_vertices = _int_tuple(metadata.get("cycle_vertices"))
        cycle_edges = _edge_tuple(metadata.get("cycle_edges"))
        cycle_detected = metadata.get("cycle_detected") is True
        indegrees = _int_dict(metadata.get("indegrees"))
        zero_indegree_queue = _int_tuple(metadata.get("zero_indegree_queue"))
        processed_vertices = _int_tuple(metadata.get("processed_vertices"))
        topological_order = _int_tuple(metadata.get("topological_order"))
        topological_sort_possible = _bool_or_none(metadata.get("topological_sort_possible"))
        candidate_edges = _weighted_edge_tuple(metadata.get("candidate_edges"))
        mst_edges = _weighted_edge_tuple(metadata.get("mst_edges"))
        mst_edge_pairs = {(source, destination) for source, destination, _weight in mst_edges}
        mst_total_weight = _int_or_none(metadata.get("mst_total_weight"))
        mst_disconnected = metadata.get("mst_disconnected") is True
        nodes = tuple(
            VisualGraphNode(
                value=vertex,
                highlighted=vertex in highlight_vertices,
                visited=vertex in visited_vertices,
                current=vertex == current_vertex,
                path=vertex in shortest_path,
                component_id=component_by_vertex.get(vertex),
                cycle=vertex in cycle_vertices,
            )
            for vertex in structure.vertices()
        )
        edges = _graph_edges(structure, highlight_edges, mst_edge_pairs)
        return VisualizationState(
            structure_name=structure_name,
            values=(),
            message=message,
            size=structure.vertex_count(),
            event_type=step.event_type if step is not None else None,
            metadata=metadata,
            graph_type=structure.graph_type,
            graph_nodes=nodes,
            graph_edges=edges,
            adjacency=structure.adjacency_list(),
            current_vertex=current_vertex,
            queue=queue,
            stack=stack,
            frontier=frontier,
            visited_vertices=visited_vertices,
            traversal_order=traversal_order,
            examined_edge=examined_edge,
            distances=distances,
            priority_queue=priority_queue,
            predecessors=predecessors,
            shortest_path=shortest_path,
            current_component=current_component,
            current_component_vertices=current_component_vertices,
            completed_components=completed_components,
            component_count=component_count if component_count is not None else (len(components) if components else None),
            traversal_path=traversal_path,
            cycle_detected=cycle_detected,
            cycle_vertices=cycle_vertices,
            cycle_edges=cycle_edges,
            indegrees=indegrees,
            zero_indegree_queue=zero_indegree_queue,
            processed_vertices=processed_vertices,
            topological_order=topological_order,
            topological_sort_possible=topological_sort_possible,
            candidate_edges=candidate_edges,
            mst_edges=mst_edges,
            mst_total_weight=mst_total_weight,
            mst_disconnected=mst_disconnected,
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
    entry_indexes: set[int],
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
                highlighted=highlighted_bucket
                and (current_entry_index == entry_index or current_entry_index in entry_indexes),
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


def _range_or_none(value: object) -> tuple[int, int] | None:
    if (
        isinstance(value, tuple)
        and len(value) == 2
        and type(value[0]) is int
        and type(value[1]) is int
    ):
        return value
    return None


def _index_in_ranges(index: int, ranges: tuple[tuple[int, int], ...]) -> bool:
    return any(start <= index <= end for start, end in ranges)


def _shift_indexes(metadata: dict[str, object]) -> set[int]:
    indexes: set[int] = set()
    for key in ("from_index", "to_index", "insert_index", "current_position", "min_index"):
        value = metadata.get(key)
        if type(value) is int:
            indexes.add(value)
    return indexes


def _int_list(value: object) -> set[int]:
    if not isinstance(value, list):
        return set()
    return {item for item in value if type(item) is int}


def _int_tuple(value: object) -> tuple[int, ...]:
    if not isinstance(value, list):
        return ()
    return tuple(item for item in value if type(item) is int)


def _priority_queue(value: object) -> tuple[tuple[int, int], ...]:
    if not isinstance(value, list):
        return ()
    entries: list[tuple[int, int]] = []
    for item in value:
        if (
            isinstance(item, tuple)
            and len(item) == 2
            and type(item[0]) is int
            and type(item[1]) is int
        ):
            entries.append(item)
    return tuple(entries)


def _distance_dict(value: object) -> dict[int, int | None] | None:
    if not isinstance(value, dict):
        return None
    distances: dict[int, int | None] = {}
    for key, distance in value.items():
        if type(key) is int and (type(distance) is int or distance is None):
            distances[key] = distance
    return distances


def _predecessor_dict(value: object) -> dict[int, int | None] | None:
    if not isinstance(value, dict):
        return None
    predecessors: dict[int, int | None] = {}
    for key, predecessor in value.items():
        if type(key) is int and (type(predecessor) is int or predecessor is None):
            predecessors[key] = predecessor
    return predecessors


def _int_dict(value: object) -> dict[int, int] | None:
    if not isinstance(value, dict):
        return None
    result: dict[int, int] = {}
    for key, item in value.items():
        if type(key) is int and type(item) is int:
            result[key] = item
    return result


def _bool_or_none(value: object) -> bool | None:
    return value if type(value) is bool else None


def _components_tuple(value: object) -> tuple[tuple[int, ...], ...]:
    if not isinstance(value, list):
        return ()
    components: list[tuple[int, ...]] = []
    for component in value:
        if isinstance(component, list):
            vertices = tuple(vertex for vertex in component if type(vertex) is int)
            components.append(vertices)
    return tuple(components)


def _component_by_vertex(
    completed_components: tuple[tuple[int, ...], ...],
    current_component_vertices: tuple[int, ...],
    current_component: int | None,
) -> dict[int, int]:
    component_by_vertex: dict[int, int] = {}
    for index, component in enumerate(completed_components, start=1):
        for vertex in component:
            component_by_vertex[vertex] = index
    if current_component is not None:
        for vertex in current_component_vertices:
            component_by_vertex[vertex] = current_component
    return component_by_vertex


def _str_or_none(value: object) -> str | None:
    return value if isinstance(value, str) else None


def _step_metadata(step: Step | AlgorithmStep | None) -> dict[str, object]:
    if step is None:
        return {}
    if isinstance(step, AlgorithmStep):
        return step.state.metadata
    return step.metadata


def _edge_set(value: object) -> set[tuple[int, int]]:
    if not isinstance(value, list):
        return set()
    edges: set[tuple[int, int]] = set()
    for item in value:
        if (
            isinstance(item, tuple)
            and len(item) == 2
            and type(item[0]) is int
            and type(item[1]) is int
        ):
            edges.add(item)
    return edges


def _edge_tuple(value: object) -> tuple[tuple[int, int], ...]:
    if not isinstance(value, list):
        return ()
    edges: list[tuple[int, int]] = []
    for item in value:
        if (
            isinstance(item, tuple)
            and len(item) == 2
            and type(item[0]) is int
            and type(item[1]) is int
        ):
            edges.append(item)
    return tuple(edges)


def _weighted_edge_tuple(value: object) -> tuple[tuple[int, int, int], ...]:
    if not isinstance(value, list):
        return ()
    edges: list[tuple[int, int, int]] = []
    for item in value:
        if (
            isinstance(item, tuple)
            and len(item) == 3
            and type(item[0]) is int
            and type(item[1]) is int
            and type(item[2]) is int
        ):
            edges.append(item)
    return tuple(edges)


def _edge_or_none(value: object) -> tuple[int, int] | None:
    if (
        isinstance(value, tuple)
        and len(value) == 2
        and type(value[0]) is int
        and type(value[1]) is int
    ):
        return value
    return None


def _graph_edges(
    structure: Graph,
    highlight_edges: set[tuple[int, int]],
    mst_edges: set[tuple[int, int]] | None = None,
) -> tuple[VisualGraphEdge, ...]:
    edges: list[VisualGraphEdge] = []
    seen_undirected: set[frozenset[int]] = set()
    mst_edges = mst_edges or set()
    for source, neighbors in structure.adjacency_list().items():
        for destination, weight in neighbors:
            if not structure.directed:
                edge_key = frozenset({source, destination})
                if edge_key in seen_undirected:
                    continue
                seen_undirected.add(edge_key)
            edges.append(
                VisualGraphEdge(
                    source=source,
                    destination=destination,
                    weight=weight,
                    directed=structure.directed,
                    highlighted=(source, destination) in highlight_edges or (destination, source) in highlight_edges,
                    mst=(source, destination) in mst_edges or (destination, source) in mst_edges,
                )
            )
    return tuple(edges)


def _two_three_nodes_and_edges(
    snapshots: tuple[TwoThreeNodeSnapshot, ...],
    highlight_node_id: int | None,
    highlight_value: int | None,
    path_node_ids: set[int],
) -> tuple[tuple[VisualMultiKeyTreeNode, ...], tuple[tuple[int, int], ...]]:
    by_id = {snapshot.node_id: snapshot for snapshot in snapshots}
    depths = _two_three_depths(snapshots, by_id)
    ordered_ids = _two_three_ordered_ids(snapshots, by_id)
    order_by_id = {node_id: order for order, node_id in enumerate(ordered_ids)}
    nodes = tuple(
        VisualMultiKeyTreeNode(
            id=snapshot.node_id,
            keys=snapshot.keys,
            depth=depths.get(snapshot.node_id, 0),
            order=order_by_id.get(snapshot.node_id, 0),
            highlighted=snapshot.node_id == highlight_node_id or snapshot.node_id in path_node_ids,
            highlighted_key=highlight_value if highlight_value in snapshot.keys else None,
            overflowing=snapshot.overflowing,
        )
        for snapshot in snapshots
    )
    edges = tuple(
        (snapshot.node_id, child_id)
        for snapshot in snapshots
        for child_id in snapshot.child_ids
    )
    return nodes, edges


def _two_three_depths(
    snapshots: tuple[TwoThreeNodeSnapshot, ...],
    by_id: dict[int, TwoThreeNodeSnapshot],
) -> dict[int, int]:
    roots = [snapshot for snapshot in snapshots if snapshot.parent_id is None]
    if not roots:
        return {}
    depths: dict[int, int] = {}

    def visit(node_id: int, depth: int) -> None:
        depths[node_id] = depth
        for child_id in by_id[node_id].child_ids:
            visit(child_id, depth + 1)

    visit(roots[0].node_id, 0)
    return depths


def _two_three_ordered_ids(
    snapshots: tuple[TwoThreeNodeSnapshot, ...],
    by_id: dict[int, TwoThreeNodeSnapshot],
) -> list[int]:
    roots = [snapshot for snapshot in snapshots if snapshot.parent_id is None]
    if not roots:
        return []
    ordered: list[int] = []

    def visit(node_id: int) -> None:
        snapshot = by_id[node_id]
        if not snapshot.child_ids:
            ordered.append(node_id)
            return
        for index, child_id in enumerate(snapshot.child_ids):
            visit(child_id)
            if index < len(snapshot.keys):
                ordered.append(node_id)

    visit(roots[0].node_id)
    deduped: list[int] = []
    for node_id in ordered:
        if node_id not in deduped:
            deduped.append(node_id)
    return deduped
