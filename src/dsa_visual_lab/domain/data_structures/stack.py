"""Stack domain model."""


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
