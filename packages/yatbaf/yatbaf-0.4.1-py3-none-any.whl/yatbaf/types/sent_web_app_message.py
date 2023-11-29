from __future__ import annotations

from typing import final

from yatbaf.typing import NoneStr

from .abc import TelegramType


@final
class SentWebAppMessage(TelegramType):
    """Describes an inline message sent by a Web App on behalf of a user.

    See: https://core.telegram.org/bots/api#sentwebappmessage
    """

    inline_message_id: NoneStr = None
    """*Optional.* Identifier of the sent inline message. Available only if
    there is an inline keyboard attached to the message.
    """
