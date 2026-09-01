"""Cycle detection over the Graph domain model."""

from __future__ import annotations

from dataclasses import dataclass

from data_structures_visual_lab.domain.algorithms.state import AlgorithmEventType, AlgorithmStep, make_algorithm_step
from data_structures_visual_lab.domain.data_structures import Graph


@dataclass(frozen=True)
class CycleDetectionResult:
    """Result of detecting a cycle in a graph."""

    ok: bool
    has_cycle: bool
    cycle_vertices: tuple[int, ...]
    cycle_edges: tuple[tuple[int, int], ...]
    message: str
    steps: list[AlgorithmStep]


def detect_cycle(graph: Graph) -> CycleDetectionResult:
    """Detect whether a directed or undirected graph contains a cycle."""
    if not isinstance(graph, Graph):
        return CycleDetectionResult(False, False, (), (), "Cycle Detection requires a Graph instance.", [])
    if graph.vertex_count() == 0:
        message = "Cycle Detection complete. No cycle found."
        step = _step(
            graph,
            AlgorithmEventType.COMPLETE,
            message,
            visited=(),
            traversal_path=(),
            completed=True,
        )
        return CycleDetectionResult(True, False, (), (), message, [step])
    if graph.directed:
        return _detect_directed_cycle(graph)
    return _detect_undirected_cycle(graph)


def _detect_undirected_cycle(graph: Graph) -> CycleDetectionResult:
    visited: set[int] = set()
    traversal_path: list[int] = []
    steps: list[AlgorithmStep] = []

    def visit(vertex: int, parent: int | None) -> tuple[tuple[int, ...], tuple[tuple[int, int], ...]] | None:
        visited.add(vertex)
        traversal_path.append(vertex)
        steps.append(
            _step(
                graph,
                AlgorithmEventType.VISIT,
                f"Visit vertex {vertex}.",
                current_vertex=vertex,
                visited=tuple(sorted(visited)),
                traversal_path=tuple(traversal_path),
            )
        )

        for neighbor, _weight in graph.neighbors(vertex):
            examined_edge = (vertex, neighbor)
            steps.append(
                _step(
                    graph,
                    AlgorithmEventType.COMPARE,
                    f"Examine edge {vertex} -> {neighbor}.",
                    current_vertex=vertex,
                    visited=tuple(sorted(visited)),
                    traversal_path=tuple(traversal_path),
                    examined_edge=examined_edge,
                )
            )
            if neighbor == parent:
                continue
            if neighbor in visited:
                cycle_vertices = _cycle_vertices_from_path(traversal_path, neighbor)
                cycle_edges = _cycle_edges(cycle_vertices)
                steps.append(
                    _step(
                        graph,
                        AlgorithmEventType.FOUND,
                        f"Cycle detected: {list(cycle_vertices)}.",
                        current_vertex=vertex,
                        visited=tuple(sorted(visited)),
                        traversal_path=tuple(traversal_path),
                        examined_edge=examined_edge,
                        cycle_vertices=cycle_vertices,
                        cycle_edges=cycle_edges,
                        cycle_detected=True,
                    )
                )
                return cycle_vertices, cycle_edges

            result = visit(neighbor, vertex)
            if result is not None:
                return result

        traversal_path.pop()
        return None

    for vertex in graph.vertices():
        if vertex in visited:
            continue
        steps.append(
            _step(
                graph,
                AlgorithmEventType.VISIT,
                f"Start cycle search at vertex {vertex}.",
                current_vertex=vertex,
                visited=tuple(sorted(visited)),
                traversal_path=tuple(traversal_path),
            )
        )
        result = visit(vertex, None)
        if result is not None:
            cycle_vertices, cycle_edges = result
            message = f"Cycle Detection complete. Cycle found: {list(cycle_vertices)}."
            steps.append(
                _step(
                    graph,
                    AlgorithmEventType.COMPLETE,
                    message,
                    visited=tuple(sorted(visited)),
                    traversal_path=tuple(traversal_path),
                    cycle_vertices=cycle_vertices,
                    cycle_edges=cycle_edges,
                    cycle_detected=True,
                    completed=True,
                )
            )
            return CycleDetectionResult(True, True, cycle_vertices, cycle_edges, message, steps)

    message = "Cycle Detection complete. No cycle found."
    steps.append(
        _step(
            graph,
            AlgorithmEventType.COMPLETE,
            message,
            visited=tuple(sorted(visited)),
            traversal_path=(),
            completed=True,
        )
    )
    return CycleDetectionResult(True, False, (), (), message, steps)


