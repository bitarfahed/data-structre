# Prompts Book

This document records the Codex-assisted development process for Interactive Data Structures & Algorithms Visual Lab.

## Foundation Step

Prompt goal: create the initial project foundation and architecture without implementing data structures, step events, visualization, or GUI behavior.

Work completed:

- Inspected the existing repository.
- Preserved the existing `.gitignore`.
- Kept runtime dependencies empty.
- Updated `pyproject.toml` with a project description and pytest configuration.
- Added a `src/` package layout with separate areas for domain logic, data structures, algorithms, event infrastructure, visualization, and GUI code.
- Added a minimal smoke test to verify that the package boundaries import correctly.
- Added README and planning documentation.

Important architectural direction:

- Data-structure and algorithm logic must stay independent from visualization and GUI code.
- Step/event infrastructure will be introduced later between domain logic and visualization.
- Each data structure should own its operations in its own module.
- Shared modules should be reserved for genuinely reusable behavior, not merely similar operation names.

Deferred intentionally:

- Stack implementation
- Queue implementation
- Singly Linked List implementation
- Dynamic Array implementation
- Step/event implementation
- Visualization implementation
- GUI implementation

## Round 1 Stack and Queue

Prompt goal: implement only the Round 1 Stack and Queue domain logic while preserving the architecture boundaries.

Work completed:

- Inspected the existing repository structure and project documentation.
- Added `Stack` in its own data-structure module.
- Added `Queue` in its own data-structure module.
- Exported both classes from the data-structures package.
- Added pytest coverage for normal operations, LIFO/FIFO ordering, empty operations, duplicates, invalid input, repeated operations, and display strings.
- Kept Stack and Queue independent from GUI, visualization, and step/event code.

Important implementation direction:

- Stack uses a Python list to demonstrate simple LIFO behavior.
- Queue uses `collections.deque` to demonstrate simple FIFO behavior.
- Both structures accept integers only and reject `bool` even though `bool` is a subclass of `int` in Python.
- Empty `pop` and `dequeue` return `None` instead of raising an exception.

Deferred intentionally:

- Singly Linked List implementation
- Dynamic Array implementation
- Step/event implementation
- Visualization implementation
- GUI implementation
