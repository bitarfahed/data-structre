# Project Plan

## Goals

data_structures_visual_lab will help learners see how data structures and algorithms behave as operations run. The project should make each operation understandable through a short explanation, controlled user input, and visual state changes.

The long-term goal is an educational visualizer that is easy to extend without mixing algorithm behavior, rendering, and GUI concerns.

## Architecture Boundaries

The intended flow is:

```text
Data Structures / Algorithms
-> Step/Event infrastructure
-> Visualization
-> GUI
```

The data-structure and algorithm layers should contain the actual domain behavior. They should not know about GUI widgets, screens, drawing canvases, colors, or layout.

The step/event layer translates domain operations into small event records that a visualizer can consume later. It stays independent from GUI framework choices and renderer details.

The visualization layer converts structure state and step events into renderer-friendly snapshots. It should not own the core rules of a structure or algorithm.

The GUI layer provides screens, controls, and user interactions. It should orchestrate the experience without embedding data-structure logic.

Each data structure should have its own module containing its own operations. Similar operation names such as `insert`, `delete`, `push`, and `pop` are not a reason to create shared operation files. Shared code should be extracted only when the behavior is genuinely reusable.

## Round 1 Scope

Round 1 will add:

- Stack: implemented
- Queue: implemented
- Singly Linked List implemented with OOP: implemented
- Dynamic Array: implemented

Round 1 focuses on clear, testable domain logic with a simple GUI shell layered on top. Stack, Queue, Singly Linked List, and Dynamic Array are available as integer-only domain models with safe empty operations.

## Planned User Flow

1. Run project.
2. Choose data structure.
3. Read short explanation.
4. Continue.
5. Choose supported operation.
6. Enter integer data.
7. Watch the structure and operation update visually.

## Deferred Work

Future expansion may include trees, hash tables, heaps, and graph algorithms. Those areas are intentionally deferred until the early architecture has been validated by Round 1.

The project should avoid adding AI, databases, authentication, networking, backend services, cloud infrastructure, or unrelated technologies.

The current Tkinter GUI is a first shell for the planned flow. Richer rendering polish remains deferred.
Current mutating Round 1 operations are connected through the GUI. The GUI executes operations immediately on Run, consumes Step/Event output for messages and visualization state, and keeps the domain structures alive across multiple operations on the same selected structure.

## Round 1 QA Result

Round 1 is stable enough to proceed to Round 2.

The final QA pass verified:

- Stack LIFO behavior
- Queue FIFO behavior
- Linked List insertion, removal, and value changes at valid indices
- Linked List invalid and negative index handling
- Dynamic Array growth, shrinking, minimum capacity protection, and value preservation across resize
- Empty-structure operations
- Invalid non-integer GUI input
- Step/Event consistency
- GUI visualization state reflecting domain state and step snapshots
- Domain and event layers remaining independent from GUI code

Remaining limitations are intentionally deferred:

- Step playback controls
- Richer animation and visual polish
- Additional Round 2 data structures and algorithms

## Round 2 Scope

Round 2 is implemented and QA-verified for AVL Tree, Min-Heap, Hash Table, and 2-3 Tree support.

Implemented:

- `TwoThreeNode`
- `TwoThreeNodeSnapshot`
- `TwoThreeTree`
- `insert_raw(value)` as leaf insertion without split/promotion repair
- `repair()` as explicit split and key-promotion repair
- `search(value)`
- Pending-repair state that blocks additional insertions while a node is overflowing
- Node keys, child relationships, tree validity, and overflowing-node inspection
- GUI structure selection and educational explanation for 2-3 Tree
- GUI operations for Insert Raw, Repair, Search, and Restart
- Simple 2-3 Tree visualization with multi-key nodes, parent-child edges, overflow highlighting, and valid/repair-required status
- `AVLNode`
- `AVLTree`
- `insert(value)` as normal BST insertion only
- `balance()` as an explicit separate operation
- Pending-rebalance state that blocks additional insertions while the tree is unbalanced
- `search(value)`
- `delete(value)`
- `min()`
- `max()`
- Height and balance-factor inspection
- GUI structure selection and educational explanation
- GUI operations for Insert, Balance, Search, Delete, Min, Max, and Restart
- Simple visualization with tree nodes, parent-child edges, balance factors, and unbalanced-node highlighting
- `MinHeap`
- `add_raw(value)` as append-only insertion
- `sift_up()` as explicit post-insert heap repair
- `extract_raw()` as root removal with last-element replacement only
- `heapify_down()` as explicit post-extraction heap repair
- `peek_min()`
- Heap validity, repair-pending state, current size, heap values, and repair index/value inspection
- GUI structure selection and educational explanation for Min-Heap
- GUI operations for Add Raw, Sift Up, Extract Raw, Heapify Down, Peek Min, and Restart
- Simple Min-Heap visualization with tree nodes, parent-child edges, array indices, an underlying array view, and repair highlighting
- `HashEntry`
- `HashTable`
- `insert(key, value)`
- `search(key)`
- `delete(key)`
- Fixed bucket count with separate chaining for collisions
- Duplicate keys stored as additional entries in the same bucket chain
- Search returns all values for a key, and delete removes all entries for a key
- Bucket count, calculated bucket index, bucket contents, and collision inspection
- GUI structure selection and educational explanation for Hash Table
- GUI operations for Insert, Search, Delete, and Restart
- Simple Hash Table visualization with indexed buckets, chained entries, calculated bucket index, collision status, and affected-entry highlighting

