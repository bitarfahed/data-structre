"""2-3 tree domain model."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TwoThreeNode:
    """A node in a 2-3 tree."""

    keys: list[int]
    children: list[TwoThreeNode] = field(default_factory=list)
    parent: TwoThreeNode | None = field(default=None, repr=False)
    node_id: int = -1

    def __post_init__(self) -> None:
        if not self.keys:
            raise ValueError("TwoThreeNode must contain at least one key.")
        if any(type(key) is not int for key in self.keys):
            raise TypeError("TwoThreeNode keys must be integers.")
        self.keys.sort()
        for child in self.children:
            child.parent = self

    @property
    def is_leaf(self) -> bool:
        """Return True when this node has no children."""
        return not self.children

    @property
    def is_overflowing(self) -> bool:
        """Return True when this node temporarily has too many keys."""
        return len(self.keys) > 2


@dataclass(frozen=True)
class TwoThreeNodeSnapshot:
    """Renderer-friendly state for one 2-3 tree node."""

    node_id: int
    keys: tuple[int, ...]
    child_ids: tuple[int, ...]
    parent_id: int | None
    overflowing: bool = False


class TwoThreeTree:
    """Integer-only 2-3 tree with explicit deferred structural repair."""

    def __init__(self) -> None:
        self.root: TwoThreeNode | None = None
        self._size = 0
        self._repair_pending = False
        self._invalid_node: TwoThreeNode | None = None
        self._next_node_id = 0

    def insert_raw(self, value: int) -> bool:
        """Insert value into the target leaf without completing split repair."""
        self._validate_integer(value)
        if self._repair_pending:
            return False
        if self.search(value):
            return False

        if self.root is None:
            self.root = self._new_node([value])
            self._size = 1
            return True

        leaf = self._find_leaf(value)
        leaf.keys.append(value)
        leaf.keys.sort()
        self._size += 1

        if leaf.is_overflowing:
            self._repair_pending = True
            self._invalid_node = leaf
        return True

    def repair(self) -> bool:
        """Restore 2-3 tree validity by splitting overflowing nodes upward."""
        if not self._repair_pending or self._invalid_node is None:
            return False

        node = self._invalid_node
        while node is not None and node.is_overflowing:
            node = self._split_overflowing_node(node)

        self._repair_pending = False
        self._invalid_node = None
        return True

    def search(self, value: int) -> bool:
        """Return True when value exists in the tree."""
        self._validate_integer(value)
        current = self.root

        while current is not None:
            if value in current.keys:
                return True
            if current.is_leaf:
                return False
            current = current.children[self._child_index_for_value(current, value)]

        return False

    def is_valid(self) -> bool:
        """Return True when all 2-3 tree invariants currently hold."""
        if self.root is None:
            return not self._repair_pending
        leaf_depths: list[int] = []
        return self._validate_subtree(
            self.root,
            minimum=None,
            maximum=None,
            depth=0,
            leaf_depths=leaf_depths,
        ) and len(set(leaf_depths)) <= 1

    @property
    def repair_pending(self) -> bool:
        """Return True when insertion is blocked until repair() runs."""
        return self._repair_pending

    @property
    def invalid_node_id(self) -> int | None:
        """Return the overflowing node id, when one is known."""
        if self._invalid_node is None:
            return None
        return self._invalid_node.node_id

    @property
    def invalid_node_keys(self) -> tuple[int, ...]:
        """Return the overflowing node keys, when one is known."""
        if self._invalid_node is None:
            return ()
        return tuple(self._invalid_node.keys)

    @property
    def size(self) -> int:
        """Return the number of stored keys."""
        return self._size

    def to_list(self) -> list[int]:
        """Return keys in sorted order."""
        values: list[int] = []
        self._in_order(self.root, values)
        return values

    def node_snapshots(self) -> tuple[TwoThreeNodeSnapshot, ...]:
        """Return all node keys and child relationships for future visualization."""
        snapshots: list[TwoThreeNodeSnapshot] = []
        self._collect_snapshots(self.root, snapshots)
        return tuple(snapshots)

    def display(self) -> str:
        """Return a readable sorted-key representation."""
        return f"TwoThreeTree(in-order): {self.to_list()}"

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return f"TwoThreeTree({self.to_list()!r})"

    def __str__(self) -> str:
        return self.display()

    def _split_overflowing_node(self, node: TwoThreeNode) -> TwoThreeNode | None:
        left_key, promoted_key, right_key = node.keys
        left_children = node.children[:2]
        right_children = node.children[2:]
        left_node = self._new_node([left_key], left_children)
        right_node = self._new_node([right_key], right_children)

        parent = node.parent
        if parent is None:
            self.root = self._new_node([promoted_key], [left_node, right_node])
            return None

        child_index = parent.children.index(node)
        parent.children.pop(child_index)
        parent.children.insert(child_index, right_node)
        parent.children.insert(child_index, left_node)
        left_node.parent = parent
        right_node.parent = parent
        parent.keys.insert(child_index, promoted_key)
        return parent

    def _find_leaf(self, value: int) -> TwoThreeNode:
        if self.root is None:
            raise ValueError("Cannot find a leaf in an empty tree.")

        current = self.root
        while not current.is_leaf:
            current = current.children[self._child_index_for_value(current, value)]
        return current

    @staticmethod
    def _child_index_for_value(node: TwoThreeNode, value: int) -> int:
        if value < node.keys[0]:
            return 0
        if len(node.keys) == 1 or value < node.keys[1]:
            return 1
        return 2

    def _validate_subtree(
        self,
        node: TwoThreeNode,
        minimum: int | None,
        maximum: int | None,
        depth: int,
        leaf_depths: list[int],
    ) -> bool:
        if node.node_id < 0:
            return False
        if len(node.keys) not in (1, 2):
            return False
        if node.keys != sorted(node.keys) or len(set(node.keys)) != len(node.keys):
            return False
        if any((minimum is not None and key <= minimum) or (maximum is not None and key >= maximum) for key in node.keys):
            return False

        if node.is_leaf:
            leaf_depths.append(depth)
            return True
        if len(node.children) != len(node.keys) + 1:
            return False
        if any(child.parent is not node for child in node.children):
            return False

        if len(node.keys) == 1:
            ranges = ((minimum, node.keys[0]), (node.keys[0], maximum))
        else:
            ranges = (
                (minimum, node.keys[0]),
                (node.keys[0], node.keys[1]),
                (node.keys[1], maximum),
            )
        return all(
            self._validate_subtree(child, child_minimum, child_maximum, depth + 1, leaf_depths)
            for child, (child_minimum, child_maximum) in zip(node.children, ranges)
        )

    def _in_order(self, node: TwoThreeNode | None, values: list[int]) -> None:
        if node is None:
            return
        if node.is_leaf:
            values.extend(node.keys)
            return
        self._in_order(node.children[0], values)
        values.append(node.keys[0])
        self._in_order(node.children[1], values)
        if len(node.keys) == 2:
            values.append(node.keys[1])
            self._in_order(node.children[2], values)

    def _collect_snapshots(self, node: TwoThreeNode | None, snapshots: list[TwoThreeNodeSnapshot]) -> None:
        if node is None:
            return
        snapshots.append(
            TwoThreeNodeSnapshot(
                node_id=node.node_id,
                keys=tuple(node.keys),
                child_ids=tuple(child.node_id for child in node.children),
                parent_id=node.parent.node_id if node.parent is not None else None,
                overflowing=node.is_overflowing,
            )
        )
        for child in node.children:
            self._collect_snapshots(child, snapshots)

    def _new_node(self, keys: list[int], children: list[TwoThreeNode] | None = None) -> TwoThreeNode:
        node = TwoThreeNode(keys=keys, children=children or [], node_id=self._next_node_id)
        self._next_node_id += 1
        return node

    @staticmethod
    def _validate_integer(value: int) -> None:
        if type(value) is not int:
            raise TypeError("TwoThreeTree values must be integers.")
