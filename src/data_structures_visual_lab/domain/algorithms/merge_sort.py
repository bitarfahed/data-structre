"""Merge Sort algorithm implementation."""

from __future__ import annotations

from data_structures_visual_lab.domain.algorithms.bubble_sort import SortResult
from data_structures_visual_lab.domain.algorithms.state import AlgorithmEventType, AlgorithmStep, make_algorithm_step
from data_structures_visual_lab.domain.algorithms.validation import validate_integer_array


def merge_sort(values: list[int] | tuple[int, ...]) -> SortResult:
    """Sort integer values with recursive Merge Sort and expose visualization steps."""
    validation = validate_integer_array(values)
    if not validation.ok:
        return SortResult(False, (), validation.message, [])

    array = list(validation.values)
    steps: list[AlgorithmStep] = []

    if len(array) < 2:
        message = "Merge Sort complete."
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

    _merge_sort_range(array, 0, len(array) - 1, steps)

    message = "Merge Sort complete."
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


def _merge_sort_range(array: list[int], start: int, end: int, steps: list[AlgorithmStep]) -> None:
    if start == end:
        steps.append(
            make_algorithm_step(
                AlgorithmEventType.VISIT,
                f"Range {start}..{end} has one value.",
                array,
                current_indices=(start,),
                current_range=(start, end),
                metadata={"completed_range": (start, end)},
            )
        )
        return

    mid = (start + end) // 2
    steps.append(
        make_algorithm_step(
            AlgorithmEventType.VISIT,
            f"Split range {start}..{end} at {mid}.",
            array,
            current_indices=(start, mid, end),
            current_range=(start, end),
            merge_ranges=((start, mid), (mid + 1, end)),
            metadata={
                "split_index": mid,
                "left_range": (start, mid),
                "right_range": (mid + 1, end),
                "left_values": tuple(array[start : mid + 1]),
                "right_values": tuple(array[mid + 1 : end + 1]),
            },
        )
    )

    _merge_sort_range(array, start, mid, steps)
    _merge_sort_range(array, mid + 1, end, steps)
    _merge(array, start, mid, end, steps)


def _merge(array: list[int], start: int, mid: int, end: int, steps: list[AlgorithmStep]) -> None:
    left = array[start : mid + 1]
    right = array[mid + 1 : end + 1]
    merged: list[int] = []
    left_index = 0
    right_index = 0
    write_index = start

    while left_index < len(left) and right_index < len(right):
        left_value = left[left_index]
        right_value = right[right_index]
        left_global_index = start + left_index
        right_global_index = mid + 1 + right_index
        steps.append(
            make_algorithm_step(
                AlgorithmEventType.COMPARE,
                f"Compare {left_value} and {right_value} while merging {start}..{end}.",
                array,
                current_indices=(left_global_index, right_global_index),
                comparison_indices=(left_global_index, right_global_index),
                current_range=(start, end),
                merge_ranges=((start, mid), (mid + 1, end)),
                metadata={
                    "left_range": (start, mid),
                    "right_range": (mid + 1, end),
                    "write_index": write_index,
                    "compared_values": (left_value, right_value),
                    "merged_values": tuple(merged),
                },
            )
        )

        if left_value <= right_value:
            chosen_value = left_value
            left_index += 1
        else:
            chosen_value = right_value
            right_index += 1
        merged.append(chosen_value)
        steps.append(_append_step(array, start, end, write_index, chosen_value, merged))
        write_index += 1

    while left_index < len(left):
        chosen_value = left[left_index]
        left_index += 1
        merged.append(chosen_value)
        steps.append(_append_step(array, start, end, write_index, chosen_value, merged))
        write_index += 1

    while right_index < len(right):
        chosen_value = right[right_index]
        right_index += 1
        merged.append(chosen_value)
        steps.append(_append_step(array, start, end, write_index, chosen_value, merged))
        write_index += 1

    array[start : end + 1] = merged
    steps.append(
        make_algorithm_step(
            AlgorithmEventType.MERGE,
            f"Merged range {start}..{end}.",
            array,
            current_indices=tuple(range(start, end + 1)),
            current_range=(start, end),
            merge_ranges=((start, end),),
            metadata={
                "completed_range": (start, end),
                "merged_values": tuple(merged),
            },
        )
    )


def _append_step(
    array: list[int],
    start: int,
    end: int,
    write_index: int,
    chosen_value: int,
    merged: list[int],
) -> AlgorithmStep:
    display_values = array.copy()
    display_values[start : start + len(merged)] = merged
    return make_algorithm_step(
        AlgorithmEventType.MERGE,
        f"Append {chosen_value} to the merged result.",
        display_values,
        current_indices=(write_index,),
        current_range=(start, end),
        merge_ranges=((start, start + len(merged) - 1),),
        metadata={
            "appended_value": chosen_value,
            "write_index": write_index,
            "merged_values": tuple(merged),
            "merge_output_range": (start, start + len(merged) - 1),
        },
    )
