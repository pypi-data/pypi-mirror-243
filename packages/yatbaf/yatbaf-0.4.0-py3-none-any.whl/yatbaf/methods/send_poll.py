from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import Message

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.enums import ParseMode
    from yatbaf.enums import PollType
    from yatbaf.types import MessageEntity
    from yatbaf.typing import NoneBool
    from yatbaf.typing import NoneInt
    from yatbaf.typing import NoneStr
    from yatbaf.typing import ReplyMarkup

# from datetime import timedelta


@final
class SendPoll(TelegramMethod[Message]):
    """See :meth:`yatbaf.bot.Bot.send_poll`"""

    chat_id: str | int
    question: str
    options: list[str]
    message_thread_id: NoneInt = None
    is_anonymous: NoneBool = None
    type: PollType | None = None
    allows_multiple_answers: NoneBool = None
    correct_option_id: NoneInt = None
    explanation: NoneStr = None
    explanation_parse_mode: ParseMode | None = None
    explanation_entities: list[MessageEntity] | None = None
    open_period: NoneInt = None
    close_date: int | None = None  # timedelta
    is_closed: NoneBool = None
    disable_notification: NoneBool = None
    protect_content: NoneBool = None
    reply_to_message_id: NoneInt = None
    allow_sending_without_reply: NoneBool = None
    reply_markup: ReplyMarkup | None = None
