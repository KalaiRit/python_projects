import pytest

from pycalc import Calculator, DivisionByZeroError, UnknownOperationError


@pytest.fixture
def calc() -> Calculator:
    return Calculator()


@pytest.mark.parametrize(
    ("operation", "a", "b", "expected"),
    [
        ("add", 6, 3, 9),
        ("subtract", 6, 3, 3),
        ("multiply", 6, 3, 18),
        ("divide", 6, 3, 2),
        ("power", 2, 10, 1024),
        ("modulo", 10, 3, 1),
        ("add", -2, -3, -5),
        ("multiply", 0.5, 4, 2),
    ],
)
def test_basic_operations(calc, operation, a, b, expected):
    assert calc.calculate(operation, a, b) == pytest.approx(expected)


def test_operation_names_are_case_insensitive(calc):
    assert calc.calculate("ADD", 1, 2) == 3


@pytest.mark.parametrize("operation", ["divide", "modulo"])
def test_division_by_zero_raises(calc, operation):
    with pytest.raises(DivisionByZeroError):
        calc.calculate(operation, 5, 0)


def test_unknown_operation_raises_with_supported_list(calc):
    with pytest.raises(UnknownOperationError) as exc_info:
        calc.calculate("sqrt", 4, 0)
    assert "sqrt" in str(exc_info.value)
    assert "add" in str(exc_info.value)


def test_operations_property_is_sorted(calc):
    assert calc.operations == sorted(calc.operations)
    assert {"add", "subtract", "multiply", "divide"} <= set(calc.operations)
