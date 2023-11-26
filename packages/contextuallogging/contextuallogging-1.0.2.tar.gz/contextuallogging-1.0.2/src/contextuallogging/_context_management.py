# Copyright 2023 Charles Andrews
"""Contains utility functions for managing the logging context."""

from __future__ import annotations

from contextvars import ContextVar, Token
from typing import Final

_context: Final[ContextVar[dict[str, object]]] = ContextVar(
    "_contextuallogging__context",
    default={},
)


def get_context() -> dict[str, object]:
    """Gets the current logging context.

    This is an advanced utility function which is not necessary for most use-cases.

    Example usage:

    >>> from contextuallogging import get_context, set_context_key
    >>> get_context()
    {}
    >>> _ = set_context_key(key="key", value="value")
    >>> get_context()
    {'key': 'value'}

    Returns:
        dict[str, object]: The current logging context.
    """
    return _context.get()


def set_context_key(key: str, value: object) -> Token[dict[str, object]]:
    """Set the given key-value pair in the logging context.

    This is an advanced utility function which is not necessary for most use-cases.

    The returned `contextvars.Token` object can be passed to `reset_context` to reset
    the logging context to its state as it was prior to this operation.

    Example usage:

    >>> from contextuallogging import get_context, set_context_key
    >>> get_context()
    {}
    >>> _ = set_context_key(key="key", value="value")
    >>> get_context()
    {'key': 'value'}

    Args:
        key (str): The key of the logging field.
        value (object): The value of the logging field.

    Returns:
        Token[dict[str, object]]: The Token required to reset the logging context to the
            previous state.
    """
    return _context.set({**get_context(), key: value})


def reset_context(token: Token[dict[str, object]]) -> None:
    """Reset the logging context with the given token.

    This is an advanced utility function which is not necessary for most use-cases.

    The given token should be obtained from a `set_context_key` call and should never be
    constructed from scratch manually.

    Example usage:

    >>> from contextuallogging import get_context, reset_context, set_context_key
    >>> get_context()
    {}
    >>> reset_token = set_context_key(key="key", value="value")
    >>> get_context()
    {'key': 'value'}
    >>> reset_context(token=reset_token)
    >>> get_context()
    {}

    Args:
        token (Token[dict[str, object]]): The reset Token.
    """
    _context.reset(token)
