import pytest

from data_structures_visual_lab.domain.algorithms import (
    AlgorithmEventType,
    bubble_sort,
    heap_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    selection_sort,
)


SORTS = [
    (bubble_sort, "Bubble Sort complete."),
    (selection_sort, "Selection Sort complete."),
    (insertion_sort, "Insertion Sort complete."),
    (merge_sort, "Merge Sort complete."),
    (quick_sort, "Quick Sort complete."),
    (heap_sort, "Heap Sort complete."),
]


@pytest.mark.parametrize(("sort_func", "message"), SORTS)
@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ((4, 1, 3, 2), (1, 2, 3, 4)),
        ((2, 1, 2, 1), (1, 1, 2, 2)),
        ((), ()),
        ((7,), (7,)),
        ((1, 2, 3), (1, 2, 3)),
        ((3, 2, 1), (1, 2, 3)),
        ((0, -2, 5, -1), (-2, -1, 0, 5)),
    ],
)
def test_sorting_algorithms_handle_round_3_edge_cases(sort_func, message: str, values: tuple[int, ...], expected: tuple[int, ...]) -> None:
    result = sort_func(values)

    assert result.ok
    assert result.values == expected
    assert result.message == message
    assert result.steps[-1].event_type is AlgorithmEventType.COMPLETE
    assert result.steps[-1].state.values == expected
    assert result.steps[-1].state.completed


@pytest.mark.parametrize("sort_func", [bubble_sort, selection_sort, insertion_sort, merge_sort, quick_sort, heap_sort])
def test_sorting_algorithms_reject_non_integer_values(sort_func) -> None:
    result = sort_func((1, "2", 3))

    assert not result.ok
    assert result.values == ()
    assert result.steps == []
    assert result.message == "Array values must be integers."


def test_bubble_sort_steps_expose_comparisons_swaps_and_sorted_suffix() -> None:
    result = bubble_sort((3, 1, 2))

    compare_steps = [step for step in result.steps if step.event_type is AlgorithmEventType.COMPARE]
    swap_steps = [step for step in result.steps if step.event_type is AlgorithmEventType.SWAP]

    assert compare_steps[0].state.comparison_indices == (0, 1)
    assert compare_steps[0].state.metadata["compared_values"] == (3, 1)
    assert swap_steps[0].state.swapped_indices == (0, 1)
    assert swap_steps[0].state.values == (1, 3, 2)
    assert result.steps[-1].state.metadata["sorted_suffix_start"] == 0


def test_selection_sort_steps_expose_current_position_minimum_and_swap() -> None:
    result = selection_sort((3, 1, 2))

    visit_steps = [step for step in result.steps if step.event_type is AlgorithmEventType.VISIT]
    swap_steps = [step for step in result.steps if step.event_type is AlgorithmEventType.SWAP]

    assert visit_steps[0].state.metadata["current_position"] == 0
    assert visit_steps[0].state.metadata["min_index"] == 0
    assert swap_steps[0].state.swapped_indices == (0, 1)
    assert swap_steps[0].state.values == (1, 3, 2)
    assert swap_steps[0].state.metadata["sorted_prefix_end"] == 0


def test_insertion_sort_steps_expose_current_element_shift_and_insert_position() -> None:
    result = insertion_sort((3, 1, 2))

    visit_steps = [step for step in result.steps if step.event_type is AlgorithmEventType.VISIT]
    move_steps = [step for step in result.steps if step.event_type is AlgorithmEventType.MOVE]

    assert visit_steps[0].state.metadata["current_index"] == 1
    assert visit_steps[0].state.metadata["insert_value"] == 1
    assert move_steps[0].message == "Shift 3 one position to the right."
    assert move_steps[0].state.metadata["from_index"] == 0
    assert move_steps[0].state.metadata["to_index"] == 1
    assert move_steps[1].message == "Place 1 at index 0."


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ((4, 1, 3, 2, 5), (1, 2, 3, 4, 5)),
        ((8, 3, 7, 1), (1, 3, 7, 8)),
    ],
)
def test_merge_sort_handles_odd_and_even_length_arrays(values: tuple[int, ...], expected: tuple[int, ...]) -> None:
    result = merge_sort(values)

    assert result.ok
    assert result.values == expected
    assert result.steps[-1].state.values == expected


