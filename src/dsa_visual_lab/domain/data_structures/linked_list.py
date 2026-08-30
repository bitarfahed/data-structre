"""Singly linked list domain model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Node:
    """A node in a singly linked list."""

    value: int
    next: Node | None = None

    def __post_init__(self) -> None:
        if type(self.value) is not int:
            raise TypeError("Node values must be integers.")


class LinkedList:
    """A simple integer-only singly linked list."""

    def __init__(self) -> None:
        self.head: Node | None = None
        self._length = 0

    def push(self, value: int, index: int = 0) -> bool:
        """Insert an integer value at index, returning False for invalid indices."""
        self._validate_integer(value, "LinkedList values must be integers.")
        self._validate_index_type(index)

        if index < 0 or index > self._length:
            return False

        new_node = Node(value)

        if index == 0:
            new_node.next = self.head
            self.head = new_node
        else:
            previous = self._node_at(index - 1)
            if previous is None:
                return False
            new_node.next = previous.next
            previous.next = new_node

        self._length += 1
        return True

    def pop(self, index: int = 0) -> int | None:
        """Remove and return the value at index, or None when removal is invalid."""
        self._validate_index_type(index)

        if index < 0 or index >= self._length or self.head is None:
            return None

        if index == 0:
            removed = self.head
            self.head = removed.next
        else:
            previous = self._node_at(index - 1)
            if previous is None or previous.next is None:
                return None
            removed = previous.next
            previous.next = removed.next

        removed.next = None
        self._length -= 1
        return removed.value

    def change_value(self, index: int, value: int) -> bool:
        """Change the value at index, returning False for invalid indices."""
        self._validate_index_type(index)
        self._validate_integer(value, "LinkedList values must be integers.")

        if index < 0 or index >= self._length:
            return False

        node = self._node_at(index)
        if node is None:
            return False

        node.value = value
        return True

    def display(self) -> str:
        """Return a readable head-to-tail linked list representation."""
        values = " -> ".join(str(value) for value in self.to_list())
        return f"LinkedList(head -> tail): {values if values else 'empty'}"

    def to_list(self) -> list[int]:
        """Return linked list values from head to tail."""
        values: list[int] = []
        current = self.head

        while current is not None:
            values.append(current.value)
            current = current.next

        return values

    def is_empty(self) -> bool:
        """Return True when the linked list has no values."""
        return self._length == 0

    def __len__(self) -> int:
        return self._length

    def __repr__(self) -> str:
        return f"LinkedList({self.to_list()!r})"

    def __str__(self) -> str:
        return self.display()

    def _node_at(self, index: int) -> Node | None:
        current = self.head

        for _ in range(index):
            if current is None:
                return None
            current = current.next

        return current

    @staticmethod
    def _validate_integer(value: int, message: str) -> None:
        if type(value) is not int:
            raise TypeError(message)

    @staticmethod
    def _validate_index_type(index: int) -> None:
        if type(index) is not int:
            raise TypeError("LinkedList indices must be integers.")
