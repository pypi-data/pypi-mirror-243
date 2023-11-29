from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import Message

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.typing import NoneBool
    from yatbaf.typing import NoneInt
    from yatbaf.typing import NoneStr
    from yatbaf.typing import ReplyMarkup


@final
class SendContact(TelegramMethod[Message]):
    """See :meth:`yatbaf.bot.Bot.send_contact`"""

    chat_id: str | int
    phone_number: str
    first_name: str
    message_thread_id: NoneInt = None
    last_name: NoneStr = None
    vcard: NoneStr = None
    disable_notification: NoneBool = None
    protect_content: NoneBool = None
    reply_to_message_id: NoneInt = None
    allow_sending_without_reply: NoneBool = None
    reply_markup: ReplyMarkup | None = None
