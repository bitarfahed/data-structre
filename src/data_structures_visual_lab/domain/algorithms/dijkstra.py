"""Dijkstra shortest paths over the Graph domain model."""

from __future__ import annotations

from dataclasses import dataclass
from heapq import heappop, heappush
from math import inf

from data_structures_visual_lab.domain.algorithms.state import AlgorithmEventType, AlgorithmStep, make_algorithm_step
from data_structures_visual_lab.domain.data_structures import Graph


@dataclass(frozen=True)
class DijkstraResult:
    """Result of running Dijkstra from one start vertex."""

    ok: bool
    distances: dict[int, int | None]
    path: tuple[int, ...]
    message: str
    steps: list[AlgorithmStep]


def dijkstra(graph: Graph, start_vertex: int, target_vertex: int | None = None) -> DijkstraResult:
    """Compute shortest distances from a start vertex using Dijkstra."""
    if not isinstance(graph, Graph):
        return DijkstraResult(False, {}, (), "Dijkstra requires a Graph instance.", [])
    if type(start_vertex) is not int:
        return DijkstraResult(False, {}, (), "Start vertex must be an integer.", [])
    if target_vertex is not None and type(target_vertex) is not int:
        return DijkstraResult(False, {}, (), "Target vertex must be an integer.", [])
    if graph.vertex_count() == 0:
        return DijkstraResult(False, {}, (), "Dijkstra skipped because the graph is empty.", [])
    if not graph.has_vertex(start_vertex):
        return DijkstraResult(False, {}, (), f"Dijkstra start vertex {start_vertex} does not exist.", [])
    if target_vertex is not None and not graph.has_vertex(target_vertex):
        return DijkstraResult(False, {}, (), f"Dijkstra target vertex {target_vertex} does not exist.", [])
    if not _has_only_non_negative_weights(graph):
        return DijkstraResult(False, {}, (), "Dijkstra requires non-negative edge weights.", [])

    distances: dict[int, float] = {vertex: inf for vertex in graph.vertices()}
    predecessors: dict[int, int | None] = {vertex: None for vertex in graph.vertices()}
    finalized: set[int] = set()
    priority_queue: list[tuple[int, int]] = [(0, start_vertex)]
    distances[start_vertex] = 0

    steps = [
        _step(
            graph,
            AlgorithmEventType.VISIT,
            f"Start Dijkstra at vertex {start_vertex}.",
            distances=distances,
            predecessors=predecessors,
            priority_queue=priority_queue,
            finalized=finalized,
            current_vertex=start_vertex,
        )
    ]

    while priority_queue:
        current_distance, current_vertex = heappop(priority_queue)
        if current_vertex in finalized or current_distance != distances[current_vertex]:
            continue

        finalized.add(current_vertex)
        steps.append(
            _step(
                graph,
                AlgorithmEventType.VISIT,
                f"Finalize vertex {current_vertex} with distance {current_distance}.",
                distances=distances,
                predecessors=predecessors,
                priority_queue=priority_queue,
                finalized=finalized,
                current_vertex=current_vertex,
            )
        )

        if target_vertex is not None and current_vertex == target_vertex:
            break

        for neighbor, weight in graph.neighbors(current_vertex):
            examined_edge = (current_vertex, neighbor)
            candidate_distance = current_distance + weight
            old_distance = distances[neighbor]
            steps.append(
                _step(
                    graph,
                    AlgorithmEventType.COMPARE,
                    f"Relax edge {current_vertex} -> {neighbor} with weight {weight}.",
                    distances=distances,
                    predecessors=predecessors,
                    priority_queue=priority_queue,
                    finalized=finalized,
                    current_vertex=current_vertex,
                    examined_edge=examined_edge,
                    updated_vertex=neighbor,
                    old_distance=old_distance,
                    new_distance=candidate_distance,
                )
            )

            if neighbor not in finalized and candidate_distance < distances[neighbor]:
                distances[neighbor] = candidate_distance
                predecessors[neighbor] = current_vertex
                heappush(priority_queue, (candidate_distance, neighbor))
                steps.append(
                    _step(
                        graph,
                        AlgorithmEventType.MOVE,
                        f"Update vertex {neighbor}: distance becomes {candidate_distance}.",
                        distances=distances,
                        predecessors=predecessors,
                        priority_queue=priority_queue,
                        finalized=finalized,
                        current_vertex=neighbor,
                        examined_edge=examined_edge,
                        updated_vertex=neighbor,
                        old_distance=old_distance,
                        new_distance=candidate_distance,
                        distance_updated=True,
                    )
                )

    result_distances = _public_distances(distances)
    path = _reconstruct_path(predecessors, start_vertex, target_vertex, distances) if target_vertex is not None else ()
    message = _complete_message(start_vertex, target_vertex, result_distances, path)
    steps.append(
        _step(
            graph,
            AlgorithmEventType.COMPLETE,
            message,
            distances=distances,
            predecessors=predecessors,
            priority_queue=priority_queue,
            finalized=finalized,
            shortest_path=path,
            completed=True,
        )
    )
    return DijkstraResult(True, result_distances, path, message, steps)