AVL Tree duplicate values are rejected. This keeps search, deletion, and educational tree diagrams unambiguous.
Min-Heap duplicate values are allowed.
Hash Table duplicate keys are preserved as multiple entries. Searches return all values for a key, and deletes remove all entries for that key.
2-3 Tree duplicate values are rejected.

## Round 2 QA Result

Round 2 is stable enough to close.

The final QA pass verified:

- AVL insert without automatic balancing, pending rebalance, blocked insertion, Balance, all four rotation cases, search, delete, min/max, and restart
- Min-Heap Add Raw, pending repair, blocked mutation, Sift Up, Extract Raw, Heapify Down, Peek Min, duplicates, and restart
- Hash Table insert, search, delete, collisions, chaining, duplicate-key accumulation, missing keys, and restart
- 2-3 Tree normal insertion, overflow state, blocked insertion, split, promotion, root split, recursive upward repair, search, and restart
- AVL, Min-Heap, Hash Table, and 2-3 Tree structural invariants after repair or mutation
- Existing Round 1 GUI flows and automated tests
- Domain and event layers remaining independent from GUI code

Remaining limitations are intentionally deferred:

- Hash Table resizing
- Richer AVL, Min-Heap, and 2-3 Tree animation
- Step playback controls
- 2-3 Tree deletion
- Additional future structures and algorithms

## Round 3 Scope

Round 3 starts with Binary Search, simple sorting algorithms, Merge Sort, Quick Sort, Heap Sort, and shared infrastructure for future array-based searching and sorting algorithms. The current work adds:

- `AlgorithmEventType`
- `AlgorithmState`
- `AlgorithmStep`
- `make_algorithm_step(...)`
- `ArrayValidationResult`
- `validate_integer_array(...)`
- `parse_integer_array_text(...)`
- `validate_ascending_sorted(...)`
- `binary_search(values, target)`
- Binary Search GUI flow under Algorithms / Searching
- `bubble_sort(values)`
- `selection_sort(values)`
- `insertion_sort(values)`
- `merge_sort(values)`
- `quick_sort(values)`
- `heap_sort(values)`
- Sorting GUI flow under Algorithms / Sorting

The algorithm logic is domain-only. It does not import GUI code or choose a renderer. Additional searching and sorting algorithms are intentionally deferred until the current Round 3 set is stable.

The execution state supports visualization of comparisons, swaps, current indices, active ranges, pivots, merge ranges, found/not-found results, and completed states. Binary Search and the implemented sorting algorithms return step lists; future algorithms may return step lists or yield steps from generators depending on what best fits the algorithm.

Binary Search GUI behavior:

- User selects Binary Search under Algorithms / Searching.
- User enters a comma-separated integer array in an editable Array field.
- User clicks Load Array to parse, validate, store, and immediately display the array before searching.
- The loaded array must already be sorted in ascending order.
- User enters an integer target in a separate Target field and clicks Search.
- Search runs against the stored loaded array, so the array does not need to be re-entered for each target.
- The canvas displays indexed cells, the active search range, low/mid/high labels, discarded ranges, and final found/not-found status.
- The GUI progresses through generated Binary Search steps automatically without Play or Next Step controls.

Sorting GUI behavior:

- User selects Bubble Sort, Selection Sort, Insertion Sort, Merge Sort, Quick Sort, or Heap Sort under Algorithms / Sorting.
- User enters a comma-separated integer array in an editable Array field.
- The canvas displays indexed cells, compared or affected elements, swaps, shifts, pivot positions, partition ranges, split/merge ranges, active heap ranges, sorted prefix/suffix hints where useful, and final completion status.
- The GUI progresses through generated sorting steps automatically without Play or Next Step controls.

Quick Sort partition strategy:

- Quick Sort uses Lomuto partitioning with the last element in the current range as the pivot.
- The partition scan moves values less than or equal to the pivot into the lower partition.
- After the scan, the pivot swaps into its final partition position, then the left and right partition ranges are processed recursively.
- This deterministic strategy is not the most robust production choice for all inputs, but it is easy to follow visually.

