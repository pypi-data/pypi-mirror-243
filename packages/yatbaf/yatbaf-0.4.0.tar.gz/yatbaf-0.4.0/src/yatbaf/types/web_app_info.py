from __future__ import annotations

from typing import final

from .abc import TelegramType


@final
class WebAppInfo(TelegramType):
    """Describes a Web App.

    See: https://core.telegram.org/bots/api#webappinfo
    """

    url: str
    """An HTTPS URL of a Web App to be opened with additional data as specified
    in Initializing Web Apps.
    """
