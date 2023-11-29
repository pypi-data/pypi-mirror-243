from __future__ import annotations

__all__ = (
    "TelegramAPIException",
    "RequestTimeoutError",
    "RequestError",
    "BotException",
    "JSONDecodeError",
    "MethodInvokeError",
    "FileDownloadError",
    "FloodError",
    "ChatMigratedError",
    "InternalError",
    "TokenError",
    "WebhookConflictError",
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .methods.abc import TelegramMethod


class TelegramAPIException(Exception):
    """Base API exception"""


class TokenError(TelegramAPIException):
    """Wrong token. Status 401"""


class WebhookConflictError(TelegramAPIException):
    """Webhook/LongPolling conflict. Status 409"""


class InternalError(TelegramAPIException):
    """Internal server error. Status >= 500"""


class RequestTimeoutError(TelegramAPIException):
    """Request timed out."""

    def __init__(self, method: str, orig: Exception) -> None:
        """
        :param method: Telegram method name.
        :param orig: Original exception.
        """

        super().__init__(f"{method}, {orig}")
        self.method = method
        self.orig = orig


class RequestError(TelegramAPIException):
    """Response status gt 200."""

    def __init__(
        self,
        error_code: int,
        description: str,
    ) -> None:
        """
        :param error_code: HTTP status code.
        :param description: Error description.
        """

        super().__init__(f"{description} [{error_code}]")
        self.error_code = error_code
        self.description = description


class FileDownloadError(RequestError):
    pass


class MethodInvokeError(RequestError):

    def __init__(
        self,
        method: TelegramMethod,
        error_code: int,
        description: str,
    ) -> None:
        """
        :param method: TelegramMethod object.
        :param error_code: HTTP status code.
        :param description: Error description.
        """

        super().__init__(error_code, description)
        self.method = method


class ChatMigratedError(MethodInvokeError):
    """The group has been migrated to a supergroup."""

    def __init__(
        self,
        method: TelegramMethod,
        error_code: int,
        description: str,
        migrate_to_chat_id: int,
    ) -> None:
        """
        :param method: TelegramMethod object.
        :param error_code: HTTP status code.
        :param description: Error description.
        :param migrate_to_chat_id: Supergroup id.
        """

        super().__init__(method, error_code, description)
        self.migrate_to_chat_id = migrate_to_chat_id


class FloodError(MethodInvokeError):
    """Too Many Requests. Status 429"""

    def __init__(
        self,
        method: TelegramMethod,
        error_code: int,
        description: str,
        retry_after: int,
    ) -> None:
        """
        :param method: TelegramMethod object.
        :param error_code: HTTP status code.
        :param description: Error description.
        :param retry_after: The number of seconds left to wait before the
            request can be repeated.
        """

        super().__init__(method, error_code, description)
        self.retry_after = retry_after


class BotException(Exception):
    """Base bot exception"""


class JSONDecodeError(BotException):
    """Decode error."""

    def __init__(self, message: str, raw_content: bytes) -> None:
        """
        :param message: Error message.
        :param raw_content: Response content.
        """

        super().__init__(f"Fail while decoding response content: {message}")
        self.raw_content = raw_content


class InvalidTokenError(BotException):
    """Api token is invalid."""


"""
TelegramAPIException
 ├── TokenError
 ├── WebhookConflictError
 ├── InternalError
 ├── RequestTimeoutError
 └── RequestError
      ├── FileDownloadError
      └── MethodInvokeError
           ├── ChatMigratedError
           └── FloodError
BotException
 ├── JSONDecodeError
 └── InvalidTokenError
"""
