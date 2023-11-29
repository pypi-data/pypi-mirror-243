from __future__ import annotations

from typing import final

from .abc import TelegramMethod


@final
class Close(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.close`"""
