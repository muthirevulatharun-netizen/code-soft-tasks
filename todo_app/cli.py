"""
To-Do List – Command-line interface.
Uses the same tasks.json as the GUI. Run: python cli.py [command] [args]
Commands: add <text>, list, done <id>, undone <id>, edit <id> <text>, delete <id>, clear-done
"""

import sys
from task_store import load_tasks, save_tasks

KEY_ID = "id"
KEY_TEXT = "text"
KEY_DONE = "done"
KEY_PRIORITY = "priority"


def _next_id(tasks):
    return max((t.get(KEY_ID, 0) for t in tasks), default=0) + 1


def add(tasks, text, priority="Medium"):
    tasks.append({KEY_ID: _next_id(tasks), KEY_TEXT: text, KEY_DONE: False, KEY_PRIORITY: priority})
    save_tasks(tasks)
    print(f"Added: {text}")


def list_tasks(tasks):
    if not tasks:
        print("No tasks.")
        return
    for t in tasks:
        status = "[x]" if t.get(KEY_DONE) else "[ ]"
        print(f"  {t[KEY_ID]}. {status} {t.get(KEY_TEXT)} ({t.get(KEY_PRIORITY, 'Medium')})")


def toggle(tasks, task_id, done):
    tid = int(task_id)
    for t in tasks:
        if t.get(KEY_ID) == tid:
            t[KEY_DONE] = done
            save_tasks(tasks)
            print(f"Marked as {'done' if done else 'pending'}.")
            return
    print(f"Task {task_id} not found.")


def edit(tasks, task_id, text):
    tid = int(task_id)
    for t in tasks:
        if t.get(KEY_ID) == tid:
            t[KEY_TEXT] = text
            save_tasks(tasks)
            print("Updated.")
            return
    print(f"Task {task_id} not found.")


def delete(tasks, task_id):
    tid = int(task_id)
    for i, t in enumerate(tasks):
        if t.get(KEY_ID) == tid:
            tasks.pop(i)
            save_tasks(tasks)
            print("Deleted.")
            return
    print(f"Task {task_id} not found.")


def clear_done(tasks):
    before = len(tasks)
    tasks[:] = [t for t in tasks if not t.get(KEY_DONE)]
    save_tasks(tasks)
    print(f"Removed {before - len(tasks)} completed task(s).")


def main():
    tasks = load_tasks()
    args = sys.argv[1:]
    if not args:
        print("To-Do CLI. Commands: add, list, done, undone, edit, delete, clear-done")
        list_tasks(tasks)
        return

    cmd = args[0].lower()
    if cmd == "add":
        add(tasks, " ".join(args[1:]) if len(args) > 1 else input("Task: "))
    elif cmd == "list":
        list_tasks(tasks)
    elif cmd == "done" and len(args) >= 2:
        toggle(tasks, args[1], True)
    elif cmd == "undone" and len(args) >= 2:
        toggle(tasks, args[1], False)
    elif cmd == "edit" and len(args) >= 3:
        edit(tasks, args[1], " ".join(args[2:]))
    elif cmd == "delete" and len(args) >= 2:
        delete(tasks, args[1])
    elif cmd == "clear-done":
        clear_done(tasks)
    else:
        print("Usage: add <text> | list | done <id> | undone <id> | edit <id> <text> | delete <id> | clear-done")


if __name__ == "__main__":
    main()
