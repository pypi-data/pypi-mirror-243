from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import Message

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.enums import ParseMode
    from yatbaf.types import InlineKeyboardMarkup
    from yatbaf.types import MessageEntity
    from yatbaf.typing import NoneBool
    from yatbaf.typing import NoneInt


@final
class EditMessageText(TelegramMethod[Message | bool]):
    """See :meth:`yatbaf.bot.Bot.edit_message_text`"""

    text: str
    chat_id: str | int | None = None
    message_id: NoneInt = None
    inline_message_id: NoneInt = None
    parse_mode: ParseMode | None = None
    entities: list[MessageEntity] | None = None
    disable_web_page_preview: NoneBool = None
    reply_markup: InlineKeyboardMarkup | None = None
