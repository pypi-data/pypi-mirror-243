"""Tests for the find_imports.py module."""
from pathlib import Path
from subprocess import CalledProcessError, run

from pytest import mark, raises

from aitoolz.find_imports import (
    _extract_imports_from_py_file,
    _is_std_lib_pkg,
    find_imports,
)


@mark.parametrize(
    ["pkg_name", "expected_result"],
    [
        ("os", True),
        ("sys", True),
        ("numpy", False),
        ("pandas", False),
        ("aitoolz", False),
    ],
)
def test_is_std_lib_pkg(pkg_name: str, expected_result: bool):
    assert _is_std_lib_pkg(pkg_name) == expected_result


def test_extract_imports_from_py_file():
    test_module = Path("tests") / "resources" / "python_pkg" / "module_a.py"
    expected_imports = {"sys", "os", "unittest", "pytest", "math"}
    assert _extract_imports_from_py_file(test_module) == expected_imports

    test_module = Path("tests") / "resources" / "python_pkg" / "sub_pkg" / "module_b.py"
    expected_imports = {"sys", "pathlib", "icecream", "nox"}
    assert _extract_imports_from_py_file(test_module) == expected_imports


def test_find_imports_finds_all_imports_in_python_module():
    test_module = "tests/resources/python_pkg/module_a.py"
    assert set(find_imports(test_module)) == {"pytest"}


def test_find_imports_finds_all_imports_in_src_dir():
    src_dir = "tests/resources/python_pkg"
    assert set(find_imports(src_dir)) == {"pytest", "icecream", "nox"}


def test_find_import_raises_error_if_file_not_found():
    bad_src_dir = "tests/resources/foo"
    with raises(FileNotFoundError, match="can't find"):
        find_imports(bad_src_dir)


def test_cli_command():
    try:
        test_module = "tests/resources/python_pkg/module_a.py"
        out = run(
            ["find-imports", test_module], check=True, capture_output=True, text=True
        )
        if out.returncode == 0 and "pytest" in out.stdout:
            assert True
        else:
            assert False
    except CalledProcessError:
        assert False


def test_cli_command_handles_exceptions():
    out = run(["find-imports", "does_not_exist"], capture_output=True, text=True)
    if out.returncode != 0 and "ERROR: can't find" in out.stdout:
        assert True
    else:
        assert False
