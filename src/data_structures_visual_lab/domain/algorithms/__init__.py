"""Shared infrastructure for future algorithm modules."""

from data_structures_visual_lab.domain.algorithms.state import (
    AlgorithmEventType,
    AlgorithmState,
    AlgorithmStep,
    make_algorithm_step,
)
from data_structures_visual_lab.domain.algorithms.validation import (
    ArrayValidationResult,
    parse_integer_array_text,
    validate_ascending_sorted,
    validate_integer_array,
)
from data_structures_visual_lab.domain.algorithms.bfs import BFSResult, bfs
from data_structures_visual_lab.domain.algorithms.binary_search import BinarySearchResult, binary_search
from data_structures_visual_lab.domain.algorithms.bubble_sort import SortResult, bubble_sort
from data_structures_visual_lab.domain.algorithms.dfs import DFSResult, dfs
from data_structures_visual_lab.domain.algorithms.heap_sort import heap_sort
from data_structures_visual_lab.domain.algorithms.insertion_sort import insertion_sort
from data_structures_visual_lab.domain.algorithms.merge_sort import merge_sort
from data_structures_visual_lab.domain.algorithms.quick_sort import quick_sort
from data_structures_visual_lab.domain.algorithms.selection_sort import selection_sort

__all__ = [
    "AlgorithmEventType",
    "AlgorithmState",
    "AlgorithmStep",
    "ArrayValidationResult",
    "BFSResult",
    "BinarySearchResult",
    "DFSResult",
    "SortResult",
    "bfs",
    "binary_search",
    "bubble_sort",
    "dfs",
    "heap_sort",
    "insertion_sort",
    "make_algorithm_step",
    "merge_sort",
    "parse_integer_array_text",
    "quick_sort",
    "selection_sort",
    "validate_ascending_sorted",
    "validate_integer_array",
]
