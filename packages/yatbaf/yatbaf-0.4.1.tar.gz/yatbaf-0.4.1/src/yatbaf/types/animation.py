from __future__ import annotations

from typing import final

from yatbaf.typing import NoneInt
from yatbaf.typing import NoneStr

from .abc import TelegramType
from .photo_size import PhotoSize


@final
class Animation(TelegramType):
    """This object represents an animation file
    (GIF or H.264/MPEG-4 AVC video without sound).

    See: https://core.telegram.org/bots/api#animation
    """

    file_id: str
    """identifier for this file, which can be used to download or reuse the file."""  # noqa: E501

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

    dutation: int
    """Duration of the video in seconds as defined by sender."""

    thumbnail: PhotoSize | None = None
    """*Optional* Animation thumbnail as defined by sender."""

    file_name: NoneStr = None
    """*Optional* Original animation filename as defined by sender."""

    mime_type: NoneStr = None
    """*Optional* MIME type of the file as defined by sender."""

    file_size: NoneInt = None
    """*Optional* File size in bytes. It can be bigger than 2^31 and some
    programming languages may have difficulty/silent defects in interpreting it.
    But it has at most 52 significant bits, so a signed 64-bit integer or
    double-precision float type are safe for storing this value.
    """
