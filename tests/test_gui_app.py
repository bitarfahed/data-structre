import tkinter as tk

import pytest

from data_structures_visual_lab.gui.app import VisualLabApp
from data_structures_visual_lab.gui.controller import StructureKey


def create_app_or_skip() -> VisualLabApp:
    try:
        return VisualLabApp()
    except tk.TclError as error:
        pytest.skip(f"Tkinter is not available: {error}")


def test_gui_main_flows_for_all_round_1_structures() -> None:
    app = create_app_or_skip()
    flows = [
        (StructureKey.STACK, "push", "10", ""),
        (StructureKey.STACK, "push", "20", ""),
        (StructureKey.STACK, "pop", "", ""),
        (StructureKey.QUEUE, "enqueue", "1", ""),
        (StructureKey.QUEUE, "enqueue", "2", ""),
        (StructureKey.QUEUE, "dequeue", "", ""),
        (StructureKey.LINKED_LIST, "push", "5", ""),
        (StructureKey.LINKED_LIST, "push", "7", "1"),
        (StructureKey.LINKED_LIST, "change_value", "9", "1"),
        (StructureKey.LINKED_LIST, "pop", "", "0"),
        (StructureKey.DYNAMIC_ARRAY, "add", "1", ""),
        (StructureKey.DYNAMIC_ARRAY, "add", "2", ""),
        (StructureKey.DYNAMIC_ARRAY, "add", "3", ""),
        (StructureKey.DYNAMIC_ARRAY, "add", "4", ""),
        (StructureKey.DYNAMIC_ARRAY, "add", "5", ""),
        (StructureKey.DYNAMIC_ARRAY, "delete", "", "0"),
    ]

    try:
        app.update()
        app.selected_structure.set(StructureKey.STACK.value)
        app._show_operations()
        app.selected_operation.set("pop")
        app.selected_structure.set(StructureKey.QUEUE.value)
        app._show_operations()
        assert app.selected_operation.get() == "enqueue"

        for structure, operation, value, index in flows:
            app.selected_structure.set(structure.value)
            app._show_structure_selection()
            assert app.explanation_label.cget("text")

            app._show_operations()
            app.selected_operation.set(operation)
            app._refresh_operation_fields()
            app.value_input.set(value)
            app.index_input.set(index)
            app._run_current_operation()

            assert app.canvas.find_all()
            app.update()

        app.selected_structure.set(StructureKey.DYNAMIC_ARRAY.value)
        app._show_operations()
        app._restart_structure()
        assert app.value_input.get() == ""
        assert app.index_input.get() == ""
        assert app.status_text.get() == "Choose an operation and enter the required integer inputs."
        assert app.controller.snapshot(StructureKey.DYNAMIC_ARRAY).size == 0
        assert app.controller.snapshot(StructureKey.DYNAMIC_ARRAY).capacity == 1

        app.selected_structure.set(StructureKey.STACK.value)
        app._show_operations()
        app.selected_operation.set("push")
        app._refresh_operation_fields()
        app.value_input.set("not-int")
        app._run_current_operation()
        assert app.status_text.get() == "Value must be an integer."
    finally:
        app.destroy()
