# Project Requirements Document

## Project

`data_structures_visual_lab` is an interactive Python desktop visualizer for common data structures and algorithms.

## Motivation

Data structures and algorithms are often taught through static diagrams or isolated code snippets. This project connects operations to visible state changes so learners can see how values move, how references change, and how algorithm decisions are made.

## Problem Being Solved

Learners need a small, inspectable environment where they can:

- Choose a structure or algorithm.
- Enter simple integer input.
- Run operations safely.
- See the resulting state and important intermediate algorithm steps.
- Review the code without GUI details being mixed into domain logic.

## Target User

The primary user is a student, junior developer, or portfolio reviewer interested in core data structures, algorithms, and clean Python architecture.

The project is not designed for production data processing, large-scale visualization, or advanced algorithm research.

## Learning Objectives

- Understand basic structure behavior such as LIFO, FIFO, node links, resizing, hashing, balancing, heap repair, and graph adjacency.
- Understand major searching, sorting, and graph algorithms through step-based state changes.
- Learn how architecture boundaries keep domain logic independent from GUI concerns.
- Practice reading tested Python implementations of educational algorithms.

## Functional Requirements

The application must:

- Launch from the terminal with `uv run python -m data_structures_visual_lab`.
- Provide a Tkinter desktop GUI.
- Let the user choose a supported structure or algorithm.
- Show a short explanation before the operation workspace.
- Accept and validate integer-only input.
- Handle invalid input without crashing.
- Run supported operations through existing domain implementations.
- Update the visualization and status message after each operation.
- Preserve the active structure state across repeated operations.
- Provide Restart behavior for clearing the active structure or algorithm state.

## Supported Data Structures

Round 1:

- Stack: `push(value)`, `pop()`, display representation.
- Queue: `enqueue(value)`, `dequeue()`, display representation.
- Singly Linked List: `push(value, index=0)`, `pop(index=0)`, `change_value(index, value)`, display representation.
- Dynamic Array: `add(value)`, `delete(index)`, display representation.

Round 2:

- AVL Tree: `insert(value)`, `balance()`, `search(value)`, `delete(value)`, `min()`, `max()`.
- Min-Heap: `add_raw(value)`, `sift_up()`, `extract_raw()`, `heapify_down()`, `peek_min()`.
- Hash Table: `insert(key, value)`, `search(key)`, `delete(key)`.
- 2-3 Tree: `insert_raw(value)`, `repair()`, `search(value)`.

Graph:

- `add_vertex(vertex)`
- `remove_vertex(vertex)`
- `add_edge(source, destination, weight=1)`
- `remove_edge(source, destination)`
- `has_vertex(vertex)`
- `has_edge(source, destination)`
- `neighbors(vertex)`
- `vertex_count()`
- `edge_count()`

## Supported Algorithms

Searching and sorting:

- Binary Search
- Bubble Sort
- Selection Sort
- Insertion Sort
- Merge Sort
- Quick Sort
- Heap Sort

Graph algorithms:

- BFS
- DFS
- Dijkstra
- Connected Components
- Cycle Detection
- Topological Sort
- Prim's MST
- Kruskal's MST

## Visualization Requirements

The GUI must show:

- Stack as a vertical stack.
- Queue as front-to-back linear order.
- Linked List as nodes with next-reference arrows.
- Dynamic Array as indexed cells with size and capacity.
- Trees and heaps as nodes with parent-child edges.
- Hash Table as indexed buckets with chained entries.
- Graph as vertices and weighted edges, with arrows for directed graphs.
- Algorithm-specific state such as current index, active range, pivot, queue, stack, visited vertices, distances, components, cycles, topological order, MST edges, and total MST weight.

Visualizations should be readable and simple. Pixel-perfect animation is not required.

## Architecture Requirements

The project must maintain these boundaries:

```text
Domain data structures / algorithms
-> Event and step records
-> Visualization state
-> GUI controller
-> Tkinter GUI
```

Requirements:

- Domain data structures and algorithms must not import GUI code or Tkinter.
- GUI code must not duplicate algorithm or data-structure logic.
- The controller may parse input and call domain methods.
- Visualization state may adapt domain snapshots and step metadata for rendering.
- Shared modules should exist only for genuinely reusable logic.

## Testing Requirements

The project must include pytest coverage for:

- Data-structure behavior and edge cases.
- Algorithm correctness.
- Validation rules.
- Step/event metadata.
- Visualization-state conversion.
- GUI controller integration.
- Basic GUI smoke flows that avoid fragile pixel-level checks.

The intended test command is:

```powershell
uv run pytest
```

## Supported Scope

The completed scope covers Rounds 1-5:

- Core linear structures.
- Core tree, heap, and hash table structures.
- Array searching and sorting algorithms.
- Weighted directed/undirected graph infrastructure.
- Major graph traversal, shortest path, component, cycle, ordering, and MST algorithms.
- Simple Tkinter GUI and visualization shell.

## Intentionally Excluded Scope

The project intentionally excludes:

- AI features.
- Databases.
- Authentication.
- Networking and backend services.
- Cloud infrastructure.
- Web deployment.
- External algorithm/data-structure libraries.
- Large-input virtualization or pagination.
- Advanced graph layouts.
- Generic comparable types beyond integers.
- Production-scale performance optimizations.

## GUI Philosophy

The GUI should be a learning tool, not a decorative interface. It should:

- Keep controls visible and direct.
- Avoid unnecessary styling.
- Show the current state clearly.
- Report invalid input clearly.
- Use simple sequential visualization for algorithm steps.
- Keep domain behavior out of drawing code.

## Educational Simplifications

- Integer-only values are used throughout the project.
- Empty inputs and empty structures are handled safely.
- Duplicate values are allowed where useful, but AVL Tree and 2-3 Tree reject duplicates.
- Hash Table duplicate keys are stored as multiple entries.
- Binary Search requires ascending sorted input.
- DFS is iterative to expose stack behavior.
- Dijkstra requires non-negative weights.
- Connected Components is undirected-only.
- Prim and Kruskal are undirected-only MST algorithms.

## Success Criteria

The project is successful when:

- A user can launch the GUI and run every supported operation.
- Visual output reflects the real domain state.
- Invalid input is rejected without crashes.
- Tests cover the implemented scope.
- Documentation explains what exists, how to run it, and why key educational choices were made.
- The repository is understandable as a portfolio project.

## Final Project Boundaries

After Round 5, the project is functionally complete for its current educational scope. Further work should focus on final QA, screenshots, demo material, cleanup, presentation polish, and documentation maintenance rather than adding more algorithms or architectural layers.
