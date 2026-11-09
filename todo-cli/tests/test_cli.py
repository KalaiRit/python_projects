import pytest

from todo_cli.cli import main


@pytest.fixture
def run(tmp_path, capsys):
    file = str(tmp_path / "tasks.json")

    def _run(*args):
        code = main(["--file", file, *args])
        captured = capsys.readouterr()
        return code, captured.out, captured.err

    return _run


def test_add_and_list(run):
    assert run("add", "buy", "milk")[:2] == (0, "Added #1: buy milk\n")
    code, out, _ = run("list")
    assert code == 0
    assert "[ ] 1. buy milk" in out


def test_done_shows_checkmark(run):
    run("add", "task")
    run("done", "1")
    assert "[x] 1. task" in run("list")[1]


def test_pending_hides_done(run):
    run("add", "a")
    run("add", "b")
    run("done", "1")
    out = run("list", "--pending")[1]
    assert "a" not in out.replace("Added", "") and "b" in out


def test_empty_list_message(run):
    assert run("list")[1].strip() == "No tasks."


def test_remove(run):
    run("add", "gone")
    assert run("remove", "1")[0] == 0
    assert run("list")[1].strip() == "No tasks."


def test_unknown_id_exits_one(run):
    code, out, err = run("done", "5")
    assert code == 1 and out == "" and "not found" in err


def test_blank_title_exits_one(run):
    code, _, err = run("add", " ")
    assert code == 1 and "empty" in err


def test_non_numeric_id_rejected_by_argparse(run):
    with pytest.raises(SystemExit) as exc_info:
        run("done", "abc")
    assert exc_info.value.code == 2
