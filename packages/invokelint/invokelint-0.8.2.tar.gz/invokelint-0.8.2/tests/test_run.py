"""Tests for `run` package."""
import sys
from typing import cast, List, TYPE_CHECKING

from invoke import Context, Result, task, UnexpectedExit
import pytest

from invokelint.run import run_all

if TYPE_CHECKING:
    from pathlib import Path


@task
def fail(context: Context) -> Result:
    if sys.platform == "win32":
        return cast(Result, context.run("exit /b 1", pty=False))
    return cast(Result, context.run("exit 1"))


@task
def create_file(context: Context) -> Result:
    """Stub for testing run_all()."""
    file_name = "test.txt"
    if sys.platform == "win32":
        result = cast(Result, context.run("copy /b NUL {}".format(file_name), pty=False))
        context.run("dir", pty=False)
        return result
    return cast(Result, context.run("touch {}".format(file_name)))


@pytest.mark.skipif(sys.platform == "win32", reason="Code: context.cd() works only in Linux.")
def test_create_file_linux(tmp_path: "Path", context: Context) -> None:
    """see:

    - Changing directories between drives on Windows doesn't work · Issue #755 · pyinvoke/invoke
      https://github.com/pyinvoke/invoke/issues/755
    """
    with context.cd(str(tmp_path.resolve())):
        check_created_file(tmp_path, context)


@pytest.mark.skipif(sys.platform != "win32", reason="Code: context.cd() works only in Linux.")
def test_create_file_windows(tmp_path: "Path", context: Context) -> None:
    """see:

    - Changing directories between drives on Windows doesn't work · Issue #755 · pyinvoke/invoke
      https://github.com/pyinvoke/invoke/issues/755
    """
    with context.prefix("cd /d {}".format(str(tmp_path.resolve()))):
        check_created_file(tmp_path, context)


def check_created_file(tmp_path: "Path", context: Context) -> None:
    result = create_file(context)
    assert result.return_code == 0
    assert (tmp_path / "test.txt").exists()


@pytest.mark.skipif(sys.platform == "win32", reason="Code: context.cd() works only in Linux.")
def test_run_all_linux(tmp_path: "Path", context: Context) -> None:
    """All commands should be run even one of them failed.

    see:
    - Changing directories between drives on Windows doesn't work · Issue #755 · pyinvoke/invoke
      https://github.com/pyinvoke/invoke/issues/755
    """
    list_expected_message = ["Encountered a bad command exit code!", "Exit code: 1"]
    with context.cd(str(tmp_path.resolve())), pytest.raises(UnexpectedExit) as excinfo:
        run_all([fail, create_file], context)
    check_run_all(list_expected_message, excinfo.value, tmp_path)


@pytest.mark.skipif(sys.platform != "win32", reason="Code: context.cd() works only in Linux.")
def test_run_all_windows(tmp_path: "Path", context: Context) -> None:
    """All commands should be run even one of them failed.

    see:
    - Changing directories between drives on Windows doesn't work · Issue #755 · pyinvoke/invoke
      https://github.com/pyinvoke/invoke/issues/755
    """
    list_expected_message = ["Encountered a bad command exit code!", "Exit code: 1"]
    with context.prefix("cd /d {}".format(str(tmp_path.resolve()))), pytest.raises(UnexpectedExit) as excinfo:
        run_all([fail, create_file], context)
    check_run_all(list_expected_message, excinfo.value, tmp_path)


def check_run_all(list_expected_message: List[str], error: UnexpectedExit, tmp_path: "Path") -> None:
    for expected_message in list_expected_message:
        assert expected_message in str(error)
    assert (tmp_path / "test.txt").exists()
