"""JSON file persistence. The only module that touches the disk."""

from __future__ import annotations

import json
from pathlib import Path

from todo_cli.errors import StorageError
from todo_cli.models import Task

DEFAULT_PATH = Path.home() / ".todo-cli" / "tasks.json"


class JsonStorage:
    def __init__(self, path: Path | str = DEFAULT_PATH) -> None:
        self.path = Path(path)

    def load(self) -> list[Task]:
        if not self.path.exists():
            return []
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            return [Task.from_dict(item) for item in raw]
        except (OSError, ValueError, KeyError, TypeError) as exc:
            raise StorageError(f"Could not read {self.path}: {exc}") from exc

    def save(self, tasks: list[Task]) -> None:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            data = json.dumps([t.to_dict() for t in tasks], indent=2)
            tmp = self.path.with_suffix(".tmp")
            tmp.write_text(data, encoding="utf-8")
            tmp.replace(self.path)
        except OSError as exc:
            raise StorageError(f"Could not write {self.path}: {exc}") from exc
