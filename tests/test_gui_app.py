import tkinter as tk

import pytest

from dsa_visual_lab.gui.app import VisualLabApp
from dsa_visual_lab.gui.controller import StructureKey


def create_app_or_skip() -> VisualLabApp:
    try:
        return VisualLabApp()
    except tk.TclError as error:
        pytest.skip(f"Tkinter is not available: {error}")


def test_gui_switching_structures_resets_to_supported_operation() -> None:
    app = create_app_or_skip()
    try:
        app.selected_structure.set(StructureKey.STACK.value)
        app._show_operations()
        app.selected_operation.set("pop")

        app.selected_structure.set(StructureKey.QUEUE.value)
        app._show_operations()

        assert app.selected_operation.get() == "enqueue"
    finally:
        app.destroy()


def test_gui_can_run_display_operation_and_populate_step_sequence() -> None:
    app = create_app_or_skip()
    try:
        app.selected_structure.set(StructureKey.DYNAMIC_ARRAY.value)
        app._show_operations()
        app.selected_operation.set("display")
        app._refresh_operation_fields()

        app._run_current_operation()

        assert app.steps_list.size() == 1
        assert app.current_steps[0].message.startswith("DynamicArray")
    finally:
        app.destroy()
