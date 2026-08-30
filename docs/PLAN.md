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
- Round 2 data structures and algorithms

## Round 2 Scope

Round 2 begins with AVL Tree domain logic.

Implemented:

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

Duplicate values are rejected. This keeps search, deletion, and educational tree diagrams unambiguous.

AVL GUI and visualization support remain deferred.
