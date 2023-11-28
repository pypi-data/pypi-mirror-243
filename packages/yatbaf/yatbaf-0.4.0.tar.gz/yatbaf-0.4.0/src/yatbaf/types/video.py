from __future__ import annotations

from typing import final

from yatbaf.typing import NoneInt
from yatbaf.typing import NoneStr

from .abc import TelegramType
from .photo_size import PhotoSize


@final
class Video(TelegramType):
    """This object represents a video file.

    See: https://core.telegram.org/bots/api#video
    """

    file_id: str
    """Identifier for this file, which can be used to download or reuse the file."""  # noqa: E501

    file_unique_id: str
    """Unique identifier for this file, which is supposed to be the same over
    time and for different bots.

    .. warning::

        Can't be used to download or reuse the file.
    """

    width: int
    """Video width as defined by sender."""

    height: int
    """Video height as defined by sender."""

    duration: int
    """Duration of the video in seconds as defined by sender."""

    thumbnail: PhotoSize | None = None
    """*Optional.* Video thumbnail."""

    file_name: NoneStr = None
    """*Optional.* Original filename as defined by sender."""

    mime_type: NoneStr = None
    """*Optional.* MIME type of the file as defined by sender."""

    file_size: NoneInt = None
    """*Optional.* File size in bytes."""
