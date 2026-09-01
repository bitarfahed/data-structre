"""Connected components over the undirected Graph domain model."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from data_structures_visual_lab.domain.algorithms.state import AlgorithmEventType, AlgorithmStep, make_algorithm_step
from data_structures_visual_lab.domain.data_structures import Graph


@dataclass(frozen=True)
class ConnectedComponentsResult:
    """Result of finding connected components."""

    ok: bool
    components: tuple[tuple[int, ...], ...]
    message: str
    steps: list[AlgorithmStep]


def connected_components(graph: Graph) -> ConnectedComponentsResult:
    """Find every connected component in an undirected graph."""
    if not isinstance(graph, Graph):
        return ConnectedComponentsResult(False, (), "Connected Components requires a Graph instance.", [])
    if graph.directed:
        return ConnectedComponentsResult(False, (), "Connected Components supports undirected graphs only.", [])
    if graph.vertex_count() == 0:
        message = "Connected Components complete. Component count: 0."
        step = _step(
            graph,
            AlgorithmEventType.COMPLETE,
            message,
            visited=(),
            current_component=0,
            current_component_vertices=(),
            completed_components=(),
            completed=True,
        )
        return ConnectedComponentsResult(True, (), message, [step])

    visited: set[int] = set()
    components: list[tuple[int, ...]] = []
    steps: list[AlgorithmStep] = []

    for start_vertex in graph.vertices():
        if start_vertex in visited:
            continue

        component_number = len(components) + 1
        current_component_vertices: list[int] = []
        queue = deque([start_vertex])
        visited.add(start_vertex)
        steps.append(
            _step(
                graph,
                AlgorithmEventType.VISIT,
                f"Start component {component_number} at vertex {start_vertex}.",
                current_vertex=start_vertex,
                visited=tuple(sorted(visited)),
                current_component=component_number,
                current_component_vertices=tuple(current_component_vertices),
                completed_components=tuple(components),
            )
        )

        while queue:
            current = queue.popleft()
            current_component_vertices.append(current)
            steps.append(
                _step(
                    graph,
                    AlgorithmEventType.VISIT,
                    f"Visit vertex {current} in component {component_number}.",
                    current_vertex=current,
                    visited=tuple(sorted(visited)),
                    current_component=component_number,
                    current_component_vertices=tuple(current_component_vertices),
                    completed_components=tuple(components),
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
                        visited=tuple(sorted(visited)),
                        current_component=component_number,
                        current_component_vertices=tuple(current_component_vertices),
                        completed_components=tuple(components),
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
                        f"Discovered vertex {neighbor} for component {component_number}.",
                        current_vertex=neighbor,
                        visited=tuple(sorted(visited)),
                        current_component=component_number,
                        current_component_vertices=tuple((*current_component_vertices, neighbor)),
                        completed_components=tuple(components),
                        examined_edge=examined_edge,
                    )
                )

        component = tuple(sorted(current_component_vertices))
        components.append(component)
        steps.append(
            _step(
                graph,
                AlgorithmEventType.COMPLETE,
                f"Completed component {component_number}: {list(component)}.",
                visited=tuple(sorted(visited)),
                current_component=component_number,
                current_component_vertices=component,
                completed_components=tuple(components),
            )
        )

    result_components = tuple(components)
    message = f"Connected Components complete. Component count: {len(result_components)}."
    steps.append(
        _step(
            graph,
            AlgorithmEventType.COMPLETE,
            message,
            visited=tuple(sorted(visited)),
            current_component=len(result_components),
            current_component_vertices=(),
            completed_components=result_components,
            completed=True,
        )
    )
    return ConnectedComponentsResult(True, result_components, message, steps)


def _step(
    graph: Graph,
    event_type: AlgorithmEventType,
    message: str,
    *,
    visited: tuple[int, ...],
    current_component: int,
    current_component_vertices: tuple[int, ...],
    completed_components: tuple[tuple[int, ...], ...],
    current_vertex: int | None = None,
    examined_edge: tuple[int, int] | None = None,
    completed: bool = False,
) -> AlgorithmStep:
    components = [list(component) for component in completed_components]
    highlight_vertices = list(current_component_vertices)
    if current_vertex is not None and current_vertex not in highlight_vertices:
        highlight_vertices.append(current_vertex)
    metadata = {
        "graph_type": graph.graph_type,
        "directed": graph.directed,
        "vertices": list(graph.vertices()),
        "adjacency": graph.adjacency_list(),
        "vertex_count": graph.vertex_count(),
        "edge_count": graph.edge_count(),
        "current_component": current_component,
        "current_vertex": current_vertex,
        "visited_vertices": list(visited),
        "current_component_vertices": list(current_component_vertices),
        "completed_components": components,
        "components": components,
        "component_count": len(completed_components),
        "highlight_vertices": highlight_vertices,
        "highlight_edges": [examined_edge] if examined_edge is not None else [],
        "examined_edge": examined_edge,
    }
    return make_algorithm_step(event_type, message, (), completed=completed, metadata=metadata)
