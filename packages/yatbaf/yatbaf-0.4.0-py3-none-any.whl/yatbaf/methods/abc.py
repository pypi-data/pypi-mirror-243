from __future__ import annotations

__all__ = (
    "TelegramMethod",
    "TelegramMethodWithFile",
    "TelegramMethodWithMedia",
)

from collections.abc import Iterable
from secrets import token_urlsafe
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar
from typing import Generic
from typing import cast
from typing import get_args

from msgspec import Struct
from msgspec import json as jsonlib
from msgspec import to_builtins

from yatbaf.typing import ResultModelT

if TYPE_CHECKING:
    from typing import TypeAlias

    from yatbaf.types import InputMedia
    from yatbaf.types import InputMediaAudio
    from yatbaf.types import InputMediaDocument
    from yatbaf.types import InputMediaPhoto
    from yatbaf.types import InputMediaVideo
    from yatbaf.typing import InputFile

Data: TypeAlias = "bytes | dict[str, Any]"
File: TypeAlias = "dict[str, Any]"
Encoded: TypeAlias = "tuple[Data | None, File | None]"

_json_encoder = jsonlib.Encoder()
_file_name_length = 12


class TelegramMethod(Struct, Generic[ResultModelT], omit_defaults=True):
    """Base class for methods"""

    __meth_name__: ClassVar[str]
    __meth_result_model__: ClassVar[Any]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)

        # Skip for `Telegram*` subclasses
        if cls.__name__.startswith("Telegram"):
            return

        cls.__meth_name__ = cls.__name__.lower()
        cls.__meth_result_model__ = (
            get_args(cls.__orig_bases__[0])[0]  # type: ignore[attr-defined]
        )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"

    def __str__(self) -> str:
        return self.__meth_name__

    @classmethod
    def _get_name(cls) -> str:
        return cls.__meth_name__

    @classmethod
    def _get_result_model(cls) -> type[ResultModelT]:
        return cast("type[ResultModelT]", cls.__meth_result_model__)

    def _encode_params(self) -> Encoded:
        json = j if (j := _json_encoder.encode(self)) != b"{}" else None
        return (json, None)


class TelegramMethodWithFile(TelegramMethod, Generic[ResultModelT]):
    """Base class for methods with file field"""

    __meth_file_fields__: ClassVar[tuple[str, ...]]

    def _encode_params(self) -> Encoded:
        files: dict[str, InputFile] = {}
        for field in self.__meth_file_fields__:
            if ((value := getattr(self, field)) is None
                    or isinstance(value, str)):
                continue

            file_name = token_urlsafe(_file_name_length)
            files[file_name] = value
            setattr(self, field, f"attach://{file_name}")

        # no files or it's `file_id`
        if not files:
            return super()._encode_params()

        data = to_builtins(self)
        return (data, files)


class TelegramMethodWithMedia(TelegramMethod, Generic[ResultModelT]):
    """Base class for methods with media field"""

    # yapf: disable
    media: InputMedia | list[InputMediaAudio | InputMediaDocument | InputMediaPhoto | InputMediaVideo]  # noqa: E501
    # yapf: enable

    def _encode_params(self) -> Encoded:
        files: dict[str, InputFile] = {}

        media: Iterable[InputMedia] = (
            self.media if isinstance(self.media, Iterable) else (self.media,)
        )

        for row in media:
            fields: tuple[str, ...] = ("media", "thumbnail")

            # InputMediaPhoto has no `thumbnail`
            if row.type == "photo":
                fields = ("media",)

            for field in fields:
                if ((value := getattr(row, field)) is None
                        or isinstance(value, str)):
                    continue

                file_name = token_urlsafe(_file_name_length)
                files[file_name] = value
                setattr(row, field, f"attach://{file_name}")

        if not files:
            return super()._encode_params()

        data = to_builtins(self)
        return (data, files)
