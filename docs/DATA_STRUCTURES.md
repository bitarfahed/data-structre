# Data Structures

This document summarizes the data structures currently implemented in `data_structures_visual_lab`.

All data-structure domain modules are independent from Tkinter and GUI rendering. The GUI calls the controller, the controller calls the domain objects, and visualization state is built from domain snapshots and step metadata.

## Shared Rules

- Values are integers unless a structure explicitly uses key/value pairs.
- `bool` is rejected where integer validation is used because it is not useful as a teaching input even though Python treats it as an `int` subclass.
- Duplicate values are allowed unless the structure documents a stricter policy.
- Invalid operations return safe results or clear validation messages instead of crashing.
- Display/string representation methods are domain utilities; the current GUI focuses on mutating and query operations.

## Round 1 Structures

### Stack

Purpose: demonstrate Last-In, First-Out behavior.

Supported operations:

- `push(value)`
- `pop()`
- `display()`

Behavior:

- `push` adds an integer to the top.
- `pop` removes and returns the top integer.
- Empty `pop` returns `None`.
- Duplicate values are allowed.

Visualization:

- Values are shown vertically.
- The top position is highlighted where useful.

Invariant and complexity:

- Only the top value is added or removed.
- `push`: `O(1)` amortized time.
- `pop`: `O(1)` time.
- Space: `O(n)` for stored values.

### Queue

Purpose: demonstrate First-In, First-Out behavior.

Supported operations:

- `enqueue(value)`
- `dequeue()`
- `display()`

Behavior:

- `enqueue` adds an integer at the back.
- `dequeue` removes and returns the front integer.
- Empty `dequeue` returns `None`.
- Duplicate values are allowed.

Visualization:

- Values are shown horizontally from front to back.
- Front and back positions are labeled where useful.

Invariant and complexity:

- Values leave in the same order they entered.
- `enqueue`: `O(1)` time.
- `dequeue`: `O(1)` time.
- Space: `O(n)` for stored values.

### Singly Linked List

Purpose: demonstrate nodes and one-way references.

Supported operations:

- `push(value, index=0)`
- `pop(index=0)`
- `change_value(index, value)`
- `display()`

Behavior:

- Uses real `Node.next` references.
- `push(value)` inserts at index `0` by default.
- `pop()` removes index `0` by default.
- Indices must be non-negative.
- Out-of-range indices are rejected safely.
- Empty-list operations are handled safely.
- Duplicate values are allowed.

Visualization:

- Nodes are drawn in sequence.
- Next references are shown as arrows.
- Traversal and affected nodes are highlighted where practical.

Invariant and complexity:

- Each node references only the next node.
- `push` at index `0`: `O(1)` time.
- `push`, `pop`, or `change_value` at index `i`: `O(i)` traversal time.
- Space: `O(n)` for nodes.

### Dynamic Array

Purpose: demonstrate contiguous indexed storage, capacity, and resizing.

Supported operations:

- `add(value)`
- `delete(index)`
- `display()`

Behavior:

- Tracks `size`, `capacity`, minimum capacity, and internal storage explicitly.
- Initial and minimum capacity are `1`.
- Adding when full doubles capacity: `1 -> 2 -> 4 -> 8 -> ...`.
- Deleting shifts later values left.
- After deletion, when `size <= capacity / 4`, capacity shrinks by half.
- Capacity never shrinks below `1`.
- Duplicate values are allowed.

Visualization:

- Indexed cells show stored values.
- Size and capacity are shown clearly.
- Growth and shrink behavior is represented through capacity changes.

Invariant and complexity:

- `0 <= size <= capacity`.
- Values occupy indices `0` through `size - 1`.
- `add`: `O(1)` amortized time, `O(n)` when resizing.
- `delete`: `O(n)` time because later values shift left.
- Space: `O(capacity)`.

## Round 2 Structures

### AVL Tree

Purpose: demonstrate binary-search-tree insertion separately from AVL balancing.

Supported operations:

- `insert(value)`
- `balance()`
- `search(value)`
- `delete(value)`
- `min()`
- `max()`

Behavior:

- `insert` performs normal BST insertion only.
- If insertion makes the tree unbalanced, `rebalance_pending` becomes true.
- While rebalance is pending, additional insertions are blocked.
- `balance` restores AVL validity with rotations and clears pending rebalance.
- `delete` uses the domain tree behavior and restores balance immediately.
- Duplicate values are rejected.
- Node heights and balance factors are exposed for inspection.

Visualization:

- Nodes and parent-child edges are drawn as a tree.
- Balance factors are shown near nodes.
- Unbalanced nodes and pending-rebalance status are highlighted.

Invariant and complexity:

- When balanced, every node has balance factor between `-1` and `1`.
- Pending-rebalance mode may temporarily violate AVL balance after BST-style insertion.
- `search`, `min`, and `max`: `O(log n)` when balanced.
- `insert`: `O(h)` for BST insertion before explicit balancing.
- `balance`: `O(n log n)` in this educational implementation because it rebuilds from sorted values.
- `delete`: `O(log n)` typical search/removal plus balancing work.
- Space: `O(n)` for nodes.

### Min-Heap

Purpose: demonstrate heap storage and repair as separate educational phases.

Supported operations:

- `add_raw(value)`
- `sift_up()`
- `extract_raw()`
- `heapify_down()`
- `peek_min()`