def test_merge_sort_steps_expose_split_compare_append_and_completed_ranges() -> None:
    result = merge_sort((3, 1, 2))

    split_steps = [step for step in result.steps if step.message.startswith("Split range")]
    compare_steps = [step for step in result.steps if step.event_type is AlgorithmEventType.COMPARE]
    append_steps = [step for step in result.steps if step.message.startswith("Append")]
    merged_steps = [step for step in result.steps if step.message.startswith("Merged range")]

    assert split_steps[0].state.current_range == (0, 2)
    assert split_steps[0].state.metadata["split_index"] == 1
    assert split_steps[0].state.metadata["left_values"] == (3, 1)
    assert split_steps[0].state.metadata["right_values"] == (2,)
    assert compare_steps[0].state.comparison_indices == (0, 1)
    assert compare_steps[0].state.metadata["compared_values"] == (3, 1)
    assert append_steps[0].state.metadata["appended_value"] == 1
    assert append_steps[0].state.metadata["write_index"] == 0
    assert merged_steps[-1].state.values == (1, 2, 3)
    assert merged_steps[-1].state.metadata["completed_range"] == (0, 2)


def test_quick_sort_steps_expose_last_element_pivot_and_comparisons() -> None:
    result = quick_sort((3, 1, 2))

    pivot_steps = [step for step in result.steps if step.event_type is AlgorithmEventType.PIVOT]
    compare_steps = [step for step in result.steps if step.event_type is AlgorithmEventType.COMPARE]

    assert pivot_steps[0].state.current_range == (0, 2)
    assert pivot_steps[0].state.pivot_index == 2
    assert pivot_steps[0].state.metadata["pivot_value"] == 2
    assert compare_steps[0].state.comparison_indices == (0, 2)
    assert compare_steps[0].state.metadata["compared_values"] == (3, 2)


def test_quick_sort_places_pivot_and_exposes_partition_ranges() -> None:
    result = quick_sort((3, 1, 2))

    pivot_move = [step for step in result.steps if step.state.metadata.get("final_pivot_index") == 1][0]

    assert pivot_move.message == "Move pivot 2 to index 1."
    assert pivot_move.state.values == (1, 2, 3)
    assert pivot_move.state.metadata["left_partition_range"] == (0, 0)
    assert pivot_move.state.metadata["right_partition_range"] == (2, 2)
    assert result.values == (1, 2, 3)


def test_quick_sort_partition_correctness_after_first_pivot() -> None:
    result = quick_sort((4, 2, 5, 1, 3))

    first_pivot_move = [step for step in result.steps if step.state.metadata.get("final_pivot_index") == 2][0]
    values = first_pivot_move.state.values
    pivot_value = first_pivot_move.state.metadata["pivot_value"]
    pivot_index = first_pivot_move.state.metadata["final_pivot_index"]

    assert pivot_value == 3
    assert all(value <= pivot_value for value in values[:pivot_index])
    assert all(value > pivot_value for value in values[pivot_index + 1 :])


def test_heap_sort_builds_max_heap_before_extraction() -> None:
    result = heap_sort((3, 1, 4, 2))

    built_step = [step for step in result.steps if step.state.metadata.get("heap_built") is True][0]

    assert built_step.message == "Max-Heap construction complete."
    assert built_step.state.values[0] == max(built_step.state.values)
    assert built_step.state.metadata["active_heap_range"] == (0, 3)


def test_heap_sort_heapify_exposes_parent_child_comparisons_and_swaps() -> None:
    result = heap_sort((1, 3, 2))

    compare_steps = [step for step in result.steps if step.event_type is AlgorithmEventType.COMPARE]
    heapify_swaps = [
        step
        for step in result.steps
        if step.event_type is AlgorithmEventType.SWAP and step.state.metadata.get("root_to_end_swap") is not True
    ]

    assert compare_steps[0].state.comparison_indices == (0, 1)
    assert compare_steps[0].state.metadata["parent_index"] == 0
    assert compare_steps[0].state.metadata["child_index"] == 1
    assert heapify_swaps[0].message == "Swap parent 1 with child 3."
    assert heapify_swaps[0].state.values == (3, 1, 2)


def test_heap_sort_root_swaps_shrink_heap_and_grow_sorted_suffix() -> None:
    result = heap_sort((3, 1, 2))

    root_swap = [step for step in result.steps if step.state.metadata.get("root_to_end_swap") is True][0]
    suffix_step = [step for step in result.steps if step.message == "Index 2 joins the sorted suffix."][0]

    assert root_swap.message == "Swap root 3 with index 2."
    assert root_swap.state.values == (2, 1, 3)
    assert root_swap.state.metadata["active_heap_range"] == (0, 1)
    assert root_swap.state.metadata["sorted_suffix_start"] == 2
    assert suffix_step.state.metadata["sorted_suffix_start"] == 2
    assert result.values == (1, 2, 3)
