"""
To-Do List Application – GUI version.
Create, update, delete, and track tasks. Data is saved to tasks.json.
"""

import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
from task_store import load_tasks, save_tasks

# Task keys in stored dict
KEY_ID = "id"
KEY_TEXT = "text"
KEY_DONE = "done"
KEY_PRIORITY = "priority"

# Priority options
PRIORITIES = ("Low", "Medium", "High")
PRIORITY_COLORS = {"Low": "#2d6a4f", "Medium": "#ca6702", "High": "#9d0208"}


class TodoApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("To-Do List")
        self.root.geometry("560x420")
        self.root.minsize(400, 320)
        self.root.configure(bg="#1b2838")

        self.tasks: list[dict] = []
        self.next_id = 1
        self._load_and_build_ui()

    def _load_and_build_ui(self):
        self.tasks = load_tasks()
        if self.tasks:
            self.next_id = max((t.get(KEY_ID, 0) for t in self.tasks), default=0) + 1

        self._style()
        self._build_widgets()

    def _style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "TFrame",
            background="#1b2838",
        )
        style.configure(
            "TLabel",
            background="#1b2838",
            foreground="#e0e0e0",
            font=("Segoe UI", 10),
        )
        style.configure(
            "Header.TLabel",
            font=("Segoe UI", 16, "bold"),
            foreground="#66c0f4",
        )
        style.configure(
            "TButton",
            font=("Segoe UI", 10),
            padding=(12, 6),
        )
        style.map("TButton", background=[("active", "#66c0f4")])

    def _build_widgets(self):
        # Header
        header = ttk.Frame(self.root, padding=(16, 12))
        header.pack(fill=tk.X)
        ttk.Label(header, text="Your To-Do List", style="Header.TLabel").pack(anchor=tk.W)

        # Input row
        input_frame = ttk.Frame(self.root, padding=(16, 0))
        input_frame.pack(fill=tk.X, pady=(0, 8))

        self.entry = tk.Entry(
            input_frame,
            font=("Segoe UI", 12),
            bg="#2a475e",
            fg="#e0e0e0",
            insertbackground="#e0e0e0",
            relief=tk.FLAT,
            bd=0,
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, ipadx=10, padx=(0, 8))
        self.entry.bind("<Return>", lambda e: self._add_task())

        self.priority_var = tk.StringVar(value="Medium")
        priority_combo = ttk.Combobox(
            input_frame,
            textvariable=self.priority_var,
            values=PRIORITIES,
            state="readonly",
            width=8,
            font=("Segoe UI", 10),
        )
        priority_combo.pack(side=tk.LEFT, padx=(0, 8))

        add_btn = ttk.Button(input_frame, text="Add Task", command=self._add_task)
        add_btn.pack(side=tk.LEFT)

        # Task list
        list_frame = ttk.Frame(self.root, padding=(16, 8))
        list_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(
            list_frame,
            columns=("priority", "text", "status"),
            show="headings",
            height=12,
            selectmode="browse",
        )
        self.tree.heading("priority", text="Priority")
        self.tree.heading("text", text="Task")
        self.tree.heading("status", text="Status")
        self.tree.column("priority", width=80)
        self.tree.column("text", width=320)
        self.tree.column("status", width=80)

        scroll = ttk.Scrollbar(list_frame)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.configure(command=self.tree.yview)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.bind("<Double-1>", lambda e: self._edit_selected())

        # Buttons
        btn_frame = ttk.Frame(self.root, padding=(16, 8))
        btn_frame.pack(fill=tk.X)

        ttk.Button(btn_frame, text="Mark Done / Undone", command=self._toggle_done).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(btn_frame, text="Edit Task", command=self._edit_selected).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(btn_frame, text="Delete Task", command=self._delete_selected).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(btn_frame, text="Clear Completed", command=self._clear_completed).pack(side=tk.LEFT)

        self._refresh_list()

    def _task_to_row(self, task: dict) -> tuple[str, str, str]:
        priority = task.get(KEY_PRIORITY, "Medium")
        text = task.get(KEY_TEXT, "")
        status = "Done" if task.get(KEY_DONE, False) else "Pending"
        return (priority, text, status)

    def _refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for task in self.tasks:
            row = self._task_to_row(task)
            iid = self.tree.insert("", tk.END, values=row)
            self.tree.set(iid, "#0", str(task.get(KEY_ID, "")))
            if task.get(KEY_DONE):
                self.tree.item(iid, tags=("done",))
        self.tree.tag_configure("done", foreground="#6c757d")
        self._persist()

    def _persist(self):
        save_tasks(self.tasks)

    def _get_selected_task(self) -> dict | None:
        sel = self.tree.selection()
        if not sel:
            return None
        item = sel[0]
        children = self.tree.get_children()
        try:
            idx = list(children).index(item)
        except ValueError:
            return None
        if 0 <= idx < len(self.tasks):
            return self.tasks[idx]
        return None

    def _add_task(self):
        text = self.entry.get().strip()
        if not text:
            messagebox.showinfo("Add Task", "Please enter a task description.")
            return
        priority = self.priority_var.get() or "Medium"
        self.tasks.append({
            KEY_ID: self.next_id,
            KEY_TEXT: text,
            KEY_DONE: False,
            KEY_PRIORITY: priority,
        })
        self.next_id += 1
        self.entry.delete(0, tk.END)
        self._refresh_list()

    def _toggle_done(self):
        task = self._get_selected_task()
        if not task:
            messagebox.showinfo("Mark Task", "Please select a task first.")
            return
        task[KEY_DONE] = not task.get(KEY_DONE, False)
        self._refresh_list()

    def _edit_selected(self):
        task = self._get_selected_task()
        if not task:
            messagebox.showinfo("Edit Task", "Please select a task first.")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Task")
        dialog.geometry("380x140")
        dialog.configure(bg="#1b2838")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Task:").pack(anchor=tk.W, padx=12, pady=(12, 2))
        entry = tk.Entry(
            dialog,
            font=("Segoe UI", 11),
            bg="#2a475e",
            fg="#e0e0e0",
            insertbackground="#e0e0e0",
        )
        entry.pack(fill=tk.X, padx=12, pady=(0, 8))
        entry.insert(0, task.get(KEY_TEXT, ""))
        entry.focus_set()

        ttk.Label(dialog, text="Priority:").pack(anchor=tk.W, padx=12, pady=(4, 2))
        pri_var = tk.StringVar(value=task.get(KEY_PRIORITY, "Medium"))
        ttk.Combobox(dialog, textvariable=pri_var, values=PRIORITIES, state="readonly", width=12).pack(anchor=tk.W, padx=12, pady=(0, 12))

        def save():
            new_text = entry.get().strip()
            if new_text:
                task[KEY_TEXT] = new_text
                task[KEY_PRIORITY] = pri_var.get()
                self._refresh_list()
            dialog.destroy()

        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill=tk.X, padx=12, pady=(0, 12))
        ttk.Button(btn_frame, text="Save", command=save).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT)
        entry.bind("<Return>", lambda e: save())

    def _delete_selected(self):
        task = self._get_selected_task()
        if not task:
            messagebox.showinfo("Delete Task", "Please select a task first.")
            return
        if messagebox.askyesno("Delete Task", "Delete this task?"):
            self.tasks.remove(task)
            self._refresh_list()

    def _clear_completed(self):
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if not t.get(KEY_DONE)]
        removed = before - len(self.tasks)
        self._refresh_list()
        if removed:
            messagebox.showinfo("Clear Completed", f"Removed {removed} completed task(s).")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    TodoApp().run()
