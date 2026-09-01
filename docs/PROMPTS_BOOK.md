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

## Round 2 Min-Heap Domain Logic

Prompt goal: implement Min-Heap domain logic while preserving the existing architecture and keeping Min-Heap GUI/visualization work deferred.

Work completed:

- Inspected the current project structure, existing data-structure modules, tests, and documentation.
- Added `MinHeap` in a dedicated data-structure module.
- Exported `MinHeap` from the data-structures package.
- Added package smoke-test coverage for the Min-Heap module.
- Added pytest coverage for raw insertion, sift-up repair, raw extraction, heapify-down repair, pending repair state, blocked mutations while repair is pending, duplicate values, empty heap behavior, invalid input, repeated add/repair cycles, repeated extract/repair cycles, minimum value behavior, display strings, and heap invariants after repair.

Important implementation direction:

- `add_raw(value)` appends without restoring heap order.
- If append violates heap order, `repair_pending` becomes `True` and `repair_index` points at the appended value.
- While repair is pending, additional add and extract operations are blocked.
- `sift_up()` repairs a pending raw insertion.
- `extract_raw()` removes the root and replaces it with the last value without heapifying.
- If extraction violates heap order, `repair_pending` becomes `True` and `repair_index` points at the root.
- `heapify_down()` repairs a pending raw extraction.
- Duplicate integer values are allowed.
- The implementation does not use Python's `heapq`.

Deferred at that step:

- Min-Heap GUI controls, completed in the next pass
- Min-Heap visualization rendering, completed in the next pass
- Step/Event integration for Min-Heap operations

## Round 2 Min-Heap GUI and Visualization

Prompt goal: connect the Min-Heap to the existing GUI and visualization architecture without adding other Round 2 structures.

Work completed:

- Added Min-Heap to the structure-selection flow.
- Added an educational Min-Heap explanation before the operation workspace.
- Added GUI operations for Add Raw, Sift Up, Extract Raw, Heapify Down, Peek Min, and Restart.
- Added Min-Heap step-emitting companion methods in the domain module for operation messages and visualization metadata.
- Extended GUI-independent visualization state with heap validity, repair-pending state, repair index/kind, heap tree nodes, parent-child edges, and array-cell highlights.
- Added simple Tkinter Min-Heap rendering for the tree view and the underlying array representation.
- Updated controller, visualization-state, and GUI smoke tests for Min-Heap flows.

Important implementation direction:

- Min-Heap algorithms remain in the domain layer.
- The GUI calls the controller, and the controller calls existing Min-Heap domain methods.
- Add Raw appends without heap repair.
- Extract Raw removes the root and applies last-element replacement without heapifying.
- While `repair_pending` is true, Add Raw and Extract Raw are blocked and the GUI disables the Run button for those operations.
- Sift Up repairs pending raw insertion, and Heapify Down repairs pending raw extraction.
- Peek Min highlights the root and safely handles an empty heap.
- Duplicate values remain allowed.

Deferred intentionally:

- Animated sift-up and heapify-down movement
- Play, Next Step, and previous-step playback controls
- Additional Round 2 structures

## Round 2 Hash Table Domain Logic and GUI Integration

Prompt goal: implement Hash Table domain logic and connect it to the existing GUI and visualization architecture without adding the 2-3 Tree or other new structures.

Work completed:

- Added `HashEntry` and `HashTable` in a dedicated data-structure module.
- Exported Hash Table classes from the data-structures package.
- Implemented fixed-bucket separate chaining without using Python `dict` as the table storage.
- Added step-emitting companion methods for insert, search, and delete with bucket index, collision, bucket contents, and affected-entry metadata.
- Added Hash Table to the GUI structure-selection flow with an educational explanation.
- Added GUI operations for Insert, Search, Delete, and Restart.
- Extended GUI-independent visualization state with hash buckets, chained entries, bucket count, calculated bucket index, collision status, and affected-entry highlights.
- Added simple Tkinter rendering for indexed buckets and chained key-value entries.
- Added domain, controller, visualization-state, package import, and GUI smoke coverage.

