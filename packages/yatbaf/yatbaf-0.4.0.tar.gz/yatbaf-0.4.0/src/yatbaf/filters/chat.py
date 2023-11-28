from __future__ import annotations

__all__ = (
    "Chat",
    "Group",
    "Channel",
)

from typing import TYPE_CHECKING
from typing import final

from yatbaf.enums import ChatType

if TYPE_CHECKING:
    from yatbaf.types import Message


@final
class Chat:
    """Private chat filter.

    Use it to filter messages coming from private chats::

        @on_message(fileters=[Chat()])
        async def handler(message: Message) -> None:
            '''messages from any Private chats'''
    """

    __slots__ = ("priority",)

    def __init__(self, *, priority: int = 100) -> None:
        """
        :param priority: Filter priority. Default 100.
        """

        self.priority = priority

    def check(self, update: Message) -> bool:
        return (
            t := update.chat.type
        ) is ChatType.PRIVATE or t is ChatType.SENDER


@final
class Group:
    """Group or supergroup filter.

    Use it to filter messages coming from Groups or Supergroups::

        @on_message(fileters=[Group()])
        async def handler(message: Message) -> None:
            '''messages from any Group'''

        @on_message(fileters=[Group(1234, 4321)])
        async def specific_groip(message: Message) -> None:
            '''messages from Group with ID 1234 or 4321'''
    """

    __slots__ = (
        "ids",
        "priority",
    )

    def __init__(self, *ids: int, priority: int = 100) -> None:
        """
        :param ids: *Optional.* Group ids.
        :param priority: Filter priority. Default 100.
        """

        self.ids = frozenset(ids)
        self.priority = priority

    def check(self, update: Message) -> bool:
        is_group = (
            t := update.chat.type
        ) is ChatType.GROUP or t is ChatType.SUPERGROUP
        if self.ids:
            return is_group and update.chat.id in self.ids
        return is_group


@final
class Channel:
    """Channel filter.

    Use it to filter messages coming from Channels::

        @on_message(filters=[Channel()])
        async def handler(message: Message) -> None:
            '''messages from any Channel'''

        @on_message(filters=[Channel(1234, 4321)])
        async def handler(message: Message) -> None:
            '''messages from Channel with ID 1234 or 4321'''
    """

    __slots__ = (
        "ids",
        "priority",
    )

    def __init__(self, *ids: int, priority: int = 100) -> None:
        """
        :param ids: *Optional.* Channel ids.
        :param priority: Filter priority. Default 100.
        """

        self.ids = frozenset(ids)
        self.priority = priority

    def check(self, update: Message) -> bool:
        is_channel = update.chat.type is ChatType.CHANNEL
        if self.ids:
            return is_channel and update.chat.id in self.ids
        return is_channel
