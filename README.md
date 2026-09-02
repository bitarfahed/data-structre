# data_structures_visual_lab

data_structures_visual_lab is a Python educational project for exploring how common data structures and algorithms change step by step.

The planned workflow is:

1. Run the project.
2. Choose a data structure.
3. Read a short explanation.
4. Continue to the operation screen.
5. Choose a supported operation.
6. Enter integer data.
7. Watch the structure and operation update visually.

Run the desktop shell from the terminal:

```powershell
uv run python -m data_structures_visual_lab
```

## Round 1 Scope

Round 1 will focus on these structures:

- Stack: implemented
- Queue: implemented
- Singly Linked List implemented with OOP: implemented
- Dynamic Array: implemented

All Round 1 structures provide domain logic that is used by the GUI shell.

## Architecture

The project is organized around clear boundaries:

```text
Data Structures / Algorithms
-> Step/Event infrastructure
-> Visualization
-> GUI
```

Domain logic should remain independent from visualization and GUI code. Each data structure should eventually live in its own module with its own operations. Shared modules should contain only genuinely reusable behavior.

## Current Status

The project foundation is in place:

- Python package structure under `src/`
- Reserved areas for data structures, algorithms, visualization, and GUI code
- Shared step/event infrastructure for future visualization
- Stack, Queue, Singly Linked List, and Dynamic Array domain implementations
- Simple Tkinter desktop GUI shell
- GUI-independent visualization state support
- GUI operation controls for Round 1 operations and implemented Round 2 structures
- Pytest configuration
- Unit tests for package imports and all Round 1 data structures
- Planning and development-process documentation

Round 2 is implemented and QA-verified for AVL Tree, Min-Heap, Hash Table, and 2-3 Tree support.
Round 3 is implemented and QA-verified for Binary Search, Bubble Sort, Selection Sort, Insertion Sort, Merge Sort, Quick Sort, Heap Sort, and shared array-algorithm infrastructure.
Round 4 graph support has started with a weighted adjacency-list graph, a simple GUI workspace, BFS, DFS, Dijkstra, and Connected Components.

## Round 1 Status

Round 1 is stable enough to proceed to Round 2.

Verified coverage includes:

- Stack LIFO behavior
- Queue FIFO behavior
- Linked List insertion, removal, value changes, and invalid indices
- Dynamic Array growth, shrinking, minimum capacity protection, and value preservation
- Empty-structure operations
- Invalid integer input through the GUI controller
- Step/Event snapshots and GUI visualization state

Known limitations:

- The GUI updates immediately after Run; it does not provide step playback controls.
- Restart clears the selected structure and starts it over as a new empty instance.
- The visualization is intentionally simple and not animated.

## Round 2 Status

Round 2 is stable enough to close.

Implemented:

- 2-3 Tree domain logic with raw insertion and explicit split/promotion repair
- 2-3 Tree pending-repair state, blocked insertion while repair is pending, valid-state checks, node keys, child relationships, and overflowing-node inspection
- 2-3 Tree GUI selection, explanation, operation controls, and Restart support
- Simple 2-3 Tree visualization with multi-key nodes, parent-child edges, overflow highlighting, and valid/repair-required status
- AVL Tree node and tree classes
- BST-style insertion with separate `balance()`
- Pending-rebalance state that blocks additional insertions
- Search, delete, root delete, min, max
- Left, right, left-right, and right-left rotation behavior
- Height and balance-factor inspection
- GUI selection, explanation, operation controls, and Restart support
- Simple tree visualization with node values, balance factors, parent-child edges, and unbalanced-node highlighting
- Min-Heap domain logic with raw add/extract operations and explicit repair operations
- Min-Heap repair-pending state, heap validity checks, size, values, and repair index/value inspection
- Min-Heap GUI selection, explanation, operation controls, and Restart support
- Simple Min-Heap visualization with tree nodes, array indices, underlying array cells, and repair highlighting
- Hash Table domain logic with fixed buckets, separate chaining, and duplicate-key entries
- Hash Table insert, search, delete, duplicate-key accumulation, and collision state
- Hash Table GUI selection, explanation, operation controls, duplicate-key search results, and Restart support
- Simple Hash Table visualization with bucket indices, chained entries, calculated bucket index, collision status, and affected-entry highlighting