Heap Sort strategy:

- Heap Sort builds a Max-Heap in place from the input array.
- It repeatedly swaps the largest root value with the end of the active heap region.
- After each root swap, the active heap region shrinks and the sorted suffix grows.
- Heapify-down restores the Max-Heap property inside the remaining active heap.
- This stays separate from the Round 2 Min-Heap domain object because Heap Sort needs a Max-Heap over the local array.

## Round 3 Edge Cases

בחרנו במקרים פשוטים כי רוצים ללמוד מבלי להרחיב ל-edge cases שלא מוסיפים ערך לימודי. ההחלטות שלנו ל-edge cases הן:

- Input values are integers only. This keeps parsing, comparison, and visual labeling simple.
- Empty arrays are valid and must be handled safely.
- Single-element arrays are valid and should complete normally.
- Duplicate values are allowed.
- Already-sorted arrays are valid input.
- Reverse-sorted arrays are valid input.
- Binary Search requires ascending sorted input.
- Binary Search on unsorted input is rejected with a clear validation result instead of silently sorting the input.
- Binary Search only needs to return one matching occurrence when duplicates exist.
- Invalid text or non-integer input is rejected safely.
- Arrays are expected to be small educational examples, so no large-input virtualization or performance infrastructure is planned.
- Floats, strings, custom comparators, and generic comparable types are intentionally out of scope.

Stronger alternatives not chosen for this learning round:

- Binary Search could support descending arrays in a production tool, but that adds a second ordering mode before learners need it.
- The app could automatically sort a copy before Binary Search, but that would hide the core precondition Binary Search depends on.
- Searches could return first, last, or all duplicate matches, but Round 3 will focus on one valid occurrence to keep the first visual explanation clear.
- Quick Sort could use randomized pivots, median-of-three pivots, or 3-way partitioning to improve robustness on difficult inputs, but the initial visual version should show the basic partition idea first.
- Recursive algorithms could include iterative fallbacks to avoid recursion-depth limits, but the project targets small educational arrays where recursion is easier to teach.
- A production GUI could add large-array limits, pagination, or virtualization, but those controls are outside the current learning core.
- A generic algorithm library could accept floats, strings, or custom comparable values, but integer-only input keeps Round 3 consistent with the existing project.

More advanced sorting variants and additional algorithms remain deferred.

## Round 3 QA Result

Round 3 is stable enough to close.

The final QA pass verified:

- Binary Search sorted-input behavior, found and not-found results, duplicates, empty arrays, single-element arrays, unsorted input rejection, and low/mid/high visualization state
- Bubble Sort comparison, swap, sorted-suffix behavior, and GUI visualization across normal, duplicate, sorted, reverse-sorted, and negative-integer inputs
- Selection Sort current-position, minimum-candidate, comparison, swap behavior, and GUI visualization across the agreed Round 3 sort inputs
- Insertion Sort current-value, sorted-prefix comparison, shift, insertion behavior, and GUI visualization across the agreed Round 3 sort inputs
- Merge Sort recursive splitting, odd/even lengths, merge comparisons, appended values, duplicate handling, final sorted result, and split/merge visualization state
- Quick Sort deterministic last-element pivot choice, Lomuto partitioning, pivot placement, duplicate handling, sorted/reverse-sorted inputs, and partition visualization state
- Heap Sort Max-Heap construction, heapify-down behavior, active heap shrinkage, sorted suffix growth, and final sorted result
- Existing Round 1 and Round 2 automated coverage
- Algorithm and event layers remaining independent from GUI code

Remaining limitations are intentionally deferred:

- Additional searching and sorting algorithms
- Play, Next Step, Previous Step, or detailed animation controls
- Production-oriented pivot strategies and recursion-depth fallbacks
- Large-array pagination, limits, or virtualization
- Generic comparable values beyond integers

## Round 4 Scope

Round 4 is stable enough to close.

Round 4 includes graph domain infrastructure, a simple graph builder GUI, BFS traversal, DFS traversal, Dijkstra shortest paths, and Connected Components. Additional graph algorithms are intentionally deferred.

Implemented:

