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
