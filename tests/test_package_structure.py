import importlib


def test_package_layers_import() -> None:
    modules = [
        "data_structures_visual_lab",
        "data_structures_visual_lab.__main__",
        "data_structures_visual_lab.domain",
        "data_structures_visual_lab.domain.data_structures",
        "data_structures_visual_lab.domain.data_structures.dynamic_array",
        "data_structures_visual_lab.domain.data_structures.linked_list",
        "data_structures_visual_lab.domain.algorithms",
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
