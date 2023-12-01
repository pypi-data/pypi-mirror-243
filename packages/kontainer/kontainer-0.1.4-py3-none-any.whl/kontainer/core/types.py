from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Generator, Generic, Iterable

from typing_extensions import TypeVar

from kontainer.utils.generator import create_generator

ValueT = TypeVar("ValueT", infer_variance=True)
OtherT = TypeVar("OtherT", infer_variance=True)
if TYPE_CHECKING:
    AnotherT = TypeVar("AnotherT", infer_variance=True)
    ElementT = TypeVar("ElementT", infer_variance=True)

__all__ = ["Container"]


class Container(Iterable[ValueT], Awaitable[ValueT], Generic[ValueT, OtherT], ABC):
    r"""Container

    map: (x, y) -> (X, y)
    bind: (x, y) -> (X, Y)
    """

    __slots__ = ("_value",)

    @abstractmethod
    def __init__(self, value: ValueT) -> None: ...

    @abstractmethod
    def __repr__(self) -> str: ...

    @abstractmethod
    def __str__(self) -> str: ...

    @abstractmethod
    def __eq__(self, other: object) -> bool: ...

    def __ne__(self, other: object) -> bool:
        return not (self == other)

    @abstractmethod
    def __hash__(self) -> int: ...

    def __iter__(self) -> Generator[Any, Any, ValueT]:
        return create_generator(self.unwrap())

    def __await__(self) -> Generator[Any, Any, ValueT]:
        return iter(self)

    @abstractmethod
    def map_value(
        self, func: Callable[[ValueT], AnotherT]
    ) -> Container[AnotherT, OtherT]:
        """_summary_

        value -> new value -> (new value, other)

        Args:
            func: _description_

        Returns:
            _description_
        """

    @abstractmethod
    def map_values(
        self, value: ElementT, func: Callable[[ValueT, ElementT], AnotherT]
    ) -> Container[AnotherT, OtherT]:
        """_summary_

        value, arg -> new value -> (new value, other)

        Args:
            value: _description_
            func: _description_

        Returns:
            _description_
        """

    @abstractmethod
    def map_container(
        self,
        value: Container[ElementT, Any],
        func: Callable[[ValueT, ElementT], AnotherT],
    ) -> Container[AnotherT, OtherT]:
        """_summary_

        value, container -> new value -> (new value, other)

        Args:
            value: _description_
            func: _description_

        Returns:
            _description_
        """

    @abstractmethod
    def bind_value(
        self, func: Callable[[ValueT], Container[AnotherT, OtherT]]
    ) -> Container[AnotherT, OtherT]:
        """_summary_

        value -> new value, new other -> (new value, new other)

        Args:
            func: _description_

        Returns:
            _description_
        """

    @abstractmethod
    def bind_values(
        self,
        value: ElementT,
        func: Callable[[ValueT, ElementT], Container[AnotherT, OtherT]],
    ) -> Container[AnotherT, OtherT]:
        """_summary_

        value, arg -> new value, new other -> (new value, new other)

        Args:
            value: _description_
            func: _description_

        Returns:
            _description_
        """

    @abstractmethod
    def bind_container(
        self,
        value: Container[ElementT, Any],
        func: Callable[[ValueT, ElementT], Container[AnotherT, OtherT]],
    ) -> Container[AnotherT, OtherT]:
        """_summary_

        value, container -> new value, new other -> (new value, new other)

        Args:
            value: _description_
            func: _description_

        Returns:
            _description_
        """

    @abstractmethod
    def switch(self) -> Container[OtherT, ValueT]: ...

    @abstractmethod
    def default(self, value: AnotherT) -> ValueT | AnotherT: ...

    @abstractmethod
    def map_default(self, func: Callable[[], AnotherT]) -> ValueT | AnotherT: ...

    @abstractmethod
    def unwrap(self) -> ValueT: ...

    @property
    @abstractmethod
    def is_positive(self) -> bool: ...

    @property
    def is_negative(self) -> bool:
        return not self.is_positive
