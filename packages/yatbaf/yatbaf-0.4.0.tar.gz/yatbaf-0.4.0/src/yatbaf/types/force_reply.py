from __future__ import annotations

from typing import final

from yatbaf.typing import NoneBool
from yatbaf.typing import NoneStr

from .abc import TelegramType


@final
class ForceReply(TelegramType):
    """Upon receiving a message with this object, Telegram clients will display
    a reply interface to the user (act as if the user has selected the bot's
    message and tapped 'Reply').

    See: https://core.telegram.org/bots/api#forcereply
    https://core.telegram.org/bots/features#privacy-mode
    """

    force_reply: bool
    """Shows reply interface to the user, as if they manually selected the
    bot's message and tapped 'Reply'.
    """

    input_field_placeholder: NoneStr = None
    """*Optional.* The placeholder to be shown in the input field when the reply
    is active.

    .. note::

        1-64 characters.
    """

    selective: NoneBool = None
    """*Optional.* Use this parameter if you want to force reply from specific
    users only. Targets: 1) users that are ``@mentioned`` in the text of the
    :class:`yatbaf.types.Message` object; 2) if the bot's message is a reply
    (has ``reply_to_message_id``), sender of the original message.
    """
