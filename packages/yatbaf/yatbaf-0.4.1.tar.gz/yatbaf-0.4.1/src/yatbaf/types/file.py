from __future__ import annotations

from typing import final

from yatbaf.typing import NoneInt
from yatbaf.typing import NoneStr

from .abc import TelegramType


@final
class File(TelegramType):
    """This object represents a file ready to be downloaded.

    See: https://core.telegram.org/bots/api#file,
    :meth:`~yatbaf.bot.Bot.get_file`, :meth:`~yatbaf.bot.Bot.download_file`
    """

    file_id: str
    """Identifier for this file, which can be used to download or reuse the file."""  # noqa: E501

    file_unique_id: str
    """Unique identifier for this file, which is supposed to be the same over
    time and for different bots.

    .. warning::

        Can't be used to download or reuse the file.
    """

    file_size: NoneInt = None
    """*Optional.* File size in bytes."""

    file_path: NoneStr = None
    """*Optional.* File path."""
