from data_structures_visual_lab.domain.algorithms import AlgorithmEventType, dfs
from data_structures_visual_lab.domain.data_structures import Graph


def test_dfs_traverses_simple_connected_graph_in_deterministic_order() -> None:
    graph = Graph()
    for vertex in (1, 2, 3, 4):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    graph.add_edge(2, 4)

    result = dfs(graph, 1)

    assert result.ok
    assert result.order == (1, 3, 2, 4)
    assert result.message == "DFS complete. Traversal order: [1, 3, 2, 4]."
    assert result.steps[-1].event_type is AlgorithmEventType.COMPLETE
    assert result.steps[-1].state.metadata["traversal_order"] == [1, 3, 2, 4]


def test_dfs_works_with_undirected_graph() -> None:
    graph = Graph()
    for vertex in (1, 2, 3):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)

    result = dfs(graph, 3)

    assert result.ok
    assert result.order == (3, 2, 1)


def test_dfs_works_with_directed_graph_direction() -> None:
    graph = Graph(directed=True)
    for vertex in (1, 2, 3):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)

    forward = dfs(graph, 1)
    reverse = dfs(graph, 3)

    assert forward.ok
    assert forward.order == (1, 2, 3)
    assert reverse.ok
    assert reverse.order == (3,)


def test_dfs_does_not_continue_into_disconnected_components() -> None:
    graph = Graph()
    for vertex in (1, 2, 3, 4):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2)
    graph.add_edge(3, 4)

    result = dfs(graph, 1)

    assert result.ok
    assert result.order == (1, 2)
    assert result.steps[-1].state.metadata["visited_vertices"] == [1, 2]


def test_dfs_handles_single_vertex() -> None:
    graph = Graph()
    graph.add_vertex(7)

    result = dfs(graph, 7)

    assert result.ok
    assert result.order == (7,)
    assert result.steps[0].state.metadata["stack"] == [7]
    assert result.steps[-1].state.metadata["stack"] == []


def test_dfs_handles_empty_graph_safely() -> None:
    result = dfs(Graph(), 1)

    assert not result.ok
    assert result.order == ()
    assert result.message == "DFS skipped because the graph is empty."
    assert result.steps == []


def test_dfs_rejects_missing_start_vertex() -> None:
    graph = Graph()
    graph.add_vertex(1)

    result = dfs(graph, 9)

    assert not result.ok
    assert result.message == "DFS start vertex 9 does not exist."
    assert result.steps == []


def test_dfs_rejects_invalid_start_vertex() -> None:
    result = dfs(Graph(), "1")  # type: ignore[arg-type]

    assert not result.ok
    assert result.message == "Start vertex must be an integer."


def test_dfs_steps_expose_stack_visited_order_and_examined_edge() -> None:
    graph = Graph()
    for vertex in (1, 2, 3):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)

    result = dfs(graph, 1)
    examine_step = [step for step in result.steps if step.message == "Examine edge 1 -> 2."][0]
    discover_step = [step for step in result.steps if step.message == "Discovered vertex 2; push it onto the stack."][0]

    assert examine_step.state.metadata["current_vertex"] == 1
    assert examine_step.state.metadata["examined_edge"] == (1, 2)
    assert discover_step.state.metadata["stack"] == [2]
    assert discover_step.state.metadata["frontier"] == "stack"
    assert discover_step.state.metadata["visited_vertices"] == [1, 2]
    assert discover_step.state.metadata["traversal_order"] == [1]
