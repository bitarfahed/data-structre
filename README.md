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
- GUI operation controls for the mutating Round 1 operations
- Pytest configuration
- Unit tests for package imports and all Round 1 data structures
- Planning and development-process documentation

Round 2 domain work has started with AVL Tree logic. The GUI and visualization are intentionally simple shells for the Round 1 structures.

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

Round 2 has started with AVL Tree domain logic.

Implemented:

- AVL Tree node and tree classes
- BST-style insertion with separate `balance()`
- Pending-rebalance state that blocks additional insertions
- Search, delete, root delete, min, max
- Left, right, left-right, and right-left rotation behavior
- Height and balance-factor inspection

The AVL Tree is not connected to the GUI or visualization shell yet.