Important implementation direction:

- Hash Table logic remains independent from GUI code.
- Integer keys and integer values are required; `bool` is rejected.
- The table uses a fixed default bucket count of `8`.
- Collisions are handled with separate chaining.
- Duplicate keys are preserved as multiple entries in the same bucket chain.
- Hash Table keys use the existing second GUI input field labeled as Key, and negative integer keys are allowed.

Deferred intentionally:

- Automatic resizing
- Animated collision traversal
- Additional Round 2 structures

## Round 2 2-3 Tree Domain Logic

Prompt goal: implement 2-3 Tree domain logic while preserving the current architecture and keeping 2-3 Tree GUI/visualization work deferred for the next pass.

Work completed:

- Added `TwoThreeNode`, `TwoThreeNodeSnapshot`, and `TwoThreeTree` in a dedicated data-structure module.
- Exported 2-3 Tree classes from the data-structures package.
- Added package smoke-test coverage for the 2-3 Tree module.
- Added pytest coverage for empty-tree insertion, insertion into 2-nodes, leaf overflow, split behavior, key promotion, root split, upward split propagation, pending repair state, blocked insertion while repair is pending, search, duplicate handling, invalid input, repeated insert/repair cycles, node snapshots, and 2-3 Tree invariants after repair.

Important implementation direction:

- `insert_raw(value)` descends to the appropriate leaf and inserts without completing split/promotion repair.
- If a node has three keys after raw insertion, `repair_pending` becomes `True`.
- Additional raw insertions return `False` while repair is pending.
- `repair()` splits overflowing nodes, promotes the middle key, propagates repair upward when needed, and may create a new root.
- Duplicate integer values are rejected by returning `False`.
- Values must be integers, and `bool` is rejected even though it subclasses `int` in Python.
- Public snapshots expose node keys, child ids, parent ids, and overflowing-node state for future visualization.

Deferred at this step:

- 2-3 Tree GUI controls, completed in the next pass
- 2-3 Tree visualization rendering, completed in the next pass
- Step/Event integration for 2-3 Tree operations, completed in the next pass

## Round 2 2-3 Tree GUI and Visualization

Prompt goal: connect the 2-3 Tree to the existing GUI and visualization architecture without adding other structures or algorithms.

Work completed:

- Added 2-3 Tree to the GUI structure-selection flow with an educational explanation.
- Added GUI operations for Insert Raw, Repair, Search, and Restart.
- Added 2-3 Tree step-emitting companion methods in the domain module for operation messages and visualization metadata.
- Extended GUI-independent visualization state with multi-key tree nodes, parent-child edges, valid state, repair-pending state, invalid-node id, highlighted nodes, and highlighted keys.
- Added simple Tkinter rendering for 2-3 Tree nodes, parent-child edges, overflowing nodes, and valid/repair-required status.
- Updated domain step tests, controller integration tests, visualization-state tests, and GUI smoke coverage.

Important implementation direction:

- 2-3 Tree algorithms remain in the domain layer.
- The GUI calls the controller, and the controller calls existing 2-3 Tree domain methods.
- Insert Raw inserts into the leaf without split/promotion repair.
- While `repair_pending` is true, Insert Raw is blocked and the GUI disables the Run button for that operation.
- Repair uses the domain split and key-promotion behavior, then redraws the repaired tree.
- Search highlights the matching node/key when found and reports a clear not-found message otherwise.
- Restart creates a fresh empty 2-3 Tree and clears tree-specific UI state.

Deferred intentionally:

- Animated split and key-promotion movement
- Play, Next Step, and previous-step playback controls
- 2-3 Tree deletion
- Additional Round 2 structures

## Round 2 Final QA and Stabilization