Known limitations:

- 2-3 Tree visualization is simple and immediate; it does not animate split or promotion movement.
- AVL visualization is simple and immediate; it does not animate rotations or provide step playback controls.
- Min-Heap visualization is simple and immediate; it does not animate sift-up or heapify-down movement.
- Hash Table uses a fixed bucket count and does not resize automatically.
- 2-3 Tree does not support deletion yet.

## Round 3 Status

Round 3 is stable enough to close.

Implemented and QA-verified:

- Shared execution-state and step representations for future array-based searching and sorting algorithms
- Metadata support for comparisons, swaps, current indices, current ranges, pivots, merge ranges, found/not-found results, and completed state
- Shared integer-array validation helpers
- Binary Search domain logic with ascending sorted-input validation
- Binary Search GUI selection, two-stage Load Array/Search workflow, editable sorted-array input, separate target input, automatic visual step progression, active range display, low/mid/high labels, discarded-range highlighting, and found/not-found status
- Bubble Sort, Selection Sort, and Insertion Sort domain logic
- Sorting GUI selection, editable array input, automatic visual step progression, compared/affected-element highlighting, swap/shift updates, and completion status
- Merge Sort domain logic with recursive split/merge execution steps
- Merge Sort GUI selection, array input, automatic visual step progression, split/merge range display, compared-value highlighting, and final sorted output
- Quick Sort domain logic using deterministic last-element-pivot partitioning
- Quick Sort GUI selection, array input, automatic visual step progression, pivot highlighting, partition-range display, swap updates, and final sorted output
- Heap Sort domain logic using in-place Max-Heap construction and root extraction
- Heap Sort GUI selection, array input, automatic visual step progression, active heap range display, parent/child comparison highlighting, root swap updates, sorted suffix display, and final sorted output

Simplified educational decisions:

- Round 3 algorithms accept integers only.
- Empty arrays and single-element arrays are valid and handled safely.
- Duplicate and negative integer values are allowed.
- Binary Search requires the user to Load Array first, requires ascending sorted input, and rejects unsorted input instead of sorting it.
- Visualizations target small educational arrays and use simple automatic progression.

Production-oriented alternatives intentionally deferred:

- Descending-order Binary Search
- Automatically sorting before Binary Search
- Returning first, last, or all duplicate search matches
- Randomized or median-of-three Quick Sort pivots
- 3-way Quick Sort partitioning
- Recursion-depth fallbacks
- Large-array pagination or virtualization
- Generic comparable types

Known limitations:

- Additional searching and sorting algorithms are not implemented yet.
- The GUI does not provide Play, Next Step, Previous Step, or detailed animation controls.
- The visualizer is intended for small learning examples rather than large production-sized arrays.

## Round 4 Status

Round 4 is stable enough to close.

Graph domain infrastructure, GUI builder support, and graph algorithms are in place.

Implemented:

- Custom `Graph` domain model
- Directed and undirected graph modes
- Weighted edges with non-negative integer weights
- Adjacency-list representation
- Integer-only vertices
- Add/remove vertex and edge operations
- Vertex, edge, neighbor, vertex-count, and edge-count queries
- Visualization-ready graph type, vertex list, weighted adjacency list, and edge-weight inspection
- Graph GUI selection, explanation, directed/undirected type selector, operation controls, and Restart support
- Simple graph visualization with deterministic circular node placement, weighted edges, and directed arrows
- BFS domain algorithm with queue-based traversal from a selected start vertex
- BFS GUI operation with sequential current-vertex, visited-vertex, queue, traversal-order, and examined-edge visualization
- DFS domain algorithm with iterative stack-based traversal from a selected start vertex
- DFS GUI operation with sequential current-vertex, visited-vertex, stack, traversal-order, and examined-edge visualization
- Dijkstra domain algorithm with non-negative weighted shortest paths from a selected start vertex
- Optional Dijkstra target path reconstruction
- Dijkstra GUI operation with current vertex, finalized vertices, tentative distances, priority queue, examined-edge, relaxation, and shortest-path visualization
- Connected Components domain algorithm for undirected graphs
- Connected Components GUI operation with component count, component membership, visited vertices, examined-edge highlighting, and visually distinct component colors

