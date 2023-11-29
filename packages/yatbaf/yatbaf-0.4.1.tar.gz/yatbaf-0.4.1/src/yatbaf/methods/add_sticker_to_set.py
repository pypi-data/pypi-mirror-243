from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.types import InputSticker


@final
class AddStickerToSet(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.add_sticker_to_set`"""

    user_id: int
    name: str
    sticker: InputSticker
