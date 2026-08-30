"""Dynamic array domain model."""

from ctypes import py_object

from data_structures_visual_lab.events import EventType, Step


class DynamicArray:
    """A simple integer-only dynamic array with explicit capacity management."""

    def __init__(self, initial_capacity: int = 1) -> None:
        if type(initial_capacity) is not int:
            raise TypeError("DynamicArray initial capacity must be an integer.")
        if initial_capacity < 1:
            raise ValueError("DynamicArray initial capacity must be at least 1.")

        self._minimum_capacity = initial_capacity
        self._capacity = initial_capacity
        self._size = 0
        self._storage = self._make_storage(self._capacity)

    def add(self, value: int) -> None:
        """Add an integer value to the end of the array."""
        self._validate_integer(value, "DynamicArray values must be integers.")

        if self._size == self._capacity:
            self._resize(self._capacity * 2)

        self._storage[self._size] = value
        self._size += 1

    def delete(self, index: int) -> int | None:
        """Delete and return the value at index, or None when deletion is invalid."""
        self._validate_index_type(index)

        if index < 0 or index >= self._size:
            return None

        removed = self._storage[index]

        for position in range(index, self._size - 1):
            self._storage[position] = self._storage[position + 1]

        self._size -= 1
        self._storage[self._size] = None
        self._shrink_if_needed()
        return removed

    def add_with_steps(self, value: int) -> list[Step]:
        """Add an integer value and return observable steps for visualization."""
        self._validate_integer(value, "DynamicArray values must be integers.")
        steps: list[Step] = []

        if self._size == self._capacity:
            old_capacity = self._capacity
            self._resize(self._capacity * 2)
            steps.append(
                Step(
                    EventType.RESIZE,
                    f"Grew capacity from {old_capacity} to {self._capacity}.",
                    {
                        "old_capacity": old_capacity,
                        "new_capacity": self._capacity,
                        "capacity": self._capacity,
                        "state": self.to_list(),
                    },
                )
            )

        self._storage[self._size] = value
        steps.append(
            Step(
                EventType.ADD,
                f"Added {value} at index {self._size}.",
                {"index": self._size, "value": value},
            )
        )
        self._size += 1
        steps.append(
            Step(
                EventType.COMPLETE,
                "DynamicArray add complete.",
                {"size": self._size, "capacity": self._capacity, "state": self.to_list()},
            )
        )
        return steps

    def delete_with_steps(self, index: int) -> tuple[int | None, list[Step]]:
        """Delete a value and return it with observable steps."""
        self._validate_index_type(index)
        steps = [
            Step(
                EventType.COMPARE,
                f"Checked whether index {index} can be deleted.",
                {"index": index, "size": self._size},
            )
        ]

        if index < 0 or index >= self._size:
            steps.append(
                Step(
                    EventType.COMPLETE,
                    "DynamicArray delete skipped because the index is invalid or the array is empty.",
                    {"value": None, "size": self._size, "capacity": self._capacity},
                )
            )
            return None, steps

        state_before = self.to_list()
        removed = self._storage[index]
        steps.append(
            Step(
                EventType.REMOVE,
                f"Removed {removed} from index {index}.",
                {
                    "index": index,
                    "value": removed,
                    "state": state_before,
                    "capacity": self._capacity,
                },
            )
        )

        for position in range(index, self._size - 1):
            self._storage[position] = self._storage[position + 1]
            steps.append(
                Step(
                    EventType.MOVE,
                    f"Moved value from index {position + 1} to index {position}.",
                    {
                        "from_index": position + 1,
                        "to_index": position,
                        "state": self.to_list(),
                        "capacity": self._capacity,
                    },
                )
            )

        self._size -= 1
        self._storage[self._size] = None
        old_capacity = self._capacity
        self._shrink_if_needed()
        if self._capacity != old_capacity:
            steps.append(
                Step(
                    EventType.RESIZE,
                    f"Shrank capacity from {old_capacity} to {self._capacity}.",
                    {
                        "old_capacity": old_capacity,
                        "new_capacity": self._capacity,
                        "capacity": self._capacity,
                        "state": self.to_list(),
                    },
                )
            )

        steps.append(
            Step(
                EventType.COMPLETE,
                "DynamicArray delete complete.",
                {
                    "value": removed,
                    "size": self._size,
                    "capacity": self._capacity,
                    "state": self.to_list(),
                },
            )
        )
        return removed, steps

    def display(self) -> str:
        """Return a readable dynamic array representation."""
        return (
            "DynamicArray"
            f"(size={self._size}, capacity={self._capacity}): {self.to_list()}"
        )

    def to_list(self) -> list[int]:
        """Return stored values from left to right."""
        return [self._storage[index] for index in range(self._size)]

    def is_empty(self) -> bool:
        """Return True when the dynamic array has no values."""
        return self._size == 0

    @property
    def size(self) -> int:
        """Return the number of stored values."""
        return self._size

    @property
    def capacity(self) -> int:
        """Return the current storage capacity."""
        return self._capacity

    @property
    def minimum_capacity(self) -> int:
        """Return the smallest capacity this array may shrink to."""
        return self._minimum_capacity

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return (
            "DynamicArray"
            f"({self.to_list()!r}, capacity={self._capacity!r})"
        )

    def __str__(self) -> str:
        return self.display()

    def _resize(self, new_capacity: int) -> None:
        new_storage = self._make_storage(new_capacity)

        for index in range(self._size):
            new_storage[index] = self._storage[index]

        self._storage = new_storage
        self._capacity = new_capacity

    def _shrink_if_needed(self) -> None:
        if self._capacity == self._minimum_capacity:
            return

        if self._size <= self._capacity / 4:
            next_capacity = max(self._minimum_capacity, self._capacity // 2)
            if next_capacity < self._capacity:
                self._resize(next_capacity)

    @staticmethod
    def _make_storage(capacity: int) -> py_object:
        storage = (py_object * capacity)()

        for index in range(capacity):
            storage[index] = None

        return storage

    @staticmethod
    def _validate_integer(value: int, message: str) -> None:
        if type(value) is not int:
            raise TypeError(message)

    @staticmethod
    def _validate_index_type(index: int) -> None:
        if type(index) is not int:
            raise TypeError("DynamicArray indices must be integers.")
