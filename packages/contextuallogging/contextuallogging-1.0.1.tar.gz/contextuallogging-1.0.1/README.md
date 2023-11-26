# contextuallogging
[![Build Status](https://github.com/cfandrews/PythonContextualLogging/actions/workflows/build.yml/badge.svg)](https://github.com/cfandrews/PythonContextualLogging/actions)
[![Documentation Status](https://github.com/cfandrews/PythonContextualLogging/actions/workflows/documentation.yml/badge.svg)](https://github.com/cfandrews/PythonContextualLogging/actions)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Linting: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Pure-Python semantic logging library with context-local values.

[Source](https://github.com/cfandrews/PythonContextualLogging/)  
[Documentation](https://cfandrews.github.io/PythonContextualLogging/contextuallogging.html)

## Basic Usage
This packages introduces two primary components:
1. The [`ContextualFormatter`](https://cfandrews.github.io/PythonContextualLogging/contextuallogging.html#ContextualFormatter)
logging formatter subclass.
2. The [`@context`](https://cfandrews.github.io/PythonContextualLogging/contextuallogging.html#context) decorator.

This is a basic example:
```python
import sys
import logging
from contextuallogging import context, ContextualFormatter

logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(ContextualFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

@context(keyword="username", key="user")
def inner_function(username: str) -> None:
    logger.info("inner_function")

@context(keyword="request_id")
def outer_function(request_id: str) -> None:
    logger.info("outer_function")
    inner_function(username="cfandrews")
    logger.info("outer_function again")

outer_function(request_id="7fb9b341")
```
Which will output:
```json lines
{"level": "INFO", "logger": "root", "message": "outer_function", "request_id": "7fb9b341", "timestamp": "2023-11-25T20:56:41.796564Z"}
{"level": "INFO", "logger": "root", "message": "inner_function", "request_id": "7fb9b341", "timestamp": "2023-11-25T20:56:41.797024Z", "user": "cfandrews"}
{"level": "INFO", "logger": "root", "message": "outer_function again", "request_id": "7fb9b341", "timestamp": "2023-11-25T20:56:41.797075Z"}
```

### ContextualFormatter
The [`ContextualFormatter`](https://cfandrews.github.io/PythonContextualLogging/contextuallogging.html#ContextualFormatter)
is a subclass of `logging.Formatter` and can be used in the exact same way as any other logging formatter. This class
formats log messages as JSON blobs and includes a number of fields by default, such as an [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)
timestamp in the UTC timezone, log level, logger name, and message. Logging context is added to the output JSON blob as
additional fields mixed into the base log.

### @context
The [`@context`](https://cfandrews.github.io/PythonContextualLogging/contextuallogging.html#context) decorator adds
fields to the logging context from the keyword arguments passed into the wrapped function. The logging context persists
for the entire function call and is automatically reset after the function returns, creating a stack-like structure in
which context is persisted down the call stack but not back up.
