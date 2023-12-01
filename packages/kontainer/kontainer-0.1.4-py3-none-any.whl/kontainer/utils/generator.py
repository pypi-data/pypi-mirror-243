from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generator

if TYPE_CHECKING:
    from typing_extensions import TypeVar

    ValueT = TypeVar("ValueT", infer_variance=True)

__all__ = ["create_generator", "unwrap_generator"]


def create_generator(value: ValueT) -> Generator[Any, Any, ValueT]:
    yield
    return value


def unwrap_generator(generator: Generator[Any, Any, ValueT]) -> ValueT:
    try:
        while True:
            next(generator)
    except StopIteration as exc:
        return exc.value
