"""Queue domain model."""

from collections import deque
from typing import Deque


class Queue:
    """A simple integer-only queue with FIFO behavior."""

    def __init__(self) -> None:
        self._items: Deque[int] = deque()

    def enqueue(self, value: int) -> None:
        """Add an integer value to the back of the queue."""
        self._validate_integer(value)
        self._items.append(value)

    def dequeue(self) -> int | None:
        """Remove and return the front value, or None when the queue is empty."""
        if not self._items:
            return None

        return self._items.popleft()

    def display(self) -> str:
        """Return a readable front-to-back queue representation."""
        return f"Queue(front -> back): {self.to_list()}"

    def to_list(self) -> list[int]:
        """Return the queue values from front to back."""
        return list(self._items)

    def is_empty(self) -> bool:
        """Return True when the queue has no values."""
        return not self._items

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"Queue({self.to_list()!r})"

    def __str__(self) -> str:
        return self.display()

    @staticmethod
    def _validate_integer(value: int) -> None:
        if type(value) is not int:
            raise TypeError("Queue values must be integers.")
