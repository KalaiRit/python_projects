"""Command-line interface for todo-cli."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from todo_cli import __version__
from todo_cli.errors import TodoError
from todo_cli.service import TodoList
from todo_cli.storage import DEFAULT_PATH, JsonStorage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="todo", description="A simple command-line to-do list.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument(
        "--file", type=Path, default=DEFAULT_PATH, help=f"task file (default: {DEFAULT_PATH})"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="add a task")
    add.add_argument("title", nargs="+", help="task title")

    lst = sub.add_parser("list", help="list tasks")
    lst.add_argument("--pending", action="store_true", help="hide completed tasks")

    done = sub.add_parser("done", help="mark a task as done")
    done.add_argument("id", type=int)

    rm = sub.add_parser("remove", help="delete a task")
    rm.add_argument("id", type=int)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point. Returns 0 on success, 1 on a handled error."""
    args = build_parser().parse_args(argv)
    try:
        todos = TodoList(JsonStorage(args.file))
        if args.command == "add":
            task = todos.add(" ".join(args.title))
            print(f"Added #{task.id}: {task.title}")
        elif args.command == "list":
            tasks = todos.list(show_done=not args.pending)
            if not tasks:
                print("No tasks.")
            for t in tasks:
                print(f"[{'x' if t.done else ' '}] {t.id}. {t.title}")
        elif args.command == "done":
            task = todos.complete(args.id)
            print(f"Completed #{task.id}: {task.title}")
        elif args.command == "remove":
            task = todos.remove(args.id)
            print(f"Removed #{task.id}: {task.title}")
    except TodoError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
