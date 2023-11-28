from __future__ import annotations

from typing import final

from .abc import TelegramType
from .inline_keyboard_button import InlineKeyboardButton


@final
class InlineKeyboardMarkup(TelegramType):
    """This object represents an inline keyboard that appears right next to the
    message it belongs to.

    See: https://core.telegram.org/bots/api#inlinekeyboardmarkup
    """

    inline_keyboard: list[list[InlineKeyboardButton]]
    """Array of button rows."""
