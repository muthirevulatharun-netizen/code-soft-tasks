# To-Do List Application

A Python application to create, update, and track your to-do list. It comes in two interfaces: **GUI** (tkinter) and **command-line**, both using the same `tasks.json` file.

## Features

- **Create** tasks with optional priority (Low, Medium, High)
- **Update** task text and priority
- **Track** status: mark tasks done or pending
- **Delete** individual tasks or clear all completed ones
- **Persistent storage** – tasks are saved to `tasks.json` in the app folder

## Requirements

- Python 3.10 or newer
- No extra packages; uses only the standard library (including `tkinter`)

## Running the GUI

```bash
cd todo_app
python main.py
```

- **Add:** Type in the box, choose priority, press Enter or click **Add Task**
- **Mark done/undone:** Select a task and click **Mark Done / Undone**
- **Edit:** Double-click a task or select it and click **Edit Task**
- **Delete:** Select a task and click **Delete Task**
- **Clear completed:** Click **Clear Completed** to remove all done tasks

## Running the command-line interface

From the `todo_app` folder:

```bash
python cli.py list
python cli.py add "Buy groceries"
python cli.py done 1
python cli.py undone 1
python cli.py edit 1 "Buy groceries and milk"
python cli.py delete 1
python cli.py clear-done
```

Running `python cli.py` with no arguments prints a short help and lists current tasks.

## Project structure

```
todo_app/
  main.py       # GUI application
  cli.py        # Command-line interface
  task_store.py # Load/save tasks (JSON)
  tasks.json    # Created automatically when you add tasks
  README.md
  requirements.txt
```
