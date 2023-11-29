from __future__ import annotations

from typing import final

from .abc import TelegramType


@final
class BotCommand(TelegramType):
    """This object represents a bot command.

    See: https://core.telegram.org/bots/api#botcommand
    """

    command: str
    """Text of the command.

    .. note::

        Can contain only lowercase English letters, digits and underscores.
    """

    description: str
    """Description of the command."""
