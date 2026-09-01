import pytest

from data_structures_visual_lab.domain.data_structures import Graph


def test_empty_graph_has_no_vertices_or_edges() -> None:
    graph = Graph()

    assert graph.graph_type == "undirected"
    assert not graph.directed
    assert graph.vertex_count() == 0
    assert graph.edge_count() == 0
    assert graph.vertices() == ()
    assert graph.adjacency_list() == {}
    assert graph.neighbors(1) == ()


def test_add_and_remove_vertex() -> None:
    graph = Graph()

    assert graph.add_vertex(1)
    assert graph.has_vertex(1)
    assert graph.vertex_count() == 1
    assert graph.remove_vertex(1)

    assert not graph.has_vertex(1)
    assert graph.vertex_count() == 0


def test_duplicate_vertices_are_rejected() -> None:
    graph = Graph()

    assert graph.add_vertex(1)
    assert not graph.add_vertex(1)
    assert graph.vertex_count() == 1


def test_remove_missing_vertex_is_safe() -> None:
    graph = Graph()

    assert not graph.remove_vertex(1)
    assert graph.vertex_count() == 0


def test_add_and_remove_undirected_edge_keeps_directions_synchronized() -> None:
    graph = Graph()
    graph.add_vertex(1)
    graph.add_vertex(2)

    assert graph.add_edge(1, 2)
    assert graph.has_edge(1, 2)
    assert graph.has_edge(2, 1)
    assert graph.neighbors(1) == ((2, 1),)
    assert graph.neighbors(2) == ((1, 1),)
    assert graph.edge_count() == 1

    assert graph.remove_edge(1, 2)
    assert not graph.has_edge(1, 2)
    assert not graph.has_edge(2, 1)
    assert graph.edge_count() == 0


def test_directed_edges_preserve_direction() -> None:
    graph = Graph(directed=True)
    graph.add_vertex(1)
    graph.add_vertex(2)

    assert graph.graph_type == "directed"
    assert graph.directed
    assert graph.add_edge(1, 2)

    assert graph.has_edge(1, 2)
    assert not graph.has_edge(2, 1)
    assert graph.neighbors(1) == ((2, 1),)
    assert graph.neighbors(2) == ()
    assert graph.edge_count() == 1


def test_weighted_edges_store_non_negative_integer_weights() -> None:
    graph = Graph()
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)

    assert graph.add_edge(1, 2, weight=0)
    assert graph.add_edge(1, 3, weight=7)

    assert graph.edge_weight(1, 2) == 0
    assert graph.edge_weight(2, 1) == 0
    assert graph.edge_weight(1, 3) == 7
    assert graph.neighbors(1) == ((2, 0), (3, 7))


def test_duplicate_edges_and_parallel_edges_are_rejected() -> None:
    graph = Graph()
    graph.add_vertex(1)
    graph.add_vertex(2)

    assert graph.add_edge(1, 2, weight=3)
    assert not graph.add_edge(1, 2, weight=5)
    assert not graph.add_edge(2, 1, weight=5)

    assert graph.edge_count() == 1
    assert graph.edge_weight(1, 2) == 3
    assert graph.edge_weight(2, 1) == 3


def test_directed_reverse_edge_is_distinct_but_duplicate_same_direction_is_rejected() -> None:
    graph = Graph(directed=True)
    graph.add_vertex(1)
    graph.add_vertex(2)

    assert graph.add_edge(1, 2, weight=3)
    assert not graph.add_edge(1, 2, weight=5)
    assert graph.add_edge(2, 1, weight=5)

    assert graph.edge_count() == 2
    assert graph.edge_weight(1, 2) == 3
    assert graph.edge_weight(2, 1) == 5


def test_self_loops_are_not_supported() -> None:
    graph = Graph()
    graph.add_vertex(1)

    assert not graph.add_edge(1, 1)
    assert not graph.has_edge(1, 1)
    assert graph.edge_count() == 0


