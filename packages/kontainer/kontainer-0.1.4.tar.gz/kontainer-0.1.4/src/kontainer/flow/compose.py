from __future__ import annotations

from functools import reduce
from typing import TYPE_CHECKING, Any, Callable, overload

if TYPE_CHECKING:
    from typing_extensions import TypeVar

    ValueT = TypeVar("ValueT", infer_variance=True)
    ValueT0 = TypeVar("ValueT0", infer_variance=True)
    ValueT1 = TypeVar("ValueT1", infer_variance=True)
    ValueT2 = TypeVar("ValueT2", infer_variance=True)
    ValueT3 = TypeVar("ValueT3", infer_variance=True)
    ValueT4 = TypeVar("ValueT4", infer_variance=True)
    ValueT5 = TypeVar("ValueT5", infer_variance=True)
    ValueT6 = TypeVar("ValueT6", infer_variance=True)
    ValueT7 = TypeVar("ValueT7", infer_variance=True)
    ValueT8 = TypeVar("ValueT8", infer_variance=True)
    ValueT9 = TypeVar("ValueT9", infer_variance=True)
    ValueT10 = TypeVar("ValueT10", infer_variance=True)

__all__ = ["compose_funcs"]


class _Compose:
    __slots__ = ("_funcs",)

    def __init__(self, funcs: tuple[Callable[[Any], Any], ...]) -> None:
        self._funcs = funcs

    def __call__(self, value: Any) -> Any:
        return reduce(_run_func, self._funcs, value)


@overload
def compose_funcs() -> Callable[[ValueT], ValueT]: ...


@overload
def compose_funcs(
    func0: Callable[[ValueT], ValueT0], /
) -> Callable[[ValueT], ValueT0]: ...


@overload
def compose_funcs(
    func0: Callable[[ValueT], ValueT0], func1: Callable[[ValueT0], ValueT1], /
) -> Callable[[ValueT], ValueT1]: ...


@overload
def compose_funcs(
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    /,
) -> Callable[[ValueT], ValueT2]: ...


@overload
def compose_funcs(
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    /,
) -> Callable[[ValueT], ValueT3]: ...


@overload
def compose_funcs(
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    /,
) -> Callable[[ValueT], ValueT4]: ...


@overload
def compose_funcs(
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    func5: Callable[[ValueT4], ValueT5],
    /,
) -> Callable[[ValueT], ValueT5]: ...


@overload
def compose_funcs(
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    func5: Callable[[ValueT4], ValueT5],
    func6: Callable[[ValueT5], ValueT6],
    /,
) -> Callable[[ValueT], ValueT6]: ...


@overload
def compose_funcs(
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    func5: Callable[[ValueT4], ValueT5],
    func6: Callable[[ValueT5], ValueT6],
    func7: Callable[[ValueT6], ValueT7],
    /,
) -> Callable[[ValueT], ValueT7]: ...


@overload
def compose_funcs(
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    func5: Callable[[ValueT4], ValueT5],
    func6: Callable[[ValueT5], ValueT6],
    func7: Callable[[ValueT6], ValueT7],
    func8: Callable[[ValueT7], ValueT8],
    /,
) -> Callable[[ValueT], ValueT8]: ...


@overload
def compose_funcs(
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    func5: Callable[[ValueT4], ValueT5],
    func6: Callable[[ValueT5], ValueT6],
    func7: Callable[[ValueT6], ValueT7],
    func8: Callable[[ValueT7], ValueT8],
    func9: Callable[[ValueT8], ValueT9],
    /,
) -> Callable[[ValueT], ValueT9]: ...


@overload
def compose_funcs(
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    func5: Callable[[ValueT4], ValueT5],
    func6: Callable[[ValueT5], ValueT6],
    func7: Callable[[ValueT6], ValueT7],
    func8: Callable[[ValueT7], ValueT8],
    func9: Callable[[ValueT8], ValueT9],
    func10: Callable[[ValueT9], ValueT10],
    /,
) -> Callable[[ValueT], ValueT10]: ...


@overload
def compose_funcs(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]: ...


def compose_funcs(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    return _Compose(funcs)


def _run_func(value: ValueT, func: Callable[[ValueT], ValueT0]) -> ValueT0:
    return func(value)
