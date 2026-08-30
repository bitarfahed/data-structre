"""GUI-independent visualization state helpers."""

from dataclasses import dataclass

from data_structures_visual_lab.domain.data_structures import DynamicArray, LinkedList, Queue, Stack
from data_structures_visual_lab.events import EventType, Step


@dataclass(frozen=True)
class VisualElement:
    """One value-bearing item to render."""

    index: int
    value: int | None
    highlighted: bool = False
    moved: bool = False


@dataclass(frozen=True)
class VisualizationState:
    """A structure snapshot plus the current operation message."""

    structure_name: str
    values: tuple[VisualElement, ...]
    message: str
    size: int
    capacity: int | None = None
    event_type: EventType | None = None
    metadata: dict[str, object] | None = None


def build_visualization_state(
    structure_name: str,
    structure: Stack | Queue | LinkedList | DynamicArray,
    step: Step | None = None,
) -> VisualizationState:
    """Build a renderer-friendly state from a domain structure and optional step."""
    metadata = step.metadata if step is not None else {}
    highlight_indexes = _highlight_indexes(metadata)
    moved_indexes = _moved_indexes(metadata)
    message = step.message if step is not None else str(structure)

    if isinstance(structure, DynamicArray):
        values = _values_from_metadata(metadata, structure.to_list())
        capacity = _capacity_from_metadata(metadata, structure.capacity)
        elements = tuple(
            VisualElement(
                index=index,
                value=values[index] if index < len(values) else None,
                highlighted=index in highlight_indexes,
                moved=index in moved_indexes,
            )
            for index in range(capacity)
        )
        return VisualizationState(
            structure_name=structure_name,
            values=elements,
            message=message,
            size=len(values),
            capacity=capacity,
            event_type=step.event_type if step is not None else None,
            metadata=metadata,
        )

    values = _values_from_metadata(metadata, structure.to_list())
    elements = tuple(
        VisualElement(
            index=index,
            value=value,
            highlighted=index in highlight_indexes,
            moved=index in moved_indexes,
        )
        for index, value in enumerate(values)
    )
    return VisualizationState(
        structure_name=structure_name,
        values=elements,
        message=message,
        size=len(values),
        event_type=step.event_type if step is not None else None,
        metadata=metadata,
    )


def _highlight_indexes(metadata: dict[str, object]) -> set[int]:
    indexes: set[int] = set()
    for key in ("index", "from_index", "to_index", "previous_index", "inserted_index"):
        value = metadata.get(key)
        if type(value) is int:
            indexes.add(value)
    return indexes


def _values_from_metadata(
    metadata: dict[str, object],
    fallback: list[int],
) -> list[int]:
    values = metadata.get("state")
    if isinstance(values, list) and all(type(value) is int for value in values):
        return values
    return fallback


def _capacity_from_metadata(metadata: dict[str, object], fallback: int) -> int:
    capacity = metadata.get("capacity")
    if type(capacity) is int and capacity >= 0:
        return capacity
    new_capacity = metadata.get("new_capacity")
    if type(new_capacity) is int and new_capacity >= 0:
        return new_capacity
    return fallback


def _moved_indexes(metadata: dict[str, object]) -> set[int]:
    indexes: set[int] = set()
    for key in ("from_index", "to_index"):
        value = metadata.get(key)
        if type(value) is int:
            indexes.add(value)
    return indexes
