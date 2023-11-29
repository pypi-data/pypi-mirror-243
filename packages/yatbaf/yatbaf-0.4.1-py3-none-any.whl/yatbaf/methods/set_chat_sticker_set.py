from __future__ import annotations

from typing import final

from .abc import TelegramMethod


@final
class SetChatStickerSet(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.set_chat_sticker_set`"""

    chat_id: str | int
    sticker_set_name: str
