"""Shared execution state for array-based algorithms."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class AlgorithmEventType(str, Enum):
    """Observable algorithm moments for future visualization."""

    COMPARE = "COMPARE"
    SWAP = "SWAP"
    VISIT = "VISIT"
    MOVE = "MOVE"
    PIVOT = "PIVOT"
    MERGE = "MERGE"
    FOUND = "FOUND"
    NOT_FOUND = "NOT_FOUND"
    COMPLETE = "COMPLETE"


@dataclass(frozen=True)
class AlgorithmState:
    """A small snapshot of an array algorithm's execution."""

    values: tuple[int, ...]
    current_indices: tuple[int, ...] = ()
    comparison_indices: tuple[int, int] | None = None
    swapped_indices: tuple[int, int] | None = None
    current_range: tuple[int, int] | None = None
    pivot_index: int | None = None
    merge_ranges: tuple[tuple[int, int], ...] = ()
    found_index: int | None = None
    found: bool | None = None
    completed: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AlgorithmStep:
    """One observable step emitted by an array algorithm."""

    event_type: AlgorithmEventType
    message: str
    state: AlgorithmState


def make_algorithm_step(
    event_type: AlgorithmEventType,
    message: str,
    values: list[int] | tuple[int, ...],
    **state_fields: Any,
) -> AlgorithmStep:
    """Build an algorithm step while normalizing values to an immutable tuple."""
    return AlgorithmStep(
        event_type=event_type,
        message=message,
        state=AlgorithmState(values=tuple(values), **state_fields),
    )
