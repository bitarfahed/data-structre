import pytest

from data_structures_visual_lab.domain.data_structures.two_three_tree import TwoThreeNode, TwoThreeTree
from data_structures_visual_lab.events import EventType


def assert_two_three_invariant(tree: TwoThreeTree) -> None:
    assert tree.is_valid()
    snapshots = tree.node_snapshots()
    ids = {snapshot.node_id for snapshot in snapshots}
    for snapshot in snapshots:
        assert 1 <= len(snapshot.keys) <= 2
        assert tuple(sorted(snapshot.keys)) == snapshot.keys
        assert all(child_id in ids for child_id in snapshot.child_ids)
        assert len(snapshot.child_ids) in (0, len(snapshot.keys) + 1)


def insert_and_repair(tree: TwoThreeTree, values: list[int]) -> None:
    for value in values:
        assert tree.insert_raw(value)
        if tree.repair_pending:
            assert tree.repair()


def test_insert_raw_into_empty_tree_creates_root() -> None:
    tree = TwoThreeTree()

    assert tree.insert_raw(10)

    assert tree.root is not None
    assert tree.root.keys == [10]
    assert tree.to_list() == [10]
    assert tree.size == 1
    assert tree.is_valid()
    assert not tree.repair_pending


def test_insert_raw_into_two_node_leaf_without_overflow() -> None:
    tree = TwoThreeTree()

    assert tree.insert_raw(10)
    assert tree.insert_raw(5)

    assert tree.root is not None
    assert tree.root.keys == [5, 10]
    assert tree.to_list() == [5, 10]
    assert tree.is_valid()
    assert not tree.repair_pending


def test_insert_raw_creates_leaf_overflow_and_pending_repair() -> None:
    tree = TwoThreeTree()

    tree.insert_raw(10)
    tree.insert_raw(5)
    assert tree.insert_raw(15)

    assert tree.root is not None
    assert tree.root.keys == [5, 10, 15]
    assert not tree.is_valid()
    assert tree.repair_pending
    assert tree.invalid_node_id == tree.root.node_id
    assert tree.invalid_node_keys == (5, 10, 15)


def test_repair_splits_overflowing_root() -> None:
    tree = TwoThreeTree()
    tree.insert_raw(10)
    tree.insert_raw(5)
    tree.insert_raw(15)

    assert tree.repair()

    assert tree.root is not None
    assert tree.root.keys == [10]
    assert [child.keys for child in tree.root.children] == [[5], [15]]
    assert tree.to_list() == [5, 10, 15]
    assert not tree.repair_pending
    assert tree.invalid_node_id is None
    assert_two_three_invariant(tree)


def test_key_promotion_splits_leaf_into_parent() -> None:
    tree = TwoThreeTree()
    insert_and_repair(tree, [10, 5, 15])

    assert tree.insert_raw(12)
    assert tree.insert_raw(11)
    assert tree.repair_pending
    assert tree.repair()

    assert tree.root is not None
    assert tree.root.keys == [10, 12]
    assert [child.keys for child in tree.root.children] == [[5], [11], [15]]
    assert tree.to_list() == [5, 10, 11, 12, 15]
    assert_two_three_invariant(tree)


def test_repair_may_propagate_upward_and_create_new_root() -> None:
    tree = TwoThreeTree()
    insert_and_repair(tree, [10, 5, 15, 12, 11])

    assert tree.insert_raw(20)
    assert tree.insert_raw(25)
    assert tree.repair_pending
    assert tree.repair()

    assert tree.root is not None
    assert tree.root.keys == [12]
    assert [child.keys for child in tree.root.children] == [[10], [20]]
    assert [[grandchild.keys for grandchild in child.children] for child in tree.root.children] == [
        [[5], [11]],
        [[15], [25]],
    ]
    assert tree.to_list() == [5, 10, 11, 12, 15, 20, 25]
    assert_two_three_invariant(tree)


def test_insert_is_blocked_while_repair_is_pending() -> None:
    tree = TwoThreeTree()
    tree.insert_raw(10)
    tree.insert_raw(5)
    tree.insert_raw(15)

    assert not tree.insert_raw(20)
    assert tree.to_list() == [5, 10, 15]


