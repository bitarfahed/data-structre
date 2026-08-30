"""Tkinter desktop shell for the visual lab."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from dsa_visual_lab.events import Step
from dsa_visual_lab.gui.controller import OperationSpec, StructureKey, VisualLabController
from dsa_visual_lab.visualization.state import VisualizationState, build_visualization_state


class VisualLabApp(tk.Tk):
    """Small desktop GUI for Round 1 structures."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Interactive Data Structures & Algorithms Visual Lab")
        self.geometry("980x620")
        self.minsize(820, 520)

        self.controller = VisualLabController()
        self.selected_structure = tk.StringVar(value=StructureKey.STACK.value)
        self.selected_operation = tk.StringVar()
        self.value_input = tk.StringVar()
        self.index_input = tk.StringVar()
        self.status_text = tk.StringVar(value="Choose a structure to begin.")
        self.play_button_text = tk.StringVar(value="Play")

        self.current_steps: list[Step] = []
        self.current_step_index = -1
        self.last_operation: tuple[StructureKey, str, str, str] | None = None
        self.playing = False
        self.play_after_id: str | None = None

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
        self._stop_playback()
        structure_key = self._current_structure_key()
        self.selected_operation.set("")
        self.current_steps = []
        self.current_step_index = -1
        self.last_operation = None
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
        self._stop_playback()
        self._clear_controls()
        structure_key = self._current_structure_key()
        operations = self.controller.operations_for(structure_key)
        if not self.selected_operation.get():
            self.selected_operation.set(operations[0].key)

        ttk.Label(self.controls, text="Operation").grid(row=0, column=0, padx=(0, 6))
        operation_menu = ttk.Combobox(
            self.controls,
            state="readonly",
            width=24,
            textvariable=self.selected_operation,
            values=[operation.key for operation in operations],
        )
        operation_menu.grid(row=0, column=1, padx=(0, 10))
        operation_menu.bind("<<ComboboxSelected>>", lambda _event: self._refresh_operation_fields())

        self.value_label = ttk.Label(self.controls, text="Value")
        self.value_entry = ttk.Entry(self.controls, width=10, textvariable=self.value_input)
        self.index_label = ttk.Label(self.controls, text="Index")
        self.index_entry = ttk.Entry(self.controls, width=10, textvariable=self.index_input)
        self.run_button = ttk.Button(self.controls, text="Run", command=self._run_current_operation)
        self.next_button = ttk.Button(self.controls, text="Next Step", command=self._next_step)
        self.play_button = ttk.Button(
            self.controls,
            textvariable=self.play_button_text,
            command=self._toggle_playback,
        )
        self.restart_button = ttk.Button(self.controls, text="Restart", command=self._restart_operation)

        self.run_button.grid(row=0, column=6, padx=(0, 6))
        self.next_button.grid(row=1, column=0, pady=(8, 0), sticky="w")
        self.play_button.grid(row=1, column=1, pady=(8, 0), sticky="w")
        self.restart_button.grid(row=1, column=2, pady=(8, 0), sticky="w")
        self._refresh_operation_fields()
        self.status_text.set("Choose an operation and enter the required integer inputs.")

    def _refresh_operation_fields(self) -> None:
        operation = self._current_operation()
        self.value_label.grid_remove()
        self.value_entry.grid_remove()
        self.index_label.grid_remove()
        self.index_entry.grid_remove()

        column = 2
        if operation.needs_value:
            self.value_label.grid(row=0, column=column, padx=(0, 4))
            self.value_entry.grid(row=0, column=column + 1, padx=(0, 10))
            column += 2
        if operation.needs_index:
            self.index_label.grid(row=0, column=column, padx=(0, 4))
            self.index_entry.grid(row=0, column=column + 1, padx=(0, 10))

    def _run_current_operation(self) -> None:
        self._stop_playback()
        structure_key = self._current_structure_key()
        operation_key = self.selected_operation.get()
        value_text = self.value_input.get()
        index_text = self.index_input.get()
        result = self.controller.run_operation(
            structure_key,
            operation_key,
            value_text=value_text,
            index_text=index_text,
        )

        if not result.steps:
            self.current_steps = []
            self.current_step_index = -1
            self.status_text.set(result.message)
            self._draw_state(self.controller.snapshot(structure_key))
            return

        self.current_steps = result.steps
        self.current_step_index = 0
        self.last_operation = (structure_key, operation_key, value_text, index_text)
        self.status_text.set(result.steps[0].message)
        self._draw_state(self.controller.snapshot(structure_key, result.steps[0]))

    def _next_step(self) -> None:
        if not self.current_steps:
            self.status_text.set("Run an operation first.")
            return

        if self.current_step_index < len(self.current_steps) - 1:
            self.current_step_index += 1

        structure_key = self._current_structure_key()
        step = self.current_steps[self.current_step_index]
        self.status_text.set(step.message)
        self._draw_state(self.controller.snapshot(structure_key, step))

    def _toggle_playback(self) -> None:
        if self.playing:
            self._stop_playback()
            return
        if not self.current_steps:
            self.status_text.set("Run an operation first.")
            return
        self.playing = True
        self.play_button_text.set("Pause")
        self._schedule_next_step()

    def _schedule_next_step(self) -> None:
        if not self.playing:
            return
        if self.current_step_index >= len(self.current_steps) - 1:
            self._stop_playback()
            return
        self._next_step()
        self.play_after_id = self.after(850, self._schedule_next_step)

    def _stop_playback(self) -> None:
        self.playing = False
        self.play_button_text.set("Play")
        if self.play_after_id is not None:
            self.after_cancel(self.play_after_id)
            self.play_after_id = None

    def _restart_operation(self) -> None:
        if self.last_operation is None or not self.current_steps:
            self.status_text.set("Run an operation first.")
            return
        self._stop_playback()
        self.current_step_index = 0
        structure_key = self.last_operation[0]
        step = self.current_steps[0]
        self.status_text.set(step.message)
        self._draw_state(self.controller.snapshot(structure_key, step))

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
        else:
            self._draw_dynamic_array(state, x=40, y=130)

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
