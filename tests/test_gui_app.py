import tkinter as tk

import pytest

from data_structures_visual_lab.gui.app import VisualLabApp
from data_structures_visual_lab.gui.controller import StructureKey


def create_app_or_skip() -> VisualLabApp:
    try:
        return VisualLabApp()
    except tk.TclError as error:
        pytest.skip(f"Tkinter is not available: {error}")


def test_gui_main_flows_for_supported_structures() -> None:
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
        (StructureKey.AVL_TREE, "insert", "30", ""),
        (StructureKey.AVL_TREE, "insert", "20", ""),
        (StructureKey.AVL_TREE, "insert", "10", ""),
        (StructureKey.AVL_TREE, "balance", "", ""),
        (StructureKey.AVL_TREE, "search", "20", ""),
        (StructureKey.AVL_TREE, "min", "", ""),
        (StructureKey.AVL_TREE, "max", "", ""),
        (StructureKey.AVL_TREE, "delete", "20", ""),
        (StructureKey.MIN_HEAP, "add_raw", "10", ""),
        (StructureKey.MIN_HEAP, "add_raw", "20", ""),
        (StructureKey.MIN_HEAP, "add_raw", "5", ""),
        (StructureKey.MIN_HEAP, "sift_up", "", ""),
        (StructureKey.MIN_HEAP, "add_raw", "5", ""),
        (StructureKey.MIN_HEAP, "sift_up", "", ""),
        (StructureKey.MIN_HEAP, "peek_min", "", ""),
        (StructureKey.MIN_HEAP, "extract_raw", "", ""),
        (StructureKey.MIN_HEAP, "heapify_down", "", ""),
        (StructureKey.HASH_TABLE, "insert", "10", "1"),
        (StructureKey.HASH_TABLE, "insert", "50", "9"),
        (StructureKey.HASH_TABLE, "insert", "99", "1"),
        (StructureKey.HASH_TABLE, "search", "", "9"),
        (StructureKey.HASH_TABLE, "delete", "", "9"),
        (StructureKey.TWO_THREE_TREE, "insert_raw", "10", ""),
        (StructureKey.TWO_THREE_TREE, "insert_raw", "5", ""),
        (StructureKey.TWO_THREE_TREE, "insert_raw", "15", ""),
        (StructureKey.TWO_THREE_TREE, "repair", "", ""),
        (StructureKey.TWO_THREE_TREE, "search", "10", ""),
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

        app.selected_structure.set(StructureKey.AVL_TREE.value)
        app._show_operations()
        for value in ("30", "20", "10"):
            app.selected_operation.set("insert")
            app._refresh_operation_fields()
            app.value_input.set(value)
            app._run_current_operation()
        assert str(app.run_button.cget("state")) == tk.DISABLED
        assert app.controller.snapshot(StructureKey.AVL_TREE).rebalance_pending
        app.selected_operation.set("balance")
        app._refresh_operation_fields()
        assert str(app.run_button.cget("state")) == tk.NORMAL
        app._run_current_operation()
        assert not app.controller.snapshot(StructureKey.AVL_TREE).rebalance_pending
        app._restart_structure()
        assert app.controller.snapshot(StructureKey.AVL_TREE).size == 0

        app.selected_structure.set(StructureKey.MIN_HEAP.value)
        app._show_structure_selection()
        assert "min-heap" in app.explanation_label.cget("text").lower()
        app._show_operations()
        for value in ("10", "20", "5"):
            app.selected_operation.set("add_raw")
            app._refresh_operation_fields()
            app.value_input.set(value)
            app._run_current_operation()
        assert str(app.run_button.cget("state")) == tk.DISABLED
        assert app.controller.snapshot(StructureKey.MIN_HEAP).repair_pending
        app.selected_operation.set("sift_up")
        app._refresh_operation_fields()
        assert str(app.run_button.cget("state")) == tk.NORMAL
        app._run_current_operation()
        assert not app.controller.snapshot(StructureKey.MIN_HEAP).repair_pending
        app.selected_operation.set("extract_raw")
        app._refresh_operation_fields()
        app._run_current_operation()
        assert app.controller.snapshot(StructureKey.MIN_HEAP).repair_pending
        app.selected_operation.set("heapify_down")
        app._refresh_operation_fields()
        app._run_current_operation()
        assert not app.controller.snapshot(StructureKey.MIN_HEAP).repair_pending
        app._restart_structure()
        assert app.controller.snapshot(StructureKey.MIN_HEAP).size == 0

        app.selected_structure.set(StructureKey.HASH_TABLE.value)
        app._show_structure_selection()
        assert "hash table" in app.explanation_label.cget("text").lower()
        app._show_operations()
        app._restart_structure()
        app.selected_operation.set("insert")
        app._refresh_operation_fields()
        assert app.index_label.cget("text") == "Key"
        app.index_input.set("1")
        app.value_input.set("10")
        app._run_current_operation()
        app.index_input.set("9")
        app.value_input.set("50")
        app._run_current_operation()
        assert app.controller.snapshot(StructureKey.HASH_TABLE).size == 2
        app.index_input.set("1")
        app.value_input.set("99")
        app._run_current_operation()
        snapshot = app.controller.snapshot(StructureKey.HASH_TABLE)
        assert snapshot.size == 3
        assert [(entry.key, entry.value) for entry in snapshot.buckets[1].entries] == [(1, 10), (9, 50), (1, 99)]
        assert app.canvas.find_all()
        app.selected_operation.set("search")
        app._refresh_operation_fields()
        app.index_input.set("1")
        app._run_current_operation()
        assert "Found key 1 with values [10, 99]" in app.status_text.get()
        app.selected_operation.set("delete")
        app._refresh_operation_fields()
        app.index_input.set("1")
        app._run_current_operation()
        assert app.controller.snapshot(StructureKey.HASH_TABLE).size == 1
        assert [(entry.key, entry.value) for entry in app.controller.snapshot(StructureKey.HASH_TABLE).buckets[1].entries] == [
            (9, 50)
        ]
        app.index_input.set("abc")
        app._run_current_operation()
        assert app.status_text.get() == "Key must be an integer."
        app._restart_structure()
        assert app.controller.snapshot(StructureKey.HASH_TABLE).size == 0

        app.selected_structure.set(StructureKey.TWO_THREE_TREE.value)
        app._show_structure_selection()
        assert "2-3 tree" in app.explanation_label.cget("text").lower()
        app._show_operations()
        app._restart_structure()
        for value in ("10", "5", "15"):
            app.selected_operation.set("insert_raw")
            app._refresh_operation_fields()
            app.value_input.set(value)
            app._run_current_operation()
        assert str(app.run_button.cget("state")) == tk.DISABLED
        assert app.controller.snapshot(StructureKey.TWO_THREE_TREE).repair_pending
        app.selected_operation.set("repair")
        app._refresh_operation_fields()
        assert str(app.run_button.cget("state")) == tk.NORMAL
        app._run_current_operation()
        assert not app.controller.snapshot(StructureKey.TWO_THREE_TREE).repair_pending
        for value in ("12", "11", "20", "25"):
            app.selected_operation.set("insert_raw")
            app._refresh_operation_fields()
            app.value_input.set(value)
            app._run_current_operation()
            if app.controller.snapshot(StructureKey.TWO_THREE_TREE).repair_pending:
                app.selected_operation.set("repair")
                app._refresh_operation_fields()
                app._run_current_operation()
        snapshot = app.controller.snapshot(StructureKey.TWO_THREE_TREE)
        assert snapshot.tree_valid
        assert [node.keys for node in snapshot.multi_key_tree_nodes if node.depth == 0] == [(12,)]
        app.selected_operation.set("search")
        app._refresh_operation_fields()
        app.value_input.set("11")
        app._run_current_operation()
        assert "search found 11" in app.status_text.get()
        app._restart_structure()
        assert app.controller.snapshot(StructureKey.TWO_THREE_TREE).size == 0

        app.selected_structure.set(StructureKey.STACK.value)
        app._show_operations()
        app.selected_operation.set("push")
        app._refresh_operation_fields()
        app.value_input.set("not-int")
        app._run_current_operation()
        assert app.status_text.get() == "Value must be an integer."
    finally:
        app.destroy()
