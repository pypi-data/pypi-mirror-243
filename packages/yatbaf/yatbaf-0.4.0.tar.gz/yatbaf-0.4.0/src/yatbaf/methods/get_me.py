from __future__ import annotations

from typing import final

from yatbaf.types import User

from .abc import TelegramMethod


@final
class GetMe(TelegramMethod[User]):
    """See :meth:`yatbaf.bot.Bot.get_me`"""
