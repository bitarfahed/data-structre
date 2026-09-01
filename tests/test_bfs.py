from data_structures_visual_lab.domain.algorithms import AlgorithmEventType, bfs
from data_structures_visual_lab.domain.data_structures import Graph


def test_bfs_traverses_simple_connected_graph_in_deterministic_order() -> None:
    graph = Graph()
    for vertex in (1, 2, 3, 4):
        graph.add_vertex(vertex)
    graph.add_edge(1, 3)
    graph.add_edge(1, 2)
    graph.add_edge(2, 4)

    result = bfs(graph, 1)

    assert result.ok
    assert result.order == (1, 2, 3, 4)
    assert result.message == "BFS complete. Traversal order: [1, 2, 3, 4]."
    assert result.steps[-1].event_type is AlgorithmEventType.COMPLETE
    assert result.steps[-1].state.metadata["traversal_order"] == [1, 2, 3, 4]


def test_bfs_works_with_undirected_graph() -> None:
    graph = Graph()
    for vertex in (1, 2, 3):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)

    result = bfs(graph, 3)

    assert result.ok
    assert result.order == (3, 2, 1)


def test_bfs_works_with_directed_graph_direction() -> None:
    graph = Graph(directed=True)
    for vertex in (1, 2, 3):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)

    forward = bfs(graph, 1)
    reverse = bfs(graph, 3)

    assert forward.ok
    assert forward.order == (1, 2, 3)
    assert reverse.ok
    assert reverse.order == (3,)


def test_bfs_does_not_continue_into_disconnected_components() -> None:
    graph = Graph()
    for vertex in (1, 2, 3, 4):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2)
    graph.add_edge(3, 4)

    result = bfs(graph, 1)

    assert result.ok
    assert result.order == (1, 2)
    assert result.steps[-1].state.metadata["visited_vertices"] == [1, 2]


def test_bfs_handles_single_vertex() -> None:
    graph = Graph()
    graph.add_vertex(7)

    result = bfs(graph, 7)

    assert result.ok
    assert result.order == (7,)
    assert result.steps[0].state.metadata["queue"] == [7]
    assert result.steps[-1].state.metadata["queue"] == []


def test_bfs_handles_empty_graph_safely() -> None:
    result = bfs(Graph(), 1)

    assert not result.ok
    assert result.order == ()
    assert result.message == "BFS skipped because the graph is empty."
    assert result.steps == []


def test_bfs_rejects_missing_start_vertex() -> None:
    graph = Graph()
    graph.add_vertex(1)

    result = bfs(graph, 9)

    assert not result.ok
    assert result.message == "BFS start vertex 9 does not exist."
    assert result.steps == []


def test_bfs_rejects_invalid_start_vertex() -> None:
    result = bfs(Graph(), "1")  # type: ignore[arg-type]

    assert not result.ok
    assert result.message == "Start vertex must be an integer."


def test_bfs_steps_expose_queue_visited_order_and_examined_edge() -> None:
    graph = Graph()
    for vertex in (1, 2, 3):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)

    result = bfs(graph, 1)
    examine_step = [step for step in result.steps if step.message == "Examine edge 1 -> 2."][0]
    discover_step = [step for step in result.steps if step.message == "Discovered vertex 2; enqueue it."][0]

    assert examine_step.state.metadata["current_vertex"] == 1
    assert examine_step.state.metadata["examined_edge"] == (1, 2)
    assert discover_step.state.metadata["queue"] == [2]
    assert discover_step.state.metadata["visited_vertices"] == [1, 2]
    assert discover_step.state.metadata["traversal_order"] == [1]
