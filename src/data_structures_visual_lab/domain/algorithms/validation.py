"""Validation helpers for Round 3 array-based algorithms."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ArrayValidationResult:
    """Result of validating user-provided array input."""

    ok: bool
    values: tuple[int, ...] = ()
    message: str = ""


def validate_integer_array(values: object) -> ArrayValidationResult:
    """Validate an iterable of integer values for Round 3 algorithms."""
    if isinstance(values, (str, bytes)) or not isinstance(values, (list, tuple)):
        return ArrayValidationResult(False, message="Array input must be a list or tuple of integers.")
    if not all(type(value) is int for value in values):
        return ArrayValidationResult(False, message="Array values must be integers.")
    return ArrayValidationResult(True, tuple(values), "Array input is valid.")


def parse_integer_array_text(text: str) -> ArrayValidationResult:
    """Parse comma-separated integer text into validated array values."""
    raw_text = text.strip()
    if not raw_text:
        return ArrayValidationResult(True, (), "Array input is valid.")

    values: list[int] = []
    for part in raw_text.split(","):
        item = part.strip()
        if not item:
            return ArrayValidationResult(False, message="Array values must be integers.")
        try:
            values.append(int(item))
        except ValueError:
            return ArrayValidationResult(False, message="Array values must be integers.")
    return validate_integer_array(values)


def validate_ascending_sorted(values: tuple[int, ...] | list[int]) -> ArrayValidationResult:
    """Validate the ascending-order precondition required by Binary Search."""
    base_result = validate_integer_array(values)
    if not base_result.ok:
        return base_result
    if any(left > right for left, right in zip(base_result.values, base_result.values[1:])):
        return ArrayValidationResult(False, base_result.values, "Binary Search requires ascending sorted input.")
    return ArrayValidationResult(True, base_result.values, "Array input is ascending sorted.")
