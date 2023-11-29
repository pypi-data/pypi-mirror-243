from __future__ import annotations

from typing import final

from yatbaf.enums import StickerType
from yatbaf.typing import NoneBool
from yatbaf.typing import NoneInt
from yatbaf.typing import NoneStr

from .abc import TelegramType
from .file import File
from .mask_position import MaskPosition
from .photo_size import PhotoSize


@final
class Sticker(TelegramType):
    """This object represents a sticker.

    See: https://core.telegram.org/bots/api#sticker
    """

    file_id: str
    """
    Identifier for this file, which can be used to download or reuse the file.
    """

    file_unique_id: str
    """Unique identifier for this file, which is supposed to be the same over
    time and for different bots. Can't be used to download or reuse the file.
    """

    type: StickerType
    """Type of the sticker."""

    width: int
    """Sticker width."""

    height: int
    """Sticker height."""

    is_animated: bool
    """True, if the sticker is animated."""

    is_video: bool
    """True, if the sticker is a video sticker."""

    thumbnail: PhotoSize | None = None
    """*Optional.* Sticker thumbnail in the .WEBP or .JPG format."""

    emoji: NoneStr = None
    """*Optional.* Emoji associated with the sticker."""

    set_name: NoneStr = None
    """*Optional.* Name of the sticker set to which the sticker belongs."""

    premium_animation: File | None = None
    """*Optional.* For premium regular stickers, premium animation for the
    sticker.
    """

    mask_position: MaskPosition | None = None
    """*Optional.* For mask stickers, the position where the mask should be
    placed.
    """

    custom_emoji_id: NoneStr = None
    """*Optional.* For custom emoji stickers, unique identifier of the custom
    emoji.
    """

    needs_repainting: NoneBool = None
    """*Optional.* True, if the sticker must be repainted to a text color in
    messages, the color of the Telegram Premium badge in emoji status, white
    color on chat photos, or another appropriate color in other places.
    """

    file_size: NoneInt = None
    """*Optional.* File size in bytes."""
