"""Quick Sort algorithm implementation."""

from __future__ import annotations

from data_structures_visual_lab.domain.algorithms.bubble_sort import SortResult
from data_structures_visual_lab.domain.algorithms.state import AlgorithmEventType, AlgorithmStep, make_algorithm_step
from data_structures_visual_lab.domain.algorithms.validation import validate_integer_array


def quick_sort(values: list[int] | tuple[int, ...]) -> SortResult:
    """Sort integer values with deterministic last-element-pivot Quick Sort."""
    validation = validate_integer_array(values)
    if not validation.ok:
        return SortResult(False, (), validation.message, [])

    array = list(validation.values)
    steps: list[AlgorithmStep] = []

    if len(array) < 2:
        message = "Quick Sort complete."
        steps.append(
            make_algorithm_step(
                AlgorithmEventType.COMPLETE,
                message,
                array,
                completed=True,
                current_range=(0, max(len(array) - 1, 0)),
                metadata={"completed_range": (0, max(len(array) - 1, 0))},
            )
        )
        return SortResult(True, tuple(array), message, steps)

    _quick_sort_range(array, 0, len(array) - 1, steps)

    message = "Quick Sort complete."
    steps.append(
        make_algorithm_step(
            AlgorithmEventType.COMPLETE,
            message,
            array,
            completed=True,
            current_range=(0, len(array) - 1),
            metadata={"completed_range": (0, len(array) - 1), "sorted_prefix_end": len(array) - 1},
        )
    )
    return SortResult(True, tuple(array), message, steps)


def _quick_sort_range(array: list[int], low: int, high: int, steps: list[AlgorithmStep]) -> None:
    if low > high:
        return
    if low == high:
        steps.append(
            make_algorithm_step(
                AlgorithmEventType.VISIT,
                f"Index {low} is already partitioned.",
                array,
                current_indices=(low,),
                current_range=(low, high),
                metadata={"completed_range": (low, high)},
            )
        )
        return

    pivot_index = _partition(array, low, high, steps)
    left_range = _valid_range(low, pivot_index - 1)
    right_range = _valid_range(pivot_index + 1, high)
    steps.append(
        make_algorithm_step(
            AlgorithmEventType.MOVE,
            f"Pivot {array[pivot_index]} is fixed at index {pivot_index}.",
            array,
            current_indices=(pivot_index,),
            current_range=(low, high),
            pivot_index=pivot_index,
            metadata={
                "pivot_index": pivot_index,
                "pivot_value": array[pivot_index],
                "final_pivot_index": pivot_index,
                "left_partition_range": left_range,
                "right_partition_range": right_range,
                "completed_range": (pivot_index, pivot_index),
            },
        )
    )
    _quick_sort_range(array, low, pivot_index - 1, steps)
    _quick_sort_range(array, pivot_index + 1, high, steps)


def _partition(array: list[int], low: int, high: int, steps: list[AlgorithmStep]) -> int:
    pivot_value = array[high]
    pivot_index = high
    boundary = low
    steps.append(
        make_algorithm_step(
            AlgorithmEventType.PIVOT,
            f"Choose {pivot_value} at index {pivot_index} as the pivot.",
            array,
            current_indices=(pivot_index,),
            current_range=(low, high),
            pivot_index=pivot_index,
            metadata={
                "pivot_index": pivot_index,
                "pivot_value": pivot_value,
                "partition_boundary": boundary,
            },
        )
    )

    for scan_index in range(low, high):
        scan_value = array[scan_index]
        steps.append(
            make_algorithm_step(
                AlgorithmEventType.COMPARE,
                f"Compare {scan_value} with pivot {pivot_value}.",
                array,
                current_indices=(scan_index, pivot_index),
                comparison_indices=(scan_index, pivot_index),
                current_range=(low, high),
                pivot_index=pivot_index,
                metadata={
                    "pivot_index": pivot_index,
                    "pivot_value": pivot_value,
                    "partition_boundary": boundary,
                    "compared_values": (scan_value, pivot_value),
                },
            )
        )
        if scan_value <= pivot_value:
            if boundary != scan_index:
                left_value = array[boundary]
                array[boundary], array[scan_index] = array[scan_index], array[boundary]
                steps.append(
                    make_algorithm_step(
                        AlgorithmEventType.SWAP,
                        f"Swap {scan_value} into the lower partition.",
                        array,
                        current_indices=(boundary, scan_index, pivot_index),
                        swapped_indices=(boundary, scan_index),
                        current_range=(low, high),
                        pivot_index=pivot_index,
                        metadata={
                            "pivot_index": pivot_index,
                            "pivot_value": pivot_value,
                            "partition_boundary": boundary + 1,
                            "swapped_values": (scan_value, left_value),
                        },
                    )
                )
            else:
                steps.append(
                    make_algorithm_step(
                        AlgorithmEventType.MOVE,
                        f"Keep {scan_value} in the lower partition.",
                        array,
                        current_indices=(scan_index, pivot_index),
                        current_range=(low, high),
                        pivot_index=pivot_index,
                        metadata={
                            "pivot_index": pivot_index,
                            "pivot_value": pivot_value,
                            "partition_boundary": boundary + 1,
                        },
                    )
                )
            boundary += 1

    array[boundary], array[high] = array[high], array[boundary]
    left_range = _valid_range(low, boundary - 1)
    right_range = _valid_range(boundary + 1, high)
    steps.append(
        make_algorithm_step(
            AlgorithmEventType.SWAP,
            f"Move pivot {pivot_value} to index {boundary}.",
            array,
            current_indices=(boundary,),
            swapped_indices=(boundary, high),
            current_range=(low, high),
            pivot_index=boundary,
            metadata={
                "pivot_index": boundary,
                "pivot_value": pivot_value,
                "final_pivot_index": boundary,
                "left_partition_range": left_range,
                "right_partition_range": right_range,
                "completed_range": (boundary, boundary),
                "swapped_values": (pivot_value, array[high]),
            },
        )
    )
    return boundary


def _valid_range(start: int, end: int) -> tuple[int, int] | None:
    if start <= end:
        return (start, end)
    return None
