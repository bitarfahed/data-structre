"""Shared step/event representations for future visualization."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class EventType(str, Enum):
    """Kinds of structure changes a visualizer may later render."""

    ADD = "ADD"
    REMOVE = "REMOVE"
    VISIT = "VISIT"
    MOVE = "MOVE"
    COMPARE = "COMPARE"
    UPDATE = "UPDATE"
    RESIZE = "RESIZE"
    COMPLETE = "COMPLETE"


@dataclass(frozen=True)
class Step:
    """A minimal description of one observable operation step."""

    event_type: EventType
    message: str
    metadata: dict[str, Any] = field(default_factory=dict)
