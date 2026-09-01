import importlib


def test_package_layers_import() -> None:
    modules = [
        "data_structures_visual_lab",
        "data_structures_visual_lab.__main__",
        "data_structures_visual_lab.domain",
        "data_structures_visual_lab.domain.data_structures",
        "data_structures_visual_lab.domain.data_structures.avl_tree",
        "data_structures_visual_lab.domain.data_structures.dynamic_array",
        "data_structures_visual_lab.domain.data_structures.graph",
        "data_structures_visual_lab.domain.data_structures.hash_table",
        "data_structures_visual_lab.domain.data_structures.linked_list",
        "data_structures_visual_lab.domain.data_structures.min_heap",
        "data_structures_visual_lab.domain.data_structures.two_three_tree",
        "data_structures_visual_lab.domain.algorithms",
        "data_structures_visual_lab.domain.algorithms.bfs",
        "data_structures_visual_lab.domain.algorithms.binary_search",
        "data_structures_visual_lab.domain.algorithms.bubble_sort",
        "data_structures_visual_lab.domain.algorithms.connected_components",
        "data_structures_visual_lab.domain.algorithms.cycle_detection",
        "data_structures_visual_lab.domain.algorithms.dfs",
        "data_structures_visual_lab.domain.algorithms.dijkstra",
        "data_structures_visual_lab.domain.algorithms.heap_sort",
        "data_structures_visual_lab.domain.algorithms.insertion_sort",
        "data_structures_visual_lab.domain.algorithms.merge_sort",
        "data_structures_visual_lab.domain.algorithms.prim_mst",
        "data_structures_visual_lab.domain.algorithms.quick_sort",
        "data_structures_visual_lab.domain.algorithms.selection_sort",
        "data_structures_visual_lab.domain.algorithms.state",
        "data_structures_visual_lab.domain.algorithms.topological_sort",
        "data_structures_visual_lab.domain.algorithms.validation",
        "data_structures_visual_lab.events",
        "data_structures_visual_lab.events.steps",
        "data_structures_visual_lab.visualization",
        "data_structures_visual_lab.visualization.state",
        "data_structures_visual_lab.gui",
        "data_structures_visual_lab.gui.app",
        "data_structures_visual_lab.gui.controller",
    ]

    for module_name in modules:
        assert importlib.import_module(module_name)
