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

Round 3 starts with Binary Search, simple sorting algorithms, and shared infrastructure for future array-based searching and sorting algorithms. The current work adds:

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
- Sorting GUI flow under Algorithms / Sorting

The algorithm logic is domain-only. It does not import GUI code or choose a renderer. Merge Sort, Quick Sort, and Heap Sort are not implemented yet.

The execution state supports visualization of comparisons, swaps, current indices, active ranges, pivots, merge ranges, found/not-found results, and completed states. Binary Search and the simple sorting algorithms return step lists; future algorithms may return step lists or yield steps from generators depending on what best fits the algorithm.

Binary Search GUI behavior:

- User selects Binary Search under Algorithms / Searching.
- User enters a comma-separated integer array and an integer target.
- The array must already be sorted in ascending order.
- The canvas displays indexed cells, the active search range, low/mid/high labels, discarded ranges, and final found/not-found status.
- The GUI progresses through generated Binary Search steps automatically without Play or Next Step controls.

Simple sorting GUI behavior:

- User selects Bubble Sort, Selection Sort, or Insertion Sort under Algorithms / Sorting.
- User enters a comma-separated integer array.
- The canvas displays indexed cells, compared or affected elements, swaps, shifts, sorted prefix/suffix hints where useful, and final completion status.
- The GUI progresses through generated sorting steps automatically without Play or Next Step controls.

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

Merge Sort, Quick Sort, Heap Sort, and more advanced sorting variants remain deferred.
