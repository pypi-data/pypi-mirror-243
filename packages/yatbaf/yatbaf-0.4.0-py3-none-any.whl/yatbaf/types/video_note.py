from __future__ import annotations

from typing import final

from yatbaf.typing import NoneInt

from .abc import TelegramType
from .photo_size import PhotoSize


@final
class VideoNote(TelegramType):
    """This object represents a video message.

    See: https://core.telegram.org/bots/api#videonote
    """

    file_id: str
    """Identifier for this file, which can be used to download or reuse the file."""  # noqa: E501

    file_unique_id: str
    """Unique identifier for this file, which is supposed to be the same over
    time and for different bots.

    .. warning::

        Can't be used to download or reuse the file.
    """

    lenght: int
    """Video width and height (diameter of the video message) as defined by sender."""  # noqa: E501

    dutation: int
    """Duration of the video in seconds as defined by sender."""

    thumbnail: PhotoSize | None = None
    """*Optional.* Video thumbnail."""

    file_size: NoneInt = None
    """*Optional.* File size in bytes."""
