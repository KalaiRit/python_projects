"""Business rules for managing tasks. No printing, no argument parsing."""

from __future__ import annotations

from todo_cli.errors import EmptyTitleError, TaskNotFoundError
from todo_cli.models import Task
from todo_cli.storage import JsonStorage


class TodoList:
    def __init__(self, storage: JsonStorage) -> None:
        self._storage = storage
        self._tasks = storage.load()

    def list(self, show_done: bool = True) -> list[Task]:
        if show_done:
            return list(self._tasks)
        return [t for t in self._tasks if not t.done]

    def add(self, title: str) -> Task:
        title = title.strip()
        if not title:
            raise EmptyTitleError()
        next_id = max((t.id for t in self._tasks), default=0) + 1
        task = Task(id=next_id, title=title)
        self._tasks.append(task)
        self._storage.save(self._tasks)
        return task

    def complete(self, task_id: int) -> Task:
        task = self._find(task_id)
        task.done = True
        self._storage.save(self._tasks)
        return task

    def remove(self, task_id: int) -> Task:
        task = self._find(task_id)
        self._tasks.remove(task)
        self._storage.save(self._tasks)
        return task

    def _find(self, task_id: int) -> Task:
        for task in self._tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundError(task_id)
