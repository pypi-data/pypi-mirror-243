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
class SendVenue(TelegramMethod[Message]):
    """See :meth:`yatbaf.bot.Bot.send_venue`"""

    chat_id: str | int
    latitude: float
    longtitude: float
    title: str
    address: str
    message_thread_id: NoneInt = None
    foursquare_id: NoneStr = None
    foursquare_type: NoneStr = None
    google_place_id: NoneStr = None
    google_place_type: NoneStr = None
    disable_notification: NoneBool = None
    protect_content: NoneBool = None
    reply_to_message_id: NoneInt = None
    allow_sending_without_reply: NoneBool = None
    reply_markup: ReplyMarkup | None = None
