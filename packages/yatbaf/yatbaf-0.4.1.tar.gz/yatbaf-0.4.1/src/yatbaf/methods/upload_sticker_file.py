from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import final

from yatbaf.types import File

from .abc import TelegramMethodWithFile

if TYPE_CHECKING:
    from yatbaf.enums import StickerFormat
    from yatbaf.typing import InputFile


@final
class UploadStickerFile(TelegramMethodWithFile[File]):
    """See :meth:`yatbaf.bot.Bot.upload_sticker_file`"""

    user_id: int
    sticker: InputFile
    sticker_format: StickerFormat

    __meth_file_fields__: ClassVar[tuple[str, ...]] = ("sticker",)
