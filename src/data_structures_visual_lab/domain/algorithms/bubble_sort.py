"""Bubble Sort algorithm implementation."""

from __future__ import annotations

from dataclasses import dataclass

from data_structures_visual_lab.domain.algorithms.state import AlgorithmEventType, AlgorithmStep, make_algorithm_step
from data_structures_visual_lab.domain.algorithms.validation import validate_integer_array


@dataclass(frozen=True)
class SortResult:
    """Result of running a sorting algorithm."""

    ok: bool
    values: tuple[int, ...]
    message: str
    steps: list[AlgorithmStep]


def bubble_sort(values: list[int] | tuple[int, ...]) -> SortResult:
    """Sort integer values using Bubble Sort and expose visualization steps."""
    validation = validate_integer_array(values)
    if not validation.ok:
        return SortResult(False, (), validation.message, [])

    array = list(validation.values)
    steps: list[AlgorithmStep] = []
    length = len(array)

    if length < 2:
        message = "Bubble Sort complete."
        steps.append(
            make_algorithm_step(
                AlgorithmEventType.COMPLETE,
                message,
                array,
                completed=True,
                metadata={"sorted_suffix_start": 0},
            )
        )
        return SortResult(True, tuple(array), message, steps)

    for pass_index in range(length - 1):
        for index in range(length - pass_index - 1):
            left = array[index]
            right = array[index + 1]
            steps.append(
                make_algorithm_step(
                    AlgorithmEventType.COMPARE,
                    f"Compare {left} and {right}.",
                    array,
                    current_indices=(index, index + 1),
                    comparison_indices=(index, index + 1),
                    metadata={
                        "pass_index": pass_index,
                        "compared_values": (left, right),
                        "sorted_suffix_start": length - pass_index,
                    },
                )
            )
            if left > right:
                array[index], array[index + 1] = array[index + 1], array[index]
                steps.append(
                    make_algorithm_step(
                        AlgorithmEventType.SWAP,
                        f"Swap {left} and {right}.",
                        array,
                        current_indices=(index, index + 1),
                        swapped_indices=(index, index + 1),
                        metadata={
                            "pass_index": pass_index,
                            "swapped_values": (left, right),
                            "sorted_suffix_start": length - pass_index,
                        },
                    )
                )
        steps.append(
            make_algorithm_step(
                AlgorithmEventType.MOVE,
                f"Position {length - pass_index - 1} is now in the sorted suffix.",
                array,
                current_indices=(length - pass_index - 1,),
                metadata={"sorted_suffix_start": length - pass_index - 1},
            )
        )

    message = "Bubble Sort complete."
    steps.append(
        make_algorithm_step(
            AlgorithmEventType.COMPLETE,
            message,
            array,
            completed=True,
            metadata={"sorted_suffix_start": 0},
        )
    )
    return SortResult(True, tuple(array), message, steps)
