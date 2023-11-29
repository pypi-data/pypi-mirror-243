from __future__ import annotations

from typing import final

from yatbaf.typing import NoneBool
from yatbaf.typing import NoneStr

from .abc import TelegramType


@final
class WriteAccessAllowed(TelegramType):
    """This object represents a service message about a user allowing a bot to
    write messages after adding the bot to the attachment menu or launching a
    Web App from a link.

    See: https://core.telegram.org/bots/api#writeaccessallowed
    """

    from_request: NoneBool = None
    """*Optional.* ``True``, if the access was granted after the user accepted
    an explicit request from a Web App sent by the method requestWriteAccess.
    """

    web_app_name: NoneStr = None
    """*Optional.* Name of the Web App which was launched from a link."""

    from_attachment_menu: NoneBool = None
    """*Optional.* ``True``, if the access was granted when the bot was added
    to the attachment or side menu.
    """
