from __future__ import annotations

from typing import final

from .abc import TelegramMethod


@final
class DeleteChatStickerSet(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.delete_chat_sticker_set`"""

    chat_id: str | int
