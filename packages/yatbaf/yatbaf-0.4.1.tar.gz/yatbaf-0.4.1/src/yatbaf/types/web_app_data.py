from __future__ import annotations

from typing import final

from .abc import TelegramType


@final
class WebAppData(TelegramType):
    """Describes data sent from a Web App to the bot.

    See: https://core.telegram.org/bots/api#webappdata
    """

    data: str
    """The data. Be aware that a bad client can send arbitrary data in this field."""  # noqa: E501

    button_text: str
    """Text of the web_app keyboard button from which the Web App was opened.
    Be aware that a bad client can send arbitrary data in this field.
    """
