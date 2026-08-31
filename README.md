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
Round 3 has started with Binary Search and shared infrastructure for future array-based sorting algorithms.

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

Round 3 has started. Implemented:

- Shared execution-state and step representations for future array-based searching and sorting algorithms
- Metadata support for comparisons, swaps, current indices, current ranges, pivots, merge ranges, found/not-found results, and completed state
- Shared integer-array validation helpers
- Binary Search domain logic with ascending sorted-input validation
- Binary Search GUI selection, array/target inputs, automatic visual step progression, active range display, low/mid/high labels, discarded-range highlighting, and found/not-found status

Sorting algorithms are not implemented yet.
