"""Core arithmetic logic. Pure functions, no I/O."""

from __future__ import annotations

from typing import Callable

from pycalc.errors import DivisionByZeroError, UnknownOperationError

Number = float


class Calculator:
    """A small calculator supporting the four basic operations plus power and modulo."""

    def __init__(self) -> None:
        self._operations: dict[str, Callable[[Number, Number], Number]] = {
            "add": self.add,
            "subtract": self.subtract,
            "multiply": self.multiply,
            "divide": self.divide,
            "power": self.power,
            "modulo": self.modulo,
        }

    @property
    def operations(self) -> list[str]:
        """Names of all supported operations."""
        return sorted(self._operations)

    @staticmethod
    def add(a: Number, b: Number) -> Number:
        return a + b

    @staticmethod
    def subtract(a: Number, b: Number) -> Number:
        return a - b

    @staticmethod
    def multiply(a: Number, b: Number) -> Number:
        return a * b

    @staticmethod
    def divide(a: Number, b: Number) -> Number:
        if b == 0:
            raise DivisionByZeroError()
        return a / b

    @staticmethod
    def power(a: Number, b: Number) -> Number:
        return a**b

    @staticmethod
    def modulo(a: Number, b: Number) -> Number:
        if b == 0:
            raise DivisionByZeroError()
        return a % b

    def calculate(self, operation: str, a: Number, b: Number) -> Number:
        """Run a named operation on two numbers.

        Raises:
            UnknownOperationError: if ``operation`` is not supported.
            DivisionByZeroError: for divide/modulo by zero.
        """
        try:
            func = self._operations[operation.lower()]
        except KeyError:
            raise UnknownOperationError(operation, self.operations) from None
        return func(a, b)
