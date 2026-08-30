# Interactive Data Structures & Algorithms Visual Lab

Interactive Data Structures & Algorithms Visual Lab is a Python educational project for exploring how common data structures and algorithms change step by step.

The planned workflow is:

1. Run the project.
2. Choose a data structure.
3. Read a short explanation.
4. Continue to the operation screen.
5. Choose a supported operation.
6. Enter integer data.
7. Watch the structure and operation update visually.

## Round 1 Scope

Round 1 will focus on these structures:

- Stack: implemented
- Queue: implemented
- Singly Linked List implemented with OOP: implemented
- Dynamic Array

Stack, Queue, and Singly Linked List currently provide domain logic only. Dynamic Array is still planned.

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
- Reserved areas for data structures, algorithms, step/event infrastructure, visualization, and GUI code
- Stack, Queue, and Singly Linked List domain implementations
- Pytest configuration
- Unit tests for package imports, Stack, Queue, and Singly Linked List
- Planning and development-process documentation

No algorithms, GUI, visualization behavior, or step events have been implemented yet.
