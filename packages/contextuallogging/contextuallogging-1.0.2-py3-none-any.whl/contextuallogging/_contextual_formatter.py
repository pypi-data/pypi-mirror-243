# Copyright 2023 Charles Andrews
"""Contains the ContextualFormatter class."""

from __future__ import annotations

from datetime import datetime, timezone
from json import JSONEncoder
from logging import Formatter, LogRecord
from typing import Final

from contextuallogging._context_management import get_context


class ContextualFormatter(Formatter):
    """Logging Formatter which can impart contextual information onto a LogRecord.

    This class can be used in the same way as any regular logging formatter but will add
    any fields set by the contextual logging decorators.

    This class is opinionated on its format. Specifically, it outputs log messages as
    JSON key-value mappings and all logged objects must be encode-able by the provided
    JSON encoder.

    By default, the formatted logs will include the fields:
    * `timestamp`
    * `level`
    * `logger`
    * `message`
    * `exception`
     * If `exc_info` present on the LogRecord
    * `stack`
     * If `stack_info` present on the LogRecord

    Example usage:

    >>> import logging
    >>> import sys
    >>> from contextuallogging import ContextualFormatter
    >>>
    >>> logger = logging.getLogger()
    >>> handler = logging.StreamHandler(sys.stdout)
    >>> handler.setFormatter(ContextualFormatter())
    >>> logger.addHandler(handler)
    >>> logger.setLevel(logging.INFO)
    >>>
    >>> logger.info("Lorem ipsum dolor sit amet")
    {"level": "INFO", "logger": "root", "message": "Lorem ipsum dolor sit amet", "timestamp": "2023-11-25T22:25:42.803579Z"}
    """  # noqa: E501

    def __init__(
        self,
        encoder: JSONEncoder | None = None,
    ) -> None:
        """Constructor.

        The default encoder is instantiated as:

        ```python
        JSONEncoder(
            skipkeys=True,
            ensure_ascii=False,
            sort_keys=True,
        )
        ```

        Args:
            encoder (JSONEncoder | None): An optional JSONEncoder to use for formatting
                log messages.
        """
        self.__encoder: Final[JSONEncoder] = (
            JSONEncoder(skipkeys=True, ensure_ascii=False, sort_keys=True)
            if encoder is None
            else encoder
        )
        super().__init__()

    def format(self, record: LogRecord) -> str:  # noqa: A003
        """Format the given record as a string.

        Args:
            record (LogRecord): The LogRecord to format.

        Returns:
            str: The formatted LogRecord.
        """
        data: Final[dict[str, object]] = {}
        timestamp: Final[datetime] = datetime.fromtimestamp(
            record.created,
            tz=timezone.utc,
        )
        data["timestamp"] = (
            f"{timestamp.year:04}-{timestamp.month:02}-{timestamp.day:02}T"
            f"{timestamp.hour:02}:{timestamp.minute:02}:{timestamp.second:02}."
            f"{timestamp.microsecond:06}Z"
        )
        data["level"] = record.levelname
        data["logger"] = record.name
        data["message"] = record.getMessage()
        if record.exc_info is not None:
            data["exception"] = record.exc_text
        if record.stack_info is not None:
            data["stack"] = self.formatStack(stack_info=record.stack_info)
        return self.__encoder.encode({**data, **get_context()})
