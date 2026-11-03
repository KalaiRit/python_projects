"""Command-line interface for pycalc."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from pycalc import __version__
from pycalc.calculator import Calculator
from pycalc.errors import CalculatorError


def format_number(value: float) -> str:
    """Render whole numbers without a trailing ``.0``."""
    if value == int(value):
        return str(int(value))
    return f"{value:.10g}"


def build_parser(calculator: Calculator) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="calc",
        description="A simple command-line calculator.",
        epilog="Example: calc add 6 3",
    )
    parser.add_argument(
        "operation",
        help=f"one of: {', '.join(calculator.operations)}",
    )
    parser.add_argument("a", type=float, help="first number")
    parser.add_argument("b", type=float, help="second number")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point. Returns a process exit code (0 on success, 1 on error)."""
    calculator = Calculator()
    args = build_parser(calculator).parse_args(argv)

    try:
        result = calculator.calculate(args.operation, args.a, args.b)
    except CalculatorError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(format_number(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
