"""Kruskal's minimum spanning tree over the Graph domain model."""

from __future__ import annotations

from dataclasses import dataclass

from data_structures_visual_lab.domain.algorithms.state import AlgorithmEventType, AlgorithmStep, make_algorithm_step
from data_structures_visual_lab.domain.data_structures import Graph


@dataclass(frozen=True)
class KruskalMSTResult:
    """Result of running Kruskal's MST algorithm."""

    ok: bool
    edges: tuple[tuple[int, int, int], ...]
    total_weight: int
    message: str
    steps: list[AlgorithmStep]


class _DisjointSet:
    """Small Union-Find structure for Kruskal cycle prevention."""

    def __init__(self, vertices: tuple[int, ...]) -> None:
        self._parent = {vertex: vertex for vertex in vertices}
        self._rank = {vertex: 0 for vertex in vertices}

    def find(self, vertex: int) -> int:
        """Return the representative for a vertex."""
        if self._parent[vertex] != vertex:
            self._parent[vertex] = self.find(self._parent[vertex])
        return self._parent[vertex]

    def union(self, first: int, second: int) -> bool:
        """Merge two sets and return whether a merge happened."""
        first_root = self.find(first)
        second_root = self.find(second)
        if first_root == second_root:
            return False

        if self._rank[first_root] < self._rank[second_root]:
            self._parent[first_root] = second_root
        elif self._rank[first_root] > self._rank[second_root]:
            self._parent[second_root] = first_root
        else:
            self._parent[second_root] = first_root
            self._rank[first_root] += 1
        return True

    def components(self) -> tuple[tuple[int, ...], ...]:
        """Return current disjoint sets in deterministic order."""
        grouped: dict[int, list[int]] = {}
        for vertex in sorted(self._parent):
            grouped.setdefault(self.find(vertex), []).append(vertex)
        return tuple(sorted((tuple(vertices) for vertices in grouped.values()), key=lambda item: item[0]))


def kruskal_mst(graph: Graph) -> KruskalMSTResult:
    """Build an MST by globally processing edges from lowest to highest weight."""
    if not isinstance(graph, Graph):
        return KruskalMSTResult(False, (), 0, "Kruskal's MST requires a Graph instance.", [])
    if graph.directed:
        return KruskalMSTResult(False, (), 0, "Kruskal's MST supports undirected graphs only.", [])
    if graph.vertex_count() == 0:
        return KruskalMSTResult(False, (), 0, "Kruskal's MST skipped because the graph is empty.", [])
    if not _has_only_non_negative_weights(graph):
        return KruskalMSTResult(False, (), 0, "Kruskal's MST requires non-negative edge weights.", [])

    sorted_edges = _sorted_edges(graph)
    disjoint_set = _DisjointSet(graph.vertices())
    mst_edges: list[tuple[int, int, int]] = []
    rejected_edges: list[tuple[int, int, int]] = []
    total_weight = 0

    steps = [
        _step(
            graph,
            AlgorithmEventType.VISIT,
            "Sort graph edges by weight.",
            sorted_edges=sorted_edges,
            disjoint_set=disjoint_set,
            mst_edges=mst_edges,
            rejected_edges=rejected_edges,
            total_weight=total_weight,
        )
    ]

    for source, destination, weight in sorted_edges:
        current_edge = (source, destination)
        steps.append(
            _step(
                graph,
                AlgorithmEventType.COMPARE,
                f"Consider edge {source} -> {destination} with weight {weight}.",
                sorted_edges=sorted_edges,
                disjoint_set=disjoint_set,
                mst_edges=mst_edges,
                rejected_edges=rejected_edges,
                total_weight=total_weight,
                current_edge=current_edge,
            )
        )

        if disjoint_set.union(source, destination):
            mst_edges.append((source, destination, weight))
            total_weight += weight
            steps.append(
                _step(
                    graph,
                    AlgorithmEventType.MOVE,
                    f"Accept edge {source} -> {destination}; total weight is now {total_weight}.",
                    sorted_edges=sorted_edges,
                    disjoint_set=disjoint_set,
                    mst_edges=mst_edges,
                    rejected_edges=rejected_edges,
                    total_weight=total_weight,
                    current_edge=current_edge,
                    accepted_edge=current_edge,
                )
            )
            if len(mst_edges) == graph.vertex_count() - 1:
                break
        else:
            rejected_edges.append((source, destination, weight))
            steps.append(
                _step(
                    graph,
                    AlgorithmEventType.COMPARE,
                    f"Reject edge {source} -> {destination} because it would create a cycle.",
                    sorted_edges=sorted_edges,
                    disjoint_set=disjoint_set,
                    mst_edges=mst_edges,
                    rejected_edges=rejected_edges,
                    total_weight=total_weight,
                    current_edge=current_edge,
                    rejected_edge=current_edge,
                )
            )

    edges = tuple(mst_edges)
    if len(mst_edges) != graph.vertex_count() - 1:
        message = "Kruskal's MST incomplete: graph is disconnected; no spanning tree covers all vertices."
        steps.append(
            _step(
                graph,
                AlgorithmEventType.COMPLETE,
                message,
                sorted_edges=sorted_edges,
                disjoint_set=disjoint_set,
                mst_edges=mst_edges,
                rejected_edges=rejected_edges,
                total_weight=total_weight,
                disconnected=True,
                completed=True,
            )
        )
        return KruskalMSTResult(False, edges, total_weight, message, steps)

    message = f"Kruskal's MST complete. Total weight: {total_weight}."
    steps.append(
        _step(
            graph,
            AlgorithmEventType.COMPLETE,
            message,
            sorted_edges=sorted_edges,
            disjoint_set=disjoint_set,
            mst_edges=mst_edges,
            rejected_edges=rejected_edges,
            total_weight=total_weight,
            completed=True,
        )
    )
    return KruskalMSTResult(True, edges, total_weight, message, steps)


