from __future__ import annotations

__all__ = (
    "Not",
    "Or",
    "And",
)

from typing import TYPE_CHECKING
from typing import Generic
from typing import TypeVar
from typing import final

if TYPE_CHECKING:
    from yatbaf.typing import Filter

T = TypeVar("T")


@final
class Not(Generic[T]):
    """NOT filter.

    Use it to invert filter result::

        @on_message(filters=[Not(User(123))])
        async def handler(message: Message) -> None:
            ...
    """

    __slots__ = (
        "filter",
        "priority",
    )

    def __init__(self, filter: Filter[T], /) -> None:
        """
        :param filter: Filter.
        """

        self.priority = filter.priority
        self.filter = filter

    def check(self, update: T) -> bool:
        return not self.filter.check(update)


@final
class Or(Generic[T]):
    """OR filter."""

    __slots__ = (
        "priority",
        "_filters",
    )

    def __init__(self, *filters: Filter[T]) -> None:
        """
        :param filters: A list of filters.
        """

        self.priority = (min(*filters, key=lambda v: v.priority)).priority
        self._filters = filters

    def check(self, update: T) -> bool:
        return any(f.check(update) for f in self._filters)


@final
class And(Generic[T]):
    """AND filter."""

    __slots__ = (
        "priority",
        "_filters",
    )

    def __init__(self, *filters: Filter[T]) -> None:
        """
        :param filters: A list of filters.
        """

        self.priority = (min(*filters, key=lambda v: v.priority)).priority
        self._filters = filters

    def check(self, update: T) -> bool:
        return all(f.check(update) for f in self._filters)
