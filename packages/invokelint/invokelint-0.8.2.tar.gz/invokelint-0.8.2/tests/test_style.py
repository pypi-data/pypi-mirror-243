"""Tests for `style` package."""

from typing import TYPE_CHECKING

from invokelint.style import fmt
from tests.testlibraries import check_list_result

if TYPE_CHECKING:
    from invoke import Context

PYTHON_DIR = "invokelint setup.py tasks.py tests"

LIST_COMMAND_EXPECTED_STYLE_WITHOUT_RUFF = [
    f"docformatter --recursive --in-place {PYTHON_DIR}",
    f"isort {PYTHON_DIR}",
    f"autoflake --recursive --in-place {PYTHON_DIR}",
    f"black {PYTHON_DIR}",
]
LIST_COMMAND_EXPECTED_STYLE = [
    *LIST_COMMAND_EXPECTED_STYLE_WITHOUT_RUFF,
    "ruff --fix --show-fixes --ignore S101 tests",
]
LIST_COMMAND_EXPECTED_STYLE_CHECK = [
    f"docformatter --recursive --check {PYTHON_DIR}",
    f"isort --check-only --diff {PYTHON_DIR}",
    f"autoflake --recursive --check {PYTHON_DIR}",
    f"black --check --diff {PYTHON_DIR}",
    "ruff --show-fixes --ignore S101 tests",
]


def test_style(context: "Context") -> None:
    """Command should success and run appropriate commands."""
    check_list_result(fmt(context), LIST_COMMAND_EXPECTED_STYLE)


def test_style_check(context: "Context") -> None:
    """Command should success and run appropriate commands."""
    check_list_result(fmt(context, check=True), LIST_COMMAND_EXPECTED_STYLE_CHECK)


def test_style_ruff(context: "Context") -> None:
    """Command should success and run appropriate commands."""
    check_list_result(fmt(context, ruff=True), LIST_COMMAND_EXPECTED_STYLE_WITHOUT_RUFF)
