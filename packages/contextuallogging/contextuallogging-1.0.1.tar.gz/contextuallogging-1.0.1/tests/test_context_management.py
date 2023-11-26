# Copyright 2023 Charles Andrews
"""Unit tests for contextuallogging._context_management."""

from __future__ import annotations  # noqa: I001

import uuid
from contextvars import Token
from typing import Final

import pytest
from assertpy import assert_that

from contextuallogging import get_context, reset_context, set_context_key


@pytest.mark.parametrize(
    "context",
    [{}, {"key": "value"}, {"foo": "bar", "baz": "qux"}],
)
def test_get_context(context: dict[str, object]) -> None:
    """Tests happy path cases of get_context().

    Args:
        context (context: dict[str, object]): The context to set and to expect.
    """
    tokens: Final[list[Token[dict[str, object]]]] = []
    for key, value in context.items():
        tokens.append(set_context_key(key=key, value=value))
    assert_that(get_context()).is_equal_to(context)
    while len(tokens) > 0:
        reset_context(token=tokens.pop())


@pytest.mark.parametrize(
    ("key", "value"),
    [("key", "value"), ("request_id", uuid.uuid4())],
)
def test_set_context_key(key: str, value: object) -> None:
    """Tests happy path cases of set_context_key().

    Args:
        key (str): The context key to set.
        value (object): The value to assign to the context key.
    """
    token: Final[Token[dict[str, object]]] = set_context_key(key=key, value=value)
    assert_that(token.old_value).is_equal_to(Token.MISSING)
    assert_that(get_context()).is_equal_to({key: value})
    reset_context(token=token)


def test_reset_context() -> None:
    """Tests happy path cases of reset_context()."""
    token: Final[Token[dict[str, object]]] = set_context_key(key="key", value="value")
    reset_context(token=token)
    assert_that(get_context()).is_equal_to({})
