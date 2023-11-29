from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramType

if TYPE_CHECKING:
    from yatbaf.enums import ParseMode
    from yatbaf.typing import NoneBool

    from .message_entity import MessageEntity


@final
class InputTextMessageContent(TelegramType):
    """Represents the content of a text message to be sent as the result of an
    inline query.

    See: https://core.telegram.org/bots/api#inputtextmessagecontent
    """

    message_text: str
    """Text of the message to be sent, 1-4096 characters."""

    parse_mode: ParseMode | None = None
    """*Optional.* Mode for parsing entities in the message text."""

    entities: list[MessageEntity] | None = None
    """*Optional.* List of special entities that appear in message text, which
    can be specified instead of ``parse_mode``.
    """

    disable_web_page_preview: NoneBool = None
    """*Optional.* Disables link previews for links in the sent message."""
