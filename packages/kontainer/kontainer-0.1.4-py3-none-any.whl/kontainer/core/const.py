from __future__ import annotations

import warnings

from kontainer.core.exception import UndefinedRecreateWarning

__all__ = ["undefined", "Undefined"]

_UNDEFINED_COUNT = 0


class Undefined:
    def __init__(self) -> None:
        global _UNDEFINED_COUNT  # noqa: PLW0603
        if not _UNDEFINED_COUNT:
            _UNDEFINED_COUNT += 1
            return

        warnings.warn(
            "Undefined is used with the assumption that it will be created only once. "
            "This can cause malfunctions.",
            category=UndefinedRecreateWarning,
            stacklevel=2,
        )

    def __eq__(self, other: object) -> bool:
        return self is other

    def __ne__(self, other: object) -> bool:
        return self is not other

    def __repr__(self) -> str:
        return "undefined"

    def __str__(self) -> str:
        return "undefined"


undefined = Undefined()
