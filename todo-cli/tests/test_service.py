import pytest

from todo_cli.errors import EmptyTitleError, StorageError, TaskNotFoundError
from todo_cli.service import TodoList
from todo_cli.storage import JsonStorage


@pytest.fixture
def path(tmp_path):
    return tmp_path / "tasks.json"


@pytest.fixture
def todos(path):
    return TodoList(JsonStorage(path))


def test_add_assigns_incrementing_ids(todos):
    assert todos.add("one").id == 1
    assert todos.add("two").id == 2


def test_add_strips_whitespace(todos):
    assert todos.add("  buy milk  ").title == "buy milk"


@pytest.mark.parametrize("title", ["", "   "])
def test_add_rejects_blank_title(todos, title):
    with pytest.raises(EmptyTitleError):
        todos.add(title)


def test_complete_marks_done(todos):
    task = todos.add("x")
    todos.complete(task.id)
    assert todos.list()[0].done is True


def test_pending_filter_hides_done(todos):
    a = todos.add("a")
    todos.add("b")
    todos.complete(a.id)
    assert [t.title for t in todos.list(show_done=False)] == ["b"]


def test_remove_deletes_task(todos):
    task = todos.add("x")
    todos.remove(task.id)
    assert todos.list() == []


def test_ids_are_not_reused_after_removing_last(todos):
    todos.add("a")
    b = todos.add("b")
    todos.remove(b.id)
    assert todos.add("c").id == 2


@pytest.mark.parametrize("method", ["complete", "remove"])
def test_unknown_id_raises(todos, method):
    with pytest.raises(TaskNotFoundError):
        getattr(todos, method)(99)


def test_tasks_persist_between_instances(path):
    TodoList(JsonStorage(path)).add("keep me")
    assert [t.title for t in TodoList(JsonStorage(path)).list()] == ["keep me"]


def test_corrupt_file_raises_storage_error(path):
    path.write_text("not json", encoding="utf-8")
    with pytest.raises(StorageError):
        TodoList(JsonStorage(path))
