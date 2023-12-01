from __future__ import annotations

from typing import Any

from kontainer.container import Maybe, Result
from kontainer.core.const import undefined
from kontainer.decorator import catch, optional
from kontainer.flow import (
    bind_elements,
    compose_funcs,
    flip,
    flip_func,
    flowtools,
    map_elements,
    pipe_bind,
    pipe_iter_bind,
    pipe_iter_map,
    pipe_map,
    toggle,
)

__all__ = [
    "flowtools",
    "Maybe",
    "Result",
    "optional",
    "catch",
    "pipe_bind",
    "pipe_map",
    "pipe_iter_map",
    "pipe_iter_bind",
    "map_elements",
    "bind_elements",
    "compose_funcs",
    "flip_func",
    "flip",
    "toggle",
    "undefined",
    "__version__",
]

__version__: str


def __getattr__(name: str) -> Any:  # pragma: no cover
    from importlib.metadata import version

    if name == "__version__":
        return version("kontainer")

    error_msg = f"The attribute named {name!r} is undefined."
    raise AttributeError(error_msg)
