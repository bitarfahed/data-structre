"""Tkinter desktop shell for the visual lab."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from data_structures_visual_lab.events import EventType
from data_structures_visual_lab.gui.controller import OperationSpec, StructureKey, VisualLabController
from data_structures_visual_lab.visualization.state import VisualizationState, build_visualization_state


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
        self.status_text = tk.StringVar(value="Choose a structure to begin.")

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

        ttk.Label(self.sidebar, text="Structures").grid(row=0, column=0, sticky="w")
        for row, structure_key in enumerate(self.controller.structure_keys(), start=1):
            ttk.Radiobutton(
                self.sidebar,
                text=structure_key.value,
                value=structure_key.value,
                variable=self.selected_structure,
                command=self._show_structure_selection,
            ).grid(row=row, column=0, sticky="w", pady=2)

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
        self._clear_controls()
        structure_key = self._current_structure_key()
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
        self.run_button = ttk.Button(self.controls, text="Run", command=self._run_current_operation)
        self.restart_button = ttk.Button(self.controls, text="Restart", command=self._restart_structure)

        self.run_button.grid(row=0, column=6, padx=(0, 6))
        self.restart_button.grid(row=0, column=7, sticky="w")
        self._refresh_operation_fields()
        self.status_text.set("Choose an operation and enter the required integer inputs.")

    def _refresh_operation_fields(self) -> None:
        operation = self._current_operation()
        self.value_label.grid_remove()
        self.value_entry.grid_remove()
        self.index_label.grid_remove()
        self.index_entry.grid_remove()
        self.value_label.configure(text="Value")
        self.index_label.configure(text=operation.index_label)

        column = 2
        if operation.needs_value:
            self.value_label.grid(row=0, column=column, padx=(0, 4))
            self.value_entry.grid(row=0, column=column + 1, padx=(0, 10))
            column += 2
        if operation.needs_index:
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
        )
        self.run_button.configure(state=tk.NORMAL if can_run else tk.DISABLED)

    def _run_current_operation(self) -> None:
        structure_key = self._current_structure_key()
        operation_key = self.selected_operation.get()
        result = self.controller.run_operation(
            structure_key,
            operation_key,
            value_text=self.value_input.get(),
            index_text=self.index_input.get(),
        )

        if not result.steps:
            self.status_text.set(result.message)
            self._draw_state(self.controller.snapshot(structure_key))
            return

        self.status_text.set(_summarize_steps(result.steps))
        self._draw_state(self.controller.snapshot(structure_key, result.steps[-1]))
        self._refresh_operation_fields()

    def _restart_structure(self) -> None:
        structure_key = self._current_structure_key()
        self.controller.reset_structure(structure_key)
        self.selected_operation.set("")
        self.value_input.set("")
        self.index_input.set("")
        self.status_text.set(f"{structure_key.value} reset to empty.")
        self._show_operations()
        self._draw_state(self.controller.snapshot(structure_key))

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
        else:
            self._draw_hash_table(state, width)

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
