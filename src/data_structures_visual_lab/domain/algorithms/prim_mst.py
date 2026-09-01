"""Prim's minimum spanning tree over the Graph domain model."""

from __future__ import annotations

from dataclasses import dataclass
from heapq import heappop, heappush

from data_structures_visual_lab.domain.algorithms.state import AlgorithmEventType, AlgorithmStep, make_algorithm_step
from data_structures_visual_lab.domain.data_structures import Graph


@dataclass(frozen=True)
class PrimMSTResult:
    """Result of running Prim's MST algorithm."""

    ok: bool
    edges: tuple[tuple[int, int, int], ...]
    total_weight: int
    message: str
    steps: list[AlgorithmStep]


def prim_mst(graph: Graph, start_vertex: int) -> PrimMSTResult:
    """Build an MST from a start vertex using Prim's algorithm."""
    if not isinstance(graph, Graph):
        return PrimMSTResult(False, (), 0, "Prim's MST requires a Graph instance.", [])
    if graph.directed:
        return PrimMSTResult(False, (), 0, "Prim's MST supports undirected graphs only.", [])
    if type(start_vertex) is not int:
        return PrimMSTResult(False, (), 0, "Start vertex must be an integer.", [])
    if graph.vertex_count() == 0:
        return PrimMSTResult(False, (), 0, "Prim's MST skipped because the graph is empty.", [])
    if not graph.has_vertex(start_vertex):
        return PrimMSTResult(False, (), 0, f"Prim's MST start vertex {start_vertex} does not exist.", [])
    if not _has_only_non_negative_weights(graph):
        return PrimMSTResult(False, (), 0, "Prim's MST requires non-negative edge weights.", [])

    included = {start_vertex}
    mst_edges: list[tuple[int, int, int]] = []
    priority_queue: list[tuple[int, int, int]] = []
    total_weight = 0

    for neighbor, weight in graph.neighbors(start_vertex):
        heappush(priority_queue, (weight, start_vertex, neighbor))

    steps = [
        _step(
            graph,
            AlgorithmEventType.VISIT,
            f"Start Prim's MST at vertex {start_vertex}.",
            included=included,
            priority_queue=priority_queue,
            mst_edges=mst_edges,
            current_vertex=start_vertex,
            total_weight=total_weight,
        )
    ]

    while priority_queue and len(included) < graph.vertex_count():
        weight, source, destination = heappop(priority_queue)
        examined_edge = (source, destination)
        steps.append(
            _step(
                graph,
                AlgorithmEventType.COMPARE,
                f"Consider edge {source} -> {destination} with weight {weight}.",
                included=included,
                priority_queue=priority_queue,
                mst_edges=mst_edges,
                current_vertex=source,
                examined_edge=examined_edge,
                total_weight=total_weight,
            )
        )

        if destination in included:
            steps.append(
                _step(
                    graph,
                    AlgorithmEventType.COMPARE,
                    f"Reject edge {source} -> {destination} because vertex {destination} is already included.",
                    included=included,
                    priority_queue=priority_queue,
                    mst_edges=mst_edges,
                    current_vertex=destination,
                    examined_edge=examined_edge,
                    rejected_edge=examined_edge,
                    total_weight=total_weight,
                )
            )
            continue

        included.add(destination)
        mst_edges.append((source, destination, weight))
        total_weight += weight
        steps.append(
            _step(
                graph,
                AlgorithmEventType.MOVE,
                f"Select edge {source} -> {destination}; total weight is now {total_weight}.",
                included=included,
                priority_queue=priority_queue,
                mst_edges=mst_edges,
                current_vertex=destination,
                examined_edge=examined_edge,
                selected_edge=examined_edge,
                total_weight=total_weight,
            )
        )

        for neighbor, neighbor_weight in graph.neighbors(destination):
            if neighbor not in included:
                heappush(priority_queue, (neighbor_weight, destination, neighbor))
        steps.append(
            _step(
                graph,
                AlgorithmEventType.VISIT,
                f"Add candidate edges from vertex {destination}.",
                included=included,
                priority_queue=priority_queue,
                mst_edges=mst_edges,
                current_vertex=destination,
                total_weight=total_weight,
            )
        )

    edges = tuple(mst_edges)
    if len(included) != graph.vertex_count():
        message = "Prim's MST incomplete: graph is disconnected; no spanning tree covers all vertices."
        steps.append(
            _step(
                graph,
                AlgorithmEventType.COMPLETE,
                message,
                included=included,
                priority_queue=priority_queue,
                mst_edges=mst_edges,
                total_weight=total_weight,
                disconnected=True,
                completed=True,
            )
        )
        return PrimMSTResult(False, edges, total_weight, message, steps)

    message = f"Prim's MST complete. Total weight: {total_weight}."
    steps.append(
        _step(
            graph,
            AlgorithmEventType.COMPLETE,
            message,
            included=included,
            priority_queue=priority_queue,
            mst_edges=mst_edges,
            total_weight=total_weight,
            completed=True,
        )
    )
    return PrimMSTResult(True, edges, total_weight, message, steps)


def _has_only_non_negative_weights(graph: Graph) -> bool:
    return all(weight >= 0 for neighbors in graph.adjacency_list().values() for _neighbor, weight in neighbors)


def _step(
    graph: Graph,
    event_type: AlgorithmEventType,
    message: str,
    *,
    included: set[int],
    priority_queue: list[tuple[int, int, int]],
    mst_edges: list[tuple[int, int, int]],
    total_weight: int,
    current_vertex: int | None = None,
    examined_edge: tuple[int, int] | None = None,
    selected_edge: tuple[int, int] | None = None,
    rejected_edge: tuple[int, int] | None = None,
    disconnected: bool = False,
    completed: bool = False,
) -> AlgorithmStep:
    highlight_vertices = [current_vertex] if current_vertex is not None else []
    if examined_edge is not None:
        highlight_vertices.extend(examined_edge)

    highlight_edges = []
    if selected_edge is not None:
        highlight_edges.append(selected_edge)
    elif rejected_edge is not None:
        highlight_edges.append(rejected_edge)
    elif examined_edge is not None:
        highlight_edges.append(examined_edge)

    metadata = {
        "graph_type": graph.graph_type,
        "directed": graph.directed,
        "vertices": list(graph.vertices()),
        "adjacency": graph.adjacency_list(),
        "vertex_count": graph.vertex_count(),
        "edge_count": graph.edge_count(),
        "current_vertex": current_vertex,
        "visited_vertices": sorted(included),
        "included_vertices": sorted(included),
        "candidate_edges": _public_priority_queue(priority_queue),
        "mst_edges": list(mst_edges),
        "mst_total_weight": total_weight,
        "mst_disconnected": disconnected,
        "highlight_vertices": highlight_vertices,
        "highlight_edges": highlight_edges,
        "examined_edge": examined_edge,
        "selected_edge": selected_edge,
        "rejected_edge": rejected_edge,
    }
    return make_algorithm_step(event_type, message, (), completed=completed, metadata=metadata)


def _public_priority_queue(priority_queue: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    return sorted(priority_queue)
