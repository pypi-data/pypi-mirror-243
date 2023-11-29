from __future__ import annotations

from typing import final

from .abc import TelegramMethod


@final
class DeleteStickerFromSet(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.delete_sticker_from_set`"""

    sticker: str
