from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, Generator, Generic, overload

from typing_extensions import ParamSpec, TypeVar

from kontainer.container.result import Error, Result
from kontainer.utils.generator import unwrap_generator

ErrorT = TypeVar("ErrorT", infer_variance=True, bound=Exception)
if TYPE_CHECKING:
    ValueT = TypeVar("ValueT", infer_variance=True)
    ErrorT2 = TypeVar("ErrorT2", infer_variance=True, bound=Exception)
    OtherValueT = TypeVar("OtherValueT", infer_variance=True)
    OtherErrorT = TypeVar("OtherErrorT", infer_variance=True, bound=Exception)
    OtherErrorT2 = TypeVar("OtherErrorT2", infer_variance=True, bound=Exception)
    ParamT = ParamSpec("ParamT")
    OtherParamT = ParamSpec("OtherParamT")


__all__ = ["catch"]


class _Catch(Generic[ErrorT]):
    __slots__ = ("_error_type",)

    def __init__(self, error_type: type[ErrorT]) -> None:
        self._error_type = error_type

    @overload
    def __call__(
        self, func: Callable[ParamT, Generator[Any, Any, Result[ValueT, ErrorT2]]]
    ) -> Callable[ParamT, Result[ValueT, ErrorT | ErrorT2]]: ...

    @overload
    def __call__(
        self, func: Callable[ParamT, Generator[Any, Any, ValueT]]
    ) -> Callable[ParamT, Result[ValueT, ErrorT]]: ...

    @overload
    def __call__(
        self, func: Callable[ParamT, Result[ValueT, ErrorT2]]
    ) -> Callable[ParamT, Result[ValueT, ErrorT | ErrorT2]]: ...

    @overload
    def __call__(
        self, func: Callable[ParamT, ValueT]
    ) -> Callable[ParamT, Result[ValueT, ErrorT]]: ...

    def __call__(
        self,
        func: Callable[ParamT, Generator[Any, Any, Result[ValueT, ErrorT2]]]
        | Callable[ParamT, Generator[Any, Any, ValueT]]
        | Callable[ParamT, Result[ValueT, ErrorT2]]
        | Callable[ParamT, ValueT],
    ) -> (
        Callable[ParamT, Result[ValueT, ErrorT | ErrorT2]]
        | Callable[ParamT, Result[ValueT, ErrorT2]]
    ):
        @wraps(func)
        def inner(*args: ParamT.args, **kwargs: ParamT.kwargs) -> Result[ValueT, Any]:
            try:
                result = func(*args, **kwargs)
                if isinstance(result, Generator):
                    result = unwrap_generator(result)
            except self._error_type as exc:
                return Error(exc)
            if isinstance(result, Error):
                return Error(result._other)  # noqa: SLF001
            if isinstance(result, Result):
                return Result(result._value)  # noqa: SLF001
            return Result(result)

        return inner


@overload
def catch() -> _Catch[Exception]: ...


@overload
def catch(*, error_type: type[ErrorT2]) -> _Catch[ErrorT2]: ...


@overload
def catch(*, error_type: type[Exception]) -> _Catch[Exception]: ...


@overload
def catch(func: None = ..., *, error_type: type[ErrorT2]) -> _Catch[ErrorT2]: ...


@overload
def catch(
    func: Callable[ParamT, Generator[Any, Any, Result[ValueT, ErrorT]]], /
) -> Callable[ParamT, Result[ValueT, ErrorT | Exception]]: ...


@overload
def catch(
    func: Callable[ParamT, Generator[Any, Any, ValueT]], /
) -> Callable[ParamT, Result[ValueT, Exception]]: ...


@overload
def catch(
    func: Callable[ParamT, Result[ValueT, ErrorT]], /
) -> Callable[ParamT, Result[ValueT, ErrorT | Exception]]: ...


@overload
def catch(
    func: Callable[ParamT, ValueT], /
) -> Callable[ParamT, Result[ValueT, Exception]]: ...


@overload
def catch(
    func: Callable[ParamT, Generator[Any, Any, Result[ValueT, ErrorT]]],
    /,
    *,
    error_type: type[ErrorT2],
) -> Callable[ParamT, Result[ValueT, ErrorT | ErrorT2]]: ...


@overload
def catch(
    func: Callable[ParamT, Generator[Any, Any, ValueT]], /, *, error_type: type[ErrorT2]
) -> Callable[ParamT, Result[ValueT, ErrorT2]]: ...


@overload
def catch(
    func: Callable[ParamT, Result[ValueT, ErrorT]], /, *, error_type: type[ErrorT2]
) -> Callable[ParamT, Result[ValueT, ErrorT | ErrorT2]]: ...


@overload
def catch(
    func: Callable[ParamT, ValueT], /, *, error_type: type[ErrorT2]
) -> Callable[ParamT, Result[ValueT, ErrorT2]]: ...


@overload
def catch(
    func: Callable[ParamT, Generator[Any, Any, Result[ValueT, ErrorT]]],
    /,
    *,
    error_type: type[Exception],
) -> Callable[ParamT, Result[ValueT, ErrorT | Exception]]: ...


@overload
def catch(
    func: Callable[ParamT, Generator[Any, Any, ValueT]],
    /,
    *,
    error_type: type[Exception],
) -> Callable[ParamT, Result[ValueT, Exception]]: ...


@overload
def catch(
    func: Callable[ParamT, Result[ValueT, ErrorT]], /, *, error_type: type[Exception]
) -> Callable[ParamT, Result[ValueT, ErrorT | Exception]]: ...


@overload
def catch(
    func: Callable[ParamT, ValueT], /, *, error_type: type[Exception]
) -> Callable[ParamT, Result[ValueT, Exception]]: ...


def catch(
    func: Callable[ParamT, Generator[Any, Any, Result[ValueT, ErrorT]]]
    | Callable[ParamT, Generator[Any, Any, ValueT]]
    | Callable[ParamT, Result[ValueT, ErrorT]]
    | Callable[ParamT, ValueT]
    | None = None,
    *,
    error_type: type[ErrorT2 | Exception] = Exception,
) -> (
    Callable[ParamT, Result[ValueT, ErrorT | Exception]]
    | Callable[ParamT, Result[ValueT, Exception]]
    | _Catch[ErrorT2]
    | _Catch[Exception]
):
    if func is None:
        return _Catch(error_type=error_type)

    @wraps(func)
    def inner(*args: ParamT.args, **kwargs: ParamT.kwargs) -> Result[ValueT, Any]:
        try:
            result = func(*args, **kwargs)
            if isinstance(result, Generator):
                result = unwrap_generator(result)
        except error_type as exc:
            return Error(exc)
        if isinstance(result, Error):
            return Error(result._other)  # noqa: SLF001
        if isinstance(result, Result):
            return Result(result._value)  # noqa: SLF001
        return Result(result)

    return inner