Verified coverage includes:

- Graph add/remove vertex and edge operations
- Directed and undirected weighted graph behavior
- Graph constraints for integer vertices, duplicate vertices/edges, self-loops, missing vertices, and negative weights
- BFS queue, visited-state, traversal-order, connected/disconnected, directed/undirected, invalid-start, and empty-graph behavior
- DFS stack, visited-state, deterministic traversal, connected/disconnected, directed/undirected, invalid-start, and empty-graph behavior
- Dijkstra directed/undirected weighted shortest paths, alternative paths, relaxation, tentative distances, priority queue state, zero-weight edges, unreachable vertices, invalid start/target, no-path result, and path reconstruction
- Connected Components one-component, multi-component, isolated-vertex, disconnected, empty-graph, directed-rejection, count, and membership behavior
- Compatibility with existing Round 1, Round 2, and Round 3 tests and representative GUI flows

Known limitations:

- Graph algorithms beyond BFS, DFS, Dijkstra, Connected Components, Cycle Detection, Topological Sort, Prim, and Kruskal are not implemented yet.
- Dijkstra intentionally does not support negative edge weights; Bellman-Ford is the relevant alternative for that case and is outside the current scope.
- Connected Components is intentionally undirected-only; directed strongly/weakly connected components are outside the current scope.

## Round 5 Status

Round 5 is stable enough to close.

Round 5 extends the existing Graph workspace with Cycle Detection, Topological Sort, Prim's Minimum Spanning Tree, and Kruskal's Minimum Spanning Tree.

Implemented:

- Cycle Detection domain algorithm
- Undirected cycle detection using DFS with parent tracking
- Directed cycle detection using DFS vertex-state tracking
- Disconnected-graph handling across all components
- Empty-graph handling
- Detected cycle vertices and edges where practical
- Cycle Detection GUI operation
- Simple cycle visualization with current vertex, traversal path, examined edge, and detected-cycle highlighting
- Topological Sort domain algorithm for directed acyclic graphs
- Kahn's algorithm using indegree tracking and a zero-indegree queue
- Cycle rejection for directed graphs that cannot be topologically sorted
- Topological Sort GUI operation
- Simple topological visualization with indegree values, zero-indegree queue, processed vertices, examined edges, and growing order
- Prim's MST domain algorithm for weighted undirected graphs
- Priority-queue based MST construction from a selected start vertex
- Disconnected-graph handling that reports no full spanning tree exists
- Prim GUI operation
- Simple MST visualization with included vertices, candidate edges, selected MST edges, and total weight
- Kruskal's MST domain algorithm for weighted undirected graphs
- Union-Find based cycle prevention while processing globally sorted edges
- Kruskal GUI operation
- Simple MST visualization with sorted edges, disjoint sets, accepted/rejected edges, and total weight

Verified coverage includes:

- Cycle Detection directed and undirected behavior, cyclic and acyclic graphs, disconnected graphs, empty graphs, and cycle highlighting
- Topological Sort DAGs, disconnected DAGs, multiple-valid-order cases, cycle rejection, undirected rejection, empty graphs, and indegree/queue/order visualization
- Prim connected weighted graphs, equal-weight edges, selected MST edges, total weight, single vertex, disconnected graphs, invalid starts, directed rejection, and MST visualization
- Kruskal connected weighted graphs, equal-weight edges, cycle-causing edge rejection, selected MST edges, total weight, single vertex, disconnected graphs, directed rejection, and accepted/rejected-edge visualization
- Prim and Kruskal both producing the same minimum total weight on the same connected weighted graph
- Compatibility with previous graph algorithms and Rounds 1-4

Known limitations:

- Cycle Detection returns one detected cycle, not all cycles.
- Topological Sort returns one valid order, not every possible valid order.
- Prim supports undirected graphs only and returns one deterministic MST for the selected start vertex.
- Kruskal supports undirected graphs only and returns one deterministic MST when equal-weight alternatives exist.
- Prim and Kruskal may select different valid edge sets when several MSTs share the same minimum total weight.
- The graph domain still intentionally rejects self-loops and parallel edges.
