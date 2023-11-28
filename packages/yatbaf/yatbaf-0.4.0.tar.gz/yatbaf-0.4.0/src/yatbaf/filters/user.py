from __future__ import annotations

__all__ = ("User",)

from typing import TYPE_CHECKING
from typing import final

if TYPE_CHECKING:
    from yatbaf.types import Message


@final
class User:
    """User filter.

    Use it to filter message coming from a specific user::

        @on_message(filters=[User("user")])
        async def handler(message: Message) -> None:
            ...
    """

    __slots__ = (
        "priority",
        "users",
    )

    def __init__(self, *users: str | int, priority: int = 200) -> None:
        """
        :param users: Public username (with or without `@`) or user id.
        :param priority: Filter priority. Default 200.
        """

        self.users = frozenset([
            u.lower().removeprefix("@") if isinstance(u, str) else u
            for u in users
        ])
        self.priority = priority

    def check(self, update: Message) -> bool:
        return (u := update.from_) is not None and (
            u.id in self.users or
            (u.username is not None and u.username.lower() in self.users)
        )
