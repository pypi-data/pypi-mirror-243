# Copyright 2023 Charles Andrews
# fmt: off
"""[![Build Status](https://github.com/cfandrews/PythonContextualLogging/actions/workflows/build.yml/badge.svg)](https://github.com/cfandrews/PythonContextualLogging/actions)
[![Documentation Status](https://github.com/cfandrews/PythonContextualLogging/actions/workflows/documentation.yml/badge.svg)](https://github.com/cfandrews/PythonContextualLogging/actions)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Linting: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Pure-Python semantic logging library with context-local values.

[Source](https://github.com/cfandrews/PythonContextualLogging/)  
[Documentation](https://cfandrews.github.io/PythonContextualLogging/contextuallogging.html)
"""  # noqa: W291, D205, D415
# fmt: on

from __future__ import annotations

from typing import Final

from contextuallogging._context import context
from contextuallogging._context_management import (
    get_context,
    reset_context,
    set_context_key,
)
from contextuallogging._contextual_formatter import ContextualFormatter

__all__: Final[list[str]] = [
    "context",
    "ContextualFormatter",
    "get_context",
    "set_context_key",
    "reset_context",
]
__docformat__: Final[str] = "google"
