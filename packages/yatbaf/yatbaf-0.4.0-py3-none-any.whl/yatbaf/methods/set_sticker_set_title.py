from __future__ import annotations

from typing import final

from .abc import TelegramMethod


@final
class SetStickerSetTitle(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.set_sticker_set_title`"""

    name: str
    title: str
