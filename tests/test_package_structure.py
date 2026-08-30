import importlib


def test_package_layers_import() -> None:
    modules = [
        "dsa_visual_lab",
        "dsa_visual_lab.__main__",
        "dsa_visual_lab.domain",
        "dsa_visual_lab.domain.data_structures",
        "dsa_visual_lab.domain.data_structures.dynamic_array",
        "dsa_visual_lab.domain.data_structures.linked_list",
        "dsa_visual_lab.domain.algorithms",
        "dsa_visual_lab.events",
        "dsa_visual_lab.events.steps",
        "dsa_visual_lab.visualization",
        "dsa_visual_lab.visualization.state",
        "dsa_visual_lab.gui",
        "dsa_visual_lab.gui.app",
        "dsa_visual_lab.gui.controller",
    ]

    for module_name in modules:
        assert importlib.import_module(module_name)
