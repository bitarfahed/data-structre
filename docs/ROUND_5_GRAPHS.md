# Round 5 Graph Algorithms

Round 5 extends the graph workspace with Cycle Detection.

## Cycle Detection

`detect_cycle(graph)` checks whether the current graph contains a cycle.

Behavior:

- Supports undirected graphs.
- Supports directed graphs.
- Handles disconnected graphs by checking every component.
- Handles empty graphs safely.
- Returns whether a cycle exists.
- When a cycle is found, returns one detected cycle as vertices and edges where practical.

## Detection Approaches

Undirected graphs use DFS with parent tracking. When traversal reaches an already visited neighbor that is not the current vertex's parent, the algorithm reports a cycle.

Directed graphs use DFS with vertex states:

- `unvisited`
- `visiting`
- `done`

If traversal reaches a vertex currently marked `visiting`, the algorithm has found a back edge and reports a cycle.

Both approaches use the graph's deterministic sorted vertex and neighbor order.

## GUI Visualization

The Graph workspace includes Cycle Detection as a no-input operation.

The visualization shows:

- current vertex
- visited vertices
- current traversal path
- examined edge
- detected cycle vertices and edges
- clear cycle/no-cycle result

## Educational Decisions

בחרנו במקרים פשוטים כי רוצים ללמוד מבלי להרחיב ל-edge cases שלא מוסיפים ערך לימודי.

Round 5 keeps cycle detection focused on the existing graph model:

- Integer vertices only.
- No self-loops.
- No parallel edges.
- Directed and undirected graph modes only.
- Small educational graphs only.
- One detected cycle is enough for visualization.

## Deferred Production-Oriented Alternatives

- Returning all cycles: useful for deeper graph analysis, but it is substantially more complex and not needed for the first cycle-detection lesson.
- Specialized cycle-basis algorithms: useful in graph theory tooling, but outside this educational GUI scope.
- Multigraph cycle handling: useful when parallel edges are allowed, but this project intentionally rejects parallel edges.
- Self-loop cycle handling: useful in general graph libraries, but self-loops are intentionally unsupported by the current graph domain.
- Large-graph optimizations: useful in production graph processing, but this project targets small interactive examples.

## Known Limitations

- The algorithm returns one detected cycle, not every cycle.
- Cycle Detection follows the existing graph constraints: no self-loops and no parallel edges.
- Visualization is sequential and simple; it does not animate recursive call stack frames separately.