def _detect_directed_cycle(graph: Graph) -> CycleDetectionResult:
    state: dict[int, str] = {vertex: "unvisited" for vertex in graph.vertices()}
    traversal_path: list[int] = []
    steps: list[AlgorithmStep] = []

    def visit(vertex: int) -> tuple[tuple[int, ...], tuple[tuple[int, int], ...]] | None:
        state[vertex] = "visiting"
        traversal_path.append(vertex)
        steps.append(
            _step(
                graph,
                AlgorithmEventType.VISIT,
                f"Visit vertex {vertex}.",
                current_vertex=vertex,
                visited=_visited_from_state(state),
                traversal_path=tuple(traversal_path),
                vertex_states=state,
            )
        )

        for neighbor, _weight in graph.neighbors(vertex):
            examined_edge = (vertex, neighbor)
            steps.append(
                _step(
                    graph,
                    AlgorithmEventType.COMPARE,
                    f"Examine edge {vertex} -> {neighbor}.",
                    current_vertex=vertex,
                    visited=_visited_from_state(state),
                    traversal_path=tuple(traversal_path),
                    examined_edge=examined_edge,
                    vertex_states=state,
                )
            )
            if state[neighbor] == "visiting":
                cycle_vertices = _cycle_vertices_from_path(traversal_path, neighbor)
                cycle_edges = _cycle_edges(cycle_vertices)
                steps.append(
                    _step(
                        graph,
                        AlgorithmEventType.FOUND,
                        f"Cycle detected: {list(cycle_vertices)}.",
                        current_vertex=vertex,
                        visited=_visited_from_state(state),
                        traversal_path=tuple(traversal_path),
                        examined_edge=examined_edge,
                        cycle_vertices=cycle_vertices,
                        cycle_edges=cycle_edges,
                        cycle_detected=True,
                        vertex_states=state,
                    )
                )
                return cycle_vertices, cycle_edges
            if state[neighbor] == "unvisited":
                result = visit(neighbor)
                if result is not None:
                    return result

        state[vertex] = "done"
        traversal_path.pop()
        return None

    for vertex in graph.vertices():
        if state[vertex] != "unvisited":
            continue
        steps.append(
            _step(
                graph,
                AlgorithmEventType.VISIT,
                f"Start cycle search at vertex {vertex}.",
                current_vertex=vertex,
                visited=_visited_from_state(state),
                traversal_path=tuple(traversal_path),
                vertex_states=state,
            )
        )
        result = visit(vertex)
        if result is not None:
            cycle_vertices, cycle_edges = result
            message = f"Cycle Detection complete. Cycle found: {list(cycle_vertices)}."
            steps.append(
                _step(
                    graph,
                    AlgorithmEventType.COMPLETE,
                    message,
                    visited=_visited_from_state(state),
                    traversal_path=tuple(traversal_path),
                    cycle_vertices=cycle_vertices,
                    cycle_edges=cycle_edges,
                    cycle_detected=True,
                    vertex_states=state,
                    completed=True,
                )
            )
            return CycleDetectionResult(True, True, cycle_vertices, cycle_edges, message, steps)

    message = "Cycle Detection complete. No cycle found."
    steps.append(
        _step(
            graph,
            AlgorithmEventType.COMPLETE,
            message,
            visited=_visited_from_state(state),
            traversal_path=(),
            vertex_states=state,
            completed=True,
        )
    )
    return CycleDetectionResult(True, False, (), (), message, steps)


def _visited_from_state(state: dict[int, str]) -> tuple[int, ...]:
    return tuple(sorted(vertex for vertex, vertex_state in state.items() if vertex_state != "unvisited"))


def _cycle_vertices_from_path(traversal_path: list[int], repeated_vertex: int) -> tuple[int, ...]:
    cycle_start = traversal_path.index(repeated_vertex)
    return tuple((*traversal_path[cycle_start:], repeated_vertex))


def _cycle_edges(cycle_vertices: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    return tuple(zip(cycle_vertices, cycle_vertices[1:]))


def _step(
    graph: Graph,
    event_type: AlgorithmEventType,
    message: str,
    *,
    visited: tuple[int, ...],
    traversal_path: tuple[int, ...],
    current_vertex: int | None = None,
    examined_edge: tuple[int, int] | None = None,
    cycle_detected: bool = False,
    cycle_vertices: tuple[int, ...] = (),
    cycle_edges: tuple[tuple[int, int], ...] = (),
    vertex_states: dict[int, str] | None = None,
    completed: bool = False,
) -> AlgorithmStep:
    highlight_vertices = list(traversal_path)
    highlight_vertices.extend(cycle_vertices)
    if current_vertex is not None and current_vertex not in highlight_vertices:
        highlight_vertices.append(current_vertex)
    highlight_edges = [examined_edge] if examined_edge is not None else []
    highlight_edges.extend(cycle_edges)
    metadata = {
        "graph_type": graph.graph_type,
        "directed": graph.directed,
        "vertices": list(graph.vertices()),
        "adjacency": graph.adjacency_list(),
        "vertex_count": graph.vertex_count(),
        "edge_count": graph.edge_count(),
        "current_vertex": current_vertex,
        "visited_vertices": list(visited),
        "traversal_path": list(traversal_path),
        "cycle_detected": cycle_detected,
        "cycle_vertices": list(cycle_vertices),
        "cycle_edges": list(cycle_edges),
        "highlight_vertices": highlight_vertices,
        "highlight_edges": highlight_edges,
        "examined_edge": examined_edge,
        "vertex_states": dict(vertex_states) if vertex_states is not None else {},
    }
    return make_algorithm_step(event_type, message, (), completed=completed, metadata=metadata)