def test_repair_returns_false_when_no_repair_is_pending() -> None:
    tree = TwoThreeTree()

    assert not tree.repair()
    assert tree.insert_raw(10)
    assert not tree.repair()


def test_search_finds_existing_values_only() -> None:
    tree = TwoThreeTree()
    insert_and_repair(tree, [10, 5, 15, 12, 11, 20, 25])

    assert tree.search(5)
    assert tree.search(12)
    assert tree.search(25)
    assert not tree.search(99)


def test_duplicate_values_are_rejected() -> None:
    tree = TwoThreeTree()

    assert tree.insert_raw(10)
    assert not tree.insert_raw(10)

    assert tree.to_list() == [10]
    assert tree.size == 1
    assert not tree.repair_pending


@pytest.mark.parametrize("value", ["1", 1.5, None, True])
def test_insert_rejects_non_integer_values(value: object) -> None:
    tree = TwoThreeTree()

    with pytest.raises(TypeError, match="integers"):
        tree.insert_raw(value)  # type: ignore[arg-type]


@pytest.mark.parametrize("value", ["1", 1.5, None, False])
def test_search_rejects_non_integer_values(value: object) -> None:
    tree = TwoThreeTree()

    with pytest.raises(TypeError, match="integers"):
        tree.search(value)  # type: ignore[arg-type]


def test_node_rejects_empty_or_non_integer_keys() -> None:
    with pytest.raises(ValueError, match="at least one key"):
        TwoThreeNode([])
    with pytest.raises(TypeError, match="integers"):
        TwoThreeNode([1, "2"])  # type: ignore[list-item]


def test_repeated_insert_repair_cycles_keep_tree_valid() -> None:
    tree = TwoThreeTree()
    values = [30, 10, 50, 5, 20, 40, 60, 1, 7, 15, 25, 35, 45, 55, 65]

    insert_and_repair(tree, values)

    assert tree.to_list() == sorted(values)
    assert tree.size == len(values)
    assert not tree.repair_pending
    assert_two_three_invariant(tree)


def test_node_snapshots_expose_keys_children_and_overflow() -> None:
    tree = TwoThreeTree()
    insert_and_repair(tree, [10, 5, 15])
    tree.insert_raw(12)
    tree.insert_raw(11)

    snapshots = tree.node_snapshots()
    overflowing = [snapshot for snapshot in snapshots if snapshot.overflowing]

    assert overflowing
    assert overflowing[0].keys == (11, 12, 15)
    assert tree.invalid_node_id == overflowing[0].node_id
    assert any(snapshot.child_ids for snapshot in snapshots)


def test_insert_raw_steps_expose_overflow_state() -> None:
    tree = TwoThreeTree()
    tree.insert_raw(10)
    tree.insert_raw(5)

    ok, steps = tree.insert_raw_with_steps(15)

    assert ok
    assert [step.event_type for step in steps] == [EventType.ADD, EventType.COMPLETE]
    assert steps[-1].message == "Raw insert complete. Repair required before another insert."
    assert steps[-1].metadata["repair_pending"] is True
    assert steps[-1].metadata["invalid_node_keys"] == (5, 10, 15)


def test_repair_steps_expose_valid_repaired_state() -> None:
    tree = TwoThreeTree()
    tree.insert_raw(10)
    tree.insert_raw(5)
    tree.insert_raw(15)

    ok, steps = tree.repair_with_steps()

    assert ok
    assert [step.event_type for step in steps] == [EventType.MOVE, EventType.COMPLETE]
    assert steps[-1].message == "2-3 Tree repair complete. Tree is valid."
    assert steps[-1].metadata["tree_valid"] is True
    assert steps[-1].metadata["repair_pending"] is False


def test_search_steps_expose_found_and_missing_paths() -> None:
    tree = TwoThreeTree()
    insert_and_repair(tree, [10, 5, 15, 12, 11])

    found, found_steps = tree.search_with_steps(11)
    missing, missing_steps = tree.search_with_steps(99)

    assert found
    assert found_steps[-1].message == "2-3 Tree search found 11."
    assert found_steps[-1].metadata["highlight_value"] == 11
    assert not missing
    assert missing_steps[-1].message == "2-3 Tree search did not find 99."
    assert missing_steps[-1].metadata["search_path_node_ids"]
