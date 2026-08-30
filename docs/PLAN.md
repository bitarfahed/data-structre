# Project Plan

## Goals

Interactive Data Structures & Algorithms Visual Lab will help learners see how data structures and algorithms behave as operations run. The project should make each operation understandable through a short explanation, controlled user input, and visual state changes.

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

The step/event layer will eventually translate domain operations into a sequence of events that a visualizer can consume. It is reserved now but intentionally not implemented yet.

The visualization layer will eventually convert events and states into visual representations. It should not own the core rules of a structure or algorithm.

The GUI layer will eventually provide screens, controls, and user interactions. It should orchestrate the experience without embedding data-structure logic.

Each data structure should have its own module containing its own operations. Similar operation names such as `insert`, `delete`, `push`, and `pop` are not a reason to create shared operation files. Shared code should be extracted only when the behavior is genuinely reusable.

## Round 1 Scope

Round 1 will add:

- Stack: implemented
- Queue: implemented
- Singly Linked List implemented with OOP: implemented
- Dynamic Array: implemented

Round 1 should focus on clear, testable domain logic before visualization and GUI work are added. Stack, Queue, Singly Linked List, and Dynamic Array are now available as integer-only domain models with safe empty operations.

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

Step/event infrastructure, visualization, and GUI implementation remain deferred until after the Round 1 domain logic.
