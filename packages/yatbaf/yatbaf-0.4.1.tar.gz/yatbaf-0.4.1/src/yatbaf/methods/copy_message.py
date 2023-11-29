from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import MessageId

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.enums import ParseMode
    from yatbaf.types import MessageEntity
    from yatbaf.typing import NoneBool
    from yatbaf.typing import NoneInt
    from yatbaf.typing import ReplyMarkup


@final
class CopyMessage(TelegramMethod[MessageId]):
    """See :meth:`yatbaf.bot.Bot.copy_message`"""

    chat_id: str | int
    from_chat_id: str | int
    message_id: int
    caption: str | None
    message_thread_id: NoneInt = None
    parse_mode: ParseMode | None = None
    caption_entities: list[MessageEntity] | None = None
    disable_notification: NoneBool = None
    protect_content: NoneBool = None
    reply_to_message_id: NoneInt = None
    allow_sending_without_reply: NoneBool = None
    reply_markup: ReplyMarkup | None = None
