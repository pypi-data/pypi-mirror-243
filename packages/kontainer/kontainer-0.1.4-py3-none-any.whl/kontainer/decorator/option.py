from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, Generator, overload

from kontainer.container.maybe import Maybe
from kontainer.utils.generator import unwrap_generator

if TYPE_CHECKING:
    from typing_extensions import ParamSpec, TypeVar

    ValueT = TypeVar("ValueT", infer_variance=True)
    ParamT = ParamSpec("ParamT")

__all__ = ["optional"]


@overload
def optional(
    func: Callable[ParamT, Generator[Any, Any, None]]
) -> Callable[ParamT, Maybe[Any]]: ...


@overload
def optional(
    func: Callable[ParamT, Generator[Any, Any, Maybe[ValueT]]]
) -> Callable[ParamT, Maybe[ValueT]]: ...


@overload
def optional(
    func: Callable[ParamT, Generator[Any, Any, ValueT | None]]
) -> Callable[ParamT, Maybe[ValueT]]: ...


@overload
def optional(
    func: Callable[ParamT, Generator[Any, Any, ValueT]]
) -> Callable[ParamT, Maybe[ValueT]]: ...


@overload
def optional(func: Callable[ParamT, None]) -> Callable[ParamT, Maybe[Any]]: ...


@overload
def optional(
    func: Callable[ParamT, Maybe[ValueT]]
) -> Callable[ParamT, Maybe[ValueT]]: ...


@overload
def optional(
    func: Callable[ParamT, ValueT | None]
) -> Callable[ParamT, Maybe[ValueT]]: ...


@overload
def optional(func: Callable[ParamT, ValueT]) -> Callable[ParamT, Maybe[ValueT]]: ...


def optional(
    func: Callable[ParamT, Generator[Any, Any, None]]
    | Callable[ParamT, Generator[Any, Any, Maybe[ValueT]]]
    | Callable[ParamT, Generator[Any, Any, ValueT | None]]
    | Callable[ParamT, Generator[Any, Any, ValueT]]
    | Callable[ParamT, None]
    | Callable[ParamT, Maybe[ValueT]]
    | Callable[ParamT, ValueT | None]
    | Callable[ParamT, ValueT],
) -> Callable[ParamT, Maybe[Any]] | Callable[ParamT, Maybe[ValueT]]:
    @wraps(func)
    def inner(*args: ParamT.args, **kwargs: ParamT.kwargs) -> Maybe[Any]:
        result = func(*args, **kwargs)
        if isinstance(result, Generator):
            result = unwrap_generator(result)
        if isinstance(result, Maybe):
            return Maybe(result._value)  # noqa: SLF001
        return Maybe(result)

    return inner
