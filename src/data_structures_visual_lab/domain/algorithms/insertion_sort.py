"""Insertion Sort algorithm implementation."""

from __future__ import annotations

from data_structures_visual_lab.domain.algorithms.bubble_sort import SortResult
from data_structures_visual_lab.domain.algorithms.state import AlgorithmEventType, AlgorithmStep, make_algorithm_step
from data_structures_visual_lab.domain.algorithms.validation import validate_integer_array


def insertion_sort(values: list[int] | tuple[int, ...]) -> SortResult:
    """Sort integer values using Insertion Sort and expose visualization steps."""
    validation = validate_integer_array(values)
    if not validation.ok:
        return SortResult(False, (), validation.message, [])

    array = list(validation.values)
    steps: list[AlgorithmStep] = []
    length = len(array)

    if length < 2:
        message = "Insertion Sort complete."
        steps.append(
            make_algorithm_step(
                AlgorithmEventType.COMPLETE,
                message,
                array,
                completed=True,
                metadata={"sorted_prefix_end": max(length - 1, -1)},
            )
        )
        return SortResult(True, tuple(array), message, steps)

    for current_index in range(1, length):
        value = array[current_index]
        insert_index = current_index
        steps.append(
            make_algorithm_step(
                AlgorithmEventType.VISIT,
                f"Insert value {value} from index {current_index}.",
                array,
                current_indices=(current_index,),
                metadata={
                    "current_index": current_index,
                    "insert_value": value,
                    "sorted_prefix_end": current_index - 1,
                },
            )
        )

        while insert_index > 0:
            steps.append(
                make_algorithm_step(
                    AlgorithmEventType.COMPARE,
                    f"Compare {array[insert_index - 1]} with value {value}.",
                    array,
                    current_indices=(insert_index - 1, insert_index),
                    comparison_indices=(insert_index - 1, insert_index),
                    metadata={
                        "current_index": current_index,
                        "insert_value": value,
                        "insert_index": insert_index,
                        "sorted_prefix_end": current_index - 1,
                    },
                )
            )
            if array[insert_index - 1] <= value:
                break

            shifted_value = array[insert_index - 1]
            array[insert_index] = shifted_value
            insert_index -= 1
            steps.append(
                make_algorithm_step(
                    AlgorithmEventType.MOVE,
                    f"Shift {shifted_value} one position to the right.",
                    array,
                    current_indices=(insert_index, insert_index + 1),
                    metadata={
                        "current_index": current_index,
                        "insert_value": value,
                        "from_index": insert_index,
                        "to_index": insert_index + 1,
                        "sorted_prefix_end": current_index - 1,
                    },
                )
            )

        array[insert_index] = value
        steps.append(
            make_algorithm_step(
                AlgorithmEventType.MOVE,
                f"Place {value} at index {insert_index}.",
                array,
                current_indices=(insert_index,),
                metadata={
                    "current_index": current_index,
                    "insert_value": value,
                    "insert_index": insert_index,
                    "sorted_prefix_end": current_index,
                },
            )
        )

    message = "Insertion Sort complete."
    steps.append(
        make_algorithm_step(
            AlgorithmEventType.COMPLETE,
            message,
            array,
            completed=True,
            metadata={"sorted_prefix_end": length - 1},
        )
    )
    return SortResult(True, tuple(array), message, steps)
