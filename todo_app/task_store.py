"""Task storage: load/save tasks to JSON file."""

import json
from pathlib import Path
from typing import Any


DATA_FILE = Path(__file__).parent / "tasks.json"


def load_tasks() -> list[dict[str, Any]]:
    """Load tasks from JSON file. Returns empty list if file missing or invalid."""
    if not DATA_FILE.exists():
        return []
    try:
        with open(DATA_FILE, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks: list[dict[str, Any]]) -> None:
    """Save tasks to JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)
