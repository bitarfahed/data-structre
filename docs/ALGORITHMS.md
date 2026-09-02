# Algorithms

This document explains the major algorithms currently implemented in `data_structures_visual_lab`.

All algorithms use integer inputs and expose step metadata for the GUI. The GUI visualizes those steps but does not implement the algorithms itself.

## Searching and Sorting

### Binary Search

Problem: find one occurrence of a target value in an ascending sorted array.

Core idea: repeatedly inspect the middle value of the active range. If the middle value is too small, discard the left half. If it is too large, discard the right half.

Main steps:

1. Validate that the array contains integers and is sorted ascending.
2. Track `low`, `high`, and `mid`.
3. Compare `values[mid]` with the target.
4. Return the found index or report not found.

Data structures used: array plus index bounds.

Complexity:

- Time: `O(log n)`
- Space: `O(1)` besides recorded visualization steps

Assumptions and simplifications:

- Input must already be sorted ascending.
- The algorithm does not sort input automatically.
- Duplicate values are allowed, but only one matching occurrence is returned.

GUI visualization:

- Shows indexed cells.
- Highlights `low`, `mid`, and `high`.
- Marks discarded ranges.
- Shows found or not-found result.

### Bubble Sort

Problem: sort an integer array.

Core idea: repeatedly compare adjacent values and swap them if they are out of order. Larger values move toward the end.

Main steps:

1. Compare adjacent pairs.
2. Swap out-of-order values.
3. Treat the end of the array as a growing sorted suffix.
4. Complete when all passes finish.

Data structures used: array.

Complexity:

- Time: `O(n^2)`
- Space: `O(1)` besides recorded visualization steps

Assumptions and simplifications:

- Integer arrays only.
- No advanced early-exit optimization is emphasized beyond the simple educational flow.

GUI visualization:

- Highlights compared adjacent values.
- Updates cells after swaps.
- Shows sorted suffix progress where useful.

### Selection Sort

Problem: sort an integer array.

Core idea: repeatedly find the smallest value in the unsorted suffix and swap it into the current final position.

Main steps:

1. Choose the current position.
2. Scan the remaining suffix for the minimum candidate.
3. Swap the minimum into the current position.
4. Move the sorted prefix boundary forward.

Data structures used: array.

Complexity:

- Time: `O(n^2)`
- Space: `O(1)` besides recorded visualization steps

Assumptions and simplifications:

- Integer arrays only.
- The implementation keeps the standard direct scan behavior for clarity.

GUI visualization:

- Highlights the current position.
- Shows comparisons with the current minimum candidate.
- Updates cells after the final-position swap.

### Insertion Sort

Problem: sort an integer array.

Core idea: maintain a sorted prefix and insert the next value into its correct position by shifting larger values right.

Main steps:

1. Select the current value.
2. Compare it against the sorted prefix.
3. Shift larger values one position right.
4. Insert the current value into the open position.

Data structures used: array.

Complexity:

- Time: `O(n^2)`
- Space: `O(1)` besides recorded visualization steps

Assumptions and simplifications:

- Integer arrays only.
- The implementation shows shifts explicitly because they are central to the algorithm.

GUI visualization:

- Highlights the value being inserted.
- Shows compared prefix values.
- Shows shifted cells and the final insertion position.

### Merge Sort

Problem: sort an integer array.

Core idea: recursively split the array into smaller ranges, then merge sorted ranges back together.

Main steps:

1. Split the current range.
2. Recursively sort the left range.
3. Recursively sort the right range.
4. Merge by comparing the front values of each side.
5. Copy merged values back into the array.

Data structures used: array plus temporary merge lists.

Complexity:

- Time: `O(n log n)`
- Space: `O(n)` for merge storage, plus recorded visualization steps

Assumptions and simplifications:

- Integer arrays only.
- Uses the standard recursive approach.
- No iterative fallback is included because the project targets small educational arrays.

GUI visualization:

- Shows current ranges and split points.
- Shows left/right merge ranges.
- Highlights compared merge values.
- Shows completed merged ranges and final sorted output.

### Quick Sort

Problem: sort an integer array.

Core idea: partition a range around a pivot so values less than or equal to the pivot move left, values greater than the pivot stay right, then recursively sort both sides.

Main steps:

1. Choose the last element of the current range as the pivot.
2. Scan the range using Lomuto partitioning.
3. Swap values less than or equal to the pivot into the lower partition.
4. Move the pivot into its final position.
5. Recursively process left and right partitions.

Data structures used: array plus recursive range bounds.

Complexity:

- Average time: `O(n log n)`
- Worst-case time: `O(n^2)`
- Space: `O(log n)` average recursion depth, plus recorded visualization steps

