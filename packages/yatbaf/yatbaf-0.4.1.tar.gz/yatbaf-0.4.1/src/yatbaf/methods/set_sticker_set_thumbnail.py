from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.typing import InputFile


@final
class SetStickerSetThumbnail(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.set_sticker_set_thumbnail`"""

    name: str
    user_id: int
    thumbnail: InputFile | str | None = None
