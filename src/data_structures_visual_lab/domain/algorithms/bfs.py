"""Breadth-first search over the Graph domain model."""

from __future__ import annotations

from dataclasses import dataclass
from collections import deque

from data_structures_visual_lab.domain.algorithms.state import AlgorithmEventType, AlgorithmStep, make_algorithm_step
from data_structures_visual_lab.domain.data_structures import Graph


@dataclass(frozen=True)
class BFSResult:
    """Result of running BFS."""

    ok: bool
    order: tuple[int, ...]
    message: str
    steps: list[AlgorithmStep]


def bfs(graph: Graph, start_vertex: int) -> BFSResult:
    """Run queue-based BFS from a start vertex."""
    if not isinstance(graph, Graph):
        return BFSResult(False, (), "BFS requires a Graph instance.", [])
    if type(start_vertex) is not int:
        return BFSResult(False, (), "Start vertex must be an integer.", [])
    if graph.vertex_count() == 0:
        return BFSResult(False, (), "BFS skipped because the graph is empty.", [])
    if not graph.has_vertex(start_vertex):
        return BFSResult(False, (), f"BFS start vertex {start_vertex} does not exist.", [])

    visited: set[int] = {start_vertex}
    order: list[int] = []
    queue: deque[int] = deque([start_vertex])
    steps = [
        _step(
            graph,
            AlgorithmEventType.VISIT,
            f"Start BFS at vertex {start_vertex}.",
            current_vertex=start_vertex,
            queue=tuple(queue),
            visited=tuple(sorted(visited)),
            traversal_order=tuple(order),
        )
    ]

    while queue:
        current = queue.popleft()
        order.append(current)
        steps.append(
            _step(
                graph,
                AlgorithmEventType.VISIT,
                f"Visit vertex {current}.",
                current_vertex=current,
                queue=tuple(queue),
                visited=tuple(sorted(visited)),
                traversal_order=tuple(order),
            )
        )

        for neighbor, _weight in graph.neighbors(current):
            examined_edge = (current, neighbor)
            steps.append(
                _step(
                    graph,
                    AlgorithmEventType.COMPARE,
                    f"Examine edge {current} -> {neighbor}.",
                    current_vertex=current,
                    queue=tuple(queue),
                    visited=tuple(sorted(visited)),
                    traversal_order=tuple(order),
                    examined_edge=examined_edge,
                )
            )
            if neighbor in visited:
                continue

            visited.add(neighbor)
            queue.append(neighbor)
            steps.append(
                _step(
                    graph,
                    AlgorithmEventType.MOVE,
                    f"Discovered vertex {neighbor}; enqueue it.",
                    current_vertex=neighbor,
                    queue=tuple(queue),
                    visited=tuple(sorted(visited)),
                    traversal_order=tuple(order),
                    examined_edge=examined_edge,
                )
            )

    message = f"BFS complete. Traversal order: {order}."
    steps.append(
        _step(
            graph,
            AlgorithmEventType.COMPLETE,
            message,
            queue=(),
            visited=tuple(sorted(visited)),
            traversal_order=tuple(order),
            completed=True,
        )
    )
    return BFSResult(True, tuple(order), message, steps)


def _step(
    graph: Graph,
    event_type: AlgorithmEventType,
    message: str,
    *,
    current_vertex: int | None = None,
    queue: tuple[int, ...],
    visited: tuple[int, ...],
    traversal_order: tuple[int, ...],
    examined_edge: tuple[int, int] | None = None,
    completed: bool = False,
) -> AlgorithmStep:
    metadata = {
        "graph_type": graph.graph_type,
        "directed": graph.directed,
        "vertices": list(graph.vertices()),
        "adjacency": graph.adjacency_list(),
        "vertex_count": graph.vertex_count(),
        "edge_count": graph.edge_count(),
        "current_vertex": current_vertex,
        "queue": list(queue),
        "visited_vertices": list(visited),
        "traversal_order": list(traversal_order),
        "highlight_vertices": [current_vertex] if current_vertex is not None else [],
        "highlight_edges": [examined_edge] if examined_edge is not None else [],
        "examined_edge": examined_edge,
    }
    return make_algorithm_step(
        event_type,
        message,
        (),
        completed=completed,
        metadata=metadata,
    )
