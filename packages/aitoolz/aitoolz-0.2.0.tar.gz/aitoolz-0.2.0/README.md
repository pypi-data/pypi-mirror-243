# aitoolz

Various Python tools, by Alex Ioannides (AI). Some of them might be useful for artificial intelligence, some of them might not.

## Installing

You can install aitoolz from PyPI using

```text
pip install aitoolz
```

Alternatively, you can install directly from the `main` branch of this repo via

```text
pip install git+https://github.com/alexioannides/aitoolz.git@main
```

Where the `@XXXX` component of the URI can be substituted for any branch, tag or commit hash. See the [pip docs](https://pip.pypa.io/en/stable/topics/vcs-support/#supported-vcs) for more info.

## Features

A brief overview of the core tools:

### Template Python Package Projects

The `aitoolz.make_project` module exposes the `create_python_pkg_project` function that can create empty Python package projects to speed-up development. This includes:

- Executable tests via PyTest.
- Fully configured code formatting and checking using Ruff and Black.
- Fully configured static type checking using MyPy.
- Dev task automation using Nox.
- Fully configured CICD using GitHub Actions.

This is an opinionated setup that reflects how I like to develop projects. This can also be called from the command line using the Make Empty Project (MEP) command - e.g.,

```text
mep my_package
```

Where `my_package` can be replaced with any valid Python module name. Either of these commands will create a directory structure and skeleton files,

```text
my_package
├── .github
│   └── workflows
│       ├── python-package-ci.yml
│       └── python-package-cd.yml
├── .gitignore
├── README.md
├── noxfile.py
├── pyproject.toml
├── src
│   └── my_package
│       ├── __init__.py
│       └── hello_world.py
└── tests
    └── test_hello_world.py
```

This has been tested to be installable and for all dev tasks automated with Nox to pass - use `nox --list` to see them all.

### Find External Dependencies in a Python Module or Source Folder

The `aitoolz.find_imports` module exposes the `find_imports` function that returns a list of all package dependencies imported into a Python module or source folder - i.e., all dependencies that are not in the Python standard library.

This can also be called from the command line - e.g.,

```text
find-imports src/my_package
```

Or,

```text
find-imports my_module.py
```
