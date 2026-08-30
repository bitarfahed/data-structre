"""Stack domain model."""

from data_structures_visual_lab.events import EventType, Step


class Stack:
    """A simple integer-only stack with LIFO behavior."""

    def __init__(self) -> None:
        self._items: list[int] = []

    def push(self, value: int) -> None:
        """Add an integer value to the top of the stack."""
        self._validate_integer(value)
        self._items.append(value)

    def pop(self) -> int | None:
        """Remove and return the top value, or None when the stack is empty."""
        if not self._items:
            return None

        return self._items.pop()

    def push_with_steps(self, value: int) -> list[Step]:
        """Add an integer value and return observable steps for visualization."""
        self._validate_integer(value)
        self._items.append(value)

        return [
            Step(
                EventType.ADD,
                f"Pushed {value} onto the stack.",
                {"value": value, "index": len(self._items) - 1},
            ),
            Step(
                EventType.COMPLETE,
                "Stack push complete.",
                {"size": len(self._items), "state": self.to_list()},
            ),
        ]

    def pop_with_steps(self) -> tuple[int | None, list[Step]]:
        """Remove the top value and return it with observable steps."""
        if not self._items:
            return None, [
                Step(
                    EventType.COMPLETE,
                    "Stack pop skipped because the stack is empty.",
                    {"size": 0, "state": []},
                )
            ]

        index = len(self._items) - 1
        state_before = self.to_list()
        value = self._items.pop()
        return value, [
            Step(
                EventType.VISIT,
                f"Visited top stack value {value}.",
                {"value": value, "index": index, "state": state_before},
            ),
            Step(
                EventType.REMOVE,
                f"Popped {value} from the stack.",
                {"value": value, "index": index, "state": state_before},
            ),
            Step(
                EventType.COMPLETE,
                "Stack pop complete.",
                {"size": len(self._items), "state": self.to_list()},
            ),
        ]

    def display(self) -> str:
        """Return a readable bottom-to-top stack representation."""
        return f"Stack(bottom -> top): {self._items}"

    def to_list(self) -> list[int]:
        """Return the stack values from bottom to top."""
        return self._items.copy()

    def is_empty(self) -> bool:
        """Return True when the stack has no values."""
        return not self._items

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"Stack({self._items!r})"

    def __str__(self) -> str:
        return self.display()

    @staticmethod
    def _validate_integer(value: int) -> None:
        if type(value) is not int:
            raise TypeError("Stack values must be integers.")
