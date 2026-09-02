from data_structures_visual_lab.domain.algorithms import AlgorithmEventType, kruskal_mst
from data_structures_visual_lab.domain.algorithms.kruskal_mst import _DisjointSet
from data_structures_visual_lab.domain.data_structures import Graph


def test_kruskal_mst_builds_simple_connected_tree() -> None:
    graph = Graph()
    for vertex in (1, 2, 3):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2, 1)
    graph.add_edge(2, 3, 2)
    graph.add_edge(1, 3, 5)

    result = kruskal_mst(graph)

    assert result.ok
    assert result.edges == ((1, 2, 1), (2, 3, 2))
    assert result.total_weight == 3
    assert result.message == "Kruskal's MST complete. Total weight: 3."


def test_kruskal_mst_processes_equal_weight_edges_deterministically() -> None:
    graph = Graph()
    for vertex in (1, 2, 3, 4):
        graph.add_vertex(vertex)
    graph.add_edge(1, 3, 1)
    graph.add_edge(1, 2, 1)
    graph.add_edge(2, 4, 2)
    graph.add_edge(3, 4, 2)

    result = kruskal_mst(graph)

    assert result.ok
    assert result.edges == ((1, 2, 1), (1, 3, 1), (2, 4, 2))
    assert result.total_weight == 4


def test_kruskal_mst_rejects_edges_that_create_cycles() -> None:
    graph = Graph()
    for vertex in (1, 2, 3, 4):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2, 1)
    graph.add_edge(2, 3, 1)
    graph.add_edge(1, 3, 2)
    graph.add_edge(3, 4, 3)

    result = kruskal_mst(graph)
    rejected_step = [step for step in result.steps if step.state.metadata.get("rejected_edge") == (1, 3)][0]

    assert result.ok
    assert result.edges == ((1, 2, 1), (2, 3, 1), (3, 4, 3))
    assert result.total_weight == 5
    assert rejected_step.event_type is AlgorithmEventType.COMPARE
    assert rejected_step.message == "Reject edge 1 -> 3 because it would create a cycle."
    assert rejected_step.state.metadata["rejected_edges"] == [(1, 3, 2)]


def test_kruskal_mst_handles_single_vertex() -> None:
    graph = Graph()
    graph.add_vertex(7)

    result = kruskal_mst(graph)

    assert result.ok
    assert result.edges == ()
    assert result.total_weight == 0
    assert result.message == "Kruskal's MST complete. Total weight: 0."


def test_kruskal_mst_reports_disconnected_graph() -> None:
    graph = Graph()
    for vertex in (1, 2, 3):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2, 4)

    result = kruskal_mst(graph)

    assert not result.ok
    assert result.edges == ((1, 2, 4),)
    assert result.total_weight == 4
    assert result.message == "Kruskal's MST incomplete: graph is disconnected; no spanning tree covers all vertices."
    assert result.steps[-1].state.metadata["mst_disconnected"] is True


def test_kruskal_mst_rejects_invalid_inputs_safely() -> None:
    assert kruskal_mst("graph").message == "Kruskal's MST requires a Graph instance."  # type: ignore[arg-type]
    assert kruskal_mst(Graph(directed=True)).message == "Kruskal's MST supports undirected graphs only."
    assert kruskal_mst(Graph()).message == "Kruskal's MST skipped because the graph is empty."


def test_kruskal_mst_edges_are_connected_and_acyclic() -> None:
    graph = Graph()
    for vertex in (1, 2, 3, 4, 5):
        graph.add_vertex(vertex)
    for source, destination, weight in (
        (1, 2, 2),
        (1, 3, 3),
        (2, 3, 1),
        (2, 4, 4),
        (3, 5, 5),
        (4, 5, 1),
    ):
        graph.add_edge(source, destination, weight)

    result = kruskal_mst(graph)

    assert result.ok
    assert len(result.edges) == graph.vertex_count() - 1
    assert _is_connected_acyclic(graph.vertices(), result.edges)
    assert result.total_weight == 8


def test_kruskal_mst_steps_expose_sorted_edges_sets_and_mst_state() -> None:
    graph = Graph()
    for vertex in (1, 2, 3):
        graph.add_vertex(vertex)
    graph.add_edge(1, 3, 5)
    graph.add_edge(1, 2, 1)
    graph.add_edge(2, 3, 2)

    result = kruskal_mst(graph)
    first_step = result.steps[0]
    accepted_step = [step for step in result.steps if step.state.metadata.get("accepted_edge") == (1, 2)][0]

    assert first_step.state.metadata["sorted_edges"] == [(1, 2, 1), (2, 3, 2), (1, 3, 5)]
    assert first_step.state.metadata["disjoint_sets"] == [[1], [2], [3]]
    assert accepted_step.state.metadata["mst_edges"] == [(1, 2, 1)]
    assert accepted_step.state.metadata["mst_total_weight"] == 1
    assert accepted_step.state.metadata["disjoint_sets"] == [[1, 2], [3]]


def test_disjoint_set_merges_sets_and_blocks_cycle_unions() -> None:
    disjoint_set = _DisjointSet((1, 2, 3))

    assert disjoint_set.union(1, 2)
    assert not disjoint_set.union(1, 2)
    assert disjoint_set.find(1) == disjoint_set.find(2)
    assert disjoint_set.find(3) != disjoint_set.find(1)
    assert disjoint_set.components() == ((1, 2), (3,))


def _is_connected_acyclic(vertices: tuple[int, ...], edges: tuple[tuple[int, int, int], ...]) -> bool:
    parent = {vertex: vertex for vertex in vertices}

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for source, destination, _weight in edges:
        source_root = find(source)
        destination_root = find(destination)
        if source_root == destination_root:
            return False
        parent[source_root] = destination_root

    return len({find(vertex) for vertex in vertices}) == 1
