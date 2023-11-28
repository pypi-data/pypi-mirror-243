from __future__ import annotations

__all__ = [
    "parse_command",
    "decode_content",
    "build_decoder",
]

import re
from typing import TYPE_CHECKING
from typing import TypeVar

from msgspec import DecodeError
from msgspec.json import Decoder

from .exceptions import InvalidTokenError
from .exceptions import JSONDecodeError
from .models import ResponseError
from .models import ResponseOk
from .types import Update

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Sequence

    from .methods.abc import TelegramMethod
    from .typing import ResultModelT

    F = TypeVar("F", bound=Callable)

    def lru_cache(
        maxsize: int = 128,  # noqa: U100
        typed: bool = False,  # noqa: U100
    ) -> Callable[[F], F]:
        pass
else:
    from functools import lru_cache

T = TypeVar("T")


def parse_command(text: str) -> str | None:
    """Parse bot command.

    :param text: Message text.
    """

    if not text.startswith("/") or text == "/":
        return None

    return text.removeprefix("/").split("@")[0].split(maxsplit=1)[0].lower()


def decode_content(content: bytes, decoder: Decoder[T]) -> T:
    """Decode content.

    :meta private:
    :param content: Raw content.
    :param decoder: Decoder object.
    """

    try:
        return decoder.decode(content)
    except DecodeError as error:
        raise JSONDecodeError(
            message=str(error),
            raw_content=content,
        ) from None


@lru_cache(maxsize=10)
def build_decoder(model: type[T]) -> Decoder[T]:
    return Decoder(model)


def decode_response(
    method: TelegramMethod[ResultModelT],
    content: bytes,
    decoder: Decoder[ResponseOk[ResultModelT]] | None = None,
) -> ResponseOk[ResultModelT]:
    """Decode response content.

    :meta private:
    :param method: TelegramMethod object.
    :param content: Response raw content.
    :param decoder: *Optional.* Decoder object.
    """

    if decoder is None:
        model = method._get_result_model()
        decoder = build_decoder(ResponseOk[model])  # type: ignore[valid-type]
    return decode_content(content, decoder)


def decode_webhook(content: bytes) -> Update:
    """Decode webhook content.

    :meta private:
    :param content: Request raw content.
    """

    decoder = build_decoder(Update)
    return decode_content(content, decoder)


def decode_error(content: bytes) -> ResponseError:
    """Decode response error.

    :meta private:
    """

    decoder = build_decoder(ResponseError)
    return decode_content(content, decoder)


DEEPLINK_PAYLOAD_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{,64}$")
USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_]{4,}$")


def is_valid_username(username: str, /) -> bool:
    return bool(USERNAME_PATTERN.match(username))


def is_valid_deeplink_parameter(param: str, /) -> bool:
    return bool(DEEPLINK_PAYLOAD_PATTERN.match(param))


def extract_bot_id(token: str) -> int:
    try:
        return int(token.split(":")[0])
    except ValueError:
        raise InvalidTokenError() from None


def ensure_unique(objs: Sequence[T]) -> list[T]:
    tmp: list[T] = []

    for obj in objs:
        if obj not in tmp:
            tmp.append(obj)
    return tmp
