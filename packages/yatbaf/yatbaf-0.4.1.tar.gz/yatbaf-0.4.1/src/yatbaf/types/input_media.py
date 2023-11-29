from __future__ import annotations

__all__ = (
    "InputMedia",
    "InputMediaAnimation",
    "InputMediaAudio",
    "InputMediaDocument",
    "InputMediaPhoto",
    "InputMediaVideo",
)

from typing import TYPE_CHECKING
from typing import Literal
from typing import TypeAlias
from typing import final

from msgspec import field

from .abc import TelegramType

if TYPE_CHECKING:
    from yatbaf.enums import ParseMode
    from yatbaf.typing import InputFile
    from yatbaf.typing import NoneBool
    from yatbaf.typing import NoneInt
    from yatbaf.typing import NoneStr

    from .message_entity import MessageEntity


@final
class InputMediaPhoto(TelegramType):
    """Represents a photo to be sent.

    See: https://core.telegram.org/bots/api#inputmediaphoto
    """

    media: str | InputFile
    """File to send."""

    caption: NoneStr = None
    """*Optional.* Caption of the photo to be sent, 0-1024 characters after
    entities parsing.
    """

    parse_mode: ParseMode | None = None
    """*Optional.* Mode for parsing entities in the photo caption."""

    caption_entities: list[MessageEntity] | None = None
    """*Optional.* List of special entities that appear in the caption, which
    can be specified instead of ``parse_mode``.
    """

    has_spoiler: NoneBool = None
    """*Optional.* Pass ``True`` if the photo needs to be covered with a
    spoiler animation.
    """

    type: Literal["photo"] = field(default_factory=lambda: "photo")
    """Type of the result, must be photo."""


@final
class InputMediaAudio(TelegramType):
    """Represents an audio file to be treated as music to be sent.

    See: https://core.telegram.org/bots/api#inputmediaaudio
    """

    media: str | InputFile
    """File to send."""

    thumbnail: InputFile | str | None = None
    """Optional. Thumbnail of the file sent."""

    caption: NoneStr = None
    """*Optional.* Caption of the audio to be sent, 0-1024 characters after
    entities parsing.
    """

    parse_mode: ParseMode | None = None
    """*Optional.* Mode for parsing entities in the audio caption. See
    formatting options for more details.
    """

    caption_entities: list[MessageEntity] | None = None
    """*Optional.* List of special entities that appear in the caption, which
    can be specified instead of ``parse_mode``.
    """

    duration: NoneInt = None
    """*Optional.* Duration of the audio in seconds."""

    performer: NoneStr = None
    """*Optional.* Performer of the audio."""

    title: NoneStr = None
    """*Optional.* Title of the audio."""

    type: Literal["audio"] = field(default_factory=lambda: "audio")
    """Type of the result, must be audio."""


@final
class InputMediaVideo(TelegramType):
    """Represents a video to be sent.

    See: https://core.telegram.org/bots/api#inputmediavideo
    """

    media: str | InputFile
    """File to send."""

    thumbnail: InputFile | str | None = None
    """*Optional.* Thumbnail of the file sent; can be ignored if thumbnail
    generation for the file is supported server-side. The thumbnail should be
    in JPEG format and less than 200 kB in size. A thumbnail's width and height
    should not exceed 320.
    """

    caption: NoneStr = None
    """*Optional.* Caption of the video to be sent, 0-1024 characters after
    entities parsing.
    """

    parse_mode: ParseMode | None = None
    """*Optional.* Mode for parsing entities in the video caption."""

    caption_entities: list[MessageEntity] | None = None
    """*Optional.* List of special entities that appear in the caption, which
    can be specified instead of ``parse_mode``.
    """

    width: NoneInt = None
    """*Optional.* Video width."""

    height: NoneInt = None
    """*Optional.* Video height."""

    duration: NoneInt = None
    """*Optional.* Video duration in seconds."""

    supports_streaming: NoneBool = None
    """
    *Optional.* Pass ``True`` if the uploaded video is suitable for streaming.
    """

    has_spoiler: NoneBool = None
    """*Optional.* Pass ``True`` if the video needs to be covered with a
    spoiler animation.
    """

    type: Literal["video"] = field(default_factory=lambda: "video")
    """Type of the result, must be video."""


@final
class InputMediaDocument(TelegramType):
    """Represents a general file to be sent.

    See: https://core.telegram.org/bots/api#inputmediadocument
    """

    media: str | InputFile
    """File to send."""

    thumbnail: InputFile | str | None = None
    """*Optional.* Thumbnail of the file sent; can be ignored if thumbnail
    generation for the file is supported server-side. The thumbnail should be
    in JPEG format and less than 200 kB in size. A thumbnail's width and height
    should not exceed 320.
    """

    caption: NoneStr = None
    """*Optional.* Caption of the document to be sent, 0-1024 characters after
    entities parsing.
    """

    parse_mode: ParseMode | None = None
    """*Optional.* Mode for parsing entities in the document caption."""

    caption_entities: list[MessageEntity] | None = None
    """*Optional.* List of special entities that appear in the caption, which
    can be specified instead of ``parse_mode``.
    """

    disable_content_type_detection: NoneBool = None
    """*Optional.* Disables automatic server-side content type detection for
    files uploaded using multipart/form-data. Always ``True``, if the document
    is sent as part of an album.
    """

    type: Literal["document"] = field(default_factory=lambda: "document")
    """Type of the result, must be document."""


@final
class InputMediaAnimation(TelegramType):
    """Represents an animation file (GIF or H.264/MPEG-4 AVC video without
    sound) to be sent.

    See: https://core.telegram.org/bots/api#inputmediaanimation
    """

    media: str | InputFile
    """File to send."""

    thumbnail: InputFile | str | None = None
    """*Optional.* Thumbnail of the file sent."""

    caption: NoneStr = None
    """*Optional.* Caption of the animation to be sent, 0-1024 characters after
    entities parsing.
    """

    parse_mode: ParseMode | None = None
    """*Optional.* Mode for parsing entities in the animation caption. See
    formatting options for more details.
    """

    caption_entities: list[MessageEntity] | None = None
    """*Optional.* List of special entities that appear in the caption, which
    can be specified instead of ``parse_mode``.
    """

    width: NoneInt = None
    """*Optional.* Animation width."""

    height: NoneInt = None
    """*Optional.* Animation height."""

    duration: NoneInt = None
    """*Optional.* Animation duration in seconds."""

    has_spoiler: NoneBool = None
    """*Optional.* Pass ``True`` if the animation needs to be covered with a
    spoiler animation.
    """

    type: Literal["animation"] = field(default_factory=lambda: "animation")
    """Type of the result, must be animation."""


# https://core.telegram.org/bots/api#inputmedia
InputMedia: TypeAlias = (
    "InputMediaAnimation "
    "| InputMediaAudio "
    "| InputMediaDocument "
    "| InputMediaPhoto "
    "| InputMediaVideo"
)
