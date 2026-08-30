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

All Round 1 structures currently provide domain logic only.

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
- GUI operation controls for all Round 1 structure operations, including display
- Step/Event sequence display with Next Step and Play/Pause controls
- Pytest configuration
- Unit tests for package imports and all Round 1 data structures
- Planning and development-process documentation

No algorithms beyond the Round 1 structures have been implemented yet. The GUI and visualization are intentionally simple shells.

## Round 1 Status

Round 1 is stable enough to proceed to Round 2.

Verified coverage includes:

- Stack LIFO behavior
- Queue FIFO behavior
- Linked List insertion, removal, value changes, and invalid indices
- Dynamic Array growth, shrinking, minimum capacity protection, and value preservation
- Empty-structure operations
- Invalid integer input through the GUI controller
- Step/Event playback snapshots and GUI visualization state

Known limitations:

- Playback is forward-only.
- Restart replays the current operation's step sequence view; it does not undo and rerun the domain mutation.
- The visualization is intentionally simple and not yet animated beyond timed step playback.
