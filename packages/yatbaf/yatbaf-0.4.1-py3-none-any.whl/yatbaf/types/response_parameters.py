from __future__ import annotations

from typing import final

from yatbaf.typing import NoneInt

from .abc import TelegramType


@final
class ResponseParameters(TelegramType):
    """Describes why a request was unsuccessful.

    See: https://core.telegram.org/bots/api#responseparameters
    """

    migrate_to_chat_id: NoneInt = None
    """*Optional.* The group has been migrated to a supergroup with the
    specified identifier.
    """

    retry_after: NoneInt = None
    """*Optional.* In case of exceeding flood control, the number of seconds
    left to wait before the request can be repeated.
    """
