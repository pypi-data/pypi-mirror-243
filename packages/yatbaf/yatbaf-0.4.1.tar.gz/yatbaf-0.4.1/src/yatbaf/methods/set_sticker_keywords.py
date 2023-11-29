from __future__ import annotations

from typing import final

from .abc import TelegramMethod


@final
class SetStickerKeywords(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.set_sticker_keywords`"""

    sticker: str
    keywords: list[str] | None = None
