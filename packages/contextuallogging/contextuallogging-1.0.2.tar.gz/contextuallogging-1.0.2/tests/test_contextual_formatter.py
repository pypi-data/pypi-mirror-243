# Copyright 2023 Charles Andrews
"""Unit tests for contextuallogging._contextual_formatter."""

from __future__ import annotations  # noqa: I001

import logging
from logging import LogRecord
from typing import TYPE_CHECKING, Final

import pytest
from assertpy import assert_that

from contextuallogging import ContextualFormatter, reset_context, set_context_key

if TYPE_CHECKING:
    from contextvars import Token


class TestContextualFormatter:
    """Unit tests for contextuallogging.ContextualFormatter."""

    @staticmethod
    @pytest.fixture()
    def contextual_formatter() -> ContextualFormatter:
        """Constructs a ContextualFormatter.

        Returns:
            ContextualFormatter: The ContextualFormatter.
        """
        return ContextualFormatter()

    @staticmethod
    @pytest.mark.parametrize(
        ("record", "context", "expected"),
        [
            (
                LogRecord(
                    name="name",
                    level=logging.INFO,
                    pathname="pathname",
                    lineno=0,
                    msg="msg",
                    args=None,
                    exc_info=None,
                ),
                {},
                '{"level": "INFO", "logger": "name", "message": "msg", "timestamp": '
                '"2023-11-18T08:21:14.722896Z"}',
            ),
            (
                LogRecord(
                    name="name",
                    level=logging.INFO,
                    pathname="pathname",
                    lineno=0,
                    msg="%s",
                    args=("message",),
                    exc_info=None,
                ),
                {},
                '{"level": "INFO", "logger": "name", "message": "message", '
                '"timestamp": "2023-11-18T08:21:14.722896Z"}',
            ),
            (
                LogRecord(
                    name="name",
                    level=logging.INFO,
                    pathname="pathname",
                    lineno=0,
                    msg="msg\n",
                    args=None,
                    exc_info=None,
                ),
                {},
                '{"level": "INFO", "logger": "name", "message": "msg\\n", '
                '"timestamp": "2023-11-18T08:21:14.722896Z"}',
            ),
            (
                LogRecord(
                    name="name",
                    level=logging.INFO,
                    pathname="pathname",
                    lineno=0,
                    msg="msg",
                    args=None,
                    exc_info=(RuntimeError, RuntimeError(), None),
                ),
                {},
                '{"exception": null, "level": "INFO", "logger": "name", "message": '
                '"msg", "timestamp": "2023-11-18T08:21:14.722896Z"}',
            ),
            (
                LogRecord(
                    name="name",
                    level=logging.INFO,
                    pathname="pathname",
                    lineno=0,
                    msg="msg",
                    args=None,
                    exc_info=None,
                    sinfo="sinfo",
                ),
                {},
                '{"level": "INFO", "logger": "name", "message": "msg", "stack": '
                '"sinfo", "timestamp": "2023-11-18T08:21:14.722896Z"}',
            ),
            (
                LogRecord(
                    name="name",
                    level=logging.INFO,
                    pathname="pathname",
                    lineno=0,
                    msg="msg",
                    args=None,
                    exc_info=None,
                ),
                {"key": "value"},
                '{"key": "value", "level": "INFO", "logger": "name", "message": '
                '"msg", "timestamp": "2023-11-18T08:21:14.722896Z"}',
            ),
        ],
    )
    def test_format(
        contextual_formatter: ContextualFormatter,
        record: LogRecord,
        context: dict[str, object],
        expected: str,
    ) -> None:
        """Tests happy path cases of ContextualFormatter.format().

        Args:
            contextual_formatter (ContextualFormatter): The ContextualFormatter.
            record (LogRecord): The LogRecord to format.
            context (dict[str, object]): The logging context.
            expected (str): The expected formatted LogRecord.
        """
        tokens: Final[list[Token[dict[str, object]]]] = []
        for key, value in context.items():
            set_context_key(key=key, value=value)
        record.created = 1700295674.722896
        assert_that(contextual_formatter.format(record=record)).is_equal_to(
            expected,
        )
        while len(tokens) > 0:
            reset_context(token=tokens.pop())
