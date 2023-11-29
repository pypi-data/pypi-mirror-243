from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import Message

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.enums import ParseMode
    from yatbaf.types import MessageEntity
    from yatbaf.typing import NoneBool
    from yatbaf.typing import NoneInt
    from yatbaf.typing import ReplyMarkup


@final
class SendMessage(TelegramMethod[Message]):
    """See :meth:`yatbaf.bot.Bot.send_message`"""

    chat_id: str | int
    text: str
    message_thread_id: NoneInt = None
    parse_mode: ParseMode | None = None
    entities: list[MessageEntity] | None = None
    disable_web_page_preview: NoneBool = None
    disable_notification: NoneBool = None
    protect_content: NoneBool = None
    reply_to_message_id: NoneInt = None
    allow_sending_without_reply: NoneBool = None
    reply_markup: ReplyMarkup | None = None
