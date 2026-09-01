from data_structures_visual_lab.domain.algorithms import AlgorithmEventType, dijkstra
from data_structures_visual_lab.domain.data_structures import Graph


def test_dijkstra_computes_shortest_distances_and_target_path() -> None:
    graph = Graph()
    for vertex in (1, 2, 3):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2, 4)
    graph.add_edge(1, 3, 1)
    graph.add_edge(3, 2, 2)

    result = dijkstra(graph, 1, 2)

    assert result.ok
    assert result.distances == {1: 0, 2: 3, 3: 1}
    assert result.path == (1, 3, 2)
    assert result.message == "Dijkstra complete. Shortest path to 2: [1, 3, 2] with distance 3."


def test_dijkstra_supports_directed_graph_direction() -> None:
    graph = Graph(directed=True)
    for vertex in (1, 2, 3):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2, 1)
    graph.add_edge(2, 3, 1)

    result = dijkstra(graph, 3)

    assert result.ok
    assert result.distances == {1: None, 2: None, 3: 0}


def test_dijkstra_supports_undirected_edges() -> None:
    graph = Graph()
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_edge(1, 2, 5)

    result = dijkstra(graph, 2, 1)

    assert result.distances == {1: 5, 2: 0}
    assert result.path == (2, 1)


def test_dijkstra_keeps_unreachable_vertices_at_infinity() -> None:
    graph = Graph()
    for vertex in (1, 2, 9):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2, 1)

    result = dijkstra(graph, 1, 9)

    assert result.ok
    assert result.distances[9] is None
    assert result.path == ()
    assert result.message == "Dijkstra complete. No path from 1 to 9."


def test_dijkstra_handles_single_vertex_and_zero_weight_edges() -> None:
    single = Graph()
    single.add_vertex(7)

    single_result = dijkstra(single, 7, 7)

    assert single_result.distances == {7: 0}
    assert single_result.path == (7,)

    graph = Graph()
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_edge(1, 2, 0)

    zero_result = dijkstra(graph, 1, 2)

    assert zero_result.distances[2] == 0
    assert zero_result.path == (1, 2)


def test_dijkstra_prefers_deterministic_tie_path() -> None:
    graph = Graph()
    for vertex in (1, 2, 3, 4):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2, 1)
    graph.add_edge(1, 3, 1)
    graph.add_edge(2, 4, 1)
    graph.add_edge(3, 4, 1)

    result = dijkstra(graph, 1, 4)

    assert result.distances[4] == 2
    assert result.path == (1, 2, 4)


def test_dijkstra_rejects_invalid_inputs_safely() -> None:
    graph = Graph()
    graph.add_vertex(1)
    graph.add_vertex(2)

    assert dijkstra("graph", 1).message == "Dijkstra requires a Graph instance."  # type: ignore[arg-type]
    assert dijkstra(graph, "1").message == "Start vertex must be an integer."  # type: ignore[arg-type]
    assert dijkstra(graph, 1, "2").message == "Target vertex must be an integer."  # type: ignore[arg-type]
    assert dijkstra(Graph(), 1).message == "Dijkstra skipped because the graph is empty."
    assert dijkstra(graph, 9).message == "Dijkstra start vertex 9 does not exist."
    assert dijkstra(graph, 1, 9).message == "Dijkstra target vertex 9 does not exist."


def test_dijkstra_rejects_negative_weights_if_present() -> None:
    graph = Graph(directed=True)
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_edge(1, 2, 1)
    graph._adjacency[1][2] = -1  # type: ignore[attr-defined]  # Force invalid internal state for validation.

    result = dijkstra(graph, 1)

    assert not result.ok
    assert result.message == "Dijkstra requires non-negative edge weights."


def test_dijkstra_steps_expose_relaxation_state() -> None:
    graph = Graph()
    for vertex in (1, 2, 3):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2, 4)
    graph.add_edge(1, 3, 1)

    result = dijkstra(graph, 1)
    update_step = [step for step in result.steps if step.message == "Update vertex 3: distance becomes 1."][0]
    complete_step = result.steps[-1]

    assert update_step.event_type is AlgorithmEventType.MOVE
    assert update_step.state.metadata["examined_edge"] == (1, 3)
    assert update_step.state.metadata["updated_vertex"] == 3
    assert update_step.state.metadata["old_distance"] is None
    assert update_step.state.metadata["new_distance"] == 1
    assert update_step.state.metadata["priority_queue"] == [(1, 3), (4, 2)]
    assert complete_step.event_type is AlgorithmEventType.COMPLETE
    assert complete_step.state.completed
