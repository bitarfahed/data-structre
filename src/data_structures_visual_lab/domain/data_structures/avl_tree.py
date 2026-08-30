"""AVL tree domain model."""

from __future__ import annotations

from dataclasses import dataclass

from data_structures_visual_lab.events import EventType, Step


@dataclass
class AVLNode:
    """A node in an AVL tree."""

    value: int
    left: AVLNode | None = None
    right: AVLNode | None = None
    height: int = 1

    def __post_init__(self) -> None:
        if type(self.value) is not int:
            raise TypeError("AVLNode values must be integers.")

    @property
    def balance_factor(self) -> int:
        """Return left subtree height minus right subtree height."""
        return _height(self.left) - _height(self.right)


class AVLTree:
    """Integer-only AVL tree with explicit deferred balancing."""

    def __init__(self) -> None:
        self.root: AVLNode | None = None
        self._size = 0
        self._rebalance_pending = False

    def insert(self, value: int) -> bool:
        """Insert using normal BST rules only, blocking while rebalance is pending."""
        self._validate_integer(value, "AVLTree values must be integers.")
        if self._rebalance_pending:
            return False
        if self.search(value):
            return False

        self.root = self._insert_bst(self.root, value)
        self._size += 1
        self._refresh_heights()
        self._rebalance_pending = not self.is_balanced()
        return True

    def insert_with_steps(self, value: int) -> tuple[bool, list[Step]]:
        """Insert a value and return observable steps for visualization."""
        self._validate_integer(value, "AVLTree values must be integers.")
        if self._rebalance_pending:
            return False, [
                self._step(
                    EventType.COMPLETE,
                    "AVL insert blocked because rebalance is pending.",
                    {"value": value},
                )
            ]

        path = self._search_path(value)
        inserted = self.insert(value)
        if not inserted:
            return False, [
                self._step(
                    EventType.COMPLETE,
                    f"AVL insert skipped because {value} already exists.",
                    {"value": value, "highlight_values": [value]},
                )
            ]

        steps = [
            self._step(
                EventType.VISIT,
                f"Traversed BST path for {value}.",
                {"highlight_values": path},
            ),
            self._step(
                EventType.ADD,
                f"Inserted {value} using BST rules.",
                {"inserted_value": value, "highlight_values": [value]},
            ),
        ]
        if self._rebalance_pending:
            steps.append(
                self._step(
                    EventType.COMPLETE,
                    "AVL insert complete. Rebalance required before another insert.",
                    {"inserted_value": value, "highlight_values": [value]},
                )
            )
        else:
            steps.append(
                self._step(
                    EventType.COMPLETE,
                    "AVL insert complete. Tree remains balanced.",
                    {"inserted_value": value, "highlight_values": [value]},
                )
            )
        return True, steps

    def balance(self) -> bool:
        """Restore AVL validity when a rebalance is pending."""
        if self.root is None:
            self._rebalance_pending = False
            return False
        if not self._rebalance_pending and self.is_balanced():
            return False

        self.root = self._balance_subtree(self.root)
        self._refresh_heights()
        self._rebalance_pending = False
        return True

    def balance_with_steps(self) -> tuple[bool, list[Step]]:
        """Balance the tree and return observable steps for visualization."""
        old_root_value = self.root.value if self.root is not None else None
        balanced = self.balance()
        if not balanced:
            return False, [
                self._step(
                    EventType.COMPLETE,
                    "AVL balance skipped because no rebalance is required.",
                    {"highlight_values": []},
                )
            ]

        new_root_value = self.root.value if self.root is not None else None
        return True, [
            self._step(
                EventType.UPDATE,
                "Applied AVL rotations to restore balance.",
                {
                    "old_root_value": old_root_value,
                    "new_root_value": new_root_value,
                    "highlight_values": [new_root_value] if type(new_root_value) is int else [],
                },
            ),
            self._step(
                EventType.COMPLETE,
                "AVL balance complete. Tree is balanced.",
                {"highlight_values": [new_root_value] if type(new_root_value) is int else []},
            ),
        ]

    def search(self, value: int) -> bool:
        """Return True when value exists in the tree."""
        self._validate_integer(value, "AVLTree values must be integers.")
        current = self.root

        while current is not None:
            if value == current.value:
                return True
            if value < current.value:
                current = current.left
            else:
                current = current.right

        return False

    def search_with_steps(self, value: int) -> tuple[bool, list[Step]]:
        """Search for a value and return observable steps for visualization."""
        self._validate_integer(value, "AVLTree values must be integers.")
        path = self._search_path(value)
        found = bool(path and path[-1] == value)
        if found:
            message = f"AVL search found {value}."
            metadata = {"value": value, "highlight_values": [value]}
        else:
            message = f"AVL search did not find {value}."
            metadata = {"value": value, "highlight_values": path}

        return found, [
            self._step(EventType.VISIT, f"Searched BST path for {value}.", {"highlight_values": path}),
            self._step(EventType.COMPLETE, message, metadata),
        ]

    def delete(self, value: int) -> bool:
        """Delete a value and restore AVL validity immediately."""
        self._validate_integer(value, "AVLTree values must be integers.")
        if not self.search(value):
            return False

        self.root = self._delete(self.root, value)
        self._size -= 1
        self._refresh_heights()
        if self.root is not None:
            self.root = self._balance_subtree(self.root)
            self._refresh_heights()
        self._rebalance_pending = False
        return True

    def delete_with_steps(self, value: int) -> tuple[bool, list[Step]]:
        """Delete a value and return observable steps for visualization."""
        self._validate_integer(value, "AVLTree values must be integers.")
        path = self._search_path(value)
        deleted = self.delete(value)
        if not deleted:
            return False, [
                self._step(EventType.VISIT, f"Searched BST path for {value}.", {"highlight_values": path}),
                self._step(
                    EventType.COMPLETE,
                    f"AVL delete skipped because {value} was not found.",
                    {"value": value, "highlight_values": path},
                ),
            ]

        return True, [
            self._step(
                EventType.REMOVE,
                f"Deleted {value} and restored AVL balance.",
                {"deleted_value": value, "highlight_values": path},
            ),
            self._step(
                EventType.COMPLETE,
                "AVL delete complete. Tree is balanced.",
                {"highlight_values": []},
            ),
        ]

    def min(self) -> int | None:
        """Return the smallest value, or None for an empty tree."""
        current = self.root
        if current is None:
            return None

        while current.left is not None:
            current = current.left
        return current.value

    def min_with_steps(self) -> tuple[int | None, list[Step]]:
        """Return the minimum value and observable traversal steps."""
        path = self._extreme_path(go_left=True)
        result = self.min()
        if result is None:
            return None, [self._step(EventType.COMPLETE, "AVL min skipped because the tree is empty.")]
        return result, [
            self._step(EventType.VISIT, "Followed left references to find the minimum.", {"highlight_values": path}),
            self._step(EventType.COMPLETE, f"AVL minimum is {result}.", {"result_value": result, "highlight_values": [result]}),
        ]

    def max(self) -> int | None:
        """Return the largest value, or None for an empty tree."""
        current = self.root
        if current is None:
            return None

        while current.right is not None:
            current = current.right
        return current.value

    def max_with_steps(self) -> tuple[int | None, list[Step]]:
        """Return the maximum value and observable traversal steps."""
        path = self._extreme_path(go_left=False)
        result = self.max()
        if result is None:
            return None, [self._step(EventType.COMPLETE, "AVL max skipped because the tree is empty.")]
        return result, [
            self._step(EventType.VISIT, "Followed right references to find the maximum.", {"highlight_values": path}),
            self._step(EventType.COMPLETE, f"AVL maximum is {result}.", {"result_value": result, "highlight_values": [result]}),
        ]

    def is_balanced(self) -> bool:
        """Return True when every node satisfies the AVL balance rule."""
        return self._is_balanced(self.root)

    @property
    def rebalance_pending(self) -> bool:
        """Return True when insertion is blocked until balance() is called."""
        return self._rebalance_pending

    def height(self) -> int:
        """Return the root height."""
        return _height(self.root)

    def balance_factor(self, value: int) -> int | None:
        """Return the balance factor for the node containing value."""
        self._validate_integer(value, "AVLTree values must be integers.")
        node = self._find_node(value)
        if node is None:
            return None
        return node.balance_factor

    def node_height(self, value: int) -> int | None:
        """Return the height for the node containing value."""
        self._validate_integer(value, "AVLTree values must be integers.")
        node = self._find_node(value)
        if node is None:
            return None
        return node.height

    def to_list(self) -> list[int]:
        """Return values in sorted order."""
        values: list[int] = []
        self._in_order(self.root, values)
        return values

    def unbalanced_values(self) -> list[int]:
        """Return values for nodes that do not currently satisfy AVL balance."""
        values: list[int] = []
        self._collect_unbalanced_values(self.root, values)
        return values

    def display(self) -> str:
        """Return a readable in-order AVL tree representation."""
        return f"AVLTree(in-order): {self.to_list()}"

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return f"AVLTree({self.to_list()!r})"

    def __str__(self) -> str:
        return self.display()

    def _insert_bst(self, node: AVLNode | None, value: int) -> AVLNode:
        if node is None:
            return AVLNode(value)
        if value < node.value:
            node.left = self._insert_bst(node.left, value)
        else:
            node.right = self._insert_bst(node.right, value)
        return node

    def _delete(self, node: AVLNode | None, value: int) -> AVLNode | None:
        if node is None:
            return None
        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            successor = self._minimum_node(node.right)
            node.value = successor.value
            node.right = self._delete(node.right, successor.value)
        return node

    def _balance_subtree(self, node: AVLNode | None) -> AVLNode | None:
        if node is None:
            return None

        node.left = self._balance_subtree(node.left)
        node.right = self._balance_subtree(node.right)
        _update_height(node)

        balance_factor = node.balance_factor
        if balance_factor > 1:
            if node.left is not None and node.left.balance_factor < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance_factor < -1:
            if node.right is not None and node.right.balance_factor > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        new_root = node.right
        if new_root is None:
            return node

        moved_subtree = new_root.left
        new_root.left = node
        node.right = moved_subtree
        _update_height(node)
        _update_height(new_root)
        return new_root

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        new_root = node.left
        if new_root is None:
            return node

        moved_subtree = new_root.right
        new_root.right = node
        node.left = moved_subtree
        _update_height(node)
        _update_height(new_root)
        return new_root

    def _refresh_heights(self) -> None:
        self._refresh_node_height(self.root)

    def _refresh_node_height(self, node: AVLNode | None) -> int:
        if node is None:
            return 0
        left_height = self._refresh_node_height(node.left)
        right_height = self._refresh_node_height(node.right)
        node.height = 1 + max(left_height, right_height)
        return node.height

    def _find_node(self, value: int) -> AVLNode | None:
        current = self.root

        while current is not None:
            if value == current.value:
                return current
            if value < current.value:
                current = current.left
            else:
                current = current.right
        return None

    def _is_balanced(self, node: AVLNode | None) -> bool:
        if node is None:
            return True
        if abs(node.balance_factor) > 1:
            return False
        return self._is_balanced(node.left) and self._is_balanced(node.right)

    def _in_order(self, node: AVLNode | None, values: list[int]) -> None:
        if node is None:
            return
        self._in_order(node.left, values)
        values.append(node.value)
        self._in_order(node.right, values)

    def _search_path(self, value: int) -> list[int]:
        path: list[int] = []
        current = self.root
        while current is not None:
            path.append(current.value)
            if value == current.value:
                break
            if value < current.value:
                current = current.left
            else:
                current = current.right
        return path

    def _extreme_path(self, go_left: bool) -> list[int]:
        path: list[int] = []
        current = self.root
        while current is not None:
            path.append(current.value)
            current = current.left if go_left else current.right
        return path

    def _collect_unbalanced_values(self, node: AVLNode | None, values: list[int]) -> None:
        if node is None:
            return
        if abs(node.balance_factor) > 1:
            values.append(node.value)
        self._collect_unbalanced_values(node.left, values)
        self._collect_unbalanced_values(node.right, values)

    def _step(
        self,
        event_type: EventType,
        message: str,
        metadata: dict[str, object] | None = None,
    ) -> Step:
        step_metadata = {
            "state": self.to_list(),
            "height": self.height(),
            "balanced": self.is_balanced(),
            "rebalance_pending": self.rebalance_pending,
            "unbalanced_values": self.unbalanced_values(),
        }
        if metadata:
            step_metadata.update(metadata)
        return Step(event_type, message, step_metadata)

    @staticmethod
    def _minimum_node(node: AVLNode) -> AVLNode:
        current = node
        while current.left is not None:
            current = current.left
        return current

    @staticmethod
    def _validate_integer(value: int, message: str) -> None:
        if type(value) is not int:
            raise TypeError(message)


def _height(node: AVLNode | None) -> int:
    return node.height if node is not None else 0


def _update_height(node: AVLNode) -> None:
    node.height = 1 + max(_height(node.left), _height(node.right))
