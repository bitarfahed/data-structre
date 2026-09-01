"""Graph domain model."""

from __future__ import annotations


class Graph:
    """Integer-only weighted graph using an adjacency list."""

    def __init__(self, directed: bool = False) -> None:
        if type(directed) is not bool:
            raise TypeError("Graph directed flag must be a boolean.")
        self._directed = directed
        self._adjacency: dict[int, dict[int, int]] = {}

    @property
    def directed(self) -> bool:
        """Return True for a directed graph."""
        return self._directed

    @property
    def graph_type(self) -> str:
        """Return the graph type for future visualization."""
        return "directed" if self._directed else "undirected"

    def add_vertex(self, vertex: int) -> bool:
        """Add a vertex if it does not already exist."""
        self._validate_vertex(vertex)
        if vertex in self._adjacency:
            return False
        self._adjacency[vertex] = {}
        return True

    def remove_vertex(self, vertex: int) -> bool:
        """Remove a vertex and all incident edges."""
        self._validate_vertex(vertex)
        if vertex not in self._adjacency:
            return False

        del self._adjacency[vertex]
        for neighbors in self._adjacency.values():
            neighbors.pop(vertex, None)
        return True

    def add_edge(self, source: int, destination: int, weight: int = 1) -> bool:
        """Add a weighted edge between existing vertices."""
        self._validate_edge_input(source, destination, weight)
        if source not in self._adjacency or destination not in self._adjacency:
            return False
        if source == destination:
            return False
        if destination in self._adjacency[source]:
            return False

        self._adjacency[source][destination] = weight
        if not self._directed:
            self._adjacency[destination][source] = weight
        return True

    def remove_edge(self, source: int, destination: int) -> bool:
        """Remove an edge when it exists."""
        self._validate_vertex(source, "Graph edge source must be an integer.")
        self._validate_vertex(destination, "Graph edge destination must be an integer.")
        if source not in self._adjacency or destination not in self._adjacency[source]:
            return False

        del self._adjacency[source][destination]
        if not self._directed:
            self._adjacency[destination].pop(source, None)
        return True

    def has_vertex(self, vertex: int) -> bool:
        """Return whether a vertex exists."""
        self._validate_vertex(vertex)
        return vertex in self._adjacency

    def has_edge(self, source: int, destination: int) -> bool:
        """Return whether an edge exists."""
        self._validate_vertex(source, "Graph edge source must be an integer.")
        self._validate_vertex(destination, "Graph edge destination must be an integer.")
        return source in self._adjacency and destination in self._adjacency[source]

    def neighbors(self, vertex: int) -> tuple[tuple[int, int], ...]:
        """Return neighboring vertices and edge weights sorted by vertex."""
        self._validate_vertex(vertex)
        if vertex not in self._adjacency:
            return ()
        return tuple(sorted(self._adjacency[vertex].items()))

    def vertex_count(self) -> int:
        """Return the number of vertices."""
        return len(self._adjacency)

    def edge_count(self) -> int:
        """Return the number of edges."""
        total = sum(len(neighbors) for neighbors in self._adjacency.values())
        if self._directed:
            return total
        return total // 2

    def vertices(self) -> tuple[int, ...]:
        """Return all vertices sorted for deterministic inspection."""
        return tuple(sorted(self._adjacency))

    def adjacency_list(self) -> dict[int, tuple[tuple[int, int], ...]]:
        """Return a visualization-friendly adjacency-list snapshot."""
        return {vertex: self.neighbors(vertex) for vertex in self.vertices()}

    def edge_weight(self, source: int, destination: int) -> int | None:
        """Return an edge weight, or None when the edge is missing."""
        self._validate_vertex(source, "Graph edge source must be an integer.")
        self._validate_vertex(destination, "Graph edge destination must be an integer.")
        if source not in self._adjacency:
            return None
        return self._adjacency[source].get(destination)

    def display(self) -> str:
        """Return a readable adjacency-list representation."""
        return f"Graph(type={self.graph_type}, adjacency={self.adjacency_list()})"

    def __len__(self) -> int:
        return self.vertex_count()

    def __repr__(self) -> str:
        return f"Graph(directed={self._directed!r}, adjacency={self.adjacency_list()!r})"

    def __str__(self) -> str:
        return self.display()

    @staticmethod
    def _validate_vertex(vertex: int, message: str = "Graph vertices must be integers.") -> None:
        if type(vertex) is not int:
            raise TypeError(message)

    @classmethod
    def _validate_edge_input(cls, source: int, destination: int, weight: int) -> None:
        cls._validate_vertex(source, "Graph edge source must be an integer.")
        cls._validate_vertex(destination, "Graph edge destination must be an integer.")
        if type(weight) is not int:
            raise TypeError("Graph edge weights must be integers.")
        if weight < 0:
            raise ValueError("Graph edge weights must be non-negative.")
