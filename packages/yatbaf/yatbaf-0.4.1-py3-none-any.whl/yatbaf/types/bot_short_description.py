from __future__ import annotations

from typing import final

from .abc import TelegramType


@final
class BotShortDescription(TelegramType):
    """This object represents the bot's short description.

    See: https://core.telegram.org/bots/api#botshortdescription
    """

    short_description: str
    """The bot's short description"""