Behavior:

- `add_raw` appends without restoring heap order.
- If heap order is violated, repair becomes pending.
- While repair is pending, additional raw add/extract operations are blocked.
- `sift_up` repairs a pending raw insertion.
- `extract_raw` removes the root and performs last-element replacement without finishing heap restoration.
- `heapify_down` repairs a pending extraction.
- Duplicate values are allowed.
- Python `heapq` is not used for this data structure.

Visualization:

- Heap values are shown as a tree.
- The underlying array representation is also shown.
- Repair-required status and repair index are highlighted where practical.

Invariant and complexity:

- When valid, each parent is less than or equal to its children.
- Pending-repair mode may temporarily violate heap order after raw mutation.
- `add_raw`: `O(1)` amortized time.
- `sift_up`: `O(log n)` time.
- `extract_raw`: `O(1)` for the raw replacement step.
- `heapify_down`: `O(log n)` time.
- `peek_min`: `O(1)` time.
- Space: `O(n)`.

### Hash Table

Purpose: demonstrate hashing, buckets, collisions, and separate chaining.

Supported operations:

- `insert(key, value)`
- `search(key)`
- `delete(key)`

Behavior:

- Keys and values are integers.
- Uses separate chaining.
- Default bucket count is fixed at `8`.
- Python `dict` is not used as the hash table implementation.
- Duplicate keys are allowed as multiple entries in the same bucket chain.
- Every insertion appends a new `(key, value)` entry.
- `search(key)` returns all values associated with the key.
- `delete(key)` removes all entries associated with the key.
- Unrelated colliding entries remain in the bucket.

Visualization:

- Buckets are shown by index.
- Entries are shown in bucket chains.
- Calculated bucket index, collisions, and affected entries are highlighted where practical.

Invariant and complexity:

- Every entry is stored in the bucket calculated from its key.
- Duplicate keys may appear multiple times in the same bucket.
- Average `insert`, `search`, and `delete`: `O(1 + k)` for bucket-chain length `k`.
- Worst-case `insert`, `search`, and `delete`: `O(n)` when many entries land in one bucket.
- Space: `O(bucket_count + n)`.

### 2-3 Tree

Purpose: demonstrate multi-key search trees and split/promotion repair.

Supported operations:

- `insert_raw(value)`
- `repair()`
- `search(value)`

Behavior:

- `insert_raw` inserts into the appropriate leaf without completing split/promotion repair.
- Overflowing nodes mark repair as pending.
- While repair is pending, additional insertions are blocked.
- `repair` restores valid 2-3 Tree structure through splits and promotions.
- Repair may propagate upward and may create a new root.
- Duplicate values are rejected.
- Deletion is not implemented.

Visualization:

- Nodes show one or two normal keys, or a temporary overflow state.
- Parent-child edges are drawn.
- Repair-required status and overflowing nodes are highlighted.

Invariant and complexity:

- When valid, internal nodes have two or three children and all leaves are at the same depth.
- Pending-repair mode may temporarily allow an overflowing node.
- `insert_raw`: `O(log n)` traversal when the tree is valid.
- `repair`: `O(log n)` for split/promotion propagation.
- `search`: `O(log n)` when valid.
- Space: `O(n)` for nodes and keys.

## Round 4 Graph Structure

### Graph

Purpose: support graph-building and graph-algorithm visualization.

Supported operations:

- `add_vertex(vertex)`
- `remove_vertex(vertex)`
- `add_edge(source, destination, weight=1)`
- `remove_edge(source, destination)`
- `has_vertex(vertex)`
- `has_edge(source, destination)`
- `neighbors(vertex)`
- `vertex_count()`
- `edge_count()`

Behavior:

- Uses an adjacency list.
- Supports directed and undirected graphs.
- Supports weighted edges with non-negative integer weights.
- Vertices are integers only.
- Duplicate vertices are rejected.
- Duplicate edges and parallel edges are rejected.
- Self-loops are rejected.
- Removing a vertex removes all incident edges.
- Undirected graphs keep both adjacency directions synchronized.
- Directed graphs preserve edge direction.

Visualization:

- Vertices are drawn as nodes.
- Edges are drawn between connected vertices.
- Directed edges show direction.
- Weights are displayed on edges.
- Node placement is deterministic and intentionally simple.

Invariant and complexity:

- Each vertex owns an adjacency entry.
- Undirected edges are stored in both directions and rendered once.
- Directed edges are stored only from source to destination.
- `add_vertex`, `has_vertex`, and `vertex_count`: `O(1)` or `O(V)` depending on snapshot needs.
- `add_edge`, `remove_edge`, and `has_edge`: `O(d)` for the source adjacency degree.
- `neighbors(vertex)`: `O(d)` to return that vertex's neighbors.
- `edge_count`: `O(V + E)` for counting from adjacency data.
- Space: `O(V + E)`.

## Educational Boundaries

The project intentionally avoids production-oriented complexity that would obscure the learning goals:

- No generic vertex or value types.
- No external data-structure libraries.
- No graph adjacency matrix.
- No Hash Table resizing.
- No 2-3 Tree deletion.
- No parallel edges, self-loops, or negative-weight graph edges.
- No advanced graph layout engine.
- No persistence, database, networking, backend service, or cloud infrastructure.
