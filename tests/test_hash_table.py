import pytest

from data_structures_visual_lab.domain.data_structures.hash_table import HashEntry, HashTable
from data_structures_visual_lab.events import EventType


def test_insert_stores_integer_key_value_pair() -> None:
    table = HashTable()

    assert table.insert(3, 30)

    assert table.search(3) == [30]
    assert table.size == 1
    assert len(table) == 1
    assert table.bucket_contents()[3] == [(3, 30)]


def test_bucket_index_uses_fixed_bucket_count() -> None:
    table = HashTable(bucket_count=4)

    assert table.bucket_count == 4
    assert table.bucket_index(0) == 0
    assert table.bucket_index(5) == 1
    assert table.bucket_index(-1) == 3


def test_collisions_use_separate_chaining() -> None:
    table = HashTable(bucket_count=4)

    assert table.insert(1, 10)
    assert table.collision_for_key(5)
    assert table.insert(5, 50)

    assert table.bucket_contents()[1] == [(1, 10), (5, 50)]
    assert table.search(1) == [10]
    assert table.search(5) == [50]


def test_duplicate_keys_are_preserved_as_multiple_entries() -> None:
    table = HashTable()

    assert table.insert(2, 20)
    assert table.insert(2, 99)

    assert table.search(2) == [20, 99]
    assert table.collision_for_key(2)
    assert table.size == 2
    assert table.bucket_contents()[2] == [(2, 20), (2, 99)]


def test_repeated_duplicate_insertions_accumulate_in_order() -> None:
    table = HashTable(bucket_count=4)

    for value in (1, 2, 3, 4):
        assert table.insert(0, value)

    assert table.search(0) == [1, 2, 3, 4]
    assert table.bucket_contents()[0] == [(0, 1), (0, 2), (0, 3), (0, 4)]
    assert table.size == 4


def test_search_missing_key_returns_empty_list() -> None:
    table = HashTable()

    table.insert(1, 10)

    assert table.search(9) == []


def test_delete_existing_key_removes_entry() -> None:
    table = HashTable(bucket_count=4)
    table.insert(1, 10)
    table.insert(5, 50)

    assert table.delete(1)

    assert table.search(1) == []
    assert table.search(5) == [50]
    assert table.bucket_contents()[1] == [(5, 50)]
    assert table.size == 1


def test_delete_removes_all_entries_for_duplicate_key_only() -> None:
    table = HashTable(bucket_count=4)
    table.insert(1, 10)
    table.insert(5, 50)
    table.insert(1, 99)
    table.insert(9, 90)

    assert table.delete(1)

    assert table.search(1) == []
    assert table.search(5) == [50]
    assert table.search(9) == [90]
    assert table.bucket_contents()[1] == [(5, 50), (9, 90)]
    assert table.size == 2


def test_delete_missing_key_is_safe() -> None:
    table = HashTable()

    table.insert(1, 10)

    assert not table.delete(2)
    assert table.bucket_contents()[1] == [(1, 10)]


def test_empty_table_behavior_is_safe() -> None:
    table = HashTable()

    assert table.search(1) == []
    assert not table.delete(1)
    assert table.size == 0
    assert table.bucket_contents() == [[], [], [], [], [], [], [], []]


@pytest.mark.parametrize("key", ["1", 1.5, None, True])
def test_key_operations_reject_non_integer_keys(key: object) -> None:
    table = HashTable()

    with pytest.raises(TypeError, match="keys"):
        table.insert(key, 1)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="keys"):
        table.search(key)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="keys"):
        table.delete(key)  # type: ignore[arg-type]


@pytest.mark.parametrize("value", ["1", 1.5, None, False])
def test_insert_rejects_non_integer_values(value: object) -> None:
    table = HashTable()

    with pytest.raises(TypeError, match="values"):
        table.insert(1, value)  # type: ignore[arg-type]


def test_hash_entry_rejects_non_integer_key_or_value() -> None:
    with pytest.raises(TypeError, match="keys"):
        HashEntry("1", 1)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="values"):
        HashEntry(1, "1")  # type: ignore[arg-type]


def test_invalid_bucket_count_is_rejected() -> None:
    with pytest.raises(TypeError, match="bucket count"):
        HashTable(bucket_count=True)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="at least 1"):
        HashTable(bucket_count=0)


def test_insert_steps_expose_bucket_index_and_collision() -> None:
    table = HashTable(bucket_count=4)
    table.insert(1, 10)

    ok, steps = table.insert_with_steps(5, 50)

    assert ok
    assert [step.event_type for step in steps] == [EventType.COMPARE, EventType.ADD]
    assert steps[-1].metadata["bucket_index"] == 1
    assert steps[-1].metadata["collision"] is True
    assert steps[-1].metadata["entry_index"] == 1
    assert steps[-1].metadata["buckets"] == [[], [(1, 10), (5, 50)], [], []]


def test_duplicate_insert_steps_report_added_entry() -> None:
    table = HashTable()
    table.insert(2, 20)

    ok, steps = table.insert_with_steps(2, 99)

    assert ok
    assert steps[-1].event_type is EventType.ADD
    assert steps[-1].message == "Inserted key 2 with value 99."
    assert steps[-1].metadata["collision"] is True
    assert steps[-1].metadata["entry_index"] == 1
    assert table.search(2) == [20, 99]


def test_search_steps_highlight_found_and_missing_bucket() -> None:
    table = HashTable(bucket_count=4)
    table.insert(1, 10)
    table.insert(5, 50)

    found, found_steps = table.search_with_steps(5)
    missing, missing_steps = table.search_with_steps(9)

    assert found == [50]
    assert found_steps[-1].message == "Found key 5 with value 50."
    assert found_steps[-1].metadata["bucket_index"] == 1
    assert found_steps[-1].metadata["entry_index"] == 1
    assert found_steps[-1].metadata["collision"] is True
    assert missing == []
    assert missing_steps[-1].message == "Key 9 was not found."
    assert missing_steps[-1].metadata["bucket_index"] == 1
    assert missing_steps[-1].metadata["entry_index"] is None


def test_delete_steps_expose_bucket_and_entry() -> None:
    table = HashTable(bucket_count=4)
    table.insert(1, 10)
    table.insert(5, 50)

    deleted, steps = table.delete_with_steps(5)

    assert deleted
    assert steps[-1].event_type is EventType.REMOVE
    assert steps[-1].metadata["bucket_index"] == 1
    assert steps[-1].metadata["entry_index"] == 1
    assert table.bucket_contents()[1] == [(1, 10)]


def test_delete_steps_report_all_removed_duplicate_entries() -> None:
    table = HashTable(bucket_count=4)
    table.insert(1, 10)
    table.insert(5, 50)
    table.insert(1, 99)

    deleted, steps = table.delete_with_steps(1)

    assert deleted
    assert steps[-1].message == "Deleted 2 entries for key 1."
    assert steps[-1].metadata["entry_indexes"] == [0, 2]
    assert steps[-1].metadata["deleted_count"] == 2
    assert table.bucket_contents()[1] == [(5, 50)]


def test_display_representation() -> None:
    table = HashTable(bucket_count=2)
    table.insert(1, 10)

    assert table.display() == "HashTable(buckets=[[], [(1, 10)]])"
    assert str(table) == table.display()
    assert repr(table) == "HashTable(bucket_count=2, entries=[[], [(1, 10)]])"
