from __future__ import annotations

from typing import final

from yatbaf.typing import NoneInt

from .abc import TelegramType


@final
class PhotoSize(TelegramType):
    """This object represents one size of a photo or a file / sticker thumbnail.

    See: https://core.telegram.org/bots/api#photosize
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
    """Photo width."""

    height: int
    """Photo height."""

    file_size: NoneInt = None
    """*Optional.* File size in bytes."""
