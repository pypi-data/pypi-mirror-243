from __future__ import annotations

__all__ = ("Command",)

from typing import TYPE_CHECKING
from typing import final

from yatbaf.utils import parse_command

if TYPE_CHECKING:
    from yatbaf.types import Message


@final
class Command:
    """Command filter.

    Usage::

        @on_message(filters=[Command("hello", "start")])
        async def cmd_start(message: Message) -> None:
            ...

        @on_message(filters=[Command("ping")])
        async def cmd_ping(message: Message) -> None:
            ...
    """

    __slots__ = (
        "commands",
        "priority",
    )

    def __init__(self, *command: str, priority: int = 400) -> None:
        """
        :param command: The commnad or list of commands.
        :param priority: Filter priority. Default 400.
        :raise ValueError: If ``command`` is empty.

        .. note::

            ``command`` case-insensitive.
        """

        if not command:
            raise ValueError("You must pass at least one command.")

        self.commands = frozenset([
            c.removeprefix("/").lower() for c in command
        ])
        self.priority = priority

    def check(self, update: Message) -> bool:
        if (text := update.text) is None:
            return False

        return ((command := parse_command(text)) is not None
                and command in self.commands)
