from data_structures_visual_lab.domain.algorithms import AlgorithmEventType, topological_sort
from data_structures_visual_lab.domain.data_structures import Graph


def test_topological_sort_simple_dag() -> None:
    graph = Graph(directed=True)
    for vertex in (1, 2, 3):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)

    result = topological_sort(graph)

    assert result.ok
    assert result.order == (1, 2, 3)
    assert result.message == "Topological Sort complete. Order: [1, 2, 3]."


def test_topological_sort_dag_with_multiple_valid_orders_is_deterministic() -> None:
    graph = Graph(directed=True)
    for vertex in (1, 2, 3):
        graph.add_vertex(vertex)
    graph.add_edge(1, 3)
    graph.add_edge(2, 3)

    result = topological_sort(graph)

    assert result.ok
    assert result.order == (1, 2, 3)
    assert _is_valid_topological_order(graph, result.order)


def test_topological_sort_handles_disconnected_dag() -> None:
    graph = Graph(directed=True)
    for vertex in (1, 2, 3, 4):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2)
    graph.add_edge(3, 4)

    result = topological_sort(graph)

    assert result.ok
    assert result.order == (1, 3, 2, 4)
    assert _is_valid_topological_order(graph, result.order)


def test_topological_sort_rejects_directed_cycle() -> None:
    graph = Graph(directed=True)
    for vertex in (1, 2, 3):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 1)

    result = topological_sort(graph)

    assert not result.ok
    assert result.order == ()
    assert result.message == "Topological sort impossible: cycle detected."
    assert result.steps[-1].state.metadata["cycle_detected"] is True


def test_topological_sort_handles_single_vertex_and_empty_graph() -> None:
    single = Graph(directed=True)
    single.add_vertex(7)

    single_result = topological_sort(single)
    empty_result = topological_sort(Graph(directed=True))

    assert single_result.ok
    assert single_result.order == (7,)
    assert empty_result.ok
    assert empty_result.order == ()
    assert empty_result.message == "Topological Sort complete. Order: []."


def test_topological_sort_rejects_undirected_graph() -> None:
    result = topological_sort(Graph())

    assert not result.ok
    assert result.order == ()
    assert result.message == "Topological Sort supports directed graphs only."
    assert result.steps == []


def test_topological_sort_rejects_invalid_graph_input() -> None:
    result = topological_sort("graph")  # type: ignore[arg-type]

    assert not result.ok
    assert result.message == "Topological Sort requires a Graph instance."


def test_topological_sort_steps_expose_indegree_queue_and_order() -> None:
    graph = Graph(directed=True)
    for vertex in (1, 2, 3):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)

    result = topological_sort(graph)
    initial_step = result.steps[0]
    queue_step = [step for step in result.steps if step.message == "Vertex 2 now has indegree 0; add it to the queue."][0]

    assert initial_step.event_type is AlgorithmEventType.VISIT
    assert initial_step.state.metadata["indegrees"] == {1: 0, 2: 1, 3: 1}
    assert initial_step.state.metadata["zero_indegree_queue"] == [1]
    assert queue_step.state.metadata["indegrees"] == {1: 0, 2: 0, 3: 1}
    assert queue_step.state.metadata["zero_indegree_queue"] == [2]
    assert queue_step.state.metadata["topological_order"] == [1]


def _is_valid_topological_order(graph: Graph, order: tuple[int, ...]) -> bool:
    positions = {vertex: index for index, vertex in enumerate(order)}
    return all(
        positions[source] < positions[destination]
        for source in graph.vertices()
        for destination, _weight in graph.neighbors(source)
    )
