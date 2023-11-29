from __future__ import annotations

from typing import final

from .abc import TelegramType
from .photo_size import PhotoSize


@final
class UserProfilePhotos(TelegramType):
    """This object represent a user's profile pictures.

    See: https://core.telegram.org/bots/api#userprofilephotos
    """

    total_count: int
    """Total number of profile pictures the target user has."""

    photos: list[list[PhotoSize]]
    """Requested profile pictures (in up to 4 sizes each)."""
