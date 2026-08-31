from data_structures_visual_lab.domain.algorithms import (
    AlgorithmEventType,
    AlgorithmState,
    make_algorithm_step,
    parse_integer_array_text,
    validate_ascending_sorted,
    validate_integer_array,
)


def test_algorithm_state_can_represent_search_and_sort_metadata() -> None:
    state = AlgorithmState(
        values=(4, 2, 1),
        current_indices=(0, 2),
        comparison_indices=(0, 1),
        swapped_indices=(1, 2),
        current_range=(0, 2),
        pivot_index=1,
        merge_ranges=((0, 1), (2, 2)),
        found_index=2,
        found=True,
        completed=True,
        metadata={"note": "future visualizer data"},
    )

    assert state.values == (4, 2, 1)
    assert state.current_indices == (0, 2)
    assert state.comparison_indices == (0, 1)
    assert state.swapped_indices == (1, 2)
    assert state.current_range == (0, 2)
    assert state.pivot_index == 1
    assert state.merge_ranges == ((0, 1), (2, 2))
    assert state.found_index == 2
    assert state.found is True
    assert state.completed
    assert state.metadata["note"] == "future visualizer data"


def test_make_algorithm_step_normalizes_values_to_tuple() -> None:
    step = make_algorithm_step(
        AlgorithmEventType.COMPARE,
        "Compare indices 0 and 1.",
        [3, 1],
        comparison_indices=(0, 1),
    )

    assert step.event_type is AlgorithmEventType.COMPARE
    assert step.message == "Compare indices 0 and 1."
    assert step.state.values == (3, 1)
    assert step.state.comparison_indices == (0, 1)


def test_algorithm_event_types_cover_round_3_visualization_needs() -> None:
    assert {event.value for event in AlgorithmEventType} == {
        "COMPARE",
        "SWAP",
        "VISIT",
        "MOVE",
        "PIVOT",
        "MERGE",
        "FOUND",
        "NOT_FOUND",
        "COMPLETE",
    }


def test_validate_integer_array_accepts_edge_case_inputs() -> None:
    assert validate_integer_array([]).values == ()
    assert validate_integer_array([5]).values == (5,)
    assert validate_integer_array([1, 1, 2]).values == (1, 1, 2)
    assert validate_integer_array([1, 2, 3]).values == (1, 2, 3)
    assert validate_integer_array([3, 2, 1]).values == (3, 2, 1)


def test_validate_integer_array_rejects_non_integer_input() -> None:
    for values in ("1,2,3", [1, "2"], [1.5], [True], None):
        result = validate_integer_array(values)

        assert not result.ok
        assert result.values == ()
        assert result.message


def test_parse_integer_array_text_accepts_commas_spaces_empty_and_negative_values() -> None:
    assert parse_integer_array_text("").values == ()
    assert parse_integer_array_text("  ").values == ()
    assert parse_integer_array_text("1, 2, -3, 2").values == (1, 2, -3, 2)


def test_parse_integer_array_text_rejects_invalid_text() -> None:
    for text in ("1 two 3", "1,,3", "1, 2.5", "1, true"):
        result = parse_integer_array_text(text)

        assert not result.ok
        assert result.message == "Array values must be integers."


def test_validate_ascending_sorted_accepts_empty_single_duplicate_and_sorted_arrays() -> None:
    assert validate_ascending_sorted(()).ok
    assert validate_ascending_sorted((1,)).ok
    assert validate_ascending_sorted((1, 1, 2, 3)).ok


def test_validate_ascending_sorted_rejects_unsorted_binary_search_input() -> None:
    result = validate_ascending_sorted((1, 3, 2))
    reverse_result = validate_ascending_sorted((3, 2, 1))

    assert not result.ok
    assert result.values == (1, 3, 2)
    assert result.message == "Binary Search requires ascending sorted input."
    assert not reverse_result.ok
    assert reverse_result.values == (3, 2, 1)
    assert reverse_result.message == "Binary Search requires ascending sorted input."
