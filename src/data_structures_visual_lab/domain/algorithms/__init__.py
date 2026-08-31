"""Shared infrastructure for future algorithm modules."""

from data_structures_visual_lab.domain.algorithms.state import (
    AlgorithmEventType,
    AlgorithmState,
    AlgorithmStep,
    make_algorithm_step,
)
from data_structures_visual_lab.domain.algorithms.validation import (
    ArrayValidationResult,
    parse_integer_array_text,
    validate_ascending_sorted,
    validate_integer_array,
)

__all__ = [
    "AlgorithmEventType",
    "AlgorithmState",
    "AlgorithmStep",
    "ArrayValidationResult",
    "make_algorithm_step",
    "parse_integer_array_text",
    "validate_ascending_sorted",
    "validate_integer_array",
]
