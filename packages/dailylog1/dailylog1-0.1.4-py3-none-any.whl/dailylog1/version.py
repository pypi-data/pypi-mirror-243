"""Top-level module cli for dailylog."""

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import tomli

VERSION = None

if VERSION is None:
    try:
        VERSION = version("dailylog")
    except PackageNotFoundError:
        pyproject = Path(__file__).resolve().parent.parent / "pyproject.toml"
        with open(pyproject, "rb") as tf:
            toml_dict = tomli.load(tf)
        VERSION = toml_dict["tool"]["poetry"]["version"]
