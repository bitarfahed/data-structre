"""Singly linked list domain model."""

from __future__ import annotations

from dataclasses import dataclass

from dsa_visual_lab.events import EventType, Step


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

    def push_with_steps(self, value: int, index: int = 0) -> tuple[bool, list[Step]]:
        """Insert a value and return whether it worked with observable steps."""
        self._validate_integer(value, "LinkedList values must be integers.")
        self._validate_index_type(index)

        steps = [
            Step(
                EventType.COMPARE,
                f"Checked whether index {index} can receive a new node.",
                {"index": index, "size": self._length},
            )
        ]

        if index < 0 or index > self._length:
            steps.append(
                Step(
                    EventType.COMPLETE,
                    "LinkedList push skipped because the index is invalid.",
                    {"success": False, "size": self._length, "state": self.to_list()},
                )
            )
            return False, steps

        new_node = Node(value)
        steps.append(
            Step(EventType.ADD, f"Created a new node holding {value}.", {"value": value})
        )

        if index == 0:
            new_node.next = self.head
            self.head = new_node
            steps.append(
                Step(
                    EventType.UPDATE,
                    "Updated the head reference to the new node.",
                    {"index": 0, "value": value},
                )
            )
        else:
            previous = self.head
            for current_index in range(index - 1):
                if previous is None:
                    break
                steps.append(
                    Step(
                        EventType.VISIT,
                        f"Visited node at index {current_index}.",
                        {"index": current_index, "value": previous.value},
                    )
                )
                previous = previous.next
                steps.append(
                    Step(
                        EventType.MOVE,
                        f"Moved to node at index {current_index + 1}.",
                        {"from_index": current_index, "to_index": current_index + 1},
                    )
                )

            if previous is None:
                steps.append(
                    Step(
                        EventType.COMPLETE,
                        "LinkedList push skipped because traversal could not reach the index.",
                        {"success": False, "size": self._length, "state": self.to_list()},
                    )
                )
                return False, steps

            steps.append(
                Step(
                    EventType.VISIT,
                    f"Visited node before insertion at index {index - 1}.",
                    {"index": index - 1, "value": previous.value},
                )
            )
            new_node.next = previous.next
            previous.next = new_node
            steps.append(
                Step(
                    EventType.UPDATE,
                    f"Linked node {index - 1} to the new node.",
                    {"previous_index": index - 1, "inserted_index": index},
                )
            )

        self._length += 1
        steps.append(
            Step(
                EventType.COMPLETE,
                "LinkedList push complete.",
                {"success": True, "size": self._length, "state": self.to_list()},
            )
        )
        return True, steps

    def pop_with_steps(self, index: int = 0) -> tuple[int | None, list[Step]]:
        """Remove a value and return it with observable steps."""
        self._validate_index_type(index)

        steps = [
            Step(
                EventType.COMPARE,
                f"Checked whether index {index} can be removed.",
                {"index": index, "size": self._length},
            )
        ]

        if index < 0 or index >= self._length or self.head is None:
            steps.append(
                Step(
                    EventType.COMPLETE,
                    "LinkedList pop skipped because the index is invalid or the list is empty.",
                    {"value": None, "size": self._length, "state": self.to_list()},
                )
            )
            return None, steps

        if index == 0:
            removed = self.head
            self.head = removed.next
            steps.append(
                Step(
                    EventType.REMOVE,
                    f"Removed head node holding {removed.value}.",
                    {"index": 0, "value": removed.value},
                )
            )
            steps.append(
                Step(
                    EventType.UPDATE,
                    "Updated the head reference.",
                    {"new_head": self.head.value if self.head is not None else None},
                )
            )
        else:
            previous = self.head
            for current_index in range(index - 1):
                if previous is None:
                    break
                steps.append(
                    Step(
                        EventType.VISIT,
                        f"Visited node at index {current_index}.",
                        {"index": current_index, "value": previous.value},
                    )
                )
                previous = previous.next
                steps.append(
                    Step(
                        EventType.MOVE,
                        f"Moved to node at index {current_index + 1}.",
                        {"from_index": current_index, "to_index": current_index + 1},
                    )
                )

            if previous is None or previous.next is None:
                steps.append(
                    Step(
                        EventType.COMPLETE,
                        "LinkedList pop skipped because traversal could not reach the index.",
                        {"value": None, "size": self._length, "state": self.to_list()},
                    )
                )
                return None, steps

            steps.append(
                Step(
                    EventType.VISIT,
                    f"Visited node before removal at index {index - 1}.",
                    {"index": index - 1, "value": previous.value},
                )
            )
            removed = previous.next
            previous.next = removed.next
            steps.append(
                Step(
                    EventType.REMOVE,
                    f"Removed node at index {index} holding {removed.value}.",
                    {"index": index, "value": removed.value},
                )
            )
            steps.append(
                Step(
                    EventType.UPDATE,
                    f"Linked node {index - 1} to the removed node's next reference.",
                    {"previous_index": index - 1, "removed_index": index},
                )
            )

        removed.next = None
        self._length -= 1
        steps.append(
            Step(
                EventType.COMPLETE,
                "LinkedList pop complete.",
                {"value": removed.value, "size": self._length, "state": self.to_list()},
            )
        )
        return removed.value, steps

    def change_value_with_steps(self, index: int, value: int) -> tuple[bool, list[Step]]:
        """Change a value and return whether it worked with observable steps."""
        self._validate_index_type(index)
        self._validate_integer(value, "LinkedList values must be integers.")

        steps = [
            Step(
                EventType.COMPARE,
                f"Checked whether index {index} can be updated.",
                {"index": index, "size": self._length},
            )
        ]

        if index < 0 or index >= self._length:
            steps.append(
                Step(
                    EventType.COMPLETE,
                    "LinkedList update skipped because the index is invalid.",
                    {"success": False, "size": self._length, "state": self.to_list()},
                )
            )
            return False, steps

        current = self.head
        for current_index in range(index):
            if current is None:
                break
            steps.append(
                Step(
                    EventType.VISIT,
                    f"Visited node at index {current_index}.",
                    {"index": current_index, "value": current.value},
                )
            )
            current = current.next
            steps.append(
                Step(
                    EventType.MOVE,
                    f"Moved to node at index {current_index + 1}.",
                    {"from_index": current_index, "to_index": current_index + 1},
                )
            )

        if current is None:
            steps.append(
                Step(
                    EventType.COMPLETE,
                    "LinkedList update skipped because traversal could not reach the index.",
                    {"success": False, "size": self._length, "state": self.to_list()},
                )
            )
            return False, steps

        old_value = current.value
        current.value = value
        steps.extend(
            [
                Step(
                    EventType.UPDATE,
                    f"Changed node at index {index} from {old_value} to {value}.",
                    {"index": index, "old_value": old_value, "new_value": value},
                ),
                Step(
                    EventType.COMPLETE,
                    "LinkedList update complete.",
                    {"success": True, "size": self._length, "state": self.to_list()},
                ),
            ]
        )
        return True, steps

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
