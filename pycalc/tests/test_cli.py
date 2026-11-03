import pytest

from pycalc.cli import format_number, main


def test_success_prints_result_and_exits_zero(capsys):
    assert main(["add", "6", "3"]) == 0
    assert capsys.readouterr().out.strip() == "9"


def test_decimal_result(capsys):
    assert main(["divide", "1", "4"]) == 0
    assert capsys.readouterr().out.strip() == "0.25"


def test_negative_numbers(capsys):
    assert main(["subtract", "3", "-4"]) == 0
    assert capsys.readouterr().out.strip() == "7"


def test_division_by_zero_exits_one(capsys):
    assert main(["divide", "1", "0"]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "divide by zero" in captured.err


def test_unknown_operation_exits_one(capsys):
    assert main(["sqrt", "4", "0"]) == 1
    assert "Unknown operation" in capsys.readouterr().err


def test_non_numeric_input_is_rejected_by_argparse():
    with pytest.raises(SystemExit) as exc_info:
        main(["add", "six", "3"])
    assert exc_info.value.code == 2


@pytest.mark.parametrize(
    ("value", "expected"),
    [(9.0, "9"), (0.25, "0.25"), (-3.0, "-3"), (1 / 3, "0.3333333333")],
)
def test_format_number(value, expected):
    assert format_number(value) == expected
