"""Custom exceptions raised by the calculator."""


class CalculatorError(Exception):
    """Base class for all calculator errors."""


class DivisionByZeroError(CalculatorError):
    """Raised when dividing (or taking a modulo) by zero."""

    def __init__(self) -> None:
        super().__init__("Cannot divide by zero.")


class UnknownOperationError(CalculatorError):
    """Raised when an unsupported operation name is requested."""

    def __init__(self, name: str, supported: list[str]) -> None:
        self.name = name
        self.supported = supported
        super().__init__(
            f"Unknown operation '{name}'. Supported operations: {', '.join(supported)}."
        )
