"""pycalc: a simple, well-tested command-line calculator."""

from pycalc.calculator import Calculator
from pycalc.errors import CalculatorError, DivisionByZeroError, UnknownOperationError

__version__ = "0.1.0"

__all__ = [
    "Calculator",
    "CalculatorError",
    "DivisionByZeroError",
    "UnknownOperationError",
    "__version__",
]
