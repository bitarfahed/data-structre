"""Topological sort over the directed Graph domain model."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from data_structures_visual_lab.domain.algorithms.state import AlgorithmEventType, AlgorithmStep, make_algorithm_step
from data_structures_visual_lab.domain.data_structures import Graph


@dataclass(frozen=True)
class TopologicalSortResult:
    """Result of running topological sort."""

    ok: bool
    order: tuple[int, ...]
    message: str
    steps: list[AlgorithmStep]


def topological_sort(graph: Graph) -> TopologicalSortResult:
    """Return one valid topological ordering for a directed acyclic graph."""
    if not isinstance(graph, Graph):
        return TopologicalSortResult(False, (), "Topological Sort requires a Graph instance.", [])
    if not graph.directed:
        return TopologicalSortResult(False, (), "Topological Sort supports directed graphs only.", [])
    if graph.vertex_count() == 0:
        message = "Topological Sort complete. Order: []."
        step = _step(
            graph,
            AlgorithmEventType.COMPLETE,
            message,
            indegrees={},
            zero_indegree_queue=(),
            processed=(),
            order=(),
            completed=True,
        )
        return TopologicalSortResult(True, (), message, [step])

    indegrees = _initial_indegrees(graph)
    zero_indegree_queue = deque(vertex for vertex in graph.vertices() if indegrees[vertex] == 0)
    processed: list[int] = []
    steps = [
        _step(
            graph,
            AlgorithmEventType.VISIT,
            "Initialize indegrees and zero-indegree queue.",
            indegrees=indegrees,
            zero_indegree_queue=tuple(zero_indegree_queue),
            processed=tuple(processed),
            order=tuple(processed),
        )
    ]

    while zero_indegree_queue:
        current = zero_indegree_queue.popleft()
        processed.append(current)
        steps.append(
            _step(
                graph,
                AlgorithmEventType.MOVE,
                f"Select vertex {current}; append it to the topological order.",
                indegrees=indegrees,
                zero_indegree_queue=tuple(zero_indegree_queue),
                processed=tuple(processed),
                order=tuple(processed),
                current_vertex=current,
            )
        )

        for neighbor, _weight in graph.neighbors(current):
            examined_edge = (current, neighbor)
            steps.append(
                _step(
                    graph,
                    AlgorithmEventType.COMPARE,
                    f"Remove edge {current} -> {neighbor}; decrement indegree for {neighbor}.",
                    indegrees=indegrees,
                    zero_indegree_queue=tuple(zero_indegree_queue),
                    processed=tuple(processed),
                    order=tuple(processed),
                    current_vertex=current,
                    examined_edge=examined_edge,
                    updated_vertex=neighbor,
                )
            )
            indegrees[neighbor] -= 1
            if indegrees[neighbor] == 0:
                zero_indegree_queue.append(neighbor)
                steps.append(
                    _step(
                        graph,
                        AlgorithmEventType.MOVE,
                        f"Vertex {neighbor} now has indegree 0; add it to the queue.",
                        indegrees=indegrees,
                        zero_indegree_queue=tuple(zero_indegree_queue),
                        processed=tuple(processed),
                        order=tuple(processed),
                        current_vertex=neighbor,
                        examined_edge=examined_edge,
                        updated_vertex=neighbor,
                    )
                )

    if len(processed) != graph.vertex_count():
        message = "Topological sort impossible: cycle detected."
        steps.append(
            _step(
                graph,
                AlgorithmEventType.COMPLETE,
                message,
                indegrees=indegrees,
                zero_indegree_queue=(),
                processed=tuple(processed),
                order=tuple(processed),
                cycle_detected=True,
                completed=True,
            )
        )
        return TopologicalSortResult(False, (), message, steps)

    order = tuple(processed)
    message = f"Topological Sort complete. Order: {list(order)}."
    steps.append(
        _step(
            graph,
            AlgorithmEventType.COMPLETE,
            message,
            indegrees=indegrees,
            zero_indegree_queue=(),
            processed=order,
            order=order,
            completed=True,
        )
    )
    return TopologicalSortResult(True, order, message, steps)


def _initial_indegrees(graph: Graph) -> dict[int, int]:
    indegrees = {vertex: 0 for vertex in graph.vertices()}
    for source in graph.vertices():
        for destination, _weight in graph.neighbors(source):
            indegrees[destination] += 1
    return indegrees


def _step(
    graph: Graph,
    event_type: AlgorithmEventType,
    message: str,
    *,
    indegrees: dict[int, int],
    zero_indegree_queue: tuple[int, ...],
    processed: tuple[int, ...],
    order: tuple[int, ...],
    current_vertex: int | None = None,
    examined_edge: tuple[int, int] | None = None,
    updated_vertex: int | None = None,
    cycle_detected: bool = False,
    completed: bool = False,
) -> AlgorithmStep:
    highlight_vertices = [vertex for vertex in (current_vertex, updated_vertex) if vertex is not None]
    metadata = {
        "graph_type": graph.graph_type,
        "directed": graph.directed,
        "vertices": list(graph.vertices()),
        "adjacency": graph.adjacency_list(),
        "vertex_count": graph.vertex_count(),
        "edge_count": graph.edge_count(),
        "current_vertex": current_vertex,
        "visited_vertices": list(processed),
        "processed_vertices": list(processed),
        "topological_order": list(order),
        "indegrees": dict(indegrees),
        "zero_indegree_queue": list(zero_indegree_queue),
        "highlight_vertices": highlight_vertices,
        "highlight_edges": [examined_edge] if examined_edge is not None else [],
        "examined_edge": examined_edge,
        "updated_vertex": updated_vertex,
        "cycle_detected": cycle_detected,
        "topological_sort_possible": not cycle_detected,
    }
    return make_algorithm_step(event_type, message, (), completed=completed, metadata=metadata)
