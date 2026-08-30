import pytest

from data_structures_visual_lab.domain.data_structures.avl_tree import AVLNode, AVLTree


def assert_avl_invariant(node: AVLNode | None) -> int:
    if node is None:
        return 0

    left_height = assert_avl_invariant(node.left)
    right_height = assert_avl_invariant(node.right)

    assert node.height == 1 + max(left_height, right_height)
    assert node.balance_factor == left_height - right_height
    assert abs(node.balance_factor) <= 1
    return node.height


def insert_and_balance(tree: AVLTree, values: list[int]) -> None:
    for value in values:
        assert tree.insert(value)
        if tree.rebalance_pending:
            assert tree.balance()


def test_insert_performs_bst_insertion_without_immediate_balancing() -> None:
    tree = AVLTree()

    assert tree.insert(30)
    assert tree.insert(20)
    assert tree.insert(10)

    assert tree.root is not None
    assert tree.root.value == 30
    assert tree.root.left is not None
    assert tree.root.left.value == 20
    assert tree.root.left.left is not None
    assert tree.root.left.left.value == 10
    assert tree.to_list() == [10, 20, 30]


def test_insert_marks_pending_rebalance_when_tree_becomes_unbalanced() -> None:
    tree = AVLTree()

    tree.insert(30)
    tree.insert(20)
    tree.insert(10)

    assert not tree.is_balanced()
    assert tree.rebalance_pending


def test_insert_is_blocked_while_rebalance_is_pending() -> None:
    tree = AVLTree()
    tree.insert(30)
    tree.insert(20)
    tree.insert(10)

    assert not tree.insert(5)
    assert tree.to_list() == [10, 20, 30]


def test_right_rotation_balances_left_left_case() -> None:
    tree = AVLTree()
    tree.insert(30)
    tree.insert(20)
    tree.insert(10)

    assert tree.balance()

    assert tree.root is not None
    assert tree.root.value == 20
    assert tree.root.left is not None
    assert tree.root.left.value == 10
    assert tree.root.right is not None
    assert tree.root.right.value == 30
    assert tree.is_balanced()
    assert not tree.rebalance_pending


def test_left_rotation_balances_right_right_case() -> None:
    tree = AVLTree()
    tree.insert(10)
    tree.insert(20)
    tree.insert(30)

    assert tree.balance()

    assert tree.root is not None
    assert tree.root.value == 20
    assert tree.root.left is not None
    assert tree.root.left.value == 10
    assert tree.root.right is not None
    assert tree.root.right.value == 30
    assert tree.is_balanced()


def test_left_right_rotation_balances_left_right_case() -> None:
    tree = AVLTree()
    tree.insert(30)
    tree.insert(10)
    tree.insert(20)

    assert tree.balance()

    assert tree.root is not None
    assert tree.root.value == 20
    assert tree.root.left is not None
    assert tree.root.left.value == 10
    assert tree.root.right is not None
    assert tree.root.right.value == 30
    assert tree.is_balanced()


def test_right_left_rotation_balances_right_left_case() -> None:
    tree = AVLTree()
    tree.insert(10)
    tree.insert(30)
    tree.insert(20)

    assert tree.balance()

    assert tree.root is not None
    assert tree.root.value == 20
    assert tree.root.left is not None
    assert tree.root.left.value == 10
    assert tree.root.right is not None
    assert tree.root.right.value == 30
    assert tree.is_balanced()


def test_search_finds_existing_values_only() -> None:
    tree = AVLTree()
    insert_and_balance(tree, [8, 4, 12, 2, 6])

    assert tree.search(6)
    assert tree.search(12)
    assert not tree.search(7)


def test_min_and_max_return_extreme_values() -> None:
    tree = AVLTree()

    assert tree.min() is None
    assert tree.max() is None

    insert_and_balance(tree, [8, 4, 12, 2, 6, 14])

    assert tree.min() == 2
    assert tree.max() == 14


def test_delete_leaf_value() -> None:
    tree = AVLTree()
    insert_and_balance(tree, [8, 4, 12, 2, 6])

    assert tree.delete(2)

    assert tree.to_list() == [4, 6, 8, 12]
    assert not tree.search(2)
    assert_avl_invariant(tree.root)


def test_delete_value_with_two_children() -> None:
    tree = AVLTree()
    insert_and_balance(tree, [8, 4, 12, 2, 6, 10, 14])

    assert tree.delete(12)

    assert tree.to_list() == [2, 4, 6, 8, 10, 14]
    assert not tree.search(12)
    assert tree.search(14)
    assert_avl_invariant(tree.root)


def test_delete_root_value() -> None:
    tree = AVLTree()
    insert_and_balance(tree, [8, 4, 12, 2, 6, 10, 14])

    assert tree.delete(8)

    assert tree.root is not None
    assert tree.root.value != 8
    assert tree.to_list() == [2, 4, 6, 10, 12, 14]
    assert_avl_invariant(tree.root)


def test_delete_missing_value_is_safe() -> None:
    tree = AVLTree()
    insert_and_balance(tree, [2, 1, 3])

    assert not tree.delete(99)
    assert tree.to_list() == [1, 2, 3]


def test_balance_factor_and_height_accessors() -> None:
    tree = AVLTree()
    insert_and_balance(tree, [20, 10, 30, 5, 15])

    assert tree.height() == 3
    assert tree.node_height(20) == 3
    assert tree.node_height(10) == 2
    assert tree.balance_factor(20) == 1
    assert tree.balance_factor(99) is None
    assert tree.node_height(99) is None


def test_duplicate_values_are_rejected() -> None:
    tree = AVLTree()

    assert tree.insert(10)
    assert not tree.insert(10)

    assert tree.to_list() == [10]
    assert len(tree) == 1


@pytest.mark.parametrize("value", ["1", 1.5, None, True])
def test_insert_rejects_non_integer_values(value: object) -> None:
    tree = AVLTree()

    with pytest.raises(TypeError, match="integers"):
        tree.insert(value)  # type: ignore[arg-type]


@pytest.mark.parametrize("method_name", ["search", "delete", "balance_factor", "node_height"])
def test_lookup_methods_reject_non_integer_values(method_name: str) -> None:
    tree = AVLTree()
    method = getattr(tree, method_name)

    with pytest.raises(TypeError, match="integers"):
        method(False)


def test_repeated_insert_balance_cycles_keep_avl_invariant() -> None:
    tree = AVLTree()

    insert_and_balance(tree, [50, 40, 30, 60, 70, 65, 20, 10, 5, 35])

    assert tree.to_list() == [5, 10, 20, 30, 35, 40, 50, 60, 65, 70]
    assert tree.is_balanced()
    assert not tree.rebalance_pending
    assert_avl_invariant(tree.root)


def test_balance_returns_false_when_no_rebalance_is_needed() -> None:
    tree = AVLTree()

    assert not tree.balance()
    assert tree.insert(10)
    assert not tree.balance()


def test_insert_becomes_available_after_balance() -> None:
    tree = AVLTree()
    tree.insert(30)
    tree.insert(20)
    tree.insert(10)

    assert tree.rebalance_pending
    assert not tree.insert(5)
    assert tree.balance()
    assert tree.insert(5)

    assert tree.to_list() == [5, 10, 20, 30]
