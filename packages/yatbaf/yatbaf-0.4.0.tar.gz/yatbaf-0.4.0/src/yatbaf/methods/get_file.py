from __future__ import annotations

from typing import final

from yatbaf.types import File

from .abc import TelegramMethod


@final
class GetFile(TelegramMethod[File]):
    """See :meth:`yatbaf.bot.Bot.get_file`"""

    file_id: str
