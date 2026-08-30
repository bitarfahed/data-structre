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

## Round 1 Singly Linked List

Prompt goal: implement only the Round 1 Singly Linked List domain logic while preserving the existing architecture and keeping GUI, visualization, and step/event work deferred.

Work completed:

- Inspected the current project structure, Stack and Queue modules, tests, and documentation.
- Added `Node` and `LinkedList` in a dedicated linked-list data-structure module.
- Exported `Node` and `LinkedList` from the data-structures package.
- Added pytest coverage for insertion, removal, default index behavior, value changes, empty operations, invalid indices, non-integer values, duplicate values, and node reference integrity.
- Updated the smoke test to include the linked-list module.
- Kept the implementation independent from GUI, visualization, and step/event code.

Important implementation direction:

- `LinkedList` uses actual `Node.next` references rather than Python list storage.
- `push(value, index=0)` inserts at the beginning by default and returns `True` when insertion succeeds.
- `pop(index=0)` removes from the beginning by default and returns the removed integer, or `None` when removal is invalid.
- `change_value(index, value)` returns `True` when mutation succeeds and `False` for invalid indices.
- Negative and out-of-range indices are rejected safely without changing the list.
- Values must be integers, and `bool` is rejected even though it subclasses `int` in Python.

Deferred intentionally:

- Dynamic Array implementation
- Step/event implementation
- Visualization implementation
- GUI implementation
