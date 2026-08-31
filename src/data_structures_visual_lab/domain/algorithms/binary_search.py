"""Binary Search algorithm implementation."""

from __future__ import annotations

from dataclasses import dataclass

from data_structures_visual_lab.domain.algorithms.state import AlgorithmEventType, AlgorithmStep, make_algorithm_step
from data_structures_visual_lab.domain.algorithms.validation import validate_ascending_sorted


@dataclass(frozen=True)
class BinarySearchResult:
    """Result of running Binary Search."""

    ok: bool
    index: int | None
    message: str
    steps: list[AlgorithmStep]


def binary_search(values: list[int] | tuple[int, ...], target: int) -> BinarySearchResult:
    """Run Binary Search over an ascending sorted integer array."""
    validation = validate_ascending_sorted(values)
    if not validation.ok:
        return BinarySearchResult(False, None, validation.message, [])
    if type(target) is not int:
        return BinarySearchResult(False, None, "Target must be an integer.", [])

    array = validation.values
    steps: list[AlgorithmStep] = []
    low = 0
    high = len(array) - 1

    if not array:
        message = f"Target {target} was not found."
        steps.append(
            make_algorithm_step(
                AlgorithmEventType.NOT_FOUND,
                "Binary Search skipped because the array is empty.",
                array,
                found=False,
                completed=True,
                metadata={"target": target},
            )
        )
        return BinarySearchResult(False, None, message, steps)

    while low <= high:
        mid = (low + high) // 2
        mid_value = array[mid]
        steps.append(
            make_algorithm_step(
                AlgorithmEventType.COMPARE,
                f"Compare target {target} with middle value {mid_value} at index {mid}.",
                array,
                current_indices=(low, mid, high),
                comparison_indices=(mid, mid),
                current_range=(low, high),
                metadata={
                    "target": target,
                    "low_index": low,
                    "high_index": high,
                    "mid_index": mid,
                    "mid_value": mid_value,
                },
            )
        )

        if mid_value == target:
            message = f"Found target {target} at index {mid}."
            steps.append(
                make_algorithm_step(
                    AlgorithmEventType.FOUND,
                    message,
                    array,
                    current_indices=(low, mid, high),
                    comparison_indices=(mid, mid),
                    current_range=(low, high),
                    found_index=mid,
                    found=True,
                    completed=True,
                    metadata={
                        "target": target,
                        "low_index": low,
                        "high_index": high,
                        "mid_index": mid,
                        "mid_value": mid_value,
                    },
                )
            )
            return BinarySearchResult(True, mid, message, steps)

        if mid_value < target:
            discarded_range = (low, mid)
            message = f"Discard indices {low} through {mid}; target is larger."
            low = mid + 1
        else:
            discarded_range = (mid, high)
            message = f"Discard indices {mid} through {high}; target is smaller."
            high = mid - 1

        steps.append(
            make_algorithm_step(
                AlgorithmEventType.MOVE,
                message,
                array,
                current_indices=(low, high) if low <= high else (),
                current_range=(low, high) if low <= high else None,
                metadata={
                    "target": target,
                    "discarded_range": discarded_range,
                    "low_index": low,
                    "high_index": high,
                    "mid_index": mid,
                    "mid_value": mid_value,
                },
            )
        )

    message = f"Target {target} was not found."
    steps.append(
        make_algorithm_step(
            AlgorithmEventType.NOT_FOUND,
            message,
            array,
            found=False,
            completed=True,
            metadata={"target": target, "low_index": low, "high_index": high},
        )
    )
    return BinarySearchResult(False, None, message, steps)
