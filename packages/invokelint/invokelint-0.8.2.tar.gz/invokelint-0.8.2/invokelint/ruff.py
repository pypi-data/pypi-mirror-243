"""To unify executing ruff from style and from lint."""
from typing import TYPE_CHECKING

from invokelint.path import EXISTING_TEST_PACKAGES, PYTHON_DIRS_EXCLUDING_TEST
from invokelint.run import run_in_pty

if TYPE_CHECKING:
    from invoke import Context, Result


def execute(context: "Context", *, fix: bool = False, show_fixes: bool = False) -> "Result":
    """Lints code with Ruff."""
    list_options = []
    if fix:
        list_options.append("--fix")
    if show_fixes:
        list_options.append("--show-fixes")
    options = " " + " ".join(list_options) if list_options else ""
    run_in_pty(context, "ruff{} {}".format(options, " ".join(PYTHON_DIRS_EXCLUDING_TEST)))
    return run_in_pty(context, "ruff{} --ignore S101 {}".format(options, " ".join(EXISTING_TEST_PACKAGES)))