def test_add_edge_requires_existing_vertices() -> None:
    graph = Graph()
    graph.add_vertex(1)

    assert not graph.add_edge(1, 2)
    assert not graph.add_edge(2, 1)
    assert graph.edge_count() == 0


def test_remove_missing_edge_is_safe() -> None:
    graph = Graph()
    graph.add_vertex(1)
    graph.add_vertex(2)

    assert not graph.remove_edge(1, 2)
    assert not graph.remove_edge(2, 1)
    assert graph.edge_count() == 0


def test_removing_vertex_removes_incident_edges() -> None:
    graph = Graph()
    for vertex in (1, 2, 3):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2, weight=4)
    graph.add_edge(2, 3, weight=6)

    assert graph.remove_vertex(2)

    assert graph.vertices() == (1, 3)
    assert graph.edge_count() == 0
    assert graph.neighbors(1) == ()
    assert graph.neighbors(3) == ()


def test_directed_remove_vertex_removes_incoming_and_outgoing_edges() -> None:
    graph = Graph(directed=True)
    for vertex in (1, 2, 3):
        graph.add_vertex(vertex)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 2)

    assert graph.remove_vertex(2)

    assert graph.vertices() == (1, 3)
    assert graph.edge_count() == 0
    assert graph.neighbors(1) == ()
    assert graph.neighbors(3) == ()


def test_adjacency_list_exposes_weighted_graph_state() -> None:
    graph = Graph()
    for vertex in (3, 1, 2):
        graph.add_vertex(vertex)
    graph.add_edge(1, 3, weight=9)
    graph.add_edge(1, 2, weight=5)

    assert graph.vertices() == (1, 2, 3)
    assert graph.adjacency_list() == {
        1: ((2, 5), (3, 9)),
        2: ((1, 5),),
        3: ((1, 9),),
    }


def test_display_representation() -> None:
    graph = Graph(directed=True)
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_edge(1, 2, weight=4)

    assert str(graph) == "Graph(type=directed, adjacency={1: ((2, 4),), 2: ()})"
    assert repr(graph) == "Graph(directed=True, adjacency={1: ((2, 4),), 2: ()})"
    assert len(graph) == 2


@pytest.mark.parametrize("directed", ["yes", 1, None])
def test_graph_rejects_non_boolean_directed_flag(directed: object) -> None:
    with pytest.raises(TypeError, match="directed flag"):
        Graph(directed=directed)  # type: ignore[arg-type]


@pytest.mark.parametrize("vertex", ["1", 1.5, None, True])
def test_vertex_operations_reject_non_integer_vertices(vertex: object) -> None:
    graph = Graph()

    with pytest.raises(TypeError, match="vertices"):
        graph.add_vertex(vertex)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="vertices"):
        graph.remove_vertex(vertex)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="vertices"):
        graph.has_vertex(vertex)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="vertices"):
        graph.neighbors(vertex)  # type: ignore[arg-type]


def test_edge_operations_reject_non_integer_vertices() -> None:
    graph = Graph()

    with pytest.raises(TypeError, match="source"):
        graph.add_edge("1", 2)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="destination"):
        graph.add_edge(1, "2")  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="source"):
        graph.remove_edge("1", 2)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="destination"):
        graph.has_edge(1, "2")  # type: ignore[arg-type]


@pytest.mark.parametrize("weight", ["1", 1.5, None, False])
def test_add_edge_rejects_non_integer_weights(weight: object) -> None:
    graph = Graph()
    graph.add_vertex(1)
    graph.add_vertex(2)

    with pytest.raises(TypeError, match="weights"):
        graph.add_edge(1, 2, weight=weight)  # type: ignore[arg-type]


def test_add_edge_rejects_negative_weights() -> None:
    graph = Graph()
    graph.add_vertex(1)
    graph.add_vertex(2)

    with pytest.raises(ValueError, match="non-negative"):
        graph.add_edge(1, 2, weight=-1)

    assert graph.edge_count() == 0
