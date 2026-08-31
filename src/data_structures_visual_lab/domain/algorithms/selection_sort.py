"""Selection Sort algorithm implementation."""

from __future__ import annotations

from data_structures_visual_lab.domain.algorithms.bubble_sort import SortResult
from data_structures_visual_lab.domain.algorithms.state import AlgorithmEventType, AlgorithmStep, make_algorithm_step
from data_structures_visual_lab.domain.algorithms.validation import validate_integer_array


def selection_sort(values: list[int] | tuple[int, ...]) -> SortResult:
    """Sort integer values using Selection Sort and expose visualization steps."""
    validation = validate_integer_array(values)
    if not validation.ok:
        return SortResult(False, (), validation.message, [])

    array = list(validation.values)
    steps: list[AlgorithmStep] = []
    length = len(array)

    for position in range(length):
        min_index = position
        steps.append(
            make_algorithm_step(
                AlgorithmEventType.VISIT,
                f"Start position {position}; current minimum is {array[min_index]}.",
                array,
                current_indices=(position, min_index),
                metadata={"current_position": position, "min_index": min_index, "sorted_prefix_end": position - 1},
            )
        )
        for candidate_index in range(position + 1, length):
            steps.append(
                make_algorithm_step(
                    AlgorithmEventType.COMPARE,
                    f"Compare current minimum {array[min_index]} with {array[candidate_index]}.",
                    array,
                    current_indices=(position, min_index, candidate_index),
                    comparison_indices=(min_index, candidate_index),
                    metadata={
                        "current_position": position,
                        "min_index": min_index,
                        "candidate_index": candidate_index,
                        "sorted_prefix_end": position - 1,
                    },
                )
            )
            if array[candidate_index] < array[min_index]:
                min_index = candidate_index
                steps.append(
                    make_algorithm_step(
                        AlgorithmEventType.VISIT,
                        f"New minimum candidate is {array[min_index]} at index {min_index}.",
                        array,
                        current_indices=(position, min_index),
                        metadata={
                            "current_position": position,
                            "min_index": min_index,
                            "sorted_prefix_end": position - 1,
                        },
                    )
                )

        if min_index != position:
            left = array[position]
            right = array[min_index]
            array[position], array[min_index] = array[min_index], array[position]
            steps.append(
                make_algorithm_step(
                    AlgorithmEventType.SWAP,
                    f"Swap minimum {right} into position {position}.",
                    array,
                    current_indices=(position, min_index),
                    swapped_indices=(position, min_index),
                    metadata={
                        "current_position": position,
                        "min_index": min_index,
                        "swapped_values": (left, right),
                        "sorted_prefix_end": position,
                    },
                )
            )
        else:
            steps.append(
                make_algorithm_step(
                    AlgorithmEventType.MOVE,
                    f"Position {position} already contains the minimum.",
                    array,
                    current_indices=(position,),
                    metadata={"current_position": position, "min_index": min_index, "sorted_prefix_end": position},
                )
            )

    message = "Selection Sort complete."
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
