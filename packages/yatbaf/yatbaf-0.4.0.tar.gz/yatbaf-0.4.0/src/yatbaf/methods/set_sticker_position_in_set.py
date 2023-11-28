from __future__ import annotations

from typing import final

from .abc import TelegramMethod


@final
class SetStickerPositionInSet(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.set_sticker_position_in_set`"""

    sticker: str
    position: int
