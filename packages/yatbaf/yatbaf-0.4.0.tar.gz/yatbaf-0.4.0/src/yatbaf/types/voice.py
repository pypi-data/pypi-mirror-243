from __future__ import annotations

from typing import final

from yatbaf.typing import NoneInt
from yatbaf.typing import NoneStr

from .abc import TelegramType


@final
class Voice(TelegramType):
    """This object represents a voice note.

    See: https://core.telegram.org/bots/api#voice
    """

    file_id: str
    """Identifier for this file, which can be used to download or reuse the file."""  # noqa: E501

    file_unique_id: str
    """Unique identifier for this file, which is supposed to be the same over
    time and for different bots. Can't be used to download or reuse the file.
    """

    dutation: int
    """Duration of the audio in seconds as defined by sender."""

    mime_type: NoneStr = None
    """*Optional.* MIME type of the file as defined by sender"""

    file_size: NoneInt = None
    """*Optional.* File size in bytes."""
