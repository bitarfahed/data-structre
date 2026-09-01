# Round 4 Graph Design

Round 4 starts the graph foundation for future graph visualizations and algorithms. This phase adds domain infrastructure, a simple graph builder GUI, BFS traversal, DFS traversal, and Dijkstra shortest paths. It does not implement Connected Components or other graph algorithms yet.

## Implemented Domain Model

- `Graph`
- Directed and undirected graph modes
- Weighted edges with non-negative integer weights
- Adjacency-list storage
- Integer-only vertices
- Vertex operations: `add_vertex(vertex)`, `remove_vertex(vertex)`
- Edge operations: `add_edge(source, destination, weight=1)`, `remove_edge(source, destination)`
- Queries: `has_vertex(vertex)`, `has_edge(source, destination)`, `neighbors(vertex)`, `vertex_count()`, `edge_count()`
- Visualization-ready inspection: `graph_type`, `directed`, `vertices()`, `adjacency_list()`, and `edge_weight(source, destination)`
- Observable operation steps for GUI status and highlighting

## GUI Builder

The Graph workspace supports:

- Directed or undirected graph selection
- Add Vertex
- Remove Vertex
- Add Edge
- Remove Edge
- Restart

The visualization uses deterministic circular node placement. This keeps small educational graphs readable without introducing a complex layout engine. Directed graphs draw arrows, undirected graphs draw a single connection, and all edges show their weights.

## BFS

`bfs(graph, start_vertex)` runs queue-based Breadth-First Search over the existing `Graph` domain object.

Behavior:

- Traverses only vertices reachable from the selected start vertex.
- Works with directed and undirected graphs.
- Uses the graph's deterministic sorted neighbor order.
- Does not automatically continue into disconnected components.
- Rejects missing start vertices.
- Handles empty graphs safely.

The BFS execution steps expose the current vertex, queue contents, visited vertices, traversal order, examined edge, and completion state for GUI visualization.

## DFS

`dfs(graph, start_vertex)` runs iterative stack-based Depth-First Search over the existing `Graph` domain object.

Behavior:

- Traverses only vertices reachable from the selected start vertex.
- Works with directed and undirected graphs.
- Uses the graph's deterministic sorted neighbor order when pushing neighbors onto the stack.
- Because the stack is LIFO, the highest sorted neighbor is visited first when multiple neighbors are discovered from the same vertex.
- Does not automatically continue into disconnected components.
- Rejects missing start vertices.
- Handles empty graphs safely.

Iterative DFS was chosen for this round because the explicit stack is easier to visualize in the GUI. Recursive DFS is a valid alternative and can be useful for compact textbook implementations, but it hides the call stack from the learner unless extra visualization infrastructure is added.

The DFS execution steps expose the current vertex, stack contents, visited vertices, traversal order, examined edge, and completion state for GUI visualization.

## Dijkstra

`dijkstra(graph, start_vertex, target_vertex=None)` runs shortest-path search over the existing weighted `Graph` domain object.

Behavior:

- Computes shortest distances from the selected start vertex.
- Works with directed and undirected graphs.
- Requires non-negative edge weights.
- Uses Python standard-library `heapq` as the priority queue because the learning target is Dijkstra, not heap implementation.
- Keeps unreachable vertices at infinity in the visualization and as `None` in the domain result.
- Reconstructs one shortest path when a target vertex is provided and reachable.
- Rejects missing start or target vertices.
- Handles empty graphs safely.

The Dijkstra execution steps expose the current finalized vertex, tentative distances, priority queue contents, predecessor relationships, examined edge, relaxation attempts, distance updates, finalized vertices, completion state, and reconstructed path for GUI visualization.

## Architecture Boundary

The graph implementation lives in the domain data-structures package and has no dependency on GUI, Tkinter, visualization rendering, or graph algorithm modules.

The graph exposes deterministic snapshots of vertices and weighted adjacency data so a future visualization layer can render the structure without owning graph behavior.

## Educational Edge-Case Decisions

בחרנו במקרים פשוטים כי רוצים ללמוד מבלי להרחיב ל-edge cases שלא מוסיפים ערך לימודי.

Our Round 4 graph decisions are:

- Use an adjacency list instead of an adjacency matrix. This matches the way most graph algorithms teach neighbor traversal.
- Vertices are integers only. This keeps labels, tests, and future algorithm inputs consistent with earlier rounds.
- Duplicate vertices are rejected. Each vertex has one adjacency entry.
- Duplicate edges are rejected. Re-adding the same edge does not overwrite or add another edge.
- Self-loops are not supported. This keeps first graph diagrams focused on relationships between distinct vertices.
- Parallel edges are not supported. Each source-destination pair has at most one edge.
- Edge weights must be non-negative integers. This prepares the project for Dijkstra without introducing negative-weight behavior.
- Only directed and undirected graphs are supported. The graph type is explicit at construction time.
- Missing vertices and missing edges are handled safely by returning `False` or an empty neighbor list where appropriate.

## Deferred Production-Oriented Alternatives

- Adjacency matrix: useful when graphs are dense or constant-time edge lookup is the central requirement, but it adds storage overhead and is less natural for teaching neighbor traversal in sparse examples.
- Generic vertex types: useful in larger systems where vertices may be strings, objects, or domain identifiers, but integer-only vertices keep parsing and visualization simple.
- Parallel edges and multigraphs: useful for transportation, routing, and network models with multiple relationships between the same endpoints, but they complicate edge identity before the core graph model is established.
- Self-loops: useful in state machines and some graph-theory examples, but they add visual and algorithmic edge cases that are not needed for the first graph round.
- Negative weights: useful for algorithms such as Bellman-Ford, but they are incompatible with standard Dijkstra assumptions. Bellman-Ford is the production-oriented alternative for graphs that may contain negative weights, and it is intentionally outside the current scope.
- Dynamic graph optimizations: useful for large, frequently changing graphs, but the project targets small educational examples.
- Immutable graph representations: useful for concurrent systems, reproducible transformations, and functional-style algorithm pipelines, but mutable operations are easier to demonstrate interactively in this project.

## Known Limitations

- Connected Components and other graph algorithms beyond BFS, DFS, and Dijkstra are not implemented yet.
- The graph does not resize, compact, or optimize storage for large inputs.
- Edge weights can be inspected and updated only by removing and re-adding an edge.
