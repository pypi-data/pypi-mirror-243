from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramType
from .mask_position import MaskPosition

if TYPE_CHECKING:
    from yatbaf.typing import InputFile


@final
class InputSticker(TelegramType):
    """This object describes a sticker to be added to a sticker set.

    See: https://core.telegram.org/bots/api#inputsticker
    """

    sticker: InputFile | str
    """The added sticker."""

    emoji_list: list[str]
    """List of 1-20 emoji associated with the sticker"""

    mask_position: MaskPosition | None = None
    """*Optional.* Position where the mask should be placed on faces. For
    “mask” stickers only.
    """

    keywords: list[str] | None = None
    """*Optional.* List of 0-20 search keywords for the sticker with total
    length of up to 64 characters. For “regular” and “custom_emoji” stickers
    only.
    """