Assumptions and simplifications:

- Integer arrays only.
- Uses deterministic last-element pivot selection.
- Does not use randomized pivots, median-of-three, or 3-way partitioning.

GUI visualization:

- Highlights the pivot.
- Highlights compared values.
- Updates cells after swaps.
- Shows partition ranges and pivot placement.

### Heap Sort

Problem: sort an integer array.

Core idea: build a Max-Heap in place, then repeatedly move the maximum value to the end of the active heap region.

Main steps:

1. Build a Max-Heap from the input array.
2. Swap the root with the end of the active heap.
3. Shrink the active heap region.
4. Heapify down to restore the Max-Heap property.
5. Continue until the array is sorted.

Data structures used: array interpreted as a binary heap.

Complexity:

- Time: `O(n log n)`
- Space: `O(1)` besides recorded visualization steps

Assumptions and simplifications:

- Integer arrays only.
- Uses an in-place Max-Heap.
- Does not reuse the Round 2 Min-Heap object because Heap Sort needs local Max-Heap behavior over the array.

GUI visualization:

- Shows indexed array cells.
- Highlights parent/child comparisons.
- Shows root-to-end swaps.
- Marks the active heap range and sorted suffix.

## Graph Algorithms

All graph algorithms run on the existing `Graph` domain object. Graph vertices are integers. Edge weights are non-negative integers.

### Breadth-First Search

Problem: traverse vertices reachable from a start vertex by increasing distance in edge count.

Core idea: use a queue to visit the start vertex, then its neighbors, then their neighbors.

Main steps:

1. Validate the start vertex.
2. Enqueue the start vertex and mark it visited.
3. Dequeue the current vertex.
4. Discover unvisited neighbors and enqueue them.
5. Stop when the queue is empty.

Data structures used: queue, visited set, traversal-order list.

Complexity:

- Time: `O(V + E)`
- Space: `O(V)`

Assumptions and simplifications:

- Traverses only the reachable component from the start vertex.
- Supports directed and undirected graphs.
- Uses the graph's deterministic neighbor ordering.

GUI visualization:

- Highlights the current vertex.
- Shows visited vertices, queue contents, traversal order, and examined edge.

### Depth-First Search

Problem: traverse vertices reachable from a start vertex by exploring as deep as possible before backtracking.

Core idea: use an explicit stack to track vertices to visit.

Main steps:

1. Validate the start vertex.
2. Push the start vertex and mark it visited.
3. Pop the current vertex.
4. Push unvisited neighbors.
5. Stop when the stack is empty.

Data structures used: stack, visited set, traversal-order list.

Complexity:

- Time: `O(V + E)`
- Space: `O(V)`

Assumptions and simplifications:

- Implemented iteratively because the stack is easier to visualize.
- Traverses only the reachable component from the start vertex.
- Supports directed and undirected graphs.
- Uses sorted neighbor order consistently; because the stack is LIFO, later pushed neighbors are visited first.

GUI visualization:

- Highlights the current vertex.
- Shows visited vertices, stack contents, traversal order, and examined edge.

### Dijkstra

Problem: compute shortest distances from a start vertex in a weighted graph with non-negative edge weights.

Core idea: repeatedly finalize the not-yet-finalized vertex with the smallest tentative distance, then relax its outgoing edges.

Main steps:

1. Validate graph, start vertex, optional target vertex, and non-negative weights.
2. Initialize distances to infinity except the start vertex.
3. Use a priority queue ordered by tentative distance.
4. Finalize the closest available vertex.
5. Relax outgoing edges.
6. Reconstruct one shortest path when a target is provided.

Data structures used: priority queue via `heapq`, distance map, predecessor map, finalized set.

Complexity:

- Time: `O((V + E) log V)`
- Space: `O(V + E)` including queue entries and recorded steps

Assumptions and simplifications:

- Requires non-negative weights.
- Supports directed and undirected graphs.
- Uses Python standard-library `heapq`.
- Unreachable vertices remain unreachable and are shown as infinity in the GUI.

GUI visualization:

- Highlights current/finalized vertices.
- Shows tentative distances, priority queue contents, examined edge, relaxation updates, and optional shortest path.

### Connected Components

Problem: find all connected components in an undirected graph.

Core idea: repeatedly start BFS from an unvisited vertex and collect all vertices reachable from it.

Main steps:

1. Reject directed graphs.
2. Iterate over all vertices.
3. Start a component search from each unvisited vertex.
4. Visit all reachable vertices.
5. Record the component.

Data structures used: queue, visited set, component lists.

Complexity:

- Time: `O(V + E)`
- Space: `O(V)`

