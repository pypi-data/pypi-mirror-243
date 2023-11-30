"""Create a skeleton Python package project ready for development."""
import argparse
import sys
from importlib.resources import files
from pathlib import Path
from string import Template
from typing import cast

from aitoolz.utils import is_valid_python_name

PROJECT_DIRS: tuple[str, ...] = (
    "src",
    "src/${pkg_name}",
    "tests",
    ".github",
    ".github/workflows",
)

FILE_TEMPLATES_AND_TARGET_DIRS: dict[str, str] = {
    "README.md": ".",
    "pyproject.toml": ".",
    "noxfile.py": ".",
    "__init__.py": "src/${pkg_name}",
    "hello_world.py": "src/${pkg_name}",
    "py.typed": "src/${pkg_name}",
    "test_hello_world.py": "tests",
    "python-package-ci.yml": ".github/workflows",
    "python-package-cd.yml": ".github/workflows",
    ".gitignore": ".",
}


def _create_directory(
    path_template: str, template_values: dict[str, str], project_root: Path
) -> None:
    """Create directory.

    Args:
    ----
        path_template: Parent directory path templace.
        template_values: Values to use for rendering path_template.
        project_root: The ultimate parent directory.
    """
    parent_dir = project_root / Template(path_template).safe_substitute(template_values)
    parent_dir.mkdir()


def _create_from_template(
    template_filename: str,
    values: dict[str, str],
    parent_dir_template: str,
    project_root: Path,
) -> None:
    """Render template and save copy in parent directory.

    Args:
    ----
        template_filename: The template within `aitoolz.resources.templates`.
        values: The values to use for rendering the template.
        parent_dir_template: Directory in which to create the file, relative to
            project_root. Can contain templated variables for dynamic path creation.
        project_root: The project's ultimate root directory.

    Raises:
    ------
        FileNotFoundError: If template_filename or parent_dir can't be found.
    """
    template = files("aitoolz.resources.pkg_templates") / template_filename
    template = cast(Path, template)
    if not template.exists():
        raise FileNotFoundError(f"{template} does not exist")
    template_rendered = Template(template.read_text()).safe_substitute(values)

    parent_dir = Template(parent_dir_template).safe_substitute(values)
    new_file = project_root / parent_dir / template_filename
    if not new_file.parent.exists():
        raise FileNotFoundError(f"{new_file.parent} does not exist")
    new_file.write_text(template_rendered)


def create_python_pkg_project(pkg_name: str, here: bool | None = None) -> None:
    """Create a skeleton Python package project ready for development.

    Args:
    ----
        pkg_name: The package's name.
        here: Whether or not to create the package project file in the curret directory.

    Raises:
    ------
        RuntimeError: If `here` is `True` the current working directory is not empty.
        RuntimeError: If `here` is `False` and a directory named `pkg_name` exists in
            the current working directory.
        ValueError: If `pkg_name` is not a valid Python object name.
    """
    if not is_valid_python_name(pkg_name):
        raise ValueError(f"{pkg_name} is not a valid Python object name.")

    if here:
        project_root = Path.cwd()
        dir_contents = [e for e in project_root.glob("*") if e.name != ".git"]
        if dir_contents:
            msg = "Current working directory must be empty to create template project."
            raise RuntimeError(msg)
    else:
        project_root = Path(".") / pkg_name
        if project_root.exists():
            raise RuntimeError(f"{project_root} directory already exists.")
        project_root.mkdir()

    template_values = {"pkg_name": pkg_name}

    for dir in PROJECT_DIRS:
        _create_directory(dir, template_values, project_root)

    for template, target_dir in FILE_TEMPLATES_AND_TARGET_DIRS.items():
        _create_from_template(template, template_values, target_dir, project_root)


def _cli() -> None:
    """Entrypoint for use on the CLI."""
    parser = argparse.ArgumentParser(
        description="Create a Python package project ready for development"
    )
    parser.add_argument(
        "package_name",
        type=str,
        help="will be used throughout project files as well for the package",
    )
    parser.add_argument(
        "--here",
        action="store_true",
        help="create project in the current directory (must be empty)",
    )
    args = parser.parse_args()

    try:
        create_python_pkg_project(args.package_name, args.here)
        sys.exit(0)
    except (RuntimeError, ValueError) as e:
        e_msg = str(e)
        print(f"ERROR: {e_msg[:1].lower() + e_msg[1:]}")
        sys.exit(1)
