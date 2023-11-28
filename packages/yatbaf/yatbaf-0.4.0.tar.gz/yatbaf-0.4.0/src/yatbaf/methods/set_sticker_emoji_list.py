from __future__ import annotations

from typing import final

from .abc import TelegramMethod


@final
class SetStickerEmojiList(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.set_sticker_emoji_list`"""

    sticker: str
    emoji_list: list[str]