Prompt goal: perform final QA across AVL Tree, Min-Heap, Hash Table, 2-3 Tree, GUI/controller integration, and existing Round 1 behavior before closing Round 2.

Work completed:

- Inspected the current repository state, Round 2 documentation, GUI/controller code, visualization state, and domain boundary references.
- Ran the full automated pytest suite.
- Manually drove the Tkinter GUI flow for AVL Tree, Min-Heap, Hash Table, 2-3 Tree, and a Round 1 smoke path in the same app instance.
- Verified AVL pending rebalance, blocked insertion, Balance, search, delete, min/max, restart, and all four rotation cases through GUI/controller interactions.
- Verified Min-Heap pending repair, blocked raw mutation, Sift Up, Extract Raw, Heapify Down, Peek Min, duplicates, and restart through GUI/controller interactions.
- Verified Hash Table collisions, chaining, duplicate-key behavior, search/delete of missing keys, and restart through GUI/controller interactions.
- Verified 2-3 Tree overflow, blocked insertion, split, promotion, root split, recursive upward repair, search, and restart through GUI/controller interactions.
- Checked that domain and event layers still do not import GUI or Tkinter code.

QA result:

- No product bugs were found during this pass.
- One QA-script assumption was corrected: operation-specific Hash Table metadata belongs to the operation step, while fresh snapshots intentionally show durable structure state.
- Round 2 is stable enough to close.

Remaining limitations:

- Visualizations are immediate and simple rather than animated.
- Step playback controls remain deferred.
- Hash Table resizing remains deferred.
- 2-3 Tree deletion remains deferred.
- Additional future structures and algorithms remain deferred.

## Hash Table Duplicate-Key Behavior Change

Prompt goal: change Hash Table duplicate-key behavior so repeated inserts preserve every `(key, value)` pair instead of overwriting the existing entry.

Work completed:

- Updated Hash Table insertion so every insert appends a new entry to the calculated bucket chain.
- Updated `search(key)` to return all values for the key.
- Updated `delete(key)` to remove all entries for the key while preserving unrelated colliding entries.
- Updated step metadata so search can highlight all matching duplicate entries in the visualization.
- Updated controller, visualization-state, domain, and GUI smoke tests for duplicate-key accumulation.
- Updated README and plan documentation to describe the new policy.

Important implementation direction:

- Hash Table logic remains independent from GUI code.
- Collision handling still uses fixed-bucket separate chaining.
- Duplicate keys are treated as accumulated entries, not updates.
- Missing searches return an empty list in the domain layer and a clear not-found result through the controller.

Deferred intentionally:

- Hash Table resizing
- Animated collision traversal

## Round 3 Algorithms Infrastructure

Prompt goal: add shared infrastructure for future array-based searching and sorting algorithms without implementing Binary Search, sorting algorithms, or GUI changes.

Work completed:

- Added shared `AlgorithmEventType`, `AlgorithmState`, and `AlgorithmStep` representations under the domain algorithms package.
- Added `make_algorithm_step(...)` so future algorithms can create normalized immutable snapshots while still choosing returned step lists or generators.
- Added Round 3 validation helpers for integer arrays, comma-separated text input, and Binary Search's ascending sorted-input precondition.
- Added pytest coverage for execution-state metadata, event coverage, empty arrays, single-element arrays, duplicates, sorted arrays, reverse-sorted arrays, invalid input, text parsing, and unsorted Binary Search validation.
- Updated package import smoke coverage.
- Updated README and plan documentation with Round 3 status and edge-case decisions.

Important implementation direction:

- Algorithm infrastructure remains independent from GUI code.
- Round 3 arrays accept integers only; `bool` is rejected because it is not useful educationally even though Python treats it as an `int` subclass.
- Empty arrays, one-element arrays, duplicates, sorted arrays, and reverse-sorted arrays are valid inputs.
- Binary Search will require ascending sorted input and reject unsorted arrays instead of sorting a copy.
- The project continues to target small educational arrays.