def _sorted_edges(graph: Graph) -> tuple[tuple[int, int, int], ...]:
    edges: list[tuple[int, int, int]] = []
    seen: set[frozenset[int]] = set()
    for source, neighbors in graph.adjacency_list().items():
        for destination, weight in neighbors:
            edge_key = frozenset({source, destination})
            if edge_key in seen:
                continue
            seen.add(edge_key)
            first, second = sorted((source, destination))
            edges.append((first, second, weight))
    return tuple(sorted(edges, key=lambda edge: (edge[2], edge[0], edge[1])))


def _has_only_non_negative_weights(graph: Graph) -> bool:
    return all(weight >= 0 for neighbors in graph.adjacency_list().values() for _neighbor, weight in neighbors)


def _step(
    graph: Graph,
    event_type: AlgorithmEventType,
    message: str,
    *,
    sorted_edges: tuple[tuple[int, int, int], ...],
    disjoint_set: _DisjointSet,
    mst_edges: list[tuple[int, int, int]],
    rejected_edges: list[tuple[int, int, int]],
    total_weight: int,
    current_edge: tuple[int, int] | None = None,
    accepted_edge: tuple[int, int] | None = None,
    rejected_edge: tuple[int, int] | None = None,
    disconnected: bool = False,
    completed: bool = False,
) -> AlgorithmStep:
    highlight_vertices = list(current_edge) if current_edge is not None else []
    highlight_edges = []
    if accepted_edge is not None:
        highlight_edges.append(accepted_edge)
    elif rejected_edge is not None:
        highlight_edges.append(rejected_edge)
    elif current_edge is not None:
        highlight_edges.append(current_edge)

    metadata = {
        "graph_type": graph.graph_type,
        "directed": graph.directed,
        "vertices": list(graph.vertices()),
        "adjacency": graph.adjacency_list(),
        "vertex_count": graph.vertex_count(),
        "edge_count": graph.edge_count(),
        "current_edge": current_edge,
        "examined_edge": current_edge,
        "accepted_edge": accepted_edge,
        "rejected_edge": rejected_edge,
        "sorted_edges": list(sorted_edges),
        "disjoint_sets": [list(component) for component in disjoint_set.components()],
        "mst_edges": list(mst_edges),
        "rejected_edges": list(rejected_edges),
        "mst_total_weight": total_weight,
        "mst_disconnected": disconnected,
        "highlight_vertices": highlight_vertices,
        "highlight_edges": highlight_edges,
    }
    return make_algorithm_step(event_type, message, (), completed=completed, metadata=metadata)
