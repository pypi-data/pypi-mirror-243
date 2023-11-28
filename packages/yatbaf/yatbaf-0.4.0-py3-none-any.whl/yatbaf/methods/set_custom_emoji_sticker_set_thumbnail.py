from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.typing import NoneStr


@final
class SetCustomEmojiStickerSetThumbnail(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.set_custom_emoji_sticker_set_thumbnail`"""

    name: str
    custom_emoji_id: NoneStr = None
