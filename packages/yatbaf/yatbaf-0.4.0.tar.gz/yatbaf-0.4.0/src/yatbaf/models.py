from __future__ import annotations

__all__ = (
    "ResponseError",
    "ResponseOk",
    "Request",
    "HTTPResponse",
    "UpdateInfo",
)

from dataclasses import dataclass
from typing import Any
from typing import Generic
from typing import TypeVar
from typing import final

from msgspec import Struct

from .types import ResponseParameters
from .typing import NoneStr
from .typing import UpdateT

T = TypeVar("T")


@final
class Request(Struct):
    """Request object"""

    url: str
    """URL."""

    method: str
    """Telegram method name."""

    data: dict[str, Any] | None = None
    """Request POST data."""

    files: dict[str, Any] | None = None
    """Request files."""

    content: bytes | None = None
    """Json (bytes) content"""

    headers: dict[str, str] | None = None
    """Request headers."""


@final
class HTTPResponse(Struct, Generic[T]):
    """This object represents HTTP response."""

    status_code: int
    """Request status code."""

    content: T
    """Response content."""


class ApiResponse(Struct):
    """Base object for api response.

    See: https://core.telegram.org/bots/api#making-requests
    """

    ok: bool
    """Request status."""


@final
class ResponseOk(ApiResponse, Generic[T]):
    """This object represents successful api response."""

    result: T
    """Result of the query."""

    description: NoneStr = None
    """Human-readable description of the result."""


@final
class ResponseError(ApiResponse):
    """This object represents unsuccessful api response."""

    error_code: int
    """HTTP status code."""

    description: str
    """Human-readable description of the error."""

    parameters: ResponseParameters | None = None
    """See :class:`yatbaf.types.ResponseParameters`."""


@dataclass(frozen=True)
class UpdateInfo(Generic[UpdateT]):
    id: int
    """Update id"""
    name: str
    """Update type"""
    content: UpdateT
    """Update content"""
