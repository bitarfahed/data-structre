# Round 5 Graph Algorithms

Round 5 extends the graph workspace with Cycle Detection, Topological Sort, and Prim's Minimum Spanning Tree.

## Cycle Detection

`detect_cycle(graph)` checks whether the current graph contains a cycle.

Behavior:

- Supports undirected graphs.
- Supports directed graphs.
- Handles disconnected graphs by checking every component.
- Handles empty graphs safely.
- Returns whether a cycle exists.
- When a cycle is found, returns one detected cycle as vertices and edges where practical.

Undirected graphs use DFS with parent tracking. When traversal reaches an already visited neighbor that is not the current vertex's parent, the algorithm reports a cycle.

Directed graphs use DFS with vertex states:

- `unvisited`
- `visiting`
- `done`

If traversal reaches a vertex currently marked `visiting`, the algorithm has found a back edge and reports a cycle.

Both approaches use the graph's deterministic sorted vertex and neighbor order.

## Topological Sort

`topological_sort(graph)` returns one valid topological ordering for a directed acyclic graph.

Behavior:

- Supports directed graphs only.
- Rejects undirected graphs with a clear message.
- Handles disconnected DAGs.
- Handles empty directed graphs safely.
- If the directed graph contains a cycle, it reports that topological sorting is impossible and does not return a false ordering.

Topological Sort uses Kahn's algorithm:

1. Compute the indegree of every vertex.
2. Add all zero-indegree vertices to a queue.
3. Repeatedly remove one zero-indegree vertex, append it to the output order, and decrement indegrees for its outgoing neighbors.
4. If not every vertex is processed, the graph contains a cycle.

Kahn's algorithm was chosen because indegree values and the zero-indegree queue are easy to visualize.

DFS-based topological sorting is a valid alternative. It is compact and common in algorithm texts, but it hides more of the ordering mechanism in recursive postorder behavior, so it is intentionally not used in this round.

The Topological Sort execution steps expose indegrees, zero-indegree queue contents, the current selected vertex, processed vertices, examined edges, indegree updates, growing topological order, cycle/impossible state, and completion state.

## Prim's Minimum Spanning Tree

`prim_mst(graph, start_vertex)` builds one minimum spanning tree for a connected weighted undirected graph.

Behavior:

- Supports weighted undirected graphs only.
- Rejects directed graphs with a clear message.
- Rejects empty graphs safely.
- Requires a valid start vertex.
- Uses the graph's existing non-negative integer edge weights.
- Grows the MST from the selected start vertex.
- Selects the lowest-weight candidate edge that reaches a not-yet-included vertex.
- Rejects candidate edges that would lead back into the already included MST set.
- Returns the selected MST edges and total MST weight.
- If the graph is disconnected, returns the reachable partial tree and reports that no spanning tree covers all vertices.

Prim uses Python standard-library `heapq` as a priority queue because the learning target is the MST algorithm, not heap implementation. Candidate edge entries are ordered by weight, then source vertex, then destination vertex so equal-weight cases remain deterministic.

Prim builds the MST incrementally from a start vertex. Other MST approaches such as Kruskal belong in separate algorithm modules and are intentionally not implemented in this step.

The Prim execution steps expose the current vertex, included vertices, candidate edges, priority queue contents, selected minimum edge, rejected edges where encountered, growing MST edge set, current total weight, completion state, and disconnected-graph state.

## GUI Visualization

The Graph workspace includes Cycle Detection and Topological Sort as no-input operations. Prim's MST uses a Start vertex input.

Cycle Detection visualization shows:

- current vertex
- visited vertices
- current traversal path
- examined edge
- detected cycle vertices and edges
- clear cycle/no-cycle result

Topological Sort visualization shows:

- current selected vertex
- indegree values
- zero-indegree queue
- processed vertices
- examined edge
- growing topological order
- clear impossible result when a directed cycle prevents sorting

Prim visualization shows:

- current vertex
- included MST vertices
- candidate edges
- selected MST edges
- selected or rejected edge highlights
- current and final total MST weight
- clear disconnected-graph result when a full spanning tree does not exist

## Educational Decisions

בחרנו במקרים פשוטים כי רוצים ללמוד מבלי להרחיב ל-edge cases שלא מוסיפים ערך לימודי.

Round 5 keeps graph algorithms focused on the existing graph model:

- Integer vertices only.
- No self-loops.
- No parallel edges.
- Directed and undirected graph modes only.
- Small educational graphs only.
- One detected cycle is enough for visualization.
- One valid topological ordering is enough for visualization.
- Kahn's algorithm is used for Topological Sort because its queue and indegree state are visible.
- Prim is limited to weighted undirected graphs because MSTs are defined for undirected graphs in this educational round.
- One deterministic MST result is enough when equal-weight alternatives exist.

## Deferred Production-Oriented Alternatives

- Returning all cycles: useful for deeper graph analysis, but it is substantially more complex and not needed for the first cycle-detection lesson.
- Specialized cycle-basis algorithms: useful in graph theory tooling, but outside this educational GUI scope.
- Multigraph cycle handling: useful when parallel edges are allowed, but this project intentionally rejects parallel edges.
- Self-loop cycle handling: useful in general graph libraries, but self-loops are intentionally unsupported by the current graph domain.
- DFS-based topological sorting: useful as a compact alternative, but Kahn's algorithm exposes clearer queue and indegree state for this visualization.
- Returning every possible topological order: useful for exhaustive dependency analysis, but not needed for the educational core.
- Kruskal's MST algorithm: useful as an edge-sorting alternative and valuable for comparing MST strategies, but it should live in its own focused implementation rather than being folded into Prim.
- Directed spanning-tree/arborescence algorithms: useful in specialized graph optimization, but they are a different topic from undirected MSTs.
- Large-graph optimizations: useful in production graph processing, but this project targets small interactive examples.

## Known Limitations

- Cycle Detection returns one detected cycle, not every cycle.
- Cycle Detection follows the existing graph constraints: no self-loops and no parallel edges.
- Topological Sort returns one valid order, not every possible order.
- Topological Sort is directed-only.
- Prim supports weighted undirected graphs only.
- Prim reports disconnected graphs instead of producing a full MST.
- Prim returns one deterministic MST when multiple equal-weight MSTs are possible.
- Kruskal is not implemented yet.
- Visualization is sequential and simple; it does not animate recursive call stack frames separately.
