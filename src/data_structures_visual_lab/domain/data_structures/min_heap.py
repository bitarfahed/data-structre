"""Min-heap domain model."""

from __future__ import annotations


class MinHeap:
    """Integer-only min-heap with explicit deferred repair operations."""

    def __init__(self) -> None:
        self._values: list[int] = []
        self._repair_pending = False
        self._repair_index: int | None = None
        self._repair_kind: str | None = None

    def add_raw(self, value: int) -> bool:
        """Append a value without restoring heap order."""
        self._validate_integer(value)
        if self._repair_pending:
            return False

        self._values.append(value)
        new_index = len(self._values) - 1
        if self._violates_parent(new_index):
            self._repair_pending = True
            self._repair_index = new_index
            self._repair_kind = "sift_up"
        return True

    def sift_up(self) -> bool:
        """Restore heap order after a raw insertion."""
        if not self._repair_pending or self._repair_index is None or self._repair_kind != "sift_up":
            return False

        index = self._repair_index
        while index > 0:
            parent_index = self._parent_index(index)
            if self._values[parent_index] <= self._values[index]:
                break
            self._swap(parent_index, index)
            index = parent_index

        self._clear_repair_state()
        return True

    def extract_raw(self) -> int | None:
        """Remove the root and replace it with the last value without heapifying."""
        if self._repair_pending or not self._values:
            return None

        minimum = self._values[0]
        last_value = self._values.pop()
        if self._values:
            self._values[0] = last_value
            if self._violates_children(0):
                self._repair_pending = True
                self._repair_index = 0
                self._repair_kind = "heapify_down"
        return minimum

    def heapify_down(self) -> bool:
        """Restore heap order after a raw extraction."""
        if not self._repair_pending or self._repair_index is None or self._repair_kind != "heapify_down":
            return False

        index = self._repair_index
        while True:
            smallest_index = index
            left_index = self._left_index(index)
            right_index = self._right_index(index)

            if left_index < len(self._values) and self._values[left_index] < self._values[smallest_index]:
                smallest_index = left_index
            if right_index < len(self._values) and self._values[right_index] < self._values[smallest_index]:
                smallest_index = right_index

            if smallest_index == index:
                break
            self._swap(index, smallest_index)
            index = smallest_index

        self._clear_repair_state()
        return True

    def peek_min(self) -> int | None:
        """Return the root value without removing it."""
        if not self._values:
            return None
        return self._values[0]

    def is_valid_heap(self) -> bool:
        """Return True when every parent is less than or equal to its children."""
        return self._first_violation_index() is None

    @property
    def repair_pending(self) -> bool:
        """Return True when add/extract are blocked until the heap is repaired."""
        return self._repair_pending

    @property
    def repair_index(self) -> int | None:
        """Return the index currently requiring repair, when known."""
        return self._repair_index

    @property
    def repair_value(self) -> int | None:
        """Return the value currently requiring repair, when known."""
        if self._repair_index is None:
            return None
        if self._repair_index >= len(self._values):
            return None
        return self._values[self._repair_index]

    @property
    def repair_kind(self) -> str | None:
        """Return the repair operation currently needed, when known."""
        return self._repair_kind

    @property
    def size(self) -> int:
        """Return the current number of heap values."""
        return len(self._values)

    def to_list(self) -> list[int]:
        """Return heap storage in array order."""
        return list(self._values)

    def display(self) -> str:
        """Return a readable heap representation."""
        return f"MinHeap(array order): {self._values}"

    def __len__(self) -> int:
        return len(self._values)

    def __repr__(self) -> str:
        return f"MinHeap({self._values!r})"

    def __str__(self) -> str:
        return self.display()

    def _violates_parent(self, index: int) -> bool:
        if index == 0:
            return False
        parent_index = self._parent_index(index)
        return self._values[parent_index] > self._values[index]

    def _violates_children(self, index: int) -> bool:
        left_index = self._left_index(index)
        right_index = self._right_index(index)
        if left_index < len(self._values) and self._values[index] > self._values[left_index]:
            return True
        return right_index < len(self._values) and self._values[index] > self._values[right_index]

    def _first_violation_index(self) -> int | None:
        for index in range(len(self._values)):
            if self._violates_children(index):
                return index
        return None

    def _clear_repair_state(self) -> None:
        self._repair_pending = False
        self._repair_index = None
        self._repair_kind = None

    def _swap(self, left_index: int, right_index: int) -> None:
        self._values[left_index], self._values[right_index] = self._values[right_index], self._values[left_index]

    @staticmethod
    def _parent_index(index: int) -> int:
        return (index - 1) // 2

    @staticmethod
    def _left_index(index: int) -> int:
        return 2 * index + 1

    @staticmethod
    def _right_index(index: int) -> int:
        return 2 * index + 2

    @staticmethod
    def _validate_integer(value: int) -> None:
        if type(value) is not int:
            raise TypeError("MinHeap values must be integers.")