Assumptions and simplifications:

- Supports undirected graphs only.
- Isolated vertices are single-vertex components.
- Directed strongly or weakly connected components are out of scope.

GUI visualization:

- Colors component groups.
- Shows current component, visited vertices, completed components, and component count.

### Cycle Detection

Problem: determine whether a graph contains a cycle.

Core idea: use different DFS state depending on whether the graph is directed or undirected.

Main steps for undirected graphs:

1. DFS through every component.
2. Track each vertex's parent.
3. If an already visited neighbor is not the parent, report a cycle.

Main steps for directed graphs:

1. DFS through every component.
2. Track vertex states: `unvisited`, `visiting`, `done`.
3. If an edge reaches a `visiting` vertex, report a directed cycle.

Data structures used: visited set or vertex-state map, traversal path.

Complexity:

- Time: `O(V + E)`
- Space: `O(V)`

Assumptions and simplifications:

- Supports directed and undirected graphs.
- Returns one detected cycle, not all cycles.
- Existing graph constraints reject self-loops and parallel edges.

GUI visualization:

- Highlights traversal path, examined edge, and detected cycle vertices/edges.
- Shows a clear cycle or no-cycle result.

### Topological Sort

Problem: produce a valid linear ordering of a directed acyclic graph so every source appears before its destinations.

Core idea: use Kahn's algorithm with indegrees and a queue of zero-indegree vertices.

Main steps:

1. Reject undirected graphs.
2. Compute indegree for every vertex.
3. Queue all zero-indegree vertices.
4. Repeatedly remove a vertex, append it to the order, and decrement neighbor indegrees.
5. If not all vertices are processed, report that a cycle makes sorting impossible.

Data structures used: indegree map, zero-indegree queue, processed list.

Complexity:

- Time: `O(V + E)`
- Space: `O(V)`

Assumptions and simplifications:

- Directed graphs only.
- Returns one valid order, not every possible valid order.
- Kahn's algorithm is used because queue and indegree state are visible.

GUI visualization:

- Shows indegree values.
- Shows zero-indegree queue and growing order.
- Highlights processed vertices and examined edges.
- Reports cyclic graphs as impossible.

### Prim's Minimum Spanning Tree

Problem: find a minimum spanning tree for a connected weighted undirected graph.

Core idea: grow a tree from a start vertex by repeatedly selecting the lowest-weight edge that connects the current tree to a new vertex.

Main steps:

1. Reject directed or empty graphs.
2. Validate the start vertex.
3. Add candidate edges from the start vertex to a priority queue.
4. Select the minimum candidate edge.
5. Accept it if it reaches a new vertex.
6. Add new candidate edges from that vertex.
7. Report disconnected graphs if not all vertices can be included.

Data structures used: priority queue via `heapq`, included-vertex set, MST edge list.

Complexity:

- Time: `O(E log E)`
- Space: `O(V + E)`

Assumptions and simplifications:

- Weighted undirected graphs only.
- Edge weights are non-negative integers through the Graph domain rules.
- Equal-weight candidates are ordered deterministically by weight, source, and destination.
- Returns one deterministic MST edge set.

GUI visualization:

- Shows included vertices.
- Shows candidate edge queue.
- Highlights selected MST edges.
- Shows current and final MST weight.
- Reports disconnected graphs clearly.

### Kruskal's Minimum Spanning Tree

Problem: find a minimum spanning tree for a connected weighted undirected graph.

Core idea: sort all edges globally by weight and accept the next lightest edge only if it connects two separate components.

Main steps:

1. Reject directed or empty graphs.
2. Sort edges by weight, source, and destination.
3. Initialize each vertex as its own Union-Find set.
4. Consider edges from lowest to highest weight.
5. Accept edges that merge two sets.
6. Reject edges that would create a cycle.
7. Report disconnected graphs if fewer than `V - 1` edges are selected.

Data structures used: sorted edge list, internal Union-Find, MST edge list.

Complexity:

- Time: `O(E log E)`
- Space: `O(V + E)`

Assumptions and simplifications:

- Weighted undirected graphs only.
- Uses an internal Union-Find with path compression and union by rank.
- Equal-weight edges are processed deterministically.
- Returns one deterministic MST edge set.

GUI visualization:

- Shows sorted edges.
- Shows current disjoint sets.
- Highlights current, accepted, and rejected edges.
- Shows MST edges and total weight.
- Reports disconnected graphs clearly.

## MST Note

Prim and Kruskal solve the same MST problem with different strategies. On the same connected weighted undirected graph, both should produce MSTs with the same minimum total weight. The exact selected edge sets may differ when several valid MSTs exist with equal total weight.
