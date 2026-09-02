import tkinter as tk

import pytest

from data_structures_visual_lab.gui.app import VisualLabApp
from data_structures_visual_lab.gui.controller import StructureKey


def create_app_or_skip() -> VisualLabApp:
    try:
        return VisualLabApp()
    except tk.TclError as error:
        pytest.skip(f"Tkinter is not available: {error}")


def test_binary_search_gui_loads_array_before_searching() -> None:
    app = create_app_or_skip()
    try:
        app.update()
        app.selected_structure.set(StructureKey.BINARY_SEARCH.value)
        app._show_structure_selection()
        app._show_operations()

        app.array_input.set("1, 3, 5, 7, 9")
        app.index_input.set("not the algorithm array")
        app._load_binary_search_array()

        loaded_values = [element.value for element in app.controller.snapshot(StructureKey.BINARY_SEARCH).values]
        assert loaded_values == [1, 3, 5, 7, 9]
        assert app.status_text.get() == "Loaded array with 5 values."
        assert app.array_input.get() == "1, 3, 5, 7, 9"
        assert str(app.search_button.cget("state")) == tk.NORMAL

        app.value_input.set("7")
        app._search_binary_search()

        app.after(2600, app.quit)
        app.mainloop()

        assert app.status_text.get() == "Found target 7 at index 3."
        assert app.canvas.find_all()
    finally:
        app.destroy()


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
        (StructureKey.BUBBLE_SORT, "sort", "", "3, 1, 2"),
        (StructureKey.SELECTION_SORT, "sort", "", "3, 1, 2"),
        (StructureKey.INSERTION_SORT, "sort", "", "3, 1, 2"),
        (StructureKey.MERGE_SORT, "sort", "", "3, 1, 2"),
        (StructureKey.QUICK_SORT, "sort", "", "3, 1, 2"),
        (StructureKey.HEAP_SORT, "sort", "", "3, 1, 2"),
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
            if structure is StructureKey.BINARY_SEARCH:
                continue
            app.selected_operation.set(operation)
            app._refresh_operation_fields()
            app.value_input.set(value)
            if app._current_operation().index_input_kind == "array":
                app.array_input.set(index)
            else:
                app.index_input.set(index)
            app._run_current_operation()

            assert app.canvas.find_all()
            app.update()

        app.selected_structure.set(StructureKey.DYNAMIC_ARRAY.value)
        app._show_operations()
        app._restart_structure()
        assert app.value_input.get() == ""
        assert app.index_input.get() == ""
        assert app.array_input.get() == ""
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

        app.selected_structure.set(StructureKey.GRAPH.value)
        app._show_structure_selection()
        assert "graph" in app.explanation_label.cget("text").lower()
        app._show_operations()
        assert app.graph_type_input.get() == "undirected"
        app.selected_operation.set("add_vertex")
        app._refresh_graph_operation_fields()
        app.graph_vertex_input.set("1")
        app._run_graph_operation()
        app.graph_vertex_input.set("2")
        app._run_graph_operation()
        app.selected_operation.set("add_edge")
        app._refresh_graph_operation_fields()
        app.graph_source_input.set("1")
        app.graph_destination_input.set("2")
        app.graph_weight_input.set("4")
        app._run_graph_operation()
        graph_snapshot = app.controller.snapshot(StructureKey.GRAPH)
        assert graph_snapshot.graph_type == "undirected"
        assert [(edge.source, edge.destination, edge.weight, edge.directed) for edge in graph_snapshot.graph_edges] == [
            (1, 2, 4, False)
        ]
        assert app.canvas.find_all()
        app.selected_operation.set("bfs")
        app._refresh_graph_operation_fields()
        app.graph_vertex_input.set("1")
        app._run_graph_operation()
        app.after(3600, app.quit)
        app.mainloop()
        assert app.status_text.get() == "BFS complete. Traversal order: [1, 2]."
        bfs_snapshot = app.controller.snapshot(StructureKey.GRAPH)
        assert [node.value for node in bfs_snapshot.graph_nodes] == [1, 2]
        app.selected_operation.set("dfs")
        app._refresh_graph_operation_fields()
        app.graph_vertex_input.set("1")
        app._run_graph_operation()
        app.after(3600, app.quit)
        app.mainloop()
        assert app.status_text.get() == "DFS complete. Traversal order: [1, 2]."
        app.selected_operation.set("dijkstra")
        app._refresh_graph_operation_fields()
        app.graph_vertex_input.set("1")
        app.graph_target_input.set("2")
        app._run_graph_operation()
        app.after(5000, app.quit)
        app.mainloop()
        assert app.status_text.get() == "Dijkstra complete. Shortest path to 2: [1, 2] with distance 4."
        dijkstra_snapshot = app.controller.snapshot(StructureKey.GRAPH)
        assert [node.value for node in dijkstra_snapshot.graph_nodes] == [1, 2]
        app.selected_operation.set("connected_components")
        app._refresh_graph_operation_fields()
        app._run_graph_operation()
        app.after(5000, app.quit)
        app.mainloop()
        assert app.status_text.get() == "Connected Components complete. Component count: 1."
        app.selected_operation.set("cycle_detection")
        app._refresh_graph_operation_fields()
        app._run_graph_operation()
        app.after(5000, app.quit)
        app.mainloop()
        assert app.status_text.get() == "Cycle Detection complete. No cycle found."
        app.selected_operation.set("prim_mst")
        app._refresh_graph_operation_fields()
        assert app.graph_vertex_label.cget("text") == "Start"
        app.graph_vertex_input.set("1")
        app._run_graph_operation()
        app.after(5000, app.quit)
        app.mainloop()
        assert app.status_text.get() == "Prim's MST complete. Total weight: 4."
        assert app.canvas.find_all()
        app.selected_operation.set("kruskal_mst")
        app._refresh_graph_operation_fields()
        app._run_graph_operation()
        app.after(5000, app.quit)
        app.mainloop()
        assert app.status_text.get() == "Kruskal's MST complete. Total weight: 4."
        assert app.canvas.find_all()
        app.graph_type_input.set("directed")
        app._set_graph_type()
        for vertex in ("1", "2", "3"):
            app.selected_operation.set("add_vertex")
            app._refresh_graph_operation_fields()
            app.graph_vertex_input.set(vertex)
            app._run_graph_operation()
        app.selected_operation.set("add_edge")
        app._refresh_graph_operation_fields()
        app.graph_source_input.set("1")
        app.graph_destination_input.set("2")
        app.graph_weight_input.set("1")
        app._run_graph_operation()
        app.graph_source_input.set("2")
        app.graph_destination_input.set("3")
        app._run_graph_operation()
        app.selected_operation.set("topological_sort")
        app._refresh_graph_operation_fields()
        app._run_graph_operation()
        app.after(5000, app.quit)
        app.mainloop()
        assert app.status_text.get() == "Topological Sort complete. Order: [1, 2, 3]."
        app.graph_type_input.set("undirected")
        app._set_graph_type()
        app.graph_weight_input.set("-1")
        app.selected_operation.set("add_edge")
        app._refresh_graph_operation_fields()
        app.graph_source_input.set("1")
        app.graph_destination_input.set("2")
        app._run_graph_operation()
        assert app.status_text.get() == "Weight must be greater than or equal to 0."
        app.graph_type_input.set("directed")
        app._set_graph_type()
        assert app.controller.graph_directed()
        assert app.controller.snapshot(StructureKey.GRAPH).graph_edges == ()
        app.graph_vertex_input.set("3")
        app.selected_operation.set("add_vertex")
        app._refresh_graph_operation_fields()
        app._run_graph_operation()
        app._restart_structure()
        assert app.controller.graph_directed()
        assert app.controller.snapshot(StructureKey.GRAPH).graph_nodes == ()
        assert app.graph_vertex_input.get() == ""
        assert app.graph_source_input.get() == ""
        assert app.graph_destination_input.get() == ""
        assert app.graph_weight_input.get() == ""
        assert app.graph_target_input.get() == ""

        app.selected_structure.set(StructureKey.BINARY_SEARCH.value)
        app._show_structure_selection()
        assert "binary search" in app.explanation_label.cget("text").lower()
        app._show_operations()
        assert app.array_label.cget("text") == "Array"
        assert int(app.array_entry.cget("width")) == 34
        assert app.status_text.get() == "Load an ascending sorted integer array."
        assert str(app.search_button.cget("state")) == tk.DISABLED
        app.array_input.set("1, 3, 5, 7, 9")
        app._load_binary_search_array()
        assert [element.value for element in app.controller.snapshot(StructureKey.BINARY_SEARCH).values] == [1, 3, 5, 7, 9]
        assert str(app.search_button.cget("state")) == tk.NORMAL
        app.value_input.set("7")
        app._search_binary_search()
        assert app.canvas.find_all()
        app.after(2600, app.quit)
        app.mainloop()
        assert "Found target 7 at index 3." in app.status_text.get()

        app.array_input.set("1, 4, 3")
        app._load_binary_search_array()
        assert app.status_text.get() == "Binary Search requires ascending sorted input."
        assert [element.value for element in app.controller.snapshot(StructureKey.BINARY_SEARCH).values] == [1, 3, 5, 7, 9]

        app.value_input.set("5")
        app.array_input.set("")
        app._load_binary_search_array()
        app._search_binary_search()
        assert app.status_text.get() == "Target 5 was not found."

        app.value_input.set("5")
        app.array_input.set("5")
        app._load_binary_search_array()
        app._search_binary_search()
        app.after(1200, app.quit)
        app.mainloop()
        assert app.status_text.get() == "Found target 5 at index 0."

        app._restart_structure()
        assert not app.controller.binary_search_array_loaded()
        assert app.controller.snapshot(StructureKey.BINARY_SEARCH).values == ()
        assert app.array_input.get() == ""
        assert app.value_input.get() == ""
        assert str(app.search_button.cget("state")) == tk.DISABLED

        for structure_key, final_message in (
            (StructureKey.BUBBLE_SORT, "Bubble Sort complete."),
            (StructureKey.SELECTION_SORT, "Selection Sort complete."),
            (StructureKey.INSERTION_SORT, "Insertion Sort complete."),
            (StructureKey.MERGE_SORT, "Merge Sort complete."),
            (StructureKey.QUICK_SORT, "Quick Sort complete."),
            (StructureKey.HEAP_SORT, "Heap Sort complete."),
        ):
            app.selected_structure.set(structure_key.value)
            app._show_structure_selection()
            assert "sort" in app.explanation_label.cget("text").lower()
            app._show_operations()
            assert app.array_label.cget("text") == "Array"
            assert int(app.array_entry.cget("width")) == 34
            assert app.status_text.get() == "Enter comma-separated integers, then run the algorithm."
            app.selected_operation.set("sort")
            app._refresh_operation_fields()
            app.array_input.set("2, 1")
            app._run_current_operation()
            assert app.canvas.find_all()
            wait_ms = 9000 if structure_key in {
                StructureKey.MERGE_SORT,
                StructureKey.QUICK_SORT,
                StructureKey.HEAP_SORT,
            } else 4200
            app.after(wait_ms, app.quit)
            app.mainloop()
            assert app.status_text.get() == final_message

            app.array_input.set("4, bad, 2")
            app._run_current_operation()
            assert app.status_text.get() == "Array values must be integers."

        app.selected_structure.set(StructureKey.STACK.value)
        app._show_operations()
        app.selected_operation.set("push")
        app._refresh_operation_fields()
        app.value_input.set("not-int")
        app._run_current_operation()
        assert app.status_text.get() == "Value must be an integer."
    finally:
        app.destroy()
