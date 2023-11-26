# Copyright 2023 Charles Andrews
"""Contains the @context decorator."""

from __future__ import annotations

import inspect
from functools import partial, wraps
from typing import TYPE_CHECKING, Any, Callable, Final

from contextuallogging._context_management import reset_context, set_context_key

if TYPE_CHECKING:
    from contextvars import Token


def context(
    function: Callable[..., Any] | None = None,
    /,
    *,
    keyword: str,
    key: str | None = None,
) -> Callable[..., Any]:
    """Decorator which adds logging context during a function call.

    The logging context is added prior to calling the wrapped function and is reset
    after the function returns, creating a stack-like context in which the context added
    here will propagate to all logging calls made in all sub-functions.

    Existing keys in the logging context will be overwritten by this decorator if they
    are already present, but the context will be reset to its original state once the
    wrapped function returns.

    This decorator supports decorating async functions, as well. As this package uses
    ContextVars behind-the-scenes, the logging context can be propagated to async
    function calls in some cases and follows the same rules as ContextVars as to when
    that happens.

    The created wrapper function raises a RuntimeError if the provided keyword name is
    not actually present in the passed-in kwargs.

    Example usage:

    >>> import sys
    >>> import logging
    >>> from contextuallogging import context, ContextualFormatter
    >>>
    >>> logger = logging.getLogger()
    >>> handler = logging.StreamHandler(sys.stdout)
    >>> handler.setFormatter(ContextualFormatter())
    >>> logger.addHandler(handler)
    >>> logger.setLevel(logging.INFO)
    >>>
    >>> @context(keyword="username", key="user")
    ... def inner_function(username: str) -> None:
    ...     logger.info("inner_function")
    ...
    >>> @context(keyword="request_id")
    ... def outer_function(request_id: str) -> None:
    ...     logger.info("outer_function")
    ...     inner_function(username="cfandrews")
    ...     logger.info("outer_function again")
    ...
    >>> outer_function(request_id="7fb9b341")
    {"level": "INFO", "logger": "root", "message": "outer_function", "request_id": "7fb9b341", "timestamp": "2023-11-25T20:56:41.796564Z"}
    {"level": "INFO", "logger": "root", "message": "inner_function", "request_id": "7fb9b341", "timestamp": "2023-11-25T20:56:41.797024Z", "user": "cfandrews"}
    {"level": "INFO", "logger": "root", "message": "outer_function again", "request_id": "7fb9b341", "timestamp": "2023-11-25T20:56:41.797075Z"}

    Args:
        function (Callable[..., Any]): The function wrapped by this decorator.
        keyword (str): The name of the keyword argument to add to the logging context.
        key (str | None): The key to use in the logging context.
    """  # noqa: E501
    if function is None:
        return partial(context, keyword=keyword, key=key)

    if inspect.iscoroutinefunction(function):

        @wraps(function)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
            if keyword not in kwargs:
                message: Final[str] = f"Keyword argument not provided: {keyword}"
                raise RuntimeError(message)
            token: Final[Token[dict[str, object]]] = set_context_key(
                key=keyword if key is None else key,
                value=kwargs[keyword],
            )
            result: Final[Any] = await function(*args, **kwargs)
            reset_context(token=token)
            return result

    else:

        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
            if keyword not in kwargs:
                message: Final[str] = f"Keyword argument not provided: {keyword}"
                raise RuntimeError(message)
            token: Final[Token[dict[str, object]]] = set_context_key(
                key=keyword if key is None else key,
                value=kwargs[keyword],
            )
            result: Final[Any] = function(*args, **kwargs)
            reset_context(token=token)
            return result

    return wrapper
