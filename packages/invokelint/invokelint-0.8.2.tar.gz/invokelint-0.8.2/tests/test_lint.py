"""Tests for `lint` package."""
import platform
import sys
from typing import TYPE_CHECKING

import pytest

from invokelint.lint import (
    bandit,
    cohesion,
    deep,
    dodgy,
    fast,
    flake8,
    mypy,
    pydocstyle,
    pylint,
    radon,
    radon_cc,
    radon_mi,
    ruff_task,
    semgrep,
    xenon,
)
from tests.test_style import LIST_COMMAND_EXPECTED_STYLE, LIST_COMMAND_EXPECTED_STYLE_WITHOUT_RUFF
from tests.testlibraries import check_list_result, check_result

if TYPE_CHECKING:
    from invoke import Context

PYTHON_DIR = "invokelint setup.py tasks.py tests"
TEST_DIR = "tests"
COMMAND_EXPECTED_RADON_CC = f"radon cc {PYTHON_DIR}"
COMMAND_EXPECTED_RADON_MI = f"radon mi {PYTHON_DIR}"
COMMAND_EXPECTED_RUFF = f"ruff --ignore S101 {TEST_DIR}"
COMMAND_EXPECTED_BANDIT = "bandit --recursive --skip B101 tests"
COMMAND_EXPECTED_DODGY = "dodgy --ignore-paths csvinput"
COMMAND_EXPECTED_FLAKE8 = f"flake8 --radon-show-closures {PYTHON_DIR}"
COMMAND_EXPECTED_PYDOCSTYLE = f"pydocstyle {PYTHON_DIR}"
COMMAND_EXPECTED_XENON = f"xenon --max-absolute A --max-modules A --max-average A {PYTHON_DIR}"
COMMAND_EXPECTED_MYPY = f"mypy {PYTHON_DIR}"
COMMAND_EXPECTED_PYLINT = f"pylint {PYTHON_DIR}"
COMMAND_EXPECTED_SEMGREP = (
    f"semgrep scan --oss-only --config auto {' '.join([f'--include {code}' for code in PYTHON_DIR.split(' ')])}"
)


def test_radon_cc(context: "Context") -> None:
    check_result(radon_cc(context), COMMAND_EXPECTED_RADON_CC)


def test_radon_mi(context: "Context") -> None:
    check_result(radon_mi(context), COMMAND_EXPECTED_RADON_MI)


def test_radon(context: "Context") -> None:
    list_command_expected = [COMMAND_EXPECTED_RADON_CC, COMMAND_EXPECTED_RADON_MI]
    list_result = radon(context)
    check_list_result(list_result, list_command_expected)


def test_cohesion(context: "Context") -> None:
    """Function: cohesion() should run appropriate commands."""
    list_command_expected = [
        "cohesion --directory invokelint",
        "cohesion --directory setup.py",
        "cohesion --directory tasks.py",
        "cohesion --directory tests",
    ]
    list_result = cohesion(context)
    check_list_result(list_result, list_command_expected)


def test_ruff(context: "Context") -> None:
    check_result(ruff_task(context), COMMAND_EXPECTED_RUFF)


def test_bandit(context: "Context") -> None:
    check_result(bandit(context), COMMAND_EXPECTED_BANDIT)


def test_dodgy(context: "Context") -> None:
    check_result(dodgy(context), COMMAND_EXPECTED_DODGY)


def test_flake8(context: "Context") -> None:
    check_result(flake8(context), COMMAND_EXPECTED_FLAKE8)


def test_pydocstyle(context: "Context") -> None:
    check_result(pydocstyle(context), COMMAND_EXPECTED_PYDOCSTYLE)


def test_xenon(context: "Context") -> None:
    check_result(xenon(context), COMMAND_EXPECTED_XENON)


LIST_COMMAND_EXPECTED = [
    COMMAND_EXPECTED_XENON,
    COMMAND_EXPECTED_RUFF,
    COMMAND_EXPECTED_BANDIT,
    COMMAND_EXPECTED_DODGY,
    COMMAND_EXPECTED_FLAKE8,
    COMMAND_EXPECTED_PYDOCSTYLE,
]


def test_fast(context: "Context") -> None:
    """Command should success and run appropriate commands."""
    list_result = fast(context)
    check_list_result(list_result, LIST_COMMAND_EXPECTED_STYLE + LIST_COMMAND_EXPECTED)


def test_fast_ruff(context: "Context") -> None:
    """Command should success and run appropriate commands."""
    list_result = fast(context, ruff=True)
    check_list_result(list_result, LIST_COMMAND_EXPECTED_STYLE_WITHOUT_RUFF + LIST_COMMAND_EXPECTED)


def test_fast_skip_format(context: "Context") -> None:
    """Command should success and run appropriate commands."""
    list_result = fast(context, skip_format=True)
    check_list_result(list_result, LIST_COMMAND_EXPECTED)


@pytest.mark.slow()
def test_mypy(context: "Context") -> None:
    check_result(mypy(context), COMMAND_EXPECTED_MYPY)


@pytest.mark.slow()
def test_pylint(context: "Context") -> None:
    check_result(pylint(context), COMMAND_EXPECTED_PYLINT)


@pytest.mark.slow()
# - semgrep does not work on windows 10 · Issue #4295 · returntocorp/semgrep
#   https://github.com/returntocorp/semgrep/issues/4295
# - No module found: resource (ModuleNotFoundError) · Issue #7146 · returntocorp/semgrep
#   https://github.com/returntocorp/semgrep/issues/7146
@pytest.mark.skipif(sys.platform == "win32", reason="Semgrep doesn't support Windows.")
def test_semgrep(context: "Context") -> None:
    """Command should success and run appropriate commands."""
    check_result(semgrep(context), COMMAND_EXPECTED_SEMGREP)


@pytest.mark.slow()
def test_deep(context: "Context") -> None:
    """Command should success and run appropriate commands."""
    list_command_expected = [COMMAND_EXPECTED_MYPY, COMMAND_EXPECTED_PYLINT]
    if platform.system() != "Windows":
        list_command_expected.append(COMMAND_EXPECTED_SEMGREP)
    list_result = deep(context)
    check_list_result(list_result, list_command_expected)
