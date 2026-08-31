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
        """Insert a key-value pair, updating the value when the key already exists."""
        self._validate_key_value(key, value)
        bucket = self._bucket_for(key)
        existing = self._find_entry(bucket, key)
        if existing is not None:
            existing.value = value
            return False

        bucket.append(HashEntry(key, value))
        self._size += 1
        return True

    def insert_with_steps(self, key: int, value: int) -> tuple[bool, list[Step]]:
        """Insert a key-value pair and return observable steps."""
        self._validate_key_value(key, value)
        bucket_index = self.bucket_index(key)
        bucket = self._buckets[bucket_index]
        existing_index = self._entry_index(bucket, key)
        collision = bool(bucket and existing_index is None)
        inserted = self.insert(key, value)
        entry_index = self._entry_index(self._buckets[bucket_index], key)

        if inserted:
            message = f"Inserted key {key} with value {value}."
            event_type = EventType.ADD
        else:
            message = f"Updated key {key} with value {value}."
            event_type = EventType.UPDATE

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
                event_type,
                message,
                {
                    "key": key,
                    "value": value,
                    "bucket_index": bucket_index,
                    "collision": collision,
                    "entry_index": entry_index,
                },
            ),
        ]

    def search(self, key: int) -> int | None:
        """Return the value for key, or None when key is missing."""
        self._validate_key(key)
        entry = self._find_entry(self._bucket_for(key), key)
        if entry is None:
            return None
        return entry.value

    def search_with_steps(self, key: int) -> tuple[int | None, list[Step]]:
        """Search for a key and return observable steps."""
        self._validate_key(key)
        bucket_index = self.bucket_index(key)
        bucket = self._buckets[bucket_index]
        entry_index = self._entry_index(bucket, key)
        value = self.search(key)
        collision = len(bucket) > 1

        if value is None:
            message = f"Key {key} was not found."
        else:
            message = f"Found key {key} with value {value}."

        return value, [
            self._step(
                EventType.COMPARE,
                f"Calculated bucket index {bucket_index} for key {key}.",
                {
                    "key": key,
                    "bucket_index": bucket_index,
                    "collision": collision,
                    "entry_index": entry_index,
                },
            ),
            self._step(
                EventType.COMPLETE,
                message,
                {
                    "key": key,
                    "value": value,
                    "bucket_index": bucket_index,
                    "collision": collision,
                    "entry_index": entry_index,
                },
            ),
        ]

    def delete(self, key: int) -> bool:
        """Delete a key-value pair when it exists."""
        self._validate_key(key)
        bucket = self._bucket_for(key)
        entry_index = self._entry_index(bucket, key)
        if entry_index is None:
            return False

        bucket.pop(entry_index)
        self._size -= 1
        return True

    def delete_with_steps(self, key: int) -> tuple[bool, list[Step]]:
        """Delete a key and return observable steps."""
        self._validate_key(key)
        bucket_index = self.bucket_index(key)
        bucket = self._buckets[bucket_index]
        entry_index = self._entry_index(bucket, key)
        collision = len(bucket) > 1
        deleted = self.delete(key)

        if deleted:
            message = f"Deleted key {key}."
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
                    "entry_index": entry_index,
                },
            ),
            self._step(
                event_type,
                message,
                {
                    "key": key,
                    "bucket_index": bucket_index,
                    "collision": collision,
                    "entry_index": entry_index,
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
        """Return True when key maps to a non-empty bucket without matching an existing key."""
        self._validate_key(key)
        bucket = self._bucket_for(key)
        return bool(bucket and self._find_entry(bucket, key) is None)

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
    def _find_entry(bucket: list[HashEntry], key: int) -> HashEntry | None:
        for entry in bucket:
            if entry.key == key:
                return entry
        return None

    @staticmethod
    def _entry_index(bucket: list[HashEntry], key: int) -> int | None:
        for index, entry in enumerate(bucket):
            if entry.key == key:
                return index
        return None

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
