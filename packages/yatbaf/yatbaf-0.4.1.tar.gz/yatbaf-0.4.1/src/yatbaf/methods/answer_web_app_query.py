from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import SentWebAppMessage

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.types import InlineQueryResult


@final
class AnswerWebAppQuery(TelegramMethod[SentWebAppMessage]):
    """See :meth:`yatbaf.bot.Bot.answer_web_app_query`"""

    web_app_query_id: str
    result: InlineQueryResult
