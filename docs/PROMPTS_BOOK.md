# Prompts Book

This document records the Codex-assisted development process for data_structures_visual_lab.

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

## Round 1 Dynamic Array

Prompt goal: implement only the Round 1 Dynamic Array domain logic while preserving the existing architecture and keeping step/event, visualization, and GUI work deferred.

Work completed:

- Inspected the current project structure, existing data-structure modules, tests, and documentation.
- Added `DynamicArray` in a dedicated data-structure module.
- Exported `DynamicArray` from the data-structures package.
- Added pytest coverage for add/delete behavior, growth, shrinking, minimum capacity, value preservation, invalid indices, empty deletion, non-integer values, duplicate values, and repeated operations.
- Updated the smoke test to include the dynamic-array module.
- Kept the implementation independent from GUI, visualization, and step/event code.

Important implementation direction:

- `DynamicArray` explicitly tracks `size`, `capacity`, minimum capacity, and internal storage.
- Internal storage uses a ctypes object array so the class is not backed by a Python list as its final storage abstraction.
- `add(value)` appends integer values and doubles capacity when size reaches capacity.
- `delete(index)` removes by index, shifts later values left, returns the removed integer, and returns `None` for invalid indices.
- Capacity shrinks by half when size is less than or equal to one quarter of capacity after deletion.
- Capacity never shrinks below the initial minimum capacity.
- Values must be integers, and `bool` is rejected even though it subclasses `int` in Python.

Deferred intentionally:

- Step/event implementation
- Visualization implementation
- GUI implementation

## Shared Step/Event Infrastructure

Prompt goal: implement shared Round 1 step/event infrastructure and integrate it with existing Stack, Queue, Singly Linked List, and Dynamic Array domain operations without adding GUI or visualization rendering.

Work completed:

- Inspected the existing Round 1 data-structure modules, tests, and documentation.
- Added a shared `EventType` enum with `ADD`, `REMOVE`, `VISIT`, `MOVE`, `COMPARE`, `UPDATE`, `RESIZE`, and `COMPLETE`.
- Added a small immutable `Step` dataclass containing an event type, a short message, and optional metadata.
- Exported the event infrastructure from the events package.
- Added step-aware companion methods for Stack, Queue, Linked List, and Dynamic Array operations while preserving the existing method behavior.
- Added pytest coverage for the shared event model and representative operation step sequences.

Important implementation direction:

- Step/event records are GUI-independent and contain only descriptive information for a later visualizer.
- Existing domain methods keep their established return values.
- Step-aware methods use returned event lists or `(result, steps)` tuples depending on whether the operation already has a meaningful result.
- Linked List steps expose traversal and reference updates.
- Dynamic Array steps expose adds, deletes, element movement, growth, shrinking, and capacity changes.

Deferred intentionally:

- Visualization renderer implementation
- GUI implementation

## Round 1 GUI and Visualization Shell

Prompt goal: implement a simple desktop GUI and visualization shell for the existing Round 1 structures without adding new data structures or duplicating domain logic.

Work completed:

- Inspected the current data-structure modules, step/event infrastructure, tests, and documentation.
- Selected Tkinter because it is included with Python and provides basic desktop controls plus a canvas without adding runtime dependencies.
- Added a no-window module entry point check and terminal launch path through `python -m data_structures_visual_lab`.
- Added non-visual GUI controller logic for selecting structures, showing explanations, validating inputs, and invoking existing domain operations.
- Added GUI-independent visualization state objects that consume `Step` metadata and expose values, highlights, messages, size, and capacity.
- Added a simple Tkinter shell with structure selection, explanation screen, operation controls, integer input fields, a canvas visualization area, and Next Step, Play/Pause, and Restart controls.
- Added pytest coverage for controller behavior and visualization state building.

Important implementation direction:

- GUI code calls the existing domain objects and step-aware methods rather than reimplementing data-structure behavior.
- Visualization state lives outside Tkinter so it can be tested and reused by future renderers.
- Stack renders vertically, Queue renders horizontally, Linked List renders nodes with arrows, and Dynamic Array renders indexed capacity cells with size and capacity text.
- Invalid GUI input is handled by the controller and shown as a status message instead of crashing.

Deferred intentionally:

- Visual polish and animations beyond basic playback
- Previous Step playback
- Additional data structures and algorithms

## Round 1 GUI Connection Pass

Prompt goal: fully connect Stack, Queue, Linked List, and Dynamic Array operations to the GUI and Step/Event system while preserving the existing architecture.

Work completed:

- Inspected the current GUI, controller, visualization state, Step/Event infrastructure, and tests.
- Added `display` operations for Stack, Queue, Linked List, and Dynamic Array to the GUI controller.
- Kept all GUI operations routed through the existing domain implementations and step-aware domain methods.
- Added a step-sequence list to the Tkinter shell so the current operation's events are visible during Next Step and Play/Pause playback.
- Improved visual cues for Stack top position, Queue front/back order, and Dynamic Array resize messages.
- Preserved live structure state across multiple operations without restarting the application.
- Added controller and GUI integration tests for display operations, repeated operations, resize metadata, and structure switching.

Bugs fixed:

- Switching structures after selecting an operation from another structure could leave an unsupported operation selected. The GUI now resets to the selected structure's first supported operation when needed.

Deferred intentionally:

- Previous Step playback
- Undo/replay of already-applied domain mutations
- Rich animation and visual polish

## Round 1 Final QA and Stabilization

Prompt goal: perform the final QA and stabilization pass for Round 1 across Stack, Queue, Linked List, Dynamic Array, Step/Event infrastructure, and GUI/visualization integration.

Work completed:

- Inspected the current repository, tests, GUI/controller code, visualization state code, and documentation.
- Ran the full automated test suite before and after stabilization changes.
- Verified domain ordering and edge cases for Stack, Queue, Linked List, and Dynamic Array.
- Verified GUI/controller invalid input handling.
- Verified the Tkinter shell flow for all Round 1 structures through a launched GUI integration check.
- Checked that domain and event layers do not import GUI or Tkinter code.
- Checked that the GUI app does not directly call data-structure operation methods; operation routing stays in the controller.
- Removed an unused visualization helper.

Bugs fixed:

- Step playback for removal operations could show only the already-mutated structure state. Step metadata now carries state snapshots where needed, and visualization state consumes those snapshots so pre-removal and resize moments are visible.
- GUI app tests could create multiple Tk roots and become flaky on the local Tcl/Tk install. The GUI integration coverage now uses a single launched app instance.

Round 1 readiness:

- Round 1 is stable enough to proceed to Round 2.

Remaining limitations:

- The GUI updates immediately after Run and does not provide step playback controls.
- Restart clears the selected structure and starts it over as a new empty instance.
- Visualization remains intentionally simple and lightly styled.

## Round 1 GUI Simplification

Prompt goal: simplify the Round 1 GUI by removing display, Play, and Next Step controls; make Run update immediately; make Restart clear the selected structure; and correct Dynamic Array default capacity behavior.

Work completed:

- Removed display operations from the GUI controller.
- Removed Play, Next Step, step-list, and playback state from the Tkinter shell.
- Changed Restart to replace the currently selected structure with a new empty domain instance and clear operation inputs.
- Changed Dynamic Array default initial capacity and minimum capacity to `1`.
- Kept domain `display()` methods for string representations and tests, but no longer exposes them as GUI operations.
- Updated tests for capacity doubling, shrinking, minimum capacity protection, value preservation, and structure reset behavior.

Important implementation direction:

- The GUI still uses existing domain objects and step-aware methods.
- The GUI now renders the final operation state immediately after Run.
- Dynamic Array capacity follows `1 -> 2 -> 4 -> 8 -> 16` as values are added.

Deferred intentionally:

- Step playback controls
- Previous Step behavior
- Animation beyond immediate redraws

## Round 2 AVL Tree Domain Logic

Prompt goal: implement AVL Tree domain logic while preserving the current architecture and keeping AVL GUI/visualization work deferred.

Work completed:

- Inspected the current project structure, package exports, tests, and documentation.
- Added `AVLNode` and `AVLTree` in a dedicated data-structure module.
- Exported AVL classes from the data-structures package.
- Added package smoke-test coverage for the AVL module.
- Added pytest coverage for BST-style insertion, pending rebalance, blocked insertion, left/right/left-right/right-left rotations, search, min/max, deletion, root deletion, height and balance-factor correctness, duplicate handling, invalid input, repeated insert/balance cycles, and AVL invariants after balancing.

Important implementation direction:

- `insert(value)` performs normal BST insertion only.
- If insertion makes the tree unbalanced, `rebalance_pending` becomes `True`.
- Additional insertions return `False` while rebalance is pending.
- `balance()` restores AVL validity and clears the pending state.
- Duplicate values are rejected by returning `False`.
- Values must be integers, and `bool` is rejected even though it subclasses `int` in Python.
- Deletion restores AVL validity immediately and clears any pending rebalance state.

Deferred intentionally:

- AVL GUI controls
- AVL visualization rendering
- Step/Event integration for AVL operations

## Project Rename

Prompt goal: rename the project and Python package consistently to `data_structures_visual_lab`.

Work completed:

- Renamed the Python package directory from `dsa_visual_lab` to `data_structures_visual_lab`.
- Updated source imports, tests, package import smoke tests, README run instructions, CLI entry point imports, and project metadata.
- Updated the intended terminal command to `uv run python -m data_structures_visual_lab`.
- Regenerated `uv.lock` through `uv sync`.

Important notes:

- `pyproject.toml` uses the requested project name `data_structures_visual_lab`.
- `uv.lock` normalizes the package distribution name as `data-structures-visual-lab`, which is expected Python packaging behavior.
- The outer workspace directory remains `Data_Structure` because renaming the current repository folder from inside the running workspace is not safe.

## Round 2 AVL Tree GUI and Visualization

Prompt goal: connect the AVL Tree to the existing GUI and visualization architecture without adding other Round 2 data structures.

Work completed:

- Added AVL Tree to the structure-selection flow.
- Added an educational AVL explanation before the operation workspace.
- Added GUI operations for Insert, Balance, Search, Delete, Min, Max, and Restart.
- Added AVL step-emitting companion methods in the domain module for operation messages and visualization metadata.
- Extended GUI-independent visualization state with tree nodes, parent-child edges, node heights, balance factors, highlighted nodes, unbalanced nodes, and rebalance status.
- Added simple Tkinter tree rendering for values, balance factors, parent-child edges, balanced status, pending-rebalance status, and highlighted results.
- Updated controller, visualization-state, and GUI smoke tests for AVL flows.

Important implementation direction:

- AVL algorithms remain in the domain layer.
- The GUI calls the controller, and the controller calls existing AVL domain methods.
- Insert still performs BST-style insertion only.
- While `rebalance_pending` is true, further inserts are blocked and the GUI disables the Run button when Insert is selected.
- Balance uses existing AVL rotation logic and redraws the rotated tree immediately.
- Search, Min, and Max highlight the resulting path or node through visualization metadata.

Deferred intentionally:

- Animated AVL rotations
- Play, Next Step, and previous-step playback controls
- Additional Round 2 structures