- `Graph`
- Directed and undirected graph modes
- Weighted edges with non-negative integer weights
- Adjacency-list representation
- Integer-only vertices
- `add_vertex(vertex)`
- `remove_vertex(vertex)`
- `add_edge(source, destination, weight=1)`
- `remove_edge(source, destination)`
- `has_vertex(vertex)`
- `has_edge(source, destination)`
- `neighbors(vertex)`
- `vertex_count()`
- `edge_count()`
- Visualization-ready inspection through graph type, vertex list, weighted adjacency list, and edge weights
- GUI structure selection and educational explanation
- Directed/undirected graph type selector
- GUI operations for Add Vertex, Remove Vertex, Add Edge, Remove Edge, and Restart
- Deterministic circular graph visualization with node labels, edge weights, and directed arrows
- `bfs(graph, start_vertex)`
- Queue-based BFS traversal over the reachable component from the selected start vertex
- BFS GUI operation with current vertex, visited vertices, queue contents, traversal order, and examined edge visualization
- `dfs(graph, start_vertex)`
- Iterative stack-based DFS traversal over the reachable component from the selected start vertex
- DFS GUI operation with current vertex, visited vertices, stack contents, traversal order, and examined edge visualization
- DFS uses the graph's sorted neighbor order when pushing neighbors onto the stack; because the stack is LIFO, the highest sorted neighbor is visited first
- `dijkstra(graph, start_vertex, target_vertex=None)`
- Dijkstra shortest-path traversal over non-negative weighted graphs
- Optional shortest-path reconstruction when a target vertex is provided
- Dijkstra GUI operation with current vertex, finalized vertices, tentative distances, priority queue contents, examined edge, relaxation updates, and final path visualization
- Python standard-library `heapq` is used as Dijkstra's priority queue because heap implementation is not the learning target in this step
- Negative weights remain unsupported; Bellman-Ford is a relevant alternative for negative-weight graphs and is intentionally outside the current scope
- `connected_components(graph)`
- BFS-based Connected Components for undirected graphs
- Isolated vertices are returned as single-vertex components
- Directed graphs are rejected clearly because strongly connected and weakly connected components are separate concepts
- Connected Components GUI operation with component count, component membership, current vertex, visited vertices, examined edges, and visually distinct component colors

Round 4 design decisions and intentionally deferred production alternatives are documented in `docs/ROUND_4_GRAPHS.md`.

Deferred intentionally:

- Additional graph algorithms

Verified in final QA:

- Graph builder operations, directed and undirected behavior, weighted edges, invalid operations, and restart
- BFS queue, visited state, traversal order, connected/disconnected behavior, directed/undirected behavior, invalid starts, and empty graph handling
- DFS stack, visited state, deterministic traversal policy, connected/disconnected behavior, directed/undirected behavior, invalid starts, and empty graph handling
- Dijkstra weighted directed and undirected graphs, alternative paths, relaxation behavior, tentative distances, priority queue state, unreachable vertices, zero-weight edges, shortest-path reconstruction, invalid start/target, and no-path results
- Connected Components one-component, multi-component, isolated-vertex, completely disconnected, empty graph, directed rejection, count, and membership behavior
- Graph domain constraints for integer-only vertices, duplicate vertices, duplicate edges, rejected self-loops, rejected parallel edges, rejected negative weights, and incident-edge cleanup after vertex removal
- Compatibility with Round 1, Round 2, and Round 3 automated tests and representative GUI flows

## Round 5 Scope

Round 5 extends the existing Graph workspace with Cycle Detection, Topological Sort, Prim's Minimum Spanning Tree, and Kruskal's Minimum Spanning Tree. Other graph algorithms are intentionally deferred.

Implemented:

- `detect_cycle(graph)`
- Cycle Detection for undirected graphs using DFS with parent tracking
- Cycle Detection for directed graphs using DFS vertex-state tracking
- Disconnected graph handling by checking every component
- Empty graph handling
- One detected cycle returned as vertices and edges where practical
- Cycle Detection GUI operation
- Simple visualization of current vertex, visited vertices, traversal path, examined edge, cycle/no-cycle result, and detected-cycle highlighting
- `topological_sort(graph)`
- Directed-only Topological Sort using Kahn's algorithm
- Indegree and zero-indegree queue state exposed for visualization
- Directed cycle handling with a clear impossible result and no false ordering
- Disconnected DAG handling
- Empty directed graph handling
- Topological Sort GUI operation with indegree values, zero-indegree queue, processed vertices, examined edges, and growing order
- `prim_mst(graph, start_vertex)`
- Weighted-undirected-only Prim's Minimum Spanning Tree using a priority queue
- Clear directed-graph, empty-graph, missing-start, and disconnected-graph validation
- MST edge set and total weight result
- Prim GUI operation with included vertices, candidate edges, selected MST edges, total weight, and disconnected-graph message
- `kruskal_mst(graph)`
- Weighted-undirected-only Kruskal's Minimum Spanning Tree using globally sorted edges
- Internal Union-Find cycle prevention
- Clear directed-graph, empty-graph, and disconnected-graph validation
- MST edge set and total weight result
- Kruskal GUI operation with sorted edges, disjoint sets, accepted MST edges, rejected cycle edges, total weight, and disconnected-graph message

Round 5 design decisions and deferred production-oriented alternatives are documented in `docs/ROUND_5_GRAPHS.md`.

Deferred intentionally:

- Returning every cycle in a graph
- Returning every possible topological ordering
