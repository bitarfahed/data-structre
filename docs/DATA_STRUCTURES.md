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
