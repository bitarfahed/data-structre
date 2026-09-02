from data_structures_visual_lab.domain.algorithms import AlgorithmEventType, kruskal_mst, prim_mst
from data_structures_visual_lab.domain.data_structures import Graph


def test_prim_mst_builds_simple_connected_tree() -> None:
    graph = Graph()
    for vertex in (1, 2, 3):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2, 1)
    graph.add_edge(2, 3, 2)
    graph.add_edge(1, 3, 5)

    result = prim_mst(graph, 1)

    assert result.ok
    assert result.edges == ((1, 2, 1), (2, 3, 2))
    assert result.total_weight == 3
    assert result.message == "Prim's MST complete. Total weight: 3."


def test_prim_mst_uses_deterministic_tie_breaking_for_equal_weights() -> None:
    graph = Graph()
    for vertex in (1, 2, 3, 4):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2, 1)
    graph.add_edge(1, 3, 1)
    graph.add_edge(2, 4, 2)
    graph.add_edge(3, 4, 2)

    result = prim_mst(graph, 1)

    assert result.ok
    assert result.edges == ((1, 2, 1), (1, 3, 1), (2, 4, 2))
    assert result.total_weight == 4


def test_prim_mst_handles_single_vertex() -> None:
    graph = Graph()
    graph.add_vertex(7)

    result = prim_mst(graph, 7)

    assert result.ok
    assert result.edges == ()
    assert result.total_weight == 0
    assert result.message == "Prim's MST complete. Total weight: 0."
    assert result.steps[-1].state.metadata["mst_total_weight"] == 0


def test_prim_mst_reports_disconnected_graph_without_claiming_full_mst() -> None:
    graph = Graph()
    for vertex in (1, 2, 3):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2, 4)

    result = prim_mst(graph, 1)

    assert not result.ok
    assert result.edges == ((1, 2, 4),)
    assert result.total_weight == 4
    assert result.message == "Prim's MST incomplete: graph is disconnected; no spanning tree covers all vertices."
    assert result.steps[-1].state.metadata["mst_disconnected"] is True


def test_prim_mst_rejects_invalid_inputs_safely() -> None:
    graph = Graph()
    graph.add_vertex(1)

    assert prim_mst("graph", 1).message == "Prim's MST requires a Graph instance."  # type: ignore[arg-type]
    assert prim_mst(Graph(directed=True), 1).message == "Prim's MST supports undirected graphs only."
    assert prim_mst(graph, "1").message == "Start vertex must be an integer."  # type: ignore[arg-type]
    assert prim_mst(Graph(), 1).message == "Prim's MST skipped because the graph is empty."
    assert prim_mst(graph, 9).message == "Prim's MST start vertex 9 does not exist."


def test_prim_mst_edges_are_connected_and_acyclic() -> None:
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

    result = prim_mst(graph, 1)

    assert result.ok
    assert len(result.edges) == graph.vertex_count() - 1
    assert _is_connected_acyclic(graph.vertices(), result.edges)
    assert result.total_weight == 8


def test_prim_and_kruskal_have_same_total_weight_on_same_graph() -> None:
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

    prim_result = prim_mst(graph, 1)
    kruskal_result = kruskal_mst(graph)

    assert prim_result.ok
    assert kruskal_result.ok
    assert _is_connected_acyclic(graph.vertices(), prim_result.edges)
    assert _is_connected_acyclic(graph.vertices(), kruskal_result.edges)
    assert prim_result.total_weight == kruskal_result.total_weight == 8


def test_prim_mst_steps_expose_queue_selected_and_rejected_edges() -> None:
    graph = Graph()
    for vertex in (1, 2, 3, 4):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2, 1)
    graph.add_edge(1, 3, 2)
    graph.add_edge(2, 3, 1)
    graph.add_edge(3, 4, 10)

    result = prim_mst(graph, 1)
    selected_step = [step for step in result.steps if step.state.metadata.get("selected_edge") == (1, 2)][0]
    rejected_step = [step for step in result.steps if step.state.metadata.get("rejected_edge") == (1, 3)][0]

    assert selected_step.event_type is AlgorithmEventType.MOVE
    assert selected_step.state.metadata["mst_edges"] == [(1, 2, 1)]
    assert selected_step.state.metadata["mst_total_weight"] == 1
    assert rejected_step.event_type is AlgorithmEventType.COMPARE
    assert rejected_step.state.metadata["included_vertices"] == [1, 2, 3]
    assert rejected_step.state.metadata["highlight_edges"] == [(1, 3)]


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
