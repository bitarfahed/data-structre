"""Hash table domain model."""

from __future__ import annotations

from dataclasses import dataclass

from data_structures_visual_lab.events import EventType, Step


@dataclass
class HashEntry:
    """One key-value entry in a hash table bucket chain."""

    key: int
    value: int

    def __post_init__(self) -> None:
        _validate_integer(self.key, "HashTable keys must be integers.")
        _validate_integer(self.value, "HashTable values must be integers.")


class HashTable:
    """Integer-only hash table using fixed buckets and separate chaining."""

    def __init__(self, bucket_count: int = 8) -> None:
        if type(bucket_count) is not int:
            raise TypeError("HashTable bucket count must be an integer.")
        if bucket_count < 1:
            raise ValueError("HashTable bucket count must be at least 1.")
        self._buckets: list[list[HashEntry]] = [[] for _ in range(bucket_count)]
        self._size = 0

    def insert(self, key: int, value: int) -> bool:
        """Insert a key-value pair, preserving duplicate keys as separate entries."""
        self._validate_key_value(key, value)
        bucket = self._bucket_for(key)
        bucket.append(HashEntry(key, value))
        self._size += 1
        return True

    def insert_with_steps(self, key: int, value: int) -> tuple[bool, list[Step]]:
        """Insert a key-value pair and return observable steps."""
        self._validate_key_value(key, value)
        bucket_index = self.bucket_index(key)
        bucket = self._buckets[bucket_index]
        collision = bool(bucket)
        self.insert(key, value)
        entry_index = len(self._buckets[bucket_index]) - 1

        return True, [
            self._step(
                EventType.COMPARE,
                f"Calculated bucket index {bucket_index} for key {key}.",
                {
                    "key": key,
                    "value": value,
                    "bucket_index": bucket_index,
                    "collision": collision,
                    "entry_index": entry_index,
                },
            ),
            self._step(
                EventType.ADD,
                f"Inserted key {key} with value {value}.",
                {
                    "key": key,
                    "value": value,
                    "bucket_index": bucket_index,
                    "collision": collision,
                    "entry_index": entry_index,
                },
            ),
        ]

    def search(self, key: int) -> list[int]:
        """Return all values for key, or an empty list when key is missing."""
        self._validate_key(key)
        return [entry.value for entry in self._bucket_for(key) if entry.key == key]

    def search_with_steps(self, key: int) -> tuple[list[int], list[Step]]:
        """Search for a key and return observable steps."""
        self._validate_key(key)
        bucket_index = self.bucket_index(key)
        bucket = self._buckets[bucket_index]
        entry_indexes = self._entry_indexes(bucket, key)
        values = self.search(key)
        collision = len(bucket) > 1

        if not values:
            message = f"Key {key} was not found."
        elif len(values) == 1:
            message = f"Found key {key} with value {values[0]}."
        else:
            message = f"Found key {key} with values {values}."

        return values, [
            self._step(
                EventType.COMPARE,
                f"Calculated bucket index {bucket_index} for key {key}.",
                {
                    "key": key,
                    "bucket_index": bucket_index,
                    "collision": collision,
                    "entry_index": entry_indexes[0] if entry_indexes else None,
                    "entry_indexes": entry_indexes,
                },
            ),
            self._step(
                EventType.COMPLETE,
                message,
                {
                    "key": key,
                    "values": values,
                    "bucket_index": bucket_index,
                    "collision": collision,
                    "entry_index": entry_indexes[0] if entry_indexes else None,
                    "entry_indexes": entry_indexes,
                },
            ),
        ]

    def delete(self, key: int) -> bool:
        """Delete all entries for key when any exist."""
        self._validate_key(key)
        bucket = self._bucket_for(key)
        original_count = len(bucket)
        kept_entries = [entry for entry in bucket if entry.key != key]
        deleted_count = original_count - len(kept_entries)
        if deleted_count == 0:
            return False

        bucket[:] = kept_entries
        self._size -= deleted_count
        return True

    def delete_with_steps(self, key: int) -> tuple[bool, list[Step]]:
        """Delete a key and return observable steps."""
        self._validate_key(key)
        bucket_index = self.bucket_index(key)
        bucket = self._buckets[bucket_index]
        entry_indexes = self._entry_indexes(bucket, key)
        collision = len(bucket) > 1
        deleted_count = len(entry_indexes)
        deleted = self.delete(key)

        if deleted:
            if deleted_count == 1:
                message = f"Deleted 1 entry for key {key}."
            else:
                message = f"Deleted {deleted_count} entries for key {key}."
            event_type = EventType.REMOVE
        else:
            message = f"Delete skipped because key {key} was not found."
            event_type = EventType.COMPLETE

        return deleted, [
            self._step(
                EventType.COMPARE,
                f"Calculated bucket index {bucket_index} for key {key}.",
                {
                    "key": key,
                    "bucket_index": bucket_index,
                    "collision": collision,
                    "entry_index": entry_indexes[0] if entry_indexes else None,
                    "entry_indexes": entry_indexes,
                },
            ),
            self._step(
                event_type,
                message,
                {
                    "key": key,
                    "bucket_index": bucket_index,
                    "collision": collision,
                    "entry_index": entry_indexes[0] if entry_indexes else None,
                    "entry_indexes": entry_indexes,
                    "deleted_count": deleted_count,
                },
            ),
        ]

    @property
    def bucket_count(self) -> int:
        """Return the fixed number of buckets."""
        return len(self._buckets)

    @property
    def size(self) -> int:
        """Return the number of stored entries."""
        return self._size

    def bucket_index(self, key: int) -> int:
        """Return the bucket index calculated for key."""
        self._validate_key(key)
        return key % self.bucket_count

    def bucket_contents(self) -> list[list[tuple[int, int]]]:
        """Return all bucket chains as key-value pairs."""
        return [[(entry.key, entry.value) for entry in bucket] for bucket in self._buckets]

    def collision_for_key(self, key: int) -> bool:
        """Return True when key maps to a non-empty bucket."""
        self._validate_key(key)
        return bool(self._bucket_for(key))

    def display(self) -> str:
        """Return a readable bucket representation."""
        return f"HashTable(buckets={self.bucket_contents()})"

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return f"HashTable(bucket_count={self.bucket_count}, entries={self.bucket_contents()!r})"

    def __str__(self) -> str:
        return self.display()

    def _bucket_for(self, key: int) -> list[HashEntry]:
        return self._buckets[self.bucket_index(key)]

    @staticmethod
    def _entry_indexes(bucket: list[HashEntry], key: int) -> list[int]:
        return [index for index, entry in enumerate(bucket) if entry.key == key]

    def _step(
        self,
        event_type: EventType,
        message: str,
        metadata: dict[str, object] | None = None,
    ) -> Step:
        step_metadata = {
            "bucket_count": self.bucket_count,
            "buckets": self.bucket_contents(),
            "size": self.size,
        }
        if metadata:
            step_metadata.update(metadata)
        return Step(event_type, message, step_metadata)

    @staticmethod
    def _validate_key(key: int) -> None:
        _validate_integer(key, "HashTable keys must be integers.")

    def _validate_key_value(self, key: int, value: int) -> None:
        self._validate_key(key)
        _validate_integer(value, "HashTable values must be integers.")


def _validate_integer(value: int, message: str) -> None:
    if type(value) is not int:
        raise TypeError(message)
