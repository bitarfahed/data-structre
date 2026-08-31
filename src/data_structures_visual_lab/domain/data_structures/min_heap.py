"""Min-heap domain model."""

from __future__ import annotations

from data_structures_visual_lab.events import EventType, Step


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

    def add_raw_with_steps(self, value: int) -> tuple[bool, list[Step]]:
        """Append a value and return observable steps for visualization."""
        self._validate_integer(value)
        if self._repair_pending:
            return False, [
                self._step(
                    EventType.COMPLETE,
                    "Min-Heap add blocked because repair is pending.",
                    {"value": value, "highlight_indexes": _maybe_index(self._repair_index)},
                )
            ]

        added = self.add_raw(value)
        new_index = len(self._values) - 1
        if not added:
            return False, [self._step(EventType.COMPLETE, "Min-Heap add skipped.")]

        if self._repair_pending:
            message = "Raw add complete. Sift Up required before another add or extract."
        else:
            message = "Raw add complete. Heap remains valid."

        return True, [
            self._step(
                EventType.ADD,
                f"Appended {value} at index {new_index}.",
                {"value": value, "index": new_index, "highlight_indexes": [new_index]},
            ),
            self._step(
                EventType.COMPLETE,
                message,
                {"value": value, "index": new_index, "highlight_indexes": [new_index]},
            ),
        ]

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

    def sift_up_with_steps(self) -> tuple[bool, list[Step]]:
        """Repair a raw insertion and return observable steps."""
        if not self._repair_pending or self._repair_kind != "sift_up" or self._repair_index is None:
            return False, [
                self._step(
                    EventType.COMPLETE,
                    "Min-Heap sift up skipped because no insertion repair is pending.",
                )
            ]

        start_index = self._repair_index
        repaired_value = self._values[start_index]
        repaired = self.sift_up()
        current_index = self._values.index(repaired_value)
        return repaired, [
            self._step(
                EventType.MOVE,
                f"Sifted {repaired_value} up from index {start_index}.",
                {"from_index": start_index, "to_index": current_index, "highlight_indexes": [current_index]},
            ),
            self._step(
                EventType.COMPLETE,
                "Sift Up complete. Heap is valid.",
                {"index": current_index, "highlight_indexes": [current_index]},
            ),
        ]

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

    def extract_raw_with_steps(self) -> tuple[int | None, list[Step]]:
        """Extract the root and return observable steps for visualization."""
        if self._repair_pending:
            return None, [
                self._step(
                    EventType.COMPLETE,
                    "Min-Heap extract blocked because repair is pending.",
                    {"highlight_indexes": _maybe_index(self._repair_index)},
                )
            ]
        if not self._values:
            return None, [self._step(EventType.COMPLETE, "Min-Heap extract skipped because the heap is empty.")]

        extracted = self.extract_raw()
        if extracted is None:
            return None, [self._step(EventType.COMPLETE, "Min-Heap extract skipped.")]

        if self._repair_pending:
            message = f"Extracted {extracted}. Heapify Down required before another add or extract."
        else:
            message = f"Extracted {extracted}. Heap remains valid."
        return extracted, [
            self._step(
                EventType.REMOVE,
                f"Removed root value {extracted}.",
                {"extracted_value": extracted, "highlight_indexes": _maybe_index(self._repair_index)},
            ),
            self._step(
                EventType.COMPLETE,
                message,
                {"extracted_value": extracted, "highlight_indexes": _maybe_index(self._repair_index)},
            ),
        ]

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

    def heapify_down_with_steps(self) -> tuple[bool, list[Step]]:
        """Repair a raw extraction and return observable steps."""
        if not self._repair_pending or self._repair_kind != "heapify_down" or self._repair_index is None:
            return False, [
                self._step(
                    EventType.COMPLETE,
                    "Min-Heap heapify down skipped because no extraction repair is pending.",
                )
            ]

        start_index = self._repair_index
        repaired_value = self._values[start_index]
        repaired = self.heapify_down()
        current_index = self._values.index(repaired_value)
        return repaired, [
            self._step(
                EventType.MOVE,
                f"Heapified {repaired_value} down from index {start_index}.",
                {"from_index": start_index, "to_index": current_index, "highlight_indexes": [current_index]},
            ),
            self._step(
                EventType.COMPLETE,
                "Heapify Down complete. Heap is valid.",
                {"index": current_index, "highlight_indexes": [current_index]},
            ),
        ]

    def peek_min(self) -> int | None:
        """Return the root value without removing it."""
        if not self._values:
            return None
        return self._values[0]

    def peek_min_with_steps(self) -> tuple[int | None, list[Step]]:
        """Return the root value with observable visualization metadata."""
        minimum = self.peek_min()
        if minimum is None:
            return None, [self._step(EventType.COMPLETE, "Min-Heap peek skipped because the heap is empty.")]
        return minimum, [
            self._step(
                EventType.COMPLETE,
                f"Min-Heap minimum is {minimum}.",
                {"result_value": minimum, "index": 0, "highlight_indexes": [0]},
            )
        ]

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

    def _step(
        self,
        event_type: EventType,
        message: str,
        metadata: dict[str, object] | None = None,
    ) -> Step:
        step_metadata = {
            "state": self.to_list(),
            "size": self.size,
            "heap_valid": self.is_valid_heap(),
            "repair_pending": self.repair_pending,
            "repair_index": self.repair_index,
            "repair_value": self.repair_value,
            "repair_kind": self.repair_kind,
        }
        if metadata:
            step_metadata.update(metadata)
        return Step(event_type, message, step_metadata)

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


def _maybe_index(index: int | None) -> list[int]:
    return [index] if type(index) is int else []
