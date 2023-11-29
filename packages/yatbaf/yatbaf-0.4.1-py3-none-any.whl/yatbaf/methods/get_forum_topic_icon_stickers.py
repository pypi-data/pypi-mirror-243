from __future__ import annotations

from typing import final

from yatbaf.types import Sticker

from .abc import TelegramMethod


@final
class GetForumTopicIconStickers(TelegramMethod[list[Sticker]]):
    """See :meth:`yatbaf.bot.Bot.get_forum_topic_icon_stickers`"""
