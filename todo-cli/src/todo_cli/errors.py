"""Custom exceptions for todo-cli."""


class TodoError(Exception):
    """Base class for all todo-cli errors."""


class TaskNotFoundError(TodoError):
    """Raised when a task id does not exist."""

    def __init__(self, task_id: int) -> None:
        self.task_id = task_id
        super().__init__(f"Task {task_id} not found.")


class EmptyTitleError(TodoError):
    """Raised when a task title is blank."""

    def __init__(self) -> None:
        super().__init__("Task title cannot be empty.")


class StorageError(TodoError):
    """Raised when the task file cannot be read or written."""
