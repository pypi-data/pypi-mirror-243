from __future__ import annotations

from typing import final

from yatbaf.enums import StickerType

from .abc import TelegramType
from .photo_size import PhotoSize
from .sticker import Sticker


@final
class StickerSet(TelegramType):
    """This object represents a sticker set.

    See: https://core.telegram.org/bots/api#stickerset
    """

    name: str
    """Sticker set name."""

    title: str
    """Sticker set title."""

    sticker_type: StickerType
    """Type of stickers in the set."""

    is_animated: bool
    """True, if the sticker set contains animated stickers."""

    is_video: bool
    """True, if the sticker set contains video stickers."""

    stickers: list[Sticker]
    """List of all set stickers."""

    thumbnail: PhotoSize
    """Optional. Sticker set thumbnail in the .WEBP, .TGS, or .WEBM format."""
