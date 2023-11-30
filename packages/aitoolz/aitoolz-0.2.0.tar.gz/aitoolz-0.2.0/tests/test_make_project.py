"""Tests for the make_project.py module."""
import os
import shutil
from collections.abc import Iterable
from pathlib import Path
from subprocess import CalledProcessError, run

from pytest import fixture, mark, raises

from aitoolz.make_project import create_python_pkg_project


@fixture(scope="module")
def test_project_name() -> str:
    return "my_new_project"


@fixture(scope="module")
def setup_and_teardown(test_project_name: str) -> Iterable[None]:
    try:
        create_python_pkg_project(test_project_name)
        yield None
    except Exception as e:
        raise e
    finally:
        shutil.rmtree(test_project_name, ignore_errors=True)


@mark.usefixtures("setup_and_teardown")
def test_create_python_pkg_project_creates_buildable_package_that_passes_tests(
    test_project_name: str,
):
    try:
        run(["nox", "-s", "run_tests"], check=True, cwd=test_project_name)
        assert True
    except CalledProcessError:
        assert False


@mark.usefixtures("setup_and_teardown")
def test_create_python_pkg_project_configured_static_code_checks_that_pass(
    test_project_name: str,
):
    try:
        run(["nox", "-s", "check_code_formatting"], check=True, cwd=test_project_name)
        assert True
    except CalledProcessError:
        assert False


@mark.usefixtures("setup_and_teardown")
def test_create_python_pkg_project_raises_exception_with_invalid_pkg_name(
    test_project_name: str,
):
    with raises(ValueError, match="not a valid Python object name"):
        create_python_pkg_project(f"1{test_project_name}$")


@mark.usefixtures("setup_and_teardown")
def test_create_python_pkg_project_raises_exception_with_repeated_calls(
    test_project_name: str,
):
    with raises(RuntimeError, match="directory already exists"):
        create_python_pkg_project(test_project_name)


def test_create_python_pkg_project_creates_files_when_called_here_in_empty_dir():
    try:
        test_project_name = "foobar42"
        project_dir = Path.cwd() / test_project_name
        project_dir.mkdir()
        project_dir.joinpath(".git").mkdir()  # should ignore .git
        os.chdir(project_dir)
        create_python_pkg_project(test_project_name, here=True)
        pyproject_dot_toml = Path("pyproject.toml")
        assert pyproject_dot_toml.exists()
    except Exception:
        assert False
    finally:
        os.chdir(project_dir.parent)
        shutil.rmtree(project_dir, ignore_errors=True)


@mark.usefixtures("setup_and_teardown")
def test_create_python_pkg_project_raises_exception_when_called_here_in_non_empty_dir(
    test_project_name: str,
):
    with raises(RuntimeError, match="working directory must be empty"):
        create_python_pkg_project(test_project_name, here=True)


def test_cli_command():
    try:
        pkg_name = "foo"
        out = run(["mep", pkg_name], check=True)
        readme = Path(".") / pkg_name / "README.md"
        if out.returncode == 0 and readme.exists():
            assert True
        else:
            assert False
    except CalledProcessError:
        assert False
    finally:
        shutil.rmtree(pkg_name, ignore_errors=True)


def test_cli_command_handles_exceptions():
    out = run(["mep", "1foo"], capture_output=True, text=True)
    if out.returncode != 0 and "ERROR: 1foo is not a valid" in out.stdout:
        assert True
    else:
        assert False

    out = run(["mep", "foo", "--here"], capture_output=True, text=True)
    if out.returncode != 0 and "ERROR: current working directory must be" in out.stdout:
        assert True
    else:
        assert False
