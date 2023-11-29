from __future__ import annotations

from typing import final

from yatbaf.types import Sticker

from .abc import TelegramMethod


@final
class GetCustomEmojiStickers(TelegramMethod[list[Sticker]]):
    """See :meth:`yatbaf.bot.Bot.get_custom_emoji_stickers`"""

    custom_emoji_ids: list[str]
