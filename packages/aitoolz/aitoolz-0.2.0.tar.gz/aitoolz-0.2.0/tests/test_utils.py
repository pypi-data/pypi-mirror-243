"""Tests for utility functions."""
from pytest import mark

from aitoolz.utils import is_valid_python_name


@mark.parametrize(
    ["name", "expected_result"],
    [
        ("1arg", False),
        ("arg-1", False),
        ("arg&1", False),
        ("arg1", True),
        ("arg_1", True),
        ("arg", True),
    ],
)
def test_is_valid_python_name(name: str, expected_result: bool):
    assert is_valid_python_name(name) == expected_result
