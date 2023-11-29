from __future__ import annotations

from typing import final

from yatbaf.typing import NoneInt
from yatbaf.typing import NoneStr

from .abc import TelegramType
from .photo_size import PhotoSize


@final
class Audio(TelegramType):
    """This object represents an audio file to be treated as music by the
    Telegram clients.

    See: https://core.telegram.org/bots/api#audio
    """

    file_id: str
    """
    Identifier for this file, which can be used to download or reuse the file.
    """

    file_unique_id: str
    """Unique identifier for this file, which is supposed to be the same over
    time and for different bots.

    .. warning::

        Can't be used to download or reuse the file.
    """

    dutation: int
    """Duration of the audio in seconds as defined by sender."""

    performer: NoneStr = None
    """*Optional.*
    Performer of the audio as defined by sender or by audio tags.
    """

    title: NoneStr = None
    """*Optional.* Title of the audio as defined by sender or by audio tags."""

    file_name: NoneStr = None
    """*Optional.* Original filename as defined by sender."""

    mime_type: NoneStr = None
    """*Optional.* MIME type of the file as defined by sender."""

    file_size: NoneInt = None
    """*Optional.* File size in bytes."""

    thumbnail: PhotoSize | None = None
    """*Optional.*
    Thumbnail of the album cover to which the music file belongs.
    """