Documented alternatives intentionally not chosen:

- Descending-array Binary Search
- Automatically sorting a copy before Binary Search
- Returning first, last, or all duplicate search matches
- Randomized pivot, median-of-three pivot, or 3-way Quick Sort partitioning
- Iterative fallbacks for recursive algorithms
- Large-array GUI limits, pagination, or virtualization
- Generic comparable types instead of integers only

Deferred at this step:

- Binary Search implementation, completed in the next pass
- Sorting algorithm implementations
- Round 3 GUI integration for Binary Search, completed in the next pass

## Round 3 Binary Search with GUI Visualization

Prompt goal: implement Binary Search as the first Round 3 algorithm and connect it to the existing GUI without adding sorting algorithms.

Work completed:

- Added `binary_search(values, target)` in its own algorithm module.
- Added `BinarySearchResult` for the algorithm result, found index, message, and execution steps.
- Reused Round 3 validation to require integer arrays and ascending sorted input.
- Added Binary Search to the GUI under Algorithms / Searching.
- Added array and target inputs using the existing simple Run workflow.
- Added automatic visual progression through Binary Search steps.
- Added array-cell visualization with indices, active range, low/mid/high labels, discarded-range highlighting, and found/not-found status.
- Added pytest coverage for found, not found, first/last positions, duplicates, empty arrays, single-element arrays, unsorted input rejection, invalid input, step metadata, controller behavior, visualization state, package imports, and GUI smoke flow.

Important implementation direction:

- Binary Search logic remains in the domain algorithms package.
- The GUI does not sort input and does not duplicate the search loop.
- Duplicates are allowed, and the algorithm returns one matching occurrence.
- Empty and single-element arrays are handled safely.

Deferred intentionally:

- Additional sorting algorithms
- Manual Play and Next Step controls
- Descending-array Binary Search
- Returning first, last, or all duplicate matches

## Round 3 Simple Sorting Algorithms with GUI Visualization

Prompt goal: implement Bubble Sort, Selection Sort, and Insertion Sort with GUI visualization while keeping Merge Sort, Quick Sort, and Heap Sort deferred.

Work completed:

- Added `bubble_sort.py`, `selection_sort.py`, and `insertion_sort.py` as separate algorithm modules.
- Reused Round 3 integer-array validation for all three sorting algorithms.
- Added step output for Bubble Sort comparisons, swaps, and sorted suffix progress.
- Added step output for Selection Sort current position, minimum candidate, comparisons, and swap/final-position progress.
- Added step output for Insertion Sort current insertion value, sorted-prefix comparisons, shifts, and final insertion position.
- Added Bubble Sort, Selection Sort, and Insertion Sort to the GUI under Algorithms / Sorting.
- Reused the simple automatic algorithm-step visualization for sorting arrays.
- Updated tests for normal sorting, duplicates, empty arrays, single-element arrays, already sorted arrays, reverse-sorted arrays, negative integers, step metadata, controller behavior, package imports, visualization state, and GUI smoke flow.

Important implementation direction:

- Sorting logic remains in the domain algorithms package.
- The GUI does not duplicate sorting loops; it consumes generated algorithm steps.
- The algorithms are intentionally straightforward and educational.
- Input remains integer-only, with duplicate and negative values allowed.

Deferred intentionally:

- Merge Sort
- Quick Sort
- Heap Sort
- Manual Play and Next Step controls
- Advanced sorting optimizations or large-array performance infrastructure

## Round 3 Merge Sort with GUI Visualization

Prompt goal: implement Merge Sort with GUI visualization while keeping Quick Sort and Heap Sort deferred.

Work completed:

- Added `merge_sort.py` as a separate algorithm module.
- Reused Round 3 integer-array validation.
- Implemented standard recursive divide-and-conquer Merge Sort for small educational arrays.
- Added step output for recursive range splitting, left/right subarrays, merge comparisons, appended merged values, and completed merged ranges.
- Added Merge Sort to the GUI under Algorithms / Sorting.
- Reused the simple automatic algorithm-step visualization for indexed array cells.
- Extended visualization state and canvas rendering with split point, merge ranges, completed merged ranges, and compared/affected-element highlighting.
- Updated tests for normal sorting, odd-length arrays, even-length arrays, duplicates, empty arrays, single-element arrays, already sorted arrays, reverse-sorted arrays, negative integers, merge-step metadata, controller behavior, package imports, visualization state, and GUI smoke flow.

Important implementation direction:

- Merge Sort logic remains in the domain algorithms package.
- The GUI does not duplicate the recursive split or merge logic; it consumes generated algorithm steps.
- The implementation intentionally keeps recursion visible rather than adding iterative fallbacks.
- Input remains integer-only, with duplicate and negative values allowed.

Deferred intentionally:

- Quick Sort
- Heap Sort
- Manual Play and Next Step controls
- Iterative recursion-depth fallback behavior
- Advanced large-array visualization infrastructure

## Round 3 Quick Sort with GUI Visualization

Prompt goal: implement Quick Sort with GUI visualization while keeping Heap Sort deferred.

Work completed:

- Added `quick_sort.py` as a separate algorithm module.
- Reused Round 3 integer-array validation.
- Implemented recursive Quick Sort with deterministic Lomuto partitioning.
- Chose the last element of each current range as the pivot so the partition step is easy to follow visually.
- Added step output for pivot choice, partition ranges, comparisons with the pivot, swaps, final pivot position, recursive left/right ranges, and completed state.
- Added Quick Sort to the GUI under Algorithms / Sorting.
- Extended visualization state and canvas rendering with pivot labels, pivot highlighting, and left/right partition range display.
- Updated tests for normal sorting, duplicates, empty arrays, single-element arrays, already sorted arrays, reverse-sorted arrays, negative integers, pivot placement, partition correctness, step metadata, controller behavior, package imports, visualization state, and GUI smoke flow.

Important implementation direction:

- Quick Sort logic remains in the domain algorithms package.
- The GUI does not duplicate partition or recursive sorting logic; it consumes generated algorithm steps.
- The implementation intentionally avoids randomized pivots, median-of-three pivots, 3-way partitioning, and recursion fallbacks in this learning round.
- Input remains integer-only, with duplicate and negative values allowed.

Deferred intentionally:

- Heap Sort
- Manual Play and Next Step controls
- Production-oriented pivot optimizations
- Iterative recursion-depth fallback behavior
- Advanced large-array visualization infrastructure

## Round 3 Heap Sort with GUI Visualization

Prompt goal: implement Heap Sort with GUI visualization without adding additional searching or sorting algorithms.

Work completed:

- Added `heap_sort.py` as a separate algorithm module.
- Reused Round 3 integer-array validation.
- Implemented standard in-place Heap Sort by building a Max-Heap, swapping the root with the end of the active heap, shrinking the heap region, and heapifying down.
- Kept Heap Sort independent from the Round 2 Min-Heap domain object because this algorithm needs a local Max-Heap over the array being sorted.
- Added step output for heap-building phase, active heap range, parent/child comparisons, heapify swaps, root-to-end swaps, sorted suffix growth, and completed state.
- Added Heap Sort to the GUI under Algorithms / Sorting.
- Extended visualization state and canvas rendering with active heap range display while reusing sorted suffix and swap highlighting.
- Updated tests for normal sorting, duplicates, empty arrays, single-element arrays, already sorted arrays, reverse-sorted arrays, negative integers, heap construction correctness, heapify correctness, step metadata, controller behavior, package imports, visualization state, and GUI smoke flow.

Important implementation direction:

