from data_structures_visual_lab.domain.algorithms import AlgorithmEventType, detect_cycle
from data_structures_visual_lab.domain.data_structures import Graph


def test_cycle_detection_finds_undirected_cycle() -> None:
    graph = Graph()
    for vertex in (1, 2, 3):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(1, 3)

    result = detect_cycle(graph)

    assert result.ok
    assert result.has_cycle
    assert result.cycle_vertices == (1, 2, 3, 1)
    assert result.cycle_edges == ((1, 2), (2, 3), (3, 1))
    assert result.message == "Cycle Detection complete. Cycle found: [1, 2, 3, 1]."


def test_cycle_detection_reports_no_undirected_cycle() -> None:
    graph = Graph()
    for vertex in (1, 2, 3):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)

    result = detect_cycle(graph)

    assert result.ok
    assert not result.has_cycle
    assert result.cycle_vertices == ()
    assert result.message == "Cycle Detection complete. No cycle found."


def test_cycle_detection_finds_directed_cycle() -> None:
    graph = Graph(directed=True)
    for vertex in (1, 2, 3):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 1)

    result = detect_cycle(graph)

    assert result.has_cycle
    assert result.cycle_vertices == (1, 2, 3, 1)
    assert result.cycle_edges == ((1, 2), (2, 3), (3, 1))


def test_cycle_detection_reports_directed_dag_has_no_cycle() -> None:
    graph = Graph(directed=True)
    for vertex in (1, 2, 3):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    graph.add_edge(2, 3)

    result = detect_cycle(graph)

    assert result.ok
    assert not result.has_cycle
    assert result.cycle_edges == ()


def test_cycle_detection_checks_disconnected_components() -> None:
    graph = Graph()
    for vertex in (1, 2, 3, 4, 5):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2)
    graph.add_edge(3, 4)
    graph.add_edge(4, 5)
    graph.add_edge(3, 5)

    result = detect_cycle(graph)

    assert result.has_cycle
    assert result.cycle_vertices == (3, 4, 5, 3)


def test_cycle_detection_handles_single_vertex_and_empty_graph() -> None:
    single = Graph()
    single.add_vertex(1)

    single_result = detect_cycle(single)
    empty_result = detect_cycle(Graph())

    assert single_result.ok
    assert not single_result.has_cycle
    assert empty_result.ok
    assert not empty_result.has_cycle
    assert empty_result.message == "Cycle Detection complete. No cycle found."


def test_cycle_detection_rejects_invalid_graph_input() -> None:
    result = detect_cycle("graph")  # type: ignore[arg-type]

    assert not result.ok
    assert result.message == "Cycle Detection requires a Graph instance."


def test_cycle_detection_steps_expose_cycle_state() -> None:
    graph = Graph(directed=True)
    for vertex in (1, 2, 3):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 1)

    result = detect_cycle(graph)
    found_step = [step for step in result.steps if step.event_type is AlgorithmEventType.FOUND][0]

    assert found_step.state.metadata["cycle_detected"] is True
    assert found_step.state.metadata["cycle_vertices"] == [1, 2, 3, 1]
    assert found_step.state.metadata["cycle_edges"] == [(1, 2), (2, 3), (3, 1)]
    assert found_step.state.metadata["traversal_path"] == [1, 2, 3]
    assert found_step.state.metadata["examined_edge"] == (3, 1)
