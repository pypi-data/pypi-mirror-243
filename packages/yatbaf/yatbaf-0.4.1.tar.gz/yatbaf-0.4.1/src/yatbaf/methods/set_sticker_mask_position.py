from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.types import MaskPosition


@final
class SetStickerMaskPosition(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.set_sticker_mask_position`"""

    sticker: str
    mask_position: MaskPosition | None = None
