from __future__ import annotations

from typing import final

from yatbaf.types import StickerSet

from .abc import TelegramMethod


@final
class GetStickerSet(TelegramMethod[StickerSet]):
    """See :meth:`yatbaf.bot.Bot.get_stickers_set`"""

    name: str
