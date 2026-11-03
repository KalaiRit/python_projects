# pycalc

[![CI](https://github.com/KalaiRit/pycalc/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/pycalc/actions)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A simple, well-tested command-line calculator written in Python.

## Features

- Add, subtract, multiply, divide, power and modulo
- Clear error messages and proper exit codes
- Clean separation between logic (`calculator.py`) and interface (`cli.py`)
- Fully tested with `pytest`, linted with `ruff`, CI on GitHub Actions

## Installation

```bash
git clone https://github.com/KalaiRit/pycalc.git
cd pycalc
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Usage

```bash
calc add 6 3          # 9
calc divide 1 4       # 0.25
calc power 2 10       # 1024
calc divide 5 0       # Error: Cannot divide by zero.  (exit code 1)

python -m pycalc multiply 7 6   # 42
calc --help
```

Use it as a library:

```python
from pycalc import Calculator

Calculator().calculate("add", 6, 3)  # 9
```

## Project structure

```
pycalc/
├── src/pycalc/
│   ├── __init__.py
│   ├── __main__.py       # python -m pycalc
│   ├── calculator.py     # pure arithmetic logic
│   ├── cli.py            # argument parsing and output
│   └── errors.py         # custom exceptions
├── tests/
│   ├── test_calculator.py
│   └── test_cli.py
├── .github/workflows/ci.yml
├── pyproject.toml
└── README.md
```

## Architecture

- **cli.py** parses arguments, calls the calculator, prints the result or error, and returns an exit code.
- **calculator.py** holds all math. It does no I/O, so it is trivial to test and reuse.
- **errors.py** defines `CalculatorError` and its subclasses, so callers can catch errors precisely.

## Development

```bash
pytest --cov=pycalc    # run tests with coverage
ruff check .           # lint
```

## License

MIT, see [LICENSE](LICENSE).
