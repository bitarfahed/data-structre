from data_structures_visual_lab.domain.algorithms import AlgorithmEventType, connected_components
from data_structures_visual_lab.domain.data_structures import Graph


def test_connected_components_finds_one_component() -> None:
    graph = Graph()
    for vertex in (1, 2, 3):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)

    result = connected_components(graph)

    assert result.ok
    assert result.components == ((1, 2, 3),)
    assert result.message == "Connected Components complete. Component count: 1."


def test_connected_components_finds_multiple_components_and_isolated_vertices() -> None:
    graph = Graph()
    for vertex in (1, 2, 3, 4, 5):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2)
    graph.add_edge(4, 5)

    result = connected_components(graph)

    assert result.ok
    assert result.components == ((1, 2), (3,), (4, 5))
    assert result.steps[-1].state.metadata["component_count"] == 3


def test_connected_components_handles_completely_disconnected_graph() -> None:
    graph = Graph()
    for vertex in (3, 1, 2):
        graph.add_vertex(vertex)

    result = connected_components(graph)

    assert result.components == ((1,), (2,), (3,))


def test_connected_components_handles_empty_graph_safely() -> None:
    result = connected_components(Graph())

    assert result.ok
    assert result.components == ()
    assert result.message == "Connected Components complete. Component count: 0."
    assert result.steps[-1].event_type is AlgorithmEventType.COMPLETE


def test_connected_components_rejects_directed_graph() -> None:
    graph = Graph(directed=True)
    graph.add_vertex(1)

    result = connected_components(graph)

    assert not result.ok
    assert result.components == ()
    assert result.message == "Connected Components supports undirected graphs only."
    assert result.steps == []


def test_connected_components_rejects_invalid_graph_input() -> None:
    result = connected_components("graph")  # type: ignore[arg-type]

    assert not result.ok
    assert result.message == "Connected Components requires a Graph instance."


def test_connected_components_steps_expose_current_and_completed_components() -> None:
    graph = Graph()
    for vertex in (1, 2, 3):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2)

    result = connected_components(graph)
    discover_step = [step for step in result.steps if step.message == "Discovered vertex 2 for component 1."][0]
    final_step = result.steps[-1]

    assert discover_step.state.metadata["current_component"] == 1
    assert discover_step.state.metadata["current_vertex"] == 2
    assert discover_step.state.metadata["current_component_vertices"] == [1, 2]
    assert discover_step.state.metadata["visited_vertices"] == [1, 2]
    assert final_step.state.metadata["completed_components"] == [[1, 2], [3]]
    assert final_step.state.metadata["component_count"] == 2
