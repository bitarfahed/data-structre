"""Tkinter desktop shell for the visual lab."""

from __future__ import annotations

import math
import tkinter as tk
from tkinter import ttk

from data_structures_visual_lab.domain.algorithms import AlgorithmStep
from data_structures_visual_lab.events import EventType
from data_structures_visual_lab.gui.controller import OperationSpec, StructureKey, VisualLabController
from data_structures_visual_lab.visualization.state import (
    VisualizationState,
    build_algorithm_visualization_state,
    build_visualization_state,
)


class VisualLabApp(tk.Tk):
    """Small desktop GUI for supported structures."""

    def __init__(self) -> None:
        super().__init__()
        self.title("data_structures_visual_lab")
        self.geometry("980x620")
        self.minsize(820, 520)

        self.controller = VisualLabController()
        self.selected_structure = tk.StringVar(value=StructureKey.STACK.value)
        self.selected_operation = tk.StringVar()
        self.value_input = tk.StringVar()
        self.index_input = tk.StringVar()
        self.array_input = tk.StringVar()
        self.graph_type_input = tk.StringVar(value="undirected")
        self.graph_vertex_input = tk.StringVar()
        self.graph_source_input = tk.StringVar()
        self.graph_destination_input = tk.StringVar()
        self.graph_weight_input = tk.StringVar()
        self.graph_target_input = tk.StringVar()
        self.status_text = tk.StringVar(value="Choose a structure to begin.")
        self._algorithm_after_id: str | None = None

        self._build_layout()
        self._show_structure_selection()

    def _build_layout(self) -> None:
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.sidebar = ttk.Frame(self, padding=12)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.main = ttk.Frame(self, padding=12)
        self.main.grid(row=0, column=1, sticky="nsew")
        self.main.columnconfigure(0, weight=1)
        self.main.rowconfigure(2, weight=1)

        row = 0
        current_category = ""
        for structure_key in self.controller.structure_keys():
            category = self.controller.category_for(structure_key)
            if category != current_category:
                current_category = category
                ttk.Label(self.sidebar, text=category).grid(row=row, column=0, sticky="w", pady=(0 if row == 0 else 10, 2))
                row += 1
            ttk.Radiobutton(
                self.sidebar,
                text=structure_key.value,
                value=structure_key.value,
                variable=self.selected_structure,
                command=self._show_structure_selection,
            ).grid(row=row, column=0, sticky="w", pady=2)
            row += 1

        self.explanation_label = ttk.Label(self.main, wraplength=700)
        self.explanation_label.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        self.controls = ttk.Frame(self.main)
        self.controls.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        for column in range(8):
            self.controls.columnconfigure(column, weight=0)
        self.controls.columnconfigure(7, weight=1)

        self.canvas = tk.Canvas(self.main, background="white", height=330)
        self.canvas.grid(row=2, column=0, sticky="nsew")

        self.status_label = ttk.Label(self.main, textvariable=self.status_text, wraplength=700)
        self.status_label.grid(row=3, column=0, sticky="ew", pady=(8, 0))

    def _show_structure_selection(self) -> None:
        self._cancel_algorithm_playback()
        structure_key = self._current_structure_key()
        self.selected_operation.set("")
        self.explanation_label.config(text=self.controller.explanation_for(structure_key))
        self._render_continue_controls()
        self._draw_state(self.controller.snapshot(structure_key))

    def _render_continue_controls(self) -> None:
        self._clear_controls()
        ttk.Button(self.controls, text="Continue", command=self._show_operations).grid(
            row=0,
            column=0,
            sticky="w",
        )
        self.status_text.set("Read the explanation, then continue to operations.")

    def _show_operations(self) -> None:
        self._cancel_algorithm_playback()
        self._clear_controls()
        structure_key = self._current_structure_key()
        if structure_key is StructureKey.BINARY_SEARCH:
            self._show_binary_search_controls()
            return
        if structure_key is StructureKey.GRAPH:
            self._show_graph_controls()
            return

        operations = self.controller.operations_for(structure_key)
        operation_keys = [operation.key for operation in operations]
        if self.selected_operation.get() not in operation_keys:
            self.selected_operation.set(operations[0].key)

        ttk.Label(self.controls, text="Operation").grid(row=0, column=0, padx=(0, 6))
        operation_menu = ttk.Combobox(
            self.controls,
            state="readonly",
            width=24,
            textvariable=self.selected_operation,
            values=operation_keys,
        )
        operation_menu.grid(row=0, column=1, padx=(0, 10))
        operation_menu.bind("<<ComboboxSelected>>", lambda _event: self._refresh_operation_fields())

        self.value_label = ttk.Label(self.controls, text="Value")
        self.value_entry = ttk.Entry(self.controls, width=10, textvariable=self.value_input)
        self.index_label = ttk.Label(self.controls, text="Index")
        self.index_entry = ttk.Entry(self.controls, width=10, textvariable=self.index_input)
        self.array_label = ttk.Label(self.controls, text="Array")
        self.array_entry = ttk.Entry(self.controls, width=34, textvariable=self.array_input)
        self.run_button = ttk.Button(self.controls, text="Run", command=self._run_current_operation)
        self.restart_button = ttk.Button(self.controls, text="Restart", command=self._restart_structure)

        self.run_button.grid(row=0, column=6, padx=(0, 6))
        self.restart_button.grid(row=0, column=7, sticky="w")
        self._refresh_operation_fields()

    def _show_binary_search_controls(self) -> None:
        self.selected_operation.set("load_array")
        ttk.Label(self.controls, text="Array").grid(row=0, column=0, padx=(0, 4))
        self.array_entry = ttk.Entry(self.controls, width=34, textvariable=self.array_input)
        self.array_entry.grid(row=0, column=1, padx=(0, 8))
        self.load_array_button = ttk.Button(self.controls, text="Load Array", command=self._load_binary_search_array)
        self.load_array_button.grid(row=0, column=2, padx=(0, 14))

        self.value_label = ttk.Label(self.controls, text="Target")
        self.value_label.grid(row=0, column=3, padx=(0, 4))
        self.value_entry = ttk.Entry(self.controls, width=10, textvariable=self.value_input)
        self.value_entry.grid(row=0, column=4, padx=(0, 8))
        self.search_button = ttk.Button(self.controls, text="Search", command=self._search_binary_search)
        self.search_button.grid(row=0, column=5, padx=(0, 6))
        self.restart_button = ttk.Button(self.controls, text="Restart", command=self._restart_structure)
        self.restart_button.grid(row=0, column=6, sticky="w")

        # These attributes keep existing non-visual tests from depending on widget creation order.
        self.index_label = ttk.Label(self.controls, text="Index")
        self.index_entry = ttk.Entry(self.controls, width=10, textvariable=self.index_input)
        self.array_label = ttk.Label(self.controls, text="Array")
        self.run_button = self.search_button

        self._update_binary_search_search_state()
        if self.controller.binary_search_array_loaded():
            self.status_text.set("Enter a target, then search.")
        else:
            self.status_text.set("Load an ascending sorted integer array.")

    def _load_binary_search_array(self) -> None:
        self._cancel_algorithm_playback()
        result = self.controller.run_operation(
            StructureKey.BINARY_SEARCH,
            "load_array",
            index_text=self.array_input.get(),
        )
        self.status_text.set(result.message)
        self._draw_state(self.controller.snapshot(StructureKey.BINARY_SEARCH))
        self._update_binary_search_search_state()

    def _search_binary_search(self) -> None:
        self._cancel_algorithm_playback()
        result = self.controller.run_operation(
            StructureKey.BINARY_SEARCH,
            "search",
            value_text=self.value_input.get(),
        )
        if not result.steps:
            self.status_text.set(result.message)
            self._draw_state(self.controller.snapshot(StructureKey.BINARY_SEARCH))
            return

        self._show_algorithm_steps([step for step in result.steps if isinstance(step, AlgorithmStep)], result.message)

    def _update_binary_search_search_state(self) -> None:
        if hasattr(self, "search_button"):
            state = tk.NORMAL if self.controller.binary_search_array_loaded() else tk.DISABLED
            self.search_button.configure(state=state)

    def _show_graph_controls(self) -> None:
        if self.graph_type_input.get() not in {"directed", "undirected"}:
            self.graph_type_input.set("directed" if self.controller.graph_directed() else "undirected")
        operations = self.controller.operations_for(StructureKey.GRAPH)
        operation_keys = [operation.key for operation in operations]
        if self.selected_operation.get() not in operation_keys:
            self.selected_operation.set(operations[0].key)

        ttk.Label(self.controls, text="Type").grid(row=0, column=0, padx=(0, 4))
        ttk.Radiobutton(
            self.controls,
            text="Undirected",
            value="undirected",
            variable=self.graph_type_input,
            command=self._set_graph_type,
        ).grid(row=0, column=1, padx=(0, 4))
        ttk.Radiobutton(
            self.controls,
            text="Directed",
            value="directed",
            variable=self.graph_type_input,
            command=self._set_graph_type,
        ).grid(row=0, column=2, padx=(0, 10))

        ttk.Label(self.controls, text="Operation").grid(row=0, column=3, padx=(0, 4))
        self.graph_operation_menu = ttk.Combobox(
            self.controls,
            state="readonly",
            width=18,
            textvariable=self.selected_operation,
            values=operation_keys,
        )
        self.graph_operation_menu.grid(row=0, column=4, padx=(0, 10))
        self.graph_operation_menu.bind("<<ComboboxSelected>>", lambda _event: self._refresh_graph_operation_fields())

        self.graph_vertex_label = ttk.Label(self.controls, text="Vertex")
        self.graph_vertex_entry = ttk.Entry(self.controls, width=8, textvariable=self.graph_vertex_input)
        self.graph_source_label = ttk.Label(self.controls, text="Source")
        self.graph_source_entry = ttk.Entry(self.controls, width=8, textvariable=self.graph_source_input)
        self.graph_destination_label = ttk.Label(self.controls, text="Destination")
        self.graph_destination_entry = ttk.Entry(self.controls, width=8, textvariable=self.graph_destination_input)
        self.graph_weight_label = ttk.Label(self.controls, text="Weight")
        self.graph_weight_entry = ttk.Entry(self.controls, width=8, textvariable=self.graph_weight_input)
        self.graph_target_label = ttk.Label(self.controls, text="Target")
        self.graph_target_entry = ttk.Entry(self.controls, width=8, textvariable=self.graph_target_input)
        self.run_button = ttk.Button(self.controls, text="Run", command=self._run_graph_operation)
        self.restart_button = ttk.Button(self.controls, text="Restart", command=self._restart_structure)
        self.run_button.grid(row=1, column=6, padx=(0, 6), pady=(6, 0))
        self.restart_button.grid(row=1, column=7, sticky="w", pady=(6, 0))
        self._refresh_graph_operation_fields()

    def _set_graph_type(self) -> None:
        directed = self.graph_type_input.get() == "directed"
        self.controller.set_graph_directed(directed)
        self._clear_graph_inputs()
        self.status_text.set(f"Graph reset as {'directed' if directed else 'undirected'}.")
        self._draw_state(self.controller.snapshot(StructureKey.GRAPH))

    def _refresh_graph_operation_fields(self) -> None:
        for widget in (
            self.graph_vertex_label,
            self.graph_vertex_entry,
            self.graph_source_label,
            self.graph_source_entry,
            self.graph_destination_label,
            self.graph_destination_entry,
            self.graph_weight_label,
            self.graph_weight_entry,
            self.graph_target_label,
            self.graph_target_entry,
        ):
            widget.grid_remove()

        operation_key = self.selected_operation.get()
        if operation_key in {"add_vertex", "remove_vertex", "bfs", "dfs", "dijkstra"}:
            self.graph_vertex_label.configure(text="Start" if operation_key in {"bfs", "dfs", "dijkstra"} else "Vertex")
            self.graph_vertex_label.grid(row=1, column=0, padx=(0, 4), pady=(6, 0))
            self.graph_vertex_entry.grid(row=1, column=1, padx=(0, 10), pady=(6, 0))
            if operation_key == "dijkstra":
                self.graph_target_label.configure(text="Target")
                self.graph_target_label.grid(row=1, column=2, padx=(0, 4), pady=(6, 0))
                self.graph_target_entry.grid(row=1, column=3, padx=(0, 10), pady=(6, 0))
        elif operation_key not in {"connected_components", "cycle_detection"}:
            self.graph_source_label.grid(row=1, column=0, padx=(0, 4), pady=(6, 0))
            self.graph_source_entry.grid(row=1, column=1, padx=(0, 10), pady=(6, 0))
            self.graph_destination_label.grid(row=1, column=2, padx=(0, 4), pady=(6, 0))
            self.graph_destination_entry.grid(row=1, column=3, padx=(0, 10), pady=(6, 0))
            if operation_key == "add_edge":
                self.graph_weight_label.grid(row=1, column=4, padx=(0, 4), pady=(6, 0))
                self.graph_weight_entry.grid(row=1, column=5, padx=(0, 10), pady=(6, 0))

        self.status_text.set("Choose a graph operation and enter integer inputs.")

    def _run_graph_operation(self) -> None:
        self._cancel_algorithm_playback()
        result = self.controller.run_graph_operation(
            self.selected_operation.get(),
            vertex_text=self.graph_vertex_input.get(),
            source_text=self.graph_source_input.get(),
            destination_text=self.graph_destination_input.get(),
            weight_text=self.graph_weight_input.get(),
            target_text=self.graph_target_input.get(),
        )
        self.status_text.set(result.message)
        if result.steps and all(isinstance(step, AlgorithmStep) for step in result.steps):
            self._show_graph_steps([step for step in result.steps if isinstance(step, AlgorithmStep)], result.message)
            return

        step = result.steps[-1] if result.steps else None
        self._draw_state(self.controller.snapshot(StructureKey.GRAPH, step))

    def _show_graph_steps(self, steps: list[AlgorithmStep], final_message: str, index: int = 0) -> None:
        if not steps:
            self.status_text.set(final_message)
            self._draw_state(self.controller.snapshot(StructureKey.GRAPH))
            return

        step = steps[index]
        self.status_text.set(step.message if index < len(steps) - 1 else final_message)
        self._draw_state(self.controller.snapshot(StructureKey.GRAPH, step))
        if index < len(steps) - 1:
            self._algorithm_after_id = self.after(500, lambda: self._show_graph_steps(steps, final_message, index + 1))
        else:
            self._algorithm_after_id = None

    def _clear_graph_inputs(self) -> None:
        self.graph_vertex_input.set("")
        self.graph_source_input.set("")
        self.graph_destination_input.set("")
        self.graph_weight_input.set("")
        self.graph_target_input.set("")

    def _refresh_operation_fields(self, update_status: bool = True) -> None:
        operation = self._current_operation()
        self.value_label.grid_remove()
        self.value_entry.grid_remove()
        self.index_label.grid_remove()
        self.index_entry.grid_remove()
        self.array_label.grid_remove()
        self.array_entry.grid_remove()
        self.value_label.configure(text=operation.value_label)
        self.index_label.configure(text=operation.index_label)
        self.value_entry.configure(width=10)
        self.index_entry.configure(width=10)
        self.array_label.configure(text=operation.index_label)

        column = 2
        if operation.needs_value:
            self.value_label.grid(row=0, column=column, padx=(0, 4))
            self.value_entry.grid(row=0, column=column + 1, padx=(0, 10))
            column += 2
        if operation.needs_index:
            if operation.index_input_kind == "array":
                self.array_label.grid(row=0, column=column, padx=(0, 4))
                self.array_entry.grid(row=0, column=column + 1, padx=(0, 10))
            else:
                self.index_label.grid(row=0, column=column, padx=(0, 4))
                self.index_entry.grid(row=0, column=column + 1, padx=(0, 10))

        can_run = not (
            self._current_structure_key() is StructureKey.AVL_TREE
            and operation.key == "insert"
            and self.controller.snapshot(StructureKey.AVL_TREE).rebalance_pending
        ) and not (
            self._current_structure_key() is StructureKey.MIN_HEAP
            and operation.key in {"add_raw", "extract_raw"}
            and self.controller.snapshot(StructureKey.MIN_HEAP).repair_pending
        ) and not (
            self._current_structure_key() is StructureKey.TWO_THREE_TREE
            and operation.key == "insert_raw"
            and self.controller.snapshot(StructureKey.TWO_THREE_TREE).repair_pending
        )
        self.run_button.configure(state=tk.NORMAL if can_run else tk.DISABLED)
        if update_status:
            if operation.index_input_kind == "array":
                self.status_text.set("Enter comma-separated integers, then run the algorithm.")
            else:
                self.status_text.set("Choose an operation and enter the required integer inputs.")

    def _run_current_operation(self) -> None:
        self._cancel_algorithm_playback()
        structure_key = self._current_structure_key()
        operation_key = self.selected_operation.get()
        result = self.controller.run_operation(
            structure_key,
            operation_key,
            value_text=self.value_input.get(),
            index_text=self._current_index_text(),
        )

        if not result.steps:
            self.status_text.set(result.message)
            self._draw_state(self.controller.snapshot(structure_key))
            return

        if _is_algorithm_key(structure_key):
            self._show_algorithm_steps([step for step in result.steps if isinstance(step, AlgorithmStep)], result.message)
            return

        self.status_text.set(_summarize_steps(result.steps))
        self._draw_state(self.controller.snapshot(structure_key, result.steps[-1]))
        self._refresh_operation_fields(update_status=False)

    def _restart_structure(self) -> None:
        self._cancel_algorithm_playback()
        structure_key = self._current_structure_key()
        self.controller.reset_structure(structure_key)
        self.selected_operation.set("")
        self.value_input.set("")
        self.index_input.set("")
        self.array_input.set("")
        self._clear_graph_inputs()
        self.status_text.set(f"{structure_key.value} reset to empty.")
        self._show_operations()
        self._draw_state(self.controller.snapshot(structure_key))

    def _show_algorithm_steps(self, steps: list[AlgorithmStep], final_message: str, index: int = 0) -> None:
        if not steps:
            self.status_text.set(final_message)
            self._draw_state(self.controller.snapshot(self._current_structure_key()))
            return

        step = steps[index]
        self.status_text.set(step.message if index < len(steps) - 1 else final_message)
        self._draw_state(build_algorithm_visualization_state(self._current_structure_key().value, step))
        if index < len(steps) - 1:
            self._algorithm_after_id = self.after(500, lambda: self._show_algorithm_steps(steps, final_message, index + 1))
        else:
            self._algorithm_after_id = None

    def _cancel_algorithm_playback(self) -> None:
        if self._algorithm_after_id is not None:
            self.after_cancel(self._algorithm_after_id)
            self._algorithm_after_id = None

    def _draw_state(self, state: VisualizationState) -> None:
        self.canvas.delete("all")
        self.canvas.update_idletasks()
        width = max(self.canvas.winfo_width(), 760)
        self.canvas.create_text(20, 24, anchor="w", text=state.structure_name, font=("Segoe UI", 14, "bold"))
        self.canvas.create_text(20, 50, anchor="w", text=state.message, font=("Segoe UI", 10))

        if state.structure_name == StructureKey.STACK.value:
            self._draw_stack(state, width)
        elif state.structure_name == StructureKey.QUEUE.value:
            self._draw_linear(state, x=40, y=145, show_arrows=False)
        elif state.structure_name == StructureKey.LINKED_LIST.value:
            self._draw_linear(state, x=40, y=145, show_arrows=True)
        elif state.structure_name == StructureKey.DYNAMIC_ARRAY.value:
            self._draw_dynamic_array(state, x=40, y=130)
        elif state.structure_name == StructureKey.AVL_TREE.value:
            self._draw_avl_tree(state, width)
        elif state.structure_name == StructureKey.MIN_HEAP.value:
            self._draw_min_heap(state, width)
        elif state.structure_name == StructureKey.HASH_TABLE.value:
            self._draw_hash_table(state, width)
        elif state.structure_name == StructureKey.TWO_THREE_TREE.value:
            self._draw_two_three_tree(state, width)
        elif state.structure_name == StructureKey.GRAPH.value:
            self._draw_graph(state, width)
        else:
            self._draw_algorithm_array(state, x=40, y=135)

    def _draw_stack(self, state: VisualizationState, width: int) -> None:
        cell_width = 96
        cell_height = 44
        x = width // 2 - cell_width // 2
        y = 285
        if not state.values:
            self.canvas.create_text(width // 2, 180, text="empty", fill="#666")
            return
        for element in state.values:
            fill = "#ffe08a" if element.highlighted else "#e8f1ff"
            self.canvas.create_rectangle(x, y, x + cell_width, y + cell_height, fill=fill, outline="#2b4c7e")
            self.canvas.create_text(x + cell_width // 2, y + cell_height // 2, text=str(element.value))
            self.canvas.create_text(x - 20, y + cell_height // 2, text=str(element.index), fill="#555")
            if element.index == len(state.values) - 1:
                self.canvas.create_text(x + cell_width + 46, y + cell_height // 2, text="top", fill="#333")
            y -= cell_height

    def _draw_linear(
        self,
        state: VisualizationState,
        x: int,
        y: int,
        show_arrows: bool,
    ) -> None:
        cell_width = 74
        cell_height = 46
        if not state.values:
            self.canvas.create_text(x, y, anchor="w", text="empty", fill="#666")
            return
        for element in state.values:
            fill = "#ffe08a" if element.highlighted else "#e8f1ff"
            self.canvas.create_rectangle(x, y, x + cell_width, y + cell_height, fill=fill, outline="#2b4c7e")
            self.canvas.create_text(x + cell_width // 2, y + cell_height // 2, text=str(element.value))
            self.canvas.create_text(x + cell_width // 2, y + cell_height + 16, text=str(element.index), fill="#555")
            if not show_arrows and element.index == 0:
                self.canvas.create_text(x + cell_width // 2, y - 16, text="front", fill="#333")
            if not show_arrows and element.index == len(state.values) - 1:
                self.canvas.create_text(x + cell_width // 2, y + cell_height + 34, text="back", fill="#333")
            if show_arrows and element.index < len(state.values) - 1:
                self.canvas.create_line(x + cell_width, y + cell_height // 2, x + cell_width + 36, y + cell_height // 2, arrow=tk.LAST)
                x += cell_width + 46
            else:
                x += cell_width + 12

    def _draw_dynamic_array(self, state: VisualizationState, x: int, y: int) -> None:
        self.canvas.create_text(
            x,
            y - 34,
            anchor="w",
            text=f"size: {state.size}    capacity: {state.capacity}",
            fill="#333",
        )
        if state.event_type is not None and state.event_type is EventType.RESIZE:
            old_capacity = state.metadata.get("old_capacity") if state.metadata else None
            new_capacity = state.metadata.get("new_capacity") if state.metadata else None
            if old_capacity is not None and new_capacity is not None:
                self.canvas.create_text(
                    x,
                    y - 14,
                    anchor="w",
                    text=f"resize: capacity {old_capacity} -> {new_capacity}",
                    fill="#7a4a00",
                )
        cell_width = 62
        cell_height = 44
        for element in state.values:
            fill = "#ffe08a" if element.highlighted else "#eef7ea"
            if element.value is None:
                fill = "#f5f5f5"
            self.canvas.create_rectangle(x, y, x + cell_width, y + cell_height, fill=fill, outline="#376b39")
            self.canvas.create_text(
                x + cell_width // 2,
                y + cell_height // 2,
                text="" if element.value is None else str(element.value),
            )
            self.canvas.create_text(x + cell_width // 2, y + cell_height + 16, text=str(element.index), fill="#555")
            x += cell_width + 6

    def _draw_avl_tree(self, state: VisualizationState, width: int) -> None:
        status = "BALANCED" if state.balanced else "REBALANCE REQUIRED"
        fill = "#1f6f43" if state.balanced else "#9f2d20"
        self.canvas.create_text(20, 76, anchor="w", text=status, fill=fill, font=("Segoe UI", 11, "bold"))
        if state.rebalance_pending:
            self.canvas.create_text(
                20,
                98,
                anchor="w",
                text="Run Balance before inserting another value.",
                fill="#9f2d20",
            )

        if not state.tree_nodes:
            self.canvas.create_text(width // 2, 185, text="empty", fill="#666")
            return

        max_order = max(node.order for node in state.tree_nodes)
        max_depth = max(node.depth for node in state.tree_nodes)
        horizontal_span = max(width - 140, 1)
        vertical_gap = max(54, min(76, 210 // max(max_depth, 1)))
        positions = {
            node.id: (
                70 + int((node.order / max(max_order, 1)) * horizontal_span),
                130 + node.depth * vertical_gap,
            )
            for node in state.tree_nodes
        }

        for parent_id, child_id in state.tree_edges:
            parent_x, parent_y = positions[parent_id]
            child_x, child_y = positions[child_id]
            self.canvas.create_line(parent_x, parent_y + 24, child_x, child_y - 24, fill="#555")

        for node in state.tree_nodes:
            x, y = positions[node.id]
            node_fill = "#ffd1cc" if node.unbalanced else "#e8f1ff"
            if node.highlighted:
                node_fill = "#ffe08a"
            self.canvas.create_oval(x - 24, y - 24, x + 24, y + 24, fill=node_fill, outline="#2b4c7e")
            self.canvas.create_text(x, y - 3, text=str(node.value), font=("Segoe UI", 10, "bold"))
            self.canvas.create_text(x, y + 13, text=f"bf {node.balance_factor}", fill="#333", font=("Segoe UI", 8))
            self.canvas.create_text(x, y + 34, text=f"h {node.height}", fill="#666", font=("Segoe UI", 8))

    def _draw_min_heap(self, state: VisualizationState, width: int) -> None:
        status = "VALID" if state.heap_valid else "REPAIR REQUIRED"
        fill = "#1f6f43" if state.heap_valid else "#9f2d20"
        self.canvas.create_text(20, 76, anchor="w", text=status, fill=fill, font=("Segoe UI", 11, "bold"))
        if state.repair_pending:
            repair = "Sift Up" if state.repair_kind == "sift_up" else "Heapify Down"
            self.canvas.create_text(
                20,
                98,
                anchor="w",
                text=f"Run {repair} before adding or extracting another value.",
                fill="#9f2d20",
            )

        if not state.tree_nodes:
            self.canvas.create_text(width // 2, 175, text="empty", fill="#666")
            return

        positions = self._heap_positions(state, width)
        for parent_id, child_id in state.tree_edges:
            parent_x, parent_y = positions[parent_id]
            child_x, child_y = positions[child_id]
            self.canvas.create_line(parent_x, parent_y + 22, child_x, child_y - 22, fill="#555")

        for node in state.tree_nodes:
            x, y = positions[node.id]
            node_fill = "#ffe08a" if node.highlighted else "#e8f1ff"
            self.canvas.create_oval(x - 23, y - 23, x + 23, y + 23, fill=node_fill, outline="#2b4c7e")
            self.canvas.create_text(x, y - 3, text=str(node.value), font=("Segoe UI", 10, "bold"))
            self.canvas.create_text(x, y + 13, text=f"i {node.array_index}", fill="#333", font=("Segoe UI", 8))

        array_y = 285
        self.canvas.create_text(40, array_y - 28, anchor="w", text=f"array order   size: {state.size}", fill="#333")
        x = 40
        cell_width = 56
        cell_height = 38
        for element in state.values:
            cell_fill = "#ffe08a" if element.highlighted else "#eef7ea"
            self.canvas.create_rectangle(x, array_y, x + cell_width, array_y + cell_height, fill=cell_fill, outline="#376b39")
            self.canvas.create_text(x + cell_width // 2, array_y + cell_height // 2, text=str(element.value))
            self.canvas.create_text(x + cell_width // 2, array_y + cell_height + 14, text=str(element.index), fill="#555")
            x += cell_width + 6

    def _heap_positions(self, state: VisualizationState, width: int) -> dict[int, tuple[int, int]]:
        max_depth = max(node.depth for node in state.tree_nodes)
        positions: dict[int, tuple[int, int]] = {}
        for node in state.tree_nodes:
            level_start = (2**node.depth) - 1
            position_in_level = node.id - level_start
            slots = 2**node.depth
            x = int(((position_in_level + 1) / (slots + 1)) * max(width - 80, 1)) + 40
            y = 125 + node.depth * max(48, min(66, 135 // max(max_depth, 1)))
            positions[node.id] = (x, y)
        return positions

    def _draw_hash_table(self, state: VisualizationState, width: int) -> None:
        self.canvas.create_text(
            20,
            76,
            anchor="w",
            text=f"buckets: {state.bucket_count}    entries: {state.size}",
            fill="#333",
            font=("Segoe UI", 10, "bold"),
        )
        if state.bucket_index is not None:
            self.canvas.create_text(
                20,
                98,
                anchor="w",
                text=f"calculated bucket index: {state.bucket_index}",
                fill="#2b4c7e",
            )
        if state.collision:
            self.canvas.create_text(260, 98, anchor="w", text="collision", fill="#9f2d20", font=("Segoe UI", 10, "bold"))

        if not state.buckets:
            self.canvas.create_text(width // 2, 185, text="empty", fill="#666")
            return

        row_height = 27
        y = 112
        for bucket in state.buckets:
            index_fill = "#ffe08a" if bucket.highlighted else "#e8f1ff"
            if bucket.collision:
                index_fill = "#ffd1cc"
            self.canvas.create_rectangle(40, y, 94, y + 23, fill=index_fill, outline="#2b4c7e")
            self.canvas.create_text(67, y + 12, text=str(bucket.index), font=("Segoe UI", 9, "bold"))

            x = 118
            if not bucket.entries:
                self.canvas.create_text(x, y + 12, anchor="w", text="empty", fill="#777")
            for entry in bucket.entries:
                entry_fill = "#ffe08a" if entry.highlighted else "#eef7ea"
                self.canvas.create_rectangle(x, y, x + 82, y + 23, fill=entry_fill, outline="#376b39")
                self.canvas.create_text(x + 41, y + 12, text=f"{entry.key}: {entry.value}")
                x += 96
                if entry.entry_index < len(bucket.entries) - 1:
                    self.canvas.create_line(x - 14, y + 12, x - 2, y + 12, arrow=tk.LAST, fill="#555")
            y += row_height

    def _draw_two_three_tree(self, state: VisualizationState, width: int) -> None:
        status = "VALID" if state.tree_valid else "REPAIR REQUIRED"
        fill = "#1f6f43" if state.tree_valid else "#9f2d20"
        self.canvas.create_text(20, 76, anchor="w", text=status, fill=fill, font=("Segoe UI", 11, "bold"))
        if state.repair_pending:
            self.canvas.create_text(
                20,
                98,
                anchor="w",
                text="Run Repair before inserting another value.",
                fill="#9f2d20",
            )

        if not state.multi_key_tree_nodes:
            self.canvas.create_text(width // 2, 185, text="empty", fill="#666")
            return

        positions = self._multi_key_tree_positions(state, width)
        for parent_id, child_id in state.multi_key_tree_edges:
            parent_x, parent_y = positions[parent_id]
            child_x, child_y = positions[child_id]
            self.canvas.create_line(parent_x, parent_y + 22, child_x, child_y - 20, fill="#555")

        for node in state.multi_key_tree_nodes:
            x, y = positions[node.id]
            key_width = 36
            node_width = key_width * len(node.keys)
            node_fill = "#ffd1cc" if node.overflowing else "#e8f1ff"
            if node.highlighted:
                node_fill = "#ffe08a"
            left = x - node_width // 2
            self.canvas.create_rectangle(left, y - 20, left + node_width, y + 20, fill=node_fill, outline="#2b4c7e")
            for index, key in enumerate(node.keys):
                key_left = left + index * key_width
                if index > 0:
                    self.canvas.create_line(key_left, y - 20, key_left, y + 20, fill="#2b4c7e")
                key_fill = "#fff2b0" if node.highlighted_key == key else node_fill
                if key_fill != node_fill:
                    self.canvas.create_rectangle(key_left + 1, y - 19, key_left + key_width - 1, y + 19, fill=key_fill, outline="")
                self.canvas.create_text(key_left + key_width // 2, y, text=str(key), font=("Segoe UI", 10, "bold"))
            if node.overflowing:
                self.canvas.create_text(x, y + 34, text="overflow", fill="#9f2d20", font=("Segoe UI", 8, "bold"))

    def _multi_key_tree_positions(self, state: VisualizationState, width: int) -> dict[int, tuple[int, int]]:
        max_order = max(node.order for node in state.multi_key_tree_nodes)
        max_depth = max(node.depth for node in state.multi_key_tree_nodes)
        horizontal_span = max(width - 140, 1)
        vertical_gap = max(58, min(76, 200 // max(max_depth, 1)))
        return {
            node.id: (
                70 + int((node.order / max(max_order, 1)) * horizontal_span),
                130 + node.depth * vertical_gap,
            )
            for node in state.multi_key_tree_nodes
        }

    def _draw_graph(self, state: VisualizationState, width: int) -> None:
        self.canvas.create_text(
            20,
            76,
            anchor="w",
            text=f"type: {state.graph_type or 'undirected'}    vertices: {len(state.graph_nodes)}    edges: {len(state.graph_edges)}",
            fill="#333",
            font=("Segoe UI", 10, "bold"),
        )
        info_lines: list[tuple[str, str]] = []
        if state.queue or state.stack or state.traversal_order:
            frontier_label = state.frontier or ("stack" if state.stack else "queue")
            frontier_values = state.stack if frontier_label == "stack" else state.queue
            info_lines.append(
                (f"{frontier_label}: {list(frontier_values)}    order: {list(state.traversal_order)}", "#2b4c7e")
            )
        if state.priority_queue:
            info_lines.append((f"priority queue: {list(state.priority_queue)}", "#2b4c7e"))
        if state.visited_vertices:
            info_lines.append((f"finalized/visited: {list(state.visited_vertices)}", "#1f6f43"))
        if state.distances:
            distances = ", ".join(
                f"{vertex}={'inf' if distance is None else distance}"
                for vertex, distance in sorted(state.distances.items())
            )
            info_lines.append((f"distances: {distances}", "#333"))
        if state.shortest_path:
            info_lines.append((f"path: {list(state.shortest_path)}", "#1f6f43"))
        if state.component_count is not None:
            info_lines.append((f"component count: {state.component_count}", "#333"))
        if state.completed_components:
            components = "; ".join(
                f"{index}: {list(component)}" for index, component in enumerate(state.completed_components, start=1)
            )
            info_lines.append((f"components: {components}", "#2b4c7e"))
        elif state.current_component_vertices:
            info_lines.append(
                (f"component {state.current_component}: {list(state.current_component_vertices)}", "#2b4c7e")
            )
        if state.traversal_path:
            info_lines.append((f"path: {list(state.traversal_path)}", "#7a4a00"))
        if state.cycle_detected:
            info_lines.append((f"cycle: {list(state.cycle_vertices)}", "#9f2d20"))
        for index, (text, fill) in enumerate(info_lines):
            self.canvas.create_text(
                20,
                98 + index * 22,
                anchor="w",
                text=text,
                fill=fill,
            )
        if not state.graph_nodes:
            self.canvas.create_text(width // 2, 185, text="empty graph", fill="#666")
            return

        positions = self._graph_positions(state, width)
        radius = 23
        for edge in state.graph_edges:
            source_x, source_y = positions[edge.source]
            destination_x, destination_y = positions[edge.destination]
            line_fill = "#9f2d20" if edge.highlighted else "#555"
            line_width = 2 if edge.highlighted else 1
            line_options = {"fill": line_fill, "width": line_width}
            if edge.directed:
                line_options["arrow"] = tk.LAST
            start_x, start_y, end_x, end_y = _shortened_line(
                source_x,
                source_y,
                destination_x,
                destination_y,
                radius + 2,
            )
            self.canvas.create_line(start_x, start_y, end_x, end_y, **line_options)
            mid_x = (source_x + destination_x) // 2
            mid_y = (source_y + destination_y) // 2
            self.canvas.create_text(mid_x, mid_y - 10, text=str(edge.weight), fill="#7a4a00", font=("Segoe UI", 9, "bold"))

        for node in state.graph_nodes:
            x, y = positions[node.value]
            node_fill = "#ffe08a" if node.highlighted else "#e8f1ff"
            if node.path:
                node_fill = "#c7e7ff"
            if node.visited:
                node_fill = "#bfe8c1"
            if node.component_id is not None:
                node_fill = _component_color(node.component_id)
            if node.cycle:
                node_fill = "#ffd1cc"
            if node.current:
                node_fill = "#ffe08a"
            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=node_fill, outline="#2b4c7e")
            self.canvas.create_text(x, y, text=str(node.value), font=("Segoe UI", 10, "bold"))

    def _graph_positions(self, state: VisualizationState, width: int) -> dict[int, tuple[int, int]]:
        nodes = state.graph_nodes
        if len(nodes) == 1:
            return {nodes[0].value: (width // 2, 190)}

        center_x = width // 2
        center_y = 195
        radius = min(145, max(80, width // 5))
        positions: dict[int, tuple[int, int]] = {}
        for index, node in enumerate(nodes):
            angle = (2 * math.pi * index / len(nodes)) - (math.pi / 2)
            positions[node.value] = (
                int(center_x + radius * math.cos(angle)),
                int(center_y + radius * math.sin(angle)),
            )
        return positions

    def _draw_algorithm_array(self, state: VisualizationState, x: int, y: int) -> None:
        if state.target is not None:
            self.canvas.create_text(x, y - 36, anchor="w", text=f"target: {state.target}", fill="#333")
        if state.pivot_index is not None and state.pivot_value is not None:
            self.canvas.create_text(
                x,
                y - 36,
                anchor="w",
                text=f"pivot: {state.pivot_value} at {state.pivot_index}",
                fill="#7a4a00",
            )
        if state.discarded_range is not None:
            self.canvas.create_text(
                x + 120,
                y - 36,
                anchor="w",
                text=f"discarded: {state.discarded_range[0]}..{state.discarded_range[1]}",
                fill="#9f2d20",
            )
        if state.sorted_prefix_end is not None and state.sorted_prefix_end >= 0:
            self.canvas.create_text(
                x,
                y - 16,
                anchor="w",
                text=f"sorted prefix: 0..{state.sorted_prefix_end}",
                fill="#1f6f43",
            )
        if state.sorted_suffix_start is not None and state.sorted_suffix_start < state.size:
            self.canvas.create_text(
                x,
                y - 16,
                anchor="w",
                text=f"sorted suffix: {state.sorted_suffix_start}..{state.size - 1}",
                fill="#1f6f43",
            )
        if state.split_index is not None:
            self.canvas.create_text(
                x,
                y - 16,
                anchor="w",
                text=f"split at: {state.split_index}",
                fill="#2b4c7e",
            )
        if state.merge_ranges:
            ranges = ", ".join(f"{start}..{end}" for start, end in state.merge_ranges)
            self.canvas.create_text(x, y + 88, anchor="w", text=f"merge ranges: {ranges}", fill="#2b4c7e")
        if state.completed_range is not None:
            self.canvas.create_text(
                x + 240,
                y + 88,
                anchor="w",
                text=f"merged: {state.completed_range[0]}..{state.completed_range[1]}",
                fill="#1f6f43",
            )
        if state.left_partition_range is not None:
            self.canvas.create_text(
                x,
                y + 108,
                anchor="w",
                text=f"left partition: {state.left_partition_range[0]}..{state.left_partition_range[1]}",
                fill="#2b4c7e",
            )
        if state.right_partition_range is not None:
            self.canvas.create_text(
                x + 240,
                y + 108,
                anchor="w",
                text=f"right partition: {state.right_partition_range[0]}..{state.right_partition_range[1]}",
                fill="#2b4c7e",
            )
        if state.active_heap_range is not None:
            self.canvas.create_text(
                x,
                y + 128,
                anchor="w",
                text=f"active heap: {state.active_heap_range[0]}..{state.active_heap_range[1]}",
                fill="#7a4a00",
            )

        if not state.values:
            self.canvas.create_text(x, y, anchor="w", text="empty array", fill="#666")
            return

        cell_width = 58
        cell_height = 42
        for element in state.values:
            fill = "#e8f1ff"
            if element.moved:
                fill = "#f0f0f0"
            if element.highlighted:
                fill = "#ffe08a"
            if state.pivot_index == element.index:
                fill = "#ffd59e"
            if state.found_index == element.index:
                fill = "#bfe8c1"

            cell_x = x + element.index * (cell_width + 8)
            self.canvas.create_rectangle(cell_x, y, cell_x + cell_width, y + cell_height, fill=fill, outline="#2b4c7e")
            self.canvas.create_text(cell_x + cell_width // 2, y + cell_height // 2, text=str(element.value))
            self.canvas.create_text(cell_x + cell_width // 2, y + cell_height + 14, text=str(element.index), fill="#555")

            labels: list[str] = []
            if state.low_index == element.index:
                labels.append("low")
            if state.mid_index == element.index:
                labels.append("mid")
            if state.high_index == element.index:
                labels.append("high")
            if state.pivot_index == element.index:
                labels.append("pivot")
            if labels:
                self.canvas.create_text(
                    cell_x + cell_width // 2,
                    y - 14,
                    text="/".join(labels),
                    fill="#333",
                    font=("Segoe UI", 8, "bold"),
                )

        if state.low_index is not None and state.high_index is not None and state.low_index <= state.high_index:
            left = x + state.low_index * (cell_width + 8)
            right = x + state.high_index * (cell_width + 8) + cell_width
            self.canvas.create_rectangle(left - 3, y - 4, right + 3, y + cell_height + 4, outline="#1f6f43", width=2)
        if state.active_heap_range is not None:
            left = x + state.active_heap_range[0] * (cell_width + 8)
            right = x + state.active_heap_range[1] * (cell_width + 8) + cell_width
            self.canvas.create_rectangle(left - 3, y - 4, right + 3, y + cell_height + 4, outline="#7a4a00", width=2)

    def _clear_controls(self) -> None:
        for child in self.controls.winfo_children():
            child.destroy()

    def _current_structure_key(self) -> StructureKey:
        return StructureKey(self.selected_structure.get())

    def _current_operation(self) -> OperationSpec:
        return self.controller.operation_for(
            self._current_structure_key(),
            self.selected_operation.get(),
        )

    def _current_index_text(self) -> str:
        operation = self._current_operation()
        if operation.index_input_kind == "array":
            return self.array_input.get()
        return self.index_input.get()


def launch() -> None:
    """Launch the desktop application."""
    app = VisualLabApp()
    app.mainloop()


def check_runtime() -> str:
    """Perform a no-window runtime check used by tests and terminal smoke checks."""
    controller = VisualLabController()
    state = build_visualization_state(
        StructureKey.STACK.value,
        controller._structures[StructureKey.STACK],
    )
    return f"{state.structure_name} ready"


def _summarize_steps(steps: list[object]) -> str:
    messages = [step.message for step in steps if hasattr(step, "message")]
    return " ".join(messages)


def _shortened_line(
    source_x: int,
    source_y: int,
    destination_x: int,
    destination_y: int,
    padding: int,
) -> tuple[int, int, int, int]:
    dx = destination_x - source_x
    dy = destination_y - source_y
    distance = math.hypot(dx, dy)
    if distance == 0:
        return source_x, source_y, destination_x, destination_y

    offset_x = int((dx / distance) * padding)
    offset_y = int((dy / distance) * padding)
    return source_x + offset_x, source_y + offset_y, destination_x - offset_x, destination_y - offset_y


def _component_color(component_id: int) -> str:
    colors = ("#c7e7ff", "#ffd8a8", "#d7f0c2", "#f5c7d7", "#ddd1ff", "#fff2a8")
    return colors[(component_id - 1) % len(colors)]


def _is_algorithm_key(structure_key: StructureKey) -> bool:
    return structure_key in {
        StructureKey.BINARY_SEARCH,
        StructureKey.BUBBLE_SORT,
        StructureKey.SELECTION_SORT,
        StructureKey.INSERTION_SORT,
        StructureKey.MERGE_SORT,
        StructureKey.QUICK_SORT,
        StructureKey.HEAP_SORT,
    }
