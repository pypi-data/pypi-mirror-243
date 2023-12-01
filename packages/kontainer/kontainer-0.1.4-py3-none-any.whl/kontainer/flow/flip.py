from __future__ import annotations

from functools import wraps
from inspect import Parameter, signature
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from typing_extensions import TypeVar, TypeVarTuple, Unpack

    ValueT1 = TypeVar("ValueT1", infer_variance=True)
    ValueT2 = TypeVar("ValueT2", infer_variance=True)
    OtherT = TypeVar("OtherT", infer_variance=True)
    ArgsT = TypeVarTuple("ArgsT")

__all__ = ["flip_func", "flip"]

ERROR_PARAM_KIND = frozenset({Parameter.KEYWORD_ONLY, Parameter.VAR_KEYWORD})


def flip_func(
    func: Callable[[ValueT1, ValueT2, Unpack[ArgsT]], OtherT]
) -> Callable[[ValueT2, ValueT1, Unpack[ArgsT]], OtherT]:
    sig = signature(func)
    length = len(sig.parameters)

    var_positional = False
    for key, param in sig.parameters.items():
        if param.kind in ERROR_PARAM_KIND:
            error_msg = (
                "only use functions that take positional parameters. "
                f"{key}: {param.kind}"
            )
            raise TypeError(error_msg)

        if param.kind is param.VAR_POSITIONAL:
            var_positional = True

    if length < 2 and not var_positional:  # noqa: PLR2004
        error_msg = f"Too few parameters required by func: {length} < 2"
        raise TypeError(error_msg)

    @wraps(func)
    def inner(*args: Any) -> OtherT:
        first, second, *new_args = args
        return func(*sig.bind(second, first, *new_args).args)  # type: ignore

    return inner


def flip(
    values: tuple[ValueT1, ValueT2, Unpack[ArgsT]]
) -> tuple[ValueT2, ValueT1, Unpack[ArgsT]]:
    return (values[1], values[0], *values[2:])  # type: ignore
