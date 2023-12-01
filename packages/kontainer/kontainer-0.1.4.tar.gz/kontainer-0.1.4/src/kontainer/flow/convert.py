from __future__ import annotations

from typing import TYPE_CHECKING, Any, overload

from kontainer.core.exception import KontainerTypeError

if TYPE_CHECKING:
    from typing_extensions import TypeVar

    from kontainer.container import Maybe, Result

    ValueT = TypeVar("ValueT", infer_variance=True)

__all__ = ["toggle"]


@overload
def toggle(container: Result[ValueT, Any]) -> Maybe[ValueT]: ...


@overload
def toggle(container: Maybe[ValueT]) -> Result[ValueT, None]: ...


@overload
def toggle(
    container: Maybe[ValueT] | Result[ValueT, Any]
) -> Result[ValueT, None] | Maybe[ValueT]: ...


def toggle(
    container: Maybe[ValueT] | Result[ValueT, Any]
) -> Result[ValueT, None] | Maybe[ValueT]:
    from kontainer.container.maybe import Null, Some
    from kontainer.container.result import Done, Error

    if isinstance(container, Some):
        return Done(container.unwrap())
    if isinstance(container, Null):
        return Error(None)
    if isinstance(container, Done):
        return Some(container.unwrap())
    if isinstance(container, Error):
        return Null(None)

    error_msg = f"invalid container type: {type(container).__name__!r}"
    raise KontainerTypeError(error_msg)