- Heap Sort logic remains in the domain algorithms package.
- The GUI does not duplicate Max-Heap construction, extraction, or heapify-down logic; it consumes generated algorithm steps.
- The implementation is intentionally straightforward and does not add unrelated optimizations.
- Input remains integer-only, with duplicate and negative values allowed.

Deferred intentionally:

- Additional searching and sorting algorithms
- Manual Play and Next Step controls
- Advanced large-array visualization infrastructure

## Round 3 Final QA and Stabilization

Prompt goal: perform final QA across Binary Search, Bubble Sort, Selection Sort, Insertion Sort, Merge Sort, Quick Sort, Heap Sort, shared algorithm infrastructure, GUI/controller integration, and compatibility with Rounds 1 and 2.

Work completed:

- Inspected the current repository state, Round 3 documentation, GUI/controller code, visualization state, and algorithm modules.
- Ran the full automated pytest suite.
- Launched the Tkinter GUI and manually drove all Round 3 algorithms through their main flows.
- Verified Binary Search found/not-found behavior, duplicate handling, empty and single-element arrays, unsorted input rejection, and low/mid/high visualization state.
- Verified Bubble Sort, Selection Sort, and Insertion Sort with normal, duplicate, already sorted, reverse-sorted, and negative-integer inputs.
- Verified Merge Sort recursive splitting, odd/even arrays, merge behavior, duplicate handling, and final sorted output.
- Verified Quick Sort last-element pivot behavior, pivot placement, duplicates, sorted/reverse-sorted inputs, and partition visualization.
- Verified Heap Sort Max-Heap construction, heapify behavior, shrinking active heap region, growing sorted suffix, and final sorted output.
- Checked that algorithm and event layers still do not import GUI or Tkinter code.
- Updated README and plan documentation to record Round 3 as stable enough to close.

QA result:

- No product bugs were found during this pass.
- No dead code or unnecessary duplication was removed.
- Round 3 is stable enough to close.

Remaining limitations:

- Additional searching and sorting algorithms remain deferred.
- Visualizations remain simple automatic step progressions without Play, Next Step, Previous Step, or detailed animation controls.
- Production-oriented variants such as randomized pivots, median-of-three pivots, 3-way partitioning, recursion fallbacks, large-array virtualization, and generic comparable values remain intentionally outside this educational round.

## Round 3 Algorithm GUI Custom Input Correction

Prompt goal: ensure Round 3 algorithm GUI screens clearly accept user-provided arrays and targets instead of relying on sample or hardcoded inputs.

Work completed:

- Kept algorithm execution routed through the existing controller and domain algorithm modules.
- Made array inputs visually explicit by widening the editable Array entry for Binary Search and all sorting algorithms.
- Kept Binary Search using a separate Target entry and an editable Array entry.
- Added algorithm-specific status guidance for comma-separated integer arrays.
- Added controller tests proving Binary Search and all sorting algorithms run against the exact custom input text provided.
- Added GUI smoke assertions for the editable Array field and guidance text.

Bug fixed:

- Prevented operation-field refresh from overwriting completed structure-operation status messages after Run.

Important implementation direction:

- No sorting or searching logic was duplicated in the GUI.
- Existing Round 3 parsing and validation rules remain the source of truth.
- Sample values are not used as algorithm inputs.

## Binary Search GUI Input Integration Fix

Prompt goal: fix Binary Search so clicking Run consumes the editable array field and target field.

Work completed:

- Inspected the Binary Search GUI and controller flow.
- Added a dedicated `array_input` state variable and `array_entry` widget for algorithm array input.
- Changed Run handling to pass the dedicated Array field text to the existing controller parser.
- Kept the Target field separate through the existing value input path.
- Updated GUI tests so algorithm screens use the actual Array field instead of the generic index input field.
- Added a regression test proving Binary Search ignores stale generic index text and uses the editable Array field.

Root cause:

