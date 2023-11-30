"""Find all explicit external package imports within a Python file or module.

I.e., Find all imported packages that are not in the Python standard library.
"""
import argparse
import re
import sys
from importlib import metadata
from pathlib import Path

IMPORT_PKG_REGEX = r"^import\s(\w+)[\s\.]*.*$"
FROM_PKG_REGEX = r"^from\s(\w+)[\s\.].*import"


def _extract_imports_from_py_file(file: Path) -> set[str]:
    """Return all valid imports from a readable file."""
    code_lines = [line.strip() for line in file.read_text().split("\n")]
    import_pkg_imports = [
        re.findall(IMPORT_PKG_REGEX, line)
        for line in code_lines
        if line.startswith("import")
    ]
    from_pkg_imports = [
        re.findall(FROM_PKG_REGEX, line)
        for line in code_lines
        if line.startswith("from")
    ]
    distinct_imports = {
        pkg
        for imports in from_pkg_imports + import_pkg_imports
        for pkg in imports
        if isinstance(imports, list)
    }
    return distinct_imports


def _is_std_lib_pkg(pkg_name: str) -> bool:
    """Is the named package in the Python standard library."""

    def _fallback_test(pkg_name: str) -> bool:
        try:
            metadata.metadata(pkg_name)
            return False
        except metadata.PackageNotFoundError:
            return True

    try:
        pkg = __import__(pkg_name)
    except ModuleNotFoundError:
        return False
    if hasattr(pkg, "__file__"):
        if pkg.__file__ is None:
            return _fallback_test(pkg_name)
        if re.search(f"site-packages/{pkg_name}", pkg.__file__):
            return False
        elif re.search(r"lib/python3.\d+/", pkg.__file__):
            return True
        else:
            return False
    else:
        return _fallback_test(pkg_name)


def find_imports(module_path: str) -> list[str]:
    """Find all explicit external package imports in a Python module.

    Args:
    ----
        module_path: The file or directory to search in.

    Raises:
    ------
        FileNotFoundError: If the file or directory cannot be found.

    Returns:
    -------
        A list of package names.
    """
    module = Path(module_path)
    if not module.exists():
        raise FileNotFoundError(f"can't find {module_path}")
    if module.is_dir():
        py_files = list(Path(module_path).glob("**/*.py"))
    else:
        py_files = [module]
    distinct_imports = {
        imports
        for py_file in py_files
        for imports in _extract_imports_from_py_file(py_file)
        if not _is_std_lib_pkg(imports) and imports != module.name
    }
    return list(distinct_imports)


def _cli() -> None:
    """Entrypoint for use on the CLI."""
    parser = argparse.ArgumentParser(
        description="Find all explicit imports not in the Python standard library"
    )
    parser.add_argument(
        "src_dir_or_file",
        type=str,
        help="to search for imports",
    )
    args = parser.parse_args()

    try:
        imports = find_imports(args.src_dir_or_file)
        if imports is not None:
            for dependency in imports:
                print(dependency)
        sys.exit(0)
    except FileNotFoundError as e:
        e_msg = str(e)
        print(f"ERROR: {e_msg[:1].lower() + e_msg[1:]}")
        sys.exit(1)
