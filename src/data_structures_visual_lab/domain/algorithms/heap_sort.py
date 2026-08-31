"""Heap Sort algorithm implementation."""

from __future__ import annotations

from data_structures_visual_lab.domain.algorithms.bubble_sort import SortResult
from data_structures_visual_lab.domain.algorithms.state import AlgorithmEventType, AlgorithmStep, make_algorithm_step
from data_structures_visual_lab.domain.algorithms.validation import validate_integer_array


def heap_sort(values: list[int] | tuple[int, ...]) -> SortResult:
    """Sort integer values in place by building and draining a Max-Heap."""
    validation = validate_integer_array(values)
    if not validation.ok:
        return SortResult(False, (), validation.message, [])

    array = list(validation.values)
    steps: list[AlgorithmStep] = []
    length = len(array)

    if length < 2:
        message = "Heap Sort complete."
        steps.append(
            make_algorithm_step(
                AlgorithmEventType.COMPLETE,
                message,
                array,
                completed=True,
                current_range=(0, max(length - 1, 0)),
                metadata={"completed_range": (0, max(length - 1, 0)), "active_heap_range": _active_heap_range(length)},
            )
        )
        return SortResult(True, tuple(array), message, steps)

    steps.append(
        make_algorithm_step(
            AlgorithmEventType.VISIT,
            "Build a Max-Heap from the array.",
            array,
            current_range=(0, length - 1),
            metadata={"phase": "build", "active_heap_range": (0, length - 1)},
        )
    )
    for parent_index in range((length // 2) - 1, -1, -1):
        _heapify_down(array, length, parent_index, steps, phase="build", sorted_suffix_start=length)

    steps.append(
        make_algorithm_step(
            AlgorithmEventType.COMPLETE,
            "Max-Heap construction complete.",
            array,
            current_range=(0, length - 1),
            metadata={"phase": "build", "active_heap_range": (0, length - 1), "heap_built": True},
        )
    )

    for heap_size in range(length, 1, -1):
        end_index = heap_size - 1
        root_value = array[0]
        end_value = array[end_index]
        array[0], array[end_index] = array[end_index], array[0]
        steps.append(
            make_algorithm_step(
                AlgorithmEventType.SWAP,
                f"Swap root {root_value} with index {end_index}.",
                array,
                current_indices=(0, end_index),
                swapped_indices=(0, end_index),
                current_range=(0, end_index),
                metadata={
                    "phase": "extract",
                    "active_heap_range": _active_heap_range(heap_size - 1),
                    "sorted_suffix_start": end_index,
                    "swapped_values": (root_value, end_value),
                    "root_to_end_swap": True,
                },
            )
        )
        steps.append(
            make_algorithm_step(
                AlgorithmEventType.MOVE,
                f"Index {end_index} joins the sorted suffix.",
                array,
                current_indices=(end_index,),
                current_range=_active_heap_range(heap_size - 1),
                metadata={
                    "phase": "extract",
                    "active_heap_range": _active_heap_range(heap_size - 1),
                    "sorted_suffix_start": end_index,
                },
            )
        )
        _heapify_down(array, heap_size - 1, 0, steps, phase="extract", sorted_suffix_start=end_index)

    message = "Heap Sort complete."
    steps.append(
        make_algorithm_step(
            AlgorithmEventType.COMPLETE,
            message,
            array,
            completed=True,
            current_range=(0, length - 1),
            metadata={"completed_range": (0, length - 1), "sorted_suffix_start": 0},
        )
    )
    return SortResult(True, tuple(array), message, steps)


def _heapify_down(
    array: list[int],
    heap_size: int,
    parent_index: int,
    steps: list[AlgorithmStep],
    *,
    phase: str,
    sorted_suffix_start: int,
) -> None:
    current_parent = parent_index
    while True:
        left_child = 2 * current_parent + 1
        right_child = 2 * current_parent + 2
        largest = current_parent

        if left_child < heap_size:
            steps.append(_compare_step(array, heap_size, current_parent, left_child, largest, phase, sorted_suffix_start))
            if array[left_child] > array[largest]:
                largest = left_child

        if right_child < heap_size:
            steps.append(_compare_step(array, heap_size, current_parent, right_child, largest, phase, sorted_suffix_start))
            if array[right_child] > array[largest]:
                largest = right_child

        if largest == current_parent:
            steps.append(
                make_algorithm_step(
                    AlgorithmEventType.VISIT,
                    f"Parent at index {current_parent} satisfies the Max-Heap property.",
                    array,
                    current_indices=(current_parent,),
                    current_range=_active_heap_range(heap_size),
                    metadata={
                        "phase": phase,
                        "active_heap_range": _active_heap_range(heap_size),
                        "parent_index": current_parent,
                        "sorted_suffix_start": sorted_suffix_start,
                    },
                )
            )
            return

        parent_value = array[current_parent]
        child_value = array[largest]
        array[current_parent], array[largest] = array[largest], array[current_parent]
        steps.append(
            make_algorithm_step(
                AlgorithmEventType.SWAP,
                f"Swap parent {parent_value} with child {child_value}.",
                array,
                current_indices=(current_parent, largest),
                swapped_indices=(current_parent, largest),
                current_range=_active_heap_range(heap_size),
                metadata={
                    "phase": phase,
                    "active_heap_range": _active_heap_range(heap_size),
                    "parent_index": current_parent,
                    "child_index": largest,
                    "sorted_suffix_start": sorted_suffix_start,
                    "swapped_values": (parent_value, child_value),
                },
            )
        )
        current_parent = largest


def _compare_step(
    array: list[int],
    heap_size: int,
    parent_index: int,
    child_index: int,
    current_largest_index: int,
    phase: str,
    sorted_suffix_start: int,
) -> AlgorithmStep:
    return make_algorithm_step(
        AlgorithmEventType.COMPARE,
        f"Compare parent {array[current_largest_index]} with child {array[child_index]}.",
        array,
        current_indices=(current_largest_index, child_index),
        comparison_indices=(current_largest_index, child_index),
        current_range=_active_heap_range(heap_size),
        metadata={
            "phase": phase,
            "active_heap_range": _active_heap_range(heap_size),
            "parent_index": parent_index,
            "child_index": child_index,
            "current_largest_index": current_largest_index,
            "compared_values": (array[current_largest_index], array[child_index]),
            "sorted_suffix_start": sorted_suffix_start,
        },
    )


def _active_heap_range(heap_size: int) -> tuple[int, int] | None:
    if heap_size > 0:
        return (0, heap_size - 1)
    return None
