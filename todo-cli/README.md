# todo-cli

A simple, well-tested command-line to-do list. Tasks are saved to a JSON file in your home folder.

## Features

- Add, list, complete and remove tasks
- Tasks persist between runs (`~/.todo-cli/tasks.json`, or any file via `--file`)
- Safe writes (temp file then rename) and clear error messages with exit codes
- Layered design: CLI, service logic and storage are separate and independently tested

## Installation

```bash
cd todo-cli
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Usage

```bash
todo add Buy milk
todo add "Write report"
todo list
todo done 1
todo list --pending
todo remove 2
todo --file ./my-tasks.json list
```

Example output:

```
[x] 1. Buy milk
[ ] 2. Write report
```

## Project structure

```
todo-cli/
├── src/todo_cli/
│   ├── cli.py        # argument parsing and printing
│   ├── service.py    # task rules (add, complete, remove)
│   ├── storage.py    # JSON read/write
│   ├── models.py     # Task dataclass
│   └── errors.py     # custom exceptions
├── tests/
├── pyproject.toml
└── README.md
```

## Development

```bash
pytest --cov=todo_cli
ruff check .
```

## License

MIT
