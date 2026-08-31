from data_structures_visual_lab.domain.algorithms import AlgorithmEventType, binary_search


def test_binary_search_finds_target() -> None:
    result = binary_search((1, 3, 5, 7, 9), 7)

    assert result.ok
    assert result.index == 3
    assert result.message == "Found target 7 at index 3."
    assert result.steps[-1].event_type is AlgorithmEventType.FOUND


def test_binary_search_reports_not_found() -> None:
    result = binary_search((1, 3, 5, 7), 4)

    assert not result.ok
    assert result.index is None
    assert result.message == "Target 4 was not found."
    assert result.steps[-1].event_type is AlgorithmEventType.NOT_FOUND
    assert result.steps[-1].state.completed
    assert result.steps[-1].state.found is False


def test_binary_search_finds_first_and_last_positions() -> None:
    first = binary_search((1, 2, 3), 1)
    last = binary_search((1, 2, 3), 3)

    assert first.index == 0
    assert last.index == 2


def test_binary_search_returns_one_duplicate_occurrence() -> None:
    result = binary_search((1, 2, 2, 2, 3), 2)

    assert result.ok
    assert result.index in {1, 2, 3}
    assert result.steps[-1].state.found_index == result.index


def test_binary_search_handles_empty_array_safely() -> None:
    result = binary_search((), 5)

    assert not result.ok
    assert result.index is None
    assert result.steps[-1].event_type is AlgorithmEventType.NOT_FOUND
    assert result.steps[-1].state.values == ()


def test_binary_search_handles_single_element_array() -> None:
    found = binary_search((5,), 5)
    missing = binary_search((5,), 4)

    assert found.ok
    assert found.index == 0
    assert not missing.ok
    assert missing.index is None


def test_binary_search_rejects_unsorted_input_without_sorting() -> None:
    result = binary_search((1, 4, 3), 3)

    assert not result.ok
    assert result.index is None
    assert result.steps == []
    assert result.message == "Binary Search requires ascending sorted input."


def test_binary_search_rejects_non_integer_array_or_target() -> None:
    invalid_array = binary_search((1, "2"), 2)  # type: ignore[list-item]
    invalid_target = binary_search((1, 2), "2")  # type: ignore[arg-type]

    assert not invalid_array.ok
    assert invalid_array.message == "Array values must be integers."
    assert not invalid_target.ok
    assert invalid_target.message == "Target must be an integer."


def test_binary_search_steps_expose_low_mid_high_and_discarded_ranges() -> None:
    result = binary_search((1, 3, 5, 7, 9), 9)

    compare_steps = [step for step in result.steps if step.event_type is AlgorithmEventType.COMPARE]
    move_steps = [step for step in result.steps if step.event_type is AlgorithmEventType.MOVE]

    assert compare_steps[0].state.metadata["low_index"] == 0
    assert compare_steps[0].state.metadata["high_index"] == 4
    assert compare_steps[0].state.metadata["mid_index"] == 2
    assert compare_steps[0].state.metadata["mid_value"] == 5
    assert move_steps[0].state.metadata["discarded_range"] == (0, 2)
    assert result.steps[-1].state.found_index == 4
    assert result.steps[-1].state.completed