def _has_only_non_negative_weights(graph: Graph) -> bool:
    return all(weight >= 0 for neighbors in graph.adjacency_list().values() for _neighbor, weight in neighbors)


def _public_distances(distances: dict[int, float]) -> dict[int, int | None]:
    return {vertex: (None if distance == inf else int(distance)) for vertex, distance in distances.items()}


def _public_predecessors(predecessors: dict[int, int | None]) -> dict[int, int | None]:
    return dict(predecessors)


def _public_priority_queue(priority_queue: list[tuple[int, int]]) -> list[tuple[int, int]]:
    return sorted(priority_queue)


def _public_distance(value: float) -> int | None:
    return None if value == inf else int(value)


def _reconstruct_path(
    predecessors: dict[int, int | None],
    start_vertex: int,
    target_vertex: int | None,
    distances: dict[int, float],
) -> tuple[int, ...]:
    if target_vertex is None or distances[target_vertex] == inf:
        return ()

    path: list[int] = []
    current: int | None = target_vertex
    while current is not None:
        path.append(current)
        if current == start_vertex:
            break
        current = predecessors[current]
    path.reverse()
    return tuple(path)


def _complete_message(
    start_vertex: int,
    target_vertex: int | None,
    distances: dict[int, int | None],
    path: tuple[int, ...],
) -> str:
    if target_vertex is None:
        return f"Dijkstra complete from {start_vertex}. Distances: {distances}."
    if not path:
        return f"Dijkstra complete. No path from {start_vertex} to {target_vertex}."
    return f"Dijkstra complete. Shortest path to {target_vertex}: {list(path)} with distance {distances[target_vertex]}."


def _step(
    graph: Graph,
    event_type: AlgorithmEventType,
    message: str,
    *,
    distances: dict[int, float],
    predecessors: dict[int, int | None],
    priority_queue: list[tuple[int, int]],
    finalized: set[int],
    current_vertex: int | None = None,
    examined_edge: tuple[int, int] | None = None,
    updated_vertex: int | None = None,
    old_distance: float | None = None,
    new_distance: float | None = None,
    distance_updated: bool = False,
    shortest_path: tuple[int, ...] = (),
    completed: bool = False,
) -> AlgorithmStep:
    path_edges = list(zip(shortest_path, shortest_path[1:]))
    highlight_vertices = [vertex for vertex in (current_vertex, updated_vertex) if vertex is not None]
    highlight_vertices.extend(shortest_path)
    highlight_edges = [examined_edge] if examined_edge is not None else []
    highlight_edges.extend(path_edges)
    metadata = {
        "graph_type": graph.graph_type,
        "directed": graph.directed,
        "vertices": list(graph.vertices()),
        "adjacency": graph.adjacency_list(),
        "vertex_count": graph.vertex_count(),
        "edge_count": graph.edge_count(),
        "current_vertex": current_vertex,
        "distances": _public_distances(distances),
        "priority_queue": _public_priority_queue(priority_queue),
        "predecessors": _public_predecessors(predecessors),
        "finalized_vertices": sorted(finalized),
        "visited_vertices": sorted(finalized),
        "highlight_vertices": highlight_vertices,
        "highlight_edges": highlight_edges,
        "examined_edge": examined_edge,
        "updated_vertex": updated_vertex,
        "old_distance": _public_distance(old_distance) if old_distance is not None else None,
        "new_distance": _public_distance(new_distance) if new_distance is not None else None,
        "distance_updated": distance_updated,
        "shortest_path": list(shortest_path),
    }
    return make_algorithm_step(
        event_type,
        message,
        (),
        completed=completed,
        metadata=metadata,
    )
