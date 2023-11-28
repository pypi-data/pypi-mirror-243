from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import Message

from .abc import TelegramMethodWithMedia

if TYPE_CHECKING:
    from yatbaf.types import InlineKeyboardMarkup
    from yatbaf.types import InputMedia
    from yatbaf.typing import NoneInt


@final
class EditMessageMedia(TelegramMethodWithMedia[Message | bool]):
    """See :meth:`yatbaf.bot.Bot.edit_message_media`"""

    media: InputMedia
    chat_id: str | int | None = None
    message_id: NoneInt = None
    inline_message_id: NoneInt = None
    reply_markup: InlineKeyboardMarkup | None = None