- Algorithm screens visually treated the generic index entry as an Array field. This made the controller path work in direct tests, but the GUI did not have a dedicated array input source. The fix makes the array field explicit and routes it on Run.

Important implementation direction:

- Binary Search algorithm logic was not changed.
- Sorting/searching logic was not duplicated in the GUI.
- Binary Search still requires ascending sorted input and rejects unsorted arrays.

## Binary Search Two-Stage GUI Workflow Fix

Prompt goal: fix Binary Search so array loading is explicit and visible before running a search.

Work completed:

- Reproduced the bug where typing an array changed only the input field while the Binary Search visualization snapshot stayed empty.
- Added controller-owned Binary Search loaded-array state.
- Added a dedicated Load Array operation that parses comma-separated integers, requires ascending sorted order, stores the validated array, and exposes it to visualization immediately.
- Changed Search to use the stored loaded array and only read the target input.
- Disabled Search before a valid array is loaded.
- Preserved sorting custom-input behavior and left the Binary Search algorithm unchanged.
- Added regression tests for loading, visualization exposure before search, stored-array search, target changes, rejected invalid/unsorted loads, and restart clearing state.

Root cause:

- Binary Search was still modeled as one combined `search(array, target)` GUI operation. The editable array text was not stored as GUI/controller state, and algorithm snapshots had no values before Search executed.

Important implementation direction:

- Binary Search array state is owned by the GUI controller, not by the canvas drawing code.
- Invalid or unsorted Load Array attempts do not replace the previous valid loaded array.
- Restart clears the loaded array, target, result state, and visualization.

## Round 4 Graph Domain Infrastructure

Prompt goal: add custom graph domain infrastructure for future graph visualizations and algorithms without implementing GUI or algorithms.

Work completed:

- Added `graph.py` with a custom `Graph` domain model.
- Supported directed and undirected graph modes.
- Used a weighted adjacency-list representation.
- Added non-negative integer edge weights for future Dijkstra work.
- Added vertex operations, edge operations, and query methods.
- Exposed deterministic vertex and adjacency-list snapshots for future visualization.
- Added pytest coverage for vertex behavior, edge behavior, weights, counts, directed and undirected behavior, missing vertices, self-loops, duplicate edges, duplicate vertices, and invalid input.
- Added dedicated Round 4 graph design documentation.

Important implementation direction:

- Graph logic remains independent from GUI and visualization code.
- No external graph libraries are used.
- No adjacency matrix is implemented.
- Graph algorithms remain deferred.

## Round 4 Graph GUI Builder

Prompt goal: add Graph to the GUI so users can build directed and undirected weighted graphs without implementing graph algorithms.

Work completed:

- Added Graph to the structure-selection screen.
- Added a short Graph explanation before the workspace.
- Added a directed/undirected type selector.
- Added GUI operations for Add Vertex, Remove Vertex, Add Edge, Remove Edge, and Restart.
- Added Graph-specific integer parsing for vertex, source, destination, and optional weight inputs.
- Reused the existing Graph domain object for all graph rules and mutations.
- Added visualization state for graph nodes, weighted graph edges, graph type, and adjacency snapshots.
- Drew vertices as labeled nodes and edges as weighted connections, with arrows for directed graphs.
- Used deterministic circular placement for small educational graphs.
- Added controller and GUI tests for graph operations, directed mode, undirected mode, validation, visualization state, and restart.

Important implementation direction:

- The GUI does not duplicate graph algorithms or graph mutation rules.
- Restart preserves the selected graph type and creates a new empty graph.
- BFS, DFS, Dijkstra, Connected Components, and other graph algorithms remain deferred.

## Round 4 BFS with GUI Visualization

Prompt goal: implement BFS over the existing Graph domain object and add a simple GUI visualization.

Work completed:

