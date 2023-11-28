from __future__ import annotations

from typing import final

from .abc import TelegramType


@final
class BotName(TelegramType):
    """This object represents the bot's name.

    See: https://core.telegram.org/bots/api#botname
    """

    name: str
    """The bot's name."""
