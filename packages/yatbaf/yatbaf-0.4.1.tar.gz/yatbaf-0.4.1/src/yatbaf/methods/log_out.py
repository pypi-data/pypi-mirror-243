from __future__ import annotations

from typing import final

from .abc import TelegramMethod


@final
class LogOut(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.log_out`"""
