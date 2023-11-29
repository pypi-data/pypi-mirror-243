from __future__ import annotations

from typing import final

from yatbaf.typing import NoneBool
from yatbaf.typing import NoneStr

from .abc import TelegramType


@final
class LoginUrl(TelegramType):
    """This object represents a parameter of the inline keyboard button used to
    automatically authorize a user.

    See: https://core.telegram.org/bots/api#loginurl
    """

    url: str
    """An HTTPS URL to be opened with user authorization data added to the query
    string when the button is pressed. If the user refuses to provide
    authorization data, the original URL without information about the user will
    be opened. The data added is the same as described in `Receiving
    authorization data`_.

    .. _Receiving authorization data: https://core.telegram.org/widgets/login#receiving-authorization-data
    """  # noqa: E501

    forward_text: NoneStr = None
    """*Optional.* New text of the button in forwarded messages."""

    bot_username: NoneStr = None
    """*Optional.* Username of a bot, which will be used for user authorization.
    See `Setting up a bot`_ for more details. If not specified, the current
    bot's username will be assumed. The ``url``'s domain must be the same as the
    domain linked with the bot. See `Linking your domain to the bot`_ for more details.

    .. _Setting up a bot: https://core.telegram.org/widgets/login#setting-up-a-bot
    .. _Linking your domain to the bot: https://core.telegram.org/widgets/login#linking-your-domain-to-the-bot
    """  # noqa: E501

    request_write_access: NoneBool = None
    """*Optional.* Pass ``True`` to request the permission for your bot to send
    messages to the user.
    """
