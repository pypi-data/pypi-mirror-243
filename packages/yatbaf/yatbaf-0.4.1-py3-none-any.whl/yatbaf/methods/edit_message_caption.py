from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import Message

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.enums import ParseMode
    from yatbaf.types import InlineKeyboardMarkup
    from yatbaf.types import MessageEntity
    from yatbaf.typing import NoneInt
    from yatbaf.typing import NoneStr


@final
class EditMessageCaption(TelegramMethod[Message | bool]):
    """See :meth:`yatbaf.bot.Bot.edit_message_caption`"""

    chat_id: str | int | None = None
    message_id: NoneInt = None
    inline_message_id: NoneInt = None
    caption: NoneStr = None
    parse_mode: ParseMode | None = None
    caption_entities: list[MessageEntity] | None = None
    reply_markup: InlineKeyboardMarkup | None = None
