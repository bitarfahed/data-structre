# data_structures_visual_lab

Interactive Data Structures & Algorithms Visual Lab is a Python desktop application for learning how core data structures and algorithms change as operations run.

The project is designed as a GitHub portfolio project: it emphasizes clear architecture, testable domain logic, simple educational visualizations, and small examples that are easy to inspect.

## Purpose

The application helps learners connect abstract algorithm steps to concrete state changes. A user can choose a structure or algorithm, enter integer data, run an operation, and watch the visual state update.

The implementation intentionally favors readable educational behavior over production-scale optimization.

## Current Features

Supported data structures:

- Stack
- Queue
- Singly Linked List
- Dynamic Array
- AVL Tree
- Min-Heap
- Hash Table
- 2-3 Tree
- Weighted adjacency-list Graph

Supported searching and sorting algorithms:

- Binary Search
- Bubble Sort
- Selection Sort
- Insertion Sort
- Merge Sort
- Quick Sort
- Heap Sort

Supported graph algorithms:

- Breadth-First Search
- Depth-First Search
- Dijkstra shortest paths
- Connected Components
- Cycle Detection
- Topological Sort
- Prim's Minimum Spanning Tree
- Kruskal's Minimum Spanning Tree

## Architecture

The project is organized into clear layers:

```text
Domain data structures / algorithms
-> Event and step records
-> Visualization state
-> GUI controller
-> Tkinter GUI
```

The domain layer contains the actual behavior for structures and algorithms. It does not import Tkinter or GUI code.

The event/step layer records what happened in a form that can be visualized later.

The visualization layer converts domain state and step metadata into renderer-friendly snapshots.

The GUI controller parses user input, owns the active domain objects, and calls the domain layer. The Tkinter GUI draws the current visualization state and does not duplicate data-structure or algorithm implementations.

## Installation

Requirements:

- Python 3.11+
- `uv`
- Tkinter available in the Python installation

Set up dependencies:

```powershell
uv sync
```

The project has no runtime third-party dependencies. Pytest is included as a development dependency.

## Run

Launch the desktop application:

```powershell
uv run python -m data_structures_visual_lab
```

Run a no-window startup check:

```powershell
uv run python -m data_structures_visual_lab --check
```

## Test

Run the full test suite:

```powershell
uv run pytest
```

## Basic GUI Usage

1. Choose a structure or algorithm from the left sidebar.
2. Read the short explanation.
3. Click `Continue`.
4. Choose an operation.
5. Enter the required integer values, indices, array, graph vertices, or edge weights.
6. Click `Run`.
7. Watch the visualization and status message update.

Binary Search uses a two-stage workflow:

1. Enter an ascending sorted comma-separated integer array.
2. Click `Load Array`.
3. Enter a target integer.
4. Click `Search`.

Graph algorithms run on the graph currently built in the Graph workspace. Restart clears the selected structure or graph while preserving the selected graph type.

## Educational Design Decisions

- Inputs are integer-only.
- Duplicate values are allowed where the structure naturally supports them.
- AVL Tree and 2-3 Tree reject duplicates to keep tree diagrams and operations unambiguous.
- Hash Table supports duplicate keys by storing multiple `(key, value)` entries in the same bucket chain.
- Dynamic Array starts with capacity `1`, doubles when full, and shrinks by half when quarter-full without going below capacity `1`.
- AVL insertion is separated from explicit `balance()` so learners can see the unbalanced intermediate state.
- Min-Heap raw mutation is separated from `sift_up()` and `heapify_down()` repair.
- 2-3 Tree raw insertion is separated from `repair()` so overflow and promotion are visible.
- Binary Search rejects unsorted input instead of silently sorting it.
- DFS is iterative so the stack is visible.
- Topological Sort uses Kahn's algorithm because indegree and queue state are easy to visualize.
- Dijkstra requires non-negative edge weights.
- Prim and Kruskal both compute MSTs for weighted undirected graphs, but they expose different strategies.

## Limitations

- The GUI is intentionally simple and uses basic Tkinter drawing.
- Visual playback is automatic and sequential; there are no Play, Next Step, or Previous Step controls.
- The visualizer targets small educational examples, not large production inputs.
- Graph layout is deterministic and simple, not force-directed.
- Connected Components is undirected-only.
- Prim and Kruskal support weighted undirected graphs only.
- Cycle Detection returns one detected cycle, not all cycles.
- Topological Sort returns one valid order, not all valid orders.
- Hash Table uses a fixed bucket count and does not resize.
- 2-3 Tree deletion is not implemented.

## Testing Approach

The test suite covers:

- Domain behavior for every implemented data structure
- Algorithm correctness and important edge cases
- Step/event metadata used by visualizations
- Controller parsing, validation, and operation routing
- GUI smoke/integration flows without fragile pixel-level tests
- Package import structure

## Repository Structure

```text
src/data_structures_visual_lab/
  domain/
    data_structures/      # Stack, Queue, lists, arrays, trees, heaps, hash table, graph
    algorithms/           # Searching, sorting, and graph algorithms
  events/                 # Shared step/event records
  visualization/          # GUI-independent visualization state
  gui/                    # Controller and Tkinter desktop shell
tests/                    # Pytest coverage
docs/                     # Planning, requirements, educational notes, and process log
```

## Documentation

- `docs/PRD.md`: project requirements and boundaries
- `docs/TODO.md`: current completion checklist
- `docs/ALGORITHMS.md`: educational notes for implemented algorithms
- `docs/DATA_STRUCTURES.md`: educational notes for implemented structures
- `docs/PLAN.md`: round-by-round project plan and QA history
- `docs/PROMPTS_BOOK.md`: Codex-assisted development process log
- `docs/ROUND_4_GRAPHS.md`: graph design decisions
- `docs/ROUND_5_GRAPHS.md`: Round 5 graph algorithm decisions

## Current Status

Rounds 1-5 are implemented and QA-verified. The repository is functionally complete for the current educational scope and ready for portfolio presentation work such as screenshots, demo material, and release polish.
