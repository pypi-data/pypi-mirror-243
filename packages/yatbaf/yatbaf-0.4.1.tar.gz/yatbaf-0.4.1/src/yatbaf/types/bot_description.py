from __future__ import annotations

from typing import final

from .abc import TelegramType


@final
class BotDescription(TelegramType):
    """This object represents the bot's description.

    See: https://core.telegram.org/bots/api#botdescription
    """

    description: str
    """The bot's description"""
