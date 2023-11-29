from __future__ import annotations

from typing import final

from yatbaf.typing import NoneInt
from yatbaf.typing import NoneStr

from .abc import TelegramType
from .photo_size import PhotoSize


@final
class Document(TelegramType):
    """This object represents a general file (as opposed to photos, voice
    messages and audio files).

    See: https://core.telegram.org/bots/api#document
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

    thumbnail: PhotoSize | None = None
    """*Optional.* Document thumbnail as defined by sender."""

    file_name: NoneStr = None
    """*Optional.* Original filename as defined by sender."""

    mime_type: NoneStr = None
    """*Optional.* MIME type of the file as defined by sender."""

    file_size: NoneInt = None
    """*Optional.* File size in bytes."""