- Added `bfs.py` as a graph algorithm module.
- Implemented queue-based BFS from a selected start vertex.
- Supported directed and undirected graph traversal using the existing graph neighbor API.
- Limited traversal to the reachable component from the start vertex.
- Added BFS execution steps for current vertex, queue contents, visited vertices, traversal order, examined edge, and completion state.
- Added BFS as a Graph GUI operation.
- Reused the existing Graph domain object and did not duplicate traversal logic in the GUI.
- Extended graph visualization state and canvas drawing for BFS queue/order/visited/current/examined-edge display.
- Added pytest coverage for connected, directed, undirected, disconnected, single-vertex, empty-graph, invalid-start, deterministic-order, and step-state behavior.

Important implementation direction:

- BFS is independent from Tkinter and GUI code.
- The GUI consumes BFS steps and renders them sequentially.
- DFS, Dijkstra, Connected Components, and other graph algorithms remain deferred.

## Round 4 DFS with GUI Visualization

Prompt goal: implement iterative DFS over the existing Graph domain object and add a simple GUI visualization.

Work completed:

- Added `dfs.py` as a graph algorithm module.
- Implemented iterative stack-based DFS from a selected start vertex.
- Supported directed and undirected graph traversal using the existing graph neighbor API.
- Limited traversal to the reachable component from the start vertex.
- Used deterministic sorted neighbor order when pushing neighbors onto the stack.
- Added DFS execution steps for current vertex, stack contents, visited vertices, traversal order, examined edge, and completion state.
- Added DFS as a Graph GUI operation.
- Reused the existing Graph domain object and did not duplicate traversal logic in the GUI.
- Extended graph visualization state and canvas drawing for DFS stack/order/visited/current/examined-edge display.
- Added pytest coverage for connected, directed, undirected, disconnected, single-vertex, empty-graph, invalid-start, deterministic-order, and step-state behavior.

Important implementation direction:

- DFS is independent from Tkinter and GUI code.
- The GUI consumes DFS steps and renders them sequentially.
- Iterative DFS was chosen because the explicit stack is easier to visualize; recursive DFS remains a valid alternative but is intentionally deferred.
- Dijkstra, Connected Components, and other graph algorithms remain deferred.

## Round 4 Dijkstra with GUI Visualization

Prompt goal: implement Dijkstra over the existing weighted Graph domain object and add a simple GUI visualization.

Work completed:

- Added `dijkstra.py` as a graph algorithm module.
- Implemented Dijkstra using Python standard-library `heapq` for the priority queue.
- Supported directed and undirected graphs through the existing Graph neighbor API.
- Computed shortest distances from a selected start vertex.
- Added optional target handling with shortest-path reconstruction.
- Kept unreachable vertices as infinity in the GUI and `None` in the domain result.
- Added validation for empty graphs, missing start vertices, missing explicit target vertices, invalid input, and non-negative edge-weight requirements.
- Added Dijkstra execution steps for current/finalized vertex, tentative distances, priority queue contents, predecessor relationships, examined edge, relaxation attempts, distance updates, finalized vertices, completion state, and reconstructed path.
- Added Dijkstra as a Graph GUI operation with Start and optional Target inputs.
- Reused the existing Graph domain object and did not duplicate shortest-path logic in the GUI.
- Extended graph visualization state and canvas drawing for Dijkstra distances, priority queue, finalized vertices, highlighted relaxation edges, and final shortest path.
- Added pytest coverage for weighted shortest paths, directed and undirected graphs, alternative paths, zero-weight edges, unreachable vertices, invalid inputs, path reconstruction, controller integration, visualization state, package imports, and GUI smoke behavior.

Important implementation direction:

- Dijkstra is independent from Tkinter and GUI code.
- The GUI consumes Dijkstra steps and renders them sequentially.
- Dijkstra requires non-negative edge weights. Bellman-Ford is the relevant alternative for negative-weight graphs, but it is intentionally outside the current educational scope.
- Connected Components and other graph algorithms remain deferred.
