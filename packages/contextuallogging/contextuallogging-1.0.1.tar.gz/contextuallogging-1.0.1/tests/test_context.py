# Copyright 2023 Charles Andrews
"""Unit tests for contextuallogging._context."""

from __future__ import annotations  # noqa: I001

import asyncio
from typing import Any

import pytest
from assertpy import assert_that

from contextuallogging import context, get_context


@pytest.mark.parametrize(
    ("keyword", "key", "arguments", "expected"),
    [
        ("foo", None, {"foo": "bar"}, {"foo": "bar"}),
        ("foo", "key", {"foo": "bar"}, {"key": "bar"}),
        ("foo", None, {"foo": "bar", "baz": "quz"}, {"foo": "bar"}),
    ],
)
def test_context(
    keyword: str,
    key: str | None,
    arguments: dict[str, object],
    expected: dict[str, object],
) -> None:
    """Tests happy path cases of @context().

    Args:
        keyword (str): The keyword to pass to @context().
        key (str | None): The key to pass to @context().
        arguments (dict[str, object]): The keyword arguments to pass to the wrapped
            function.
        expected (dict[str, object]): The expected logging context.
    """

    @context(keyword=keyword, key=key)
    def function(**kwargs: Any) -> None:  # noqa: ARG001, ANN401
        assert_that(get_context()).is_equal_to(expected)

    @context(keyword=keyword, key=key)
    async def async_function(**kwargs: Any) -> None:  # noqa: ARG001, ANN401
        assert_that(get_context()).is_equal_to(expected)

    assert_that(get_context()).is_equal_to({})
    function(**arguments)
    assert_that(get_context()).is_equal_to({})
    asyncio.get_event_loop().run_until_complete(async_function(**arguments))
    assert_that(get_context()).is_equal_to({})


def test_context_runtime_error() -> None:
    """Tests RuntimeError cases of @context()."""

    @context(keyword="keyword")
    def function() -> None:
        pass

    @context(keyword="keyword")
    async def async_function() -> None:
        pass

    with pytest.raises(RuntimeError, match="Keyword argument not provided: keyword"):
        function()
    with pytest.raises(RuntimeError, match="Keyword argument not provided: keyword"):
        asyncio.get_event_loop().run_until_complete(async_function())
