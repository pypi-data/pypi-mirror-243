from __future__ import annotations

__all__ = (
    "InlineQueryResult",
    "InlineQueryResultArticle",
    "InlineQueryResultAudio",
    "InlineQueryResultsButton",
    "InlineQueryResultCachedAudio",
    "InlineQueryResultCachedDocument",
    "InlineQueryResultCachedGif",
    "InlineQueryResultCachedMpeg4Gif",
    "InlineQueryResultCachedPhoto",
    "InlineQueryResultCachedSticker",
    "InlineQueryResultCachedVideo",
    "InlineQueryResultCachedVoice",
    "InlineQueryResultContact",
    "InlineQueryResultDocument",
    "InlineQueryResultGame",
    "InlineQueryResultGif",
    "InlineQueryResultLocation",
    "InlineQueryResultMpeg4Gif",
    "InlineQueryResultPhoto",
    "InlineQueryResultVenue",
    "InlineQueryResultVideo",
    "InlineQueryResultVoice",
)

from typing import Literal
from typing import TypeAlias
from typing import final

from msgspec import field

from yatbaf.enums import DocumentMimeType
from yatbaf.enums import ParseMode
from yatbaf.enums import ThumbnailMimeType
from yatbaf.enums import VideoMimeType
from yatbaf.typing import NoneBool
from yatbaf.typing import NoneInt
from yatbaf.typing import NoneStr

from .abc import TelegramType
from .inline_keyboard_markup import InlineKeyboardMarkup
from .input_message_content import InputMessageContent
from .message_entity import MessageEntity
from .web_app_info import WebAppInfo


@final
class InlineQueryResultGame(TelegramType):
    """Represents a Game.

    See: https://core.telegram.org/bots/api#inlinequeryresultgame
    """

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    game_short_name: str
    """Short name of the game."""

    reply_markup: InlineKeyboardMarkup | None = None
    """*Optional.* Inline keyboard attached to the message."""

    type: Literal["game"] = field(default_factory=lambda: "game")
    """Type of the result, must be `game`."""


@final
class InlineQueryResultPhoto(TelegramType):
    """Represents a link to a photo stored on the Telegram servers. By default,
    this photo will be sent by the user with an optional caption. Alternatively,
    you can use ``input_message_content`` to send a message with the specified
    content instead of the photo.

    See: https://core.telegram.org/bots/api#inlinequeryresultphoto
    """

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    photo_url: str
    """A valid URL of the photo. Photo must be in JPEG format. Photo size must
    not exceed 5MB.
    """

    thumbnail_url: str
    """URL of the thumbnail for the photo."""

    photo_width: NoneInt = None
    """*Optional.* Width of the photo."""

    photo_height: NoneInt = None
    """*Optional.* Height of the photo."""

    title: NoneStr = None
    """*Optional.* Title for the result."""

    description: NoneStr = None
    """*Optional.* Short description of the result."""

    caption: NoneStr = None
    """*Optional.* Caption of the photo to be sent, 0-1024 characters after
    entities parsing.
    """

    parse_mode: ParseMode | None = None
    """*Optional.* Mode for parsing entities in the photo caption. See
    formatting options for more details.
    """

    caption_entities: list[MessageEntity] | None = None
    """*Optional.* List of special entities that appear in the caption, which
    can be specified instead of ``parse_mode``.
    """

    reply_markup: InlineKeyboardMarkup | None = None
    """*Optional.* Inline keyboard attached to the message."""

    input_message_content: InputMessageContent | None = None
    """*Optional.* Content of the message to be sent instead of the photo."""

    type: Literal["photo"] = field(default_factory=lambda: "photo")
    """Type of the result, must be `photo`."""


@final
class InlineQueryResultAudio(TelegramType):
    """Represents a link to an MP3 audio file. By default, this audio file will
    be sent by the user. Alternatively, you can use ``input_message_content``
    to send a message with the specified content instead of the audio.

    See: https://core.telegram.org/bots/api#inlinequeryresultaudio
    """

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    audio_url: str
    """A valid URL for the audio file."""

    title: str
    """Title."""

    caption: str | None = None
    """*Optional.* Caption, 0-1024 characters after entities parsing."""

    parse_mode: ParseMode | None = None
    """*Optional.* Mode for parsing entities in the audio caption."""

    caption_entities: list[MessageEntity] | None = None
    """*Optional.* List of special entities that appear in the caption, which
    can be specified instead of ``parse_mode``.
    """

    performer: NoneStr = None
    """*Optional.* Performer."""

    audio_duration: NoneInt = None
    """*Optional.* Audio duration in seconds."""

    reply_markup: InlineKeyboardMarkup | None = None
    """*Optional.* Inline keyboard attached to the message."""

    input_message_content: InputMessageContent | None = None
    """*Optional.* Content of the message to be sent instead of the audio."""

    type: Literal["audio"] = field(default_factory=lambda: "audio")
    """Type of the result, must be `audio`."""


@final
class InlineQueryResultVoice(TelegramType):
    """Represents a link to a voice recording in an .OGG container encoded with
    OPUS. By default, this voice recording will be sent by the user.
    Alternatively, you can use ``input_message_content`` to send a message with
    the specified content instead of the the voice message.

    See: https://core.telegram.org/bots/api#inlinequeryresultvoice
    """

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    voice_url: str
    """A valid URL for the voice recording."""

    title: str
    """Recording title."""

    caption: NoneStr = None
    """*Optional.* Caption, 0-1024 characters after entities parsing."""

    parse_mode: ParseMode | None = None
    """*Optional.* Mode for parsing entities in the voice message caption."""

    caption_entities: list[MessageEntity] | None = None
    """*Optional.* List of special entities that appear in the caption, which
    can be specified instead of ``parse_mode``."""

    voice_duration: NoneInt = None
    """*Optional.* Recording duration in seconds."""

    reply_markup: InlineKeyboardMarkup | None = None
    """*Optional.* Inline keyboard attached to the message."""

    input_message_content: InputMessageContent | None = None
    """*Optional.* Content of the message to be sent instead of the voice
    recording.
    """

    type: Literal["voice"] = field(default_factory=lambda: "voice")
    """Type of the result, must be `voice`."""


@final
class InlineQueryResultVenue(TelegramType):
    """Represents a venue. By default, the venue will be sent by the user.
    Alternatively, you can use ``input_message_content`` to send a message with
    the specified content instead of the venue.

    See: https://core.telegram.org/bots/api#inlinequeryresultvenue
    """

    id: str
    """Unique identifier for this result, 1-64 Bytes."""

    latitude: float
    """Latitude of the venue location in degrees."""

    longtitude: float
    """Longitude of the venue location in degrees."""

    address: str
    """Address of the venue."""

    thumbnail_url: str
    """*Optional.* Url of the thumbnail for the result."""

    title: NoneStr = None
    """Title of the venue."""

    foursquare_id: NoneInt = None
    """*Optional.* Foursquare identifier of the venue if known."""

    foursquare_type: NoneStr = None
    """*Optional.* Foursquare type of the venue, if known."""

    google_place_id: NoneStr = None
    """*Optional.* Google Places identifier of the venue."""

    google_place_type: NoneStr = None
    """*Optional.* Google Places type of the venue."""

    reply_markup: InlineKeyboardMarkup | None = None
    """*Optional.* Inline keyboard attached to the message."""

    input_message_content: InputMessageContent | None = None
    """*Optional.* Content of the message to be sent instead of the venue."""

    thumbnail_width: NoneInt = None
    """*Optional.* Thumbnail width."""

    thumbnail_height: NoneInt = None
    """*Optional.* Thumbnail height."""

    type: Literal["venue"] = field(default_factory=lambda: "venue")
    """Type of the result, must be `venue`."""


@final
class InlineQueryResultVideo(TelegramType):
    """Represents a link to a page containing an embedded video player or a
    video file. By default, this video file will be sent by the user with an
    optional caption. Alternatively, you can use ``input_message_content`` to
    send a message with the specified content instead of the video.

    .. note::

        If an InlineQueryResultVideo message contains an embedded video
        (e.g., YouTube), you *must* replace its content using
        ``input_message_content``.

    See: https://core.telegram.org/bots/api#inlinequeryresultvideo
    """

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    video_url: str
    """A valid URL for the embedded video player or video file."""

    mime_type: VideoMimeType
    """MIME type of the content of the video URL, 'text/html' or 'video/mp4'."""

    thumbnail_url: str
    """URL of the thumbnail (JPEG only) for the video."""

    title: NoneStr = None
    """Title for the result."""

    caption: NoneStr = None
    """*Optional.* Caption of the video to be sent, 0-1024 characters after
    entities parsing.
    """

    parse_mode: ParseMode | None = None
    """*Optional.* Mode for parsing entities in the video caption. See
    formatting options for more details.
    """

    caption_entities: list[MessageEntity] | None = None
    """*Optional.* List of special entities that appear in the caption, which
    can be specified instead of ``parse_mode``.
    """

    video_width: NoneInt = None
    """*Optional.* Video width."""

    video_height: NoneInt = None
    """*Optional.* Video height."""

    video_duration: NoneInt = None
    """*Optional.* Video duration in seconds."""

    description: NoneStr = None
    """*Optional.* Short description of the result."""

    reply_markup: InlineKeyboardMarkup | None = None
    """*Optional.* Inline keyboard attached to the message."""

    input_message_content: InputMessageContent | None = None
    """*Optional.* Content of the message to be sent instead of the video. This
    field is *required* if InlineQueryResultVideo is used to send an HTML-page
    as a result (e.g., a YouTube video).
    """

    type: Literal["video"] = field(default_factory=lambda: "video")
    """Type of the result, must be `video`."""


@final
class InlineQueryResultArticle(TelegramType):
    """Represents a link to an article or web page.

    See: https://core.telegram.org/bots/api#inlinequeryresultarticle
    """

    id: str
    """Unique identifier for this result, 1-64 Bytes."""

    title: str
    """Title of the result."""

    input_message_content: InputMessageContent
    """Content of the message to be sent."""

    reply_markup: InlineKeyboardMarkup | None = None
    """Optional. Inline keyboard attached to the message."""

    url: NoneStr = None
    """*Optional.* URL of the result."""

    hide_url: NoneBool = None
    """*Optional.* Pass True if you don't want the URL to be shown in the
    message.
    """

    description: NoneStr = None
    """*Optional.* Short description of the result."""

    thumbnail_url: NoneStr = None
    """*Optional.* Url of the thumbnail for the result."""

    thumbnail_width: NoneInt = None
    """*Optional.* Thumbnail width."""

    thumbnail_height: NoneInt = None
    """*Optional.* Thumbnail height."""

    type: Literal["article"] = field(default_factory=lambda: "article")
    """Type of the result, must be `article`."""


@final
class InlineQueryResultContact(TelegramType):
    """Represents a contact with a phone number. By default, this contact will
    be sent by the user. Alternatively, you can use ``input_message_content``
    to send a message with the specified content instead of the contact.

    See: https://core.telegram.org/bots/api#inlinequeryresultcontact
    """

    id: str
    """Unique identifier for this result, 1-64 Bytes."""

    phone_number: str
    """Contact's phone number."""

    first_name: str
    """Contact's first name."""

    thumbnail_url: str
    """*Optional.* Url of the thumbnail for the result."""

    last_name: NoneStr = None
    """*Optional.* Contact's last name."""

    vcard: NoneStr = None
    """*Optional.* Additional data about the contact in the form of a vCard,
    0-2048 bytes.
    """

    reply_markup: InlineKeyboardMarkup | None = None
    """*Optional.* Inline keyboard attached to the message."""

    input_message_content: InputMessageContent | None = None
    """*Optional.* Content of the message to be sent instead of the contact."""

    thumbnail_width: NoneInt = None
    """*Optional.* Thumbnail width."""

    thumbnail_height: NoneInt = None
    """*Optional.* Thumbnail height."""

    type: Literal["contact"] = field(default_factory=lambda: "contact")
    """Type of the result, must be `contact`."""


@final
class InlineQueryResultLocation(TelegramType):
    """Represents a location on a map. By default, the location will be sent
    by the user. Alternatively, you can use ``input_message_content`` to send
    a message with the specified content instead of the location.

    See: https://core.telegram.org/bots/api#inlinequeryresultlocation
    """

    id: str
    """Unique identifier for this result, 1-64 Bytes."""

    latitude: float
    """Location latitude in degrees."""

    longtitude: float
    """Location longitude in degrees."""

    thumbnail_url: str
    """*Optional.* Url of the thumbnail for the result."""

    title: NoneStr = None
    """Location title."""

    horizontal_accuracy: float | None = None
    """*Optional.* The radius of uncertainty for the location, measured in
    meters; 0-1500.
    """

    live_period: int | None = None
    """*Optional.* Period in seconds for which the location can be updated,
    should be between 60 and 86400.
    """

    heading: int | None = None
    """*Optional.* For live locations, a direction in which the user is moving,
    in degrees. Must be between 1 and 360 if specified.
    """

    proximity_alert_radius: int | None = None
    """*Optional.* For live locations, a maximum distance for proximity alerts
    about approaching another chat member, in meters. Must be between 1 and
    100000 if specified.
    """

    reply_markup: InlineKeyboardMarkup | None = None
    """*Optional.* Inline keyboard attached to the message."""

    input_message_content: InputMessageContent | None = None
    """*Optional.* Content of the message to be sent instead of the location."""

    thumbnail_width: NoneInt = None
    """*Optional.* Thumbnail width."""

    thumbnail_height: NoneInt = None
    """*Optional.* Thumbnail height."""

    type: Literal["location"] = field(default_factory=lambda: "location")
    """Type of the result, must be `location`."""


@final
class InlineQueryResultDocument(TelegramType):
    """Represents a link to a file. By default, this file will be sent by the
    user with an optional caption. Alternatively, you can use
    ``input_message_content`` to send a message with the specified content
    instead of the file. Currently, only .PDF and .ZIP files can be sent using
    this method.

    See: https://core.telegram.org/bots/api#inlinequeryresultdocument
    """

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    title: str
    """Title for the result."""

    document_url: str
    """A valid URL for the file."""

    mime_type: DocumentMimeType
    """MIME type of the content of the file, either 'application/pdf' or
    'application/zip'.
    """

    caption: str | None = None
    """*Optional.* Caption of the document to be sent, 0-1024 characters after
    entities parsing.
    """

    parse_mode: ParseMode | None = None
    """*Optional.* Mode for parsing entities in the document caption."""

    caption_entities: list[MessageEntity] | None = None
    """*Optional.* List of special entities that appear in the caption, which
    can be specified instead of ``parse_mode``.
    """

    description: NoneStr = None
    """*Optional.* Short description of the result."""

    reply_markup: InlineKeyboardMarkup | None = None
    """*Optional.* Inline keyboard attached to the message."""

    input_message_content: InputMessageContent | None = None
    """*Optional.* Content of the message to be sent instead of the file."""

    thumbnail_url: NoneStr = None
    """*Optional.* URL of the thumbnail (JPEG only) for the file."""

    thumbnail_width: NoneInt = None
    """*Optional.* Thumbnail width."""

    thumbnail_height: NoneInt = None
    """*Optional.* Thumbnail height."""

    type: Literal["document"] = field(default_factory=lambda: "document")
    """Type of the result, must be `document`."""


@final
class InlineQueryResultMpeg4Gif(TelegramType):
    """Represents a link to a video animation (H.264/MPEG-4 AVC video without
    sound). By default, this animated MPEG-4 file will be sent by the user with
    optional caption. Alternatively, you can use ``input_message_content``
    to send a message with the specified content instead of the animation.

    See: https://core.telegram.org/bots/api#inlinequeryresultmpeg4gif
    """

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    mpeg4_url: str
    """A valid URL for the MPEG4 file. File size must not exceed 1MB."""

    thumbnail_url: str
    """URL of the static (JPEG or GIF) or animated (MPEG4) thumbnail for the
    result.
    """

    mpeg4_width: NoneInt = None
    """Optional. Video width."""

    mpeg4_height: NoneInt = None
    """Optional. Video height."""

    mpeg4_duration: NoneInt = None
    """Optional. Video duration in seconds."""

    thumbnail_mime_type: ThumbnailMimeType | None = None
    """*Optional.* MIME type of the thumbnail, must be one of 'image/jpeg',
    'image/gif', or 'video/mp4'. Defaults to 'image/jpeg'.
    """

    title: NoneStr = None
    """Optional. Title for the result."""

    caption: NoneStr = None
    """*Optional.* Caption of the MPEG-4 file to be sent, 0-1024 characters
    after entities parsing.
    """

    parse_mode: ParseMode | None = None
    """*Optional.* Mode for parsing entities in the caption."""

    caption_entities: list[MessageEntity] | None = None
    """*Optional.* List of special entities that appear in the caption, which
    can be specified instead of ``parse_mode``.
    """

    reply_markup: InlineKeyboardMarkup | None = None
    """*Optional.* Inline keyboard attached to the message."""

    input_message_content: InputMessageContent | None = None
    """*Optional.* Content of the message to be sent instead of the video
    animation.
    """

    type: Literal["mpeg4_gif"] = field(default_factory=lambda: "mpeg4_gif")
    """Type of the result, must be `mpeg4_gif`."""


@final
class InlineQueryResultCachedGif(TelegramType):
    """Represents a link to an animated GIF file stored on the Telegram servers.
    By default, this animated GIF file will be sent by the user with an optional
    caption. Alternatively, you can use ``input_message_content`` to send a
    message with specified content instead of the animation.

    See: https://core.telegram.org/bots/api#inlinequeryresultcachedgif
    """

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    gif_file_id: str
    """A valid file identifier for the GIF file."""

    title: NoneStr = None
    """*Optional.* Title for the result."""

    caption: str | None = None
    """*Optional.* Caption of the GIF file to be sent, 0-1024 characters after
    entities parsing.
    """

    parse_mode: ParseMode | None = None
    """*Optional.* Mode for parsing entities in the caption."""

    caption_entities: list[MessageEntity] | None = None
    """*Optional.* List of special entities that appear in the caption, which
    can be specified instead of ``parse_mode``.
    """

    reply_markup: InlineKeyboardMarkup | None = None
    """*Optional.* Inline keyboard attached to the message."""

    input_message_content: InputMessageContent | None = None
    """*Optional.* Content of the message to be sent instead of the GIF
    animation.
    """

    type: Literal["gif"] = field(default_factory=lambda: "gif")
    """Type of the result, must be `gif`."""


@final
class InlineQueryResultCachedPhoto(TelegramType):
    """Represents a link to a photo stored on the Telegram servers. By default,
    this photo will be sent by the user with an optional caption. Alternatively,
    you can use ``input_message_content`` to send a message with the specified
    content instead of the photo.

    See: https://core.telegram.org/bots/api#inlinequeryresultcachedphoto
    """

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    photo_file_id: str
    """A valid file identifier of the photo."""

    title: NoneStr = None
    """*Optional.* Title for the result."""

    description: NoneStr = None
    """*Optional.* Short description of the result."""

    caption: str | None = None
    """*Optional.* Caption of the photo to be sent, 0-1024 characters after
    entities parsing.
    """

    parse_mode: ParseMode | None = None
    """*Optional.* Mode for parsing entities in the photo caption."""

    caption_entities: list[MessageEntity] | None = None
    """*Optional.* List of special entities that appear in the caption, which
    can be specified instead of ``parse_mode``.
    """

    reply_markup: InlineKeyboardMarkup | None = None
    """*Optional.* Inline keyboard attached to the message."""

    input_message_content: InputMessageContent | None = None
    """*Optional.* Content of the message to be sent instead of the photo."""

    type: Literal["photo"] = field(default_factory=lambda: "photo")
    """Type of the result, must be photo."""


@final
class InlineQueryResultCachedVoice(TelegramType):
    """Represents a link to a voice message stored on the Telegram servers. By
    default, this voice message will be sent by the user. Alternatively, you can
    use ``input_message_content`` to send a message with the specified content
    instead of the voice message.

    See: https://core.telegram.org/bots/api#inlinequeryresultcachedvoice
    """

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    voice_file_id: str
    """A valid file identifier for the voice message."""

    title: str
    """Voice message title."""

    caption: str | None = None
    """*Optional.* Caption, 0-1024 characters after entities parsing."""

    parse_mode: ParseMode | None = None
    """*Optional.* Mode for parsing entities in the voice message caption."""

    caption_entities: list[MessageEntity] | None = None
    """*Optional.* List of special entities that appear in the caption, which
    can be specified instead of ``parse_mode``.
    """

    reply_markup: InlineKeyboardMarkup | None = None
    """*Optional.* Inline keyboard attached to the message."""

    input_message_content: InputMessageContent | None = None
    """*Optional.* Content of the message to be sent instead of the voice
    message.
    """

    type: Literal["voice"] = field(default_factory=lambda: "voice")
    """Type of the result, must be `voice`."""


@final
class InlineQueryResultCachedAudio(TelegramType):
    """Represents a link to an MP3 audio file stored on the Telegram servers.
    By default, this audio file will be sent by the user. Alternatively, you can
    use ``input_message_content`` to send a message with the specified content
    instead of the audio.

    See: https://core.telegram.org/bots/api#inlinequeryresultcachedaudio
    """

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    audio_file_id: str
    """A valid file identifier for the audio file."""

    caption: str | None = None
    """*Optional.* Caption, 0-1024 characters after entities parsing."""

    parse_mode: ParseMode | None = None
    """*Optional.* Mode for parsing entities in the audio caption."""

    caption_entities: list[MessageEntity] | None = None
    """*Optional.* List of special entities that appear in the caption, which
    can be specified instead of parse_mode.
    """

    reply_markup: InlineKeyboardMarkup | None = None
    """*Optional.* Inline keyboard attached to the message."""

    input_message_content: InputMessageContent | None = None
    """*Optional.* Content of the message to be sent instead of the audio."""

    type: Literal["audio"] = field(default_factory=lambda: "audio")
    """Type of the result, must be `audio`."""


@final
class InlineQueryResultCachedVideo(TelegramType):
    """Represents a link to a video file stored on the Telegram servers. By
    default, this video file will be sent by the user with an optional caption.
    Alternatively, you can use ``input_message_content`` to send a message with
    the specified content instead of the video.

    See: https://core.telegram.org/bots/api#inlinequeryresultcachedvideo
    """

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    video_file_id: str
    """A valid file identifier for the video file."""

    title: NoneStr = None
    """Title for the result."""

    description: NoneStr = None
    """*Optional.* Short description of the result."""

    caption: str | None = None
    """*Optional.* Caption of the video to be sent, 0-1024 characters after
    entities parsing.
    """

    parse_mode: ParseMode | None = None
    """*Optional.* Mode for parsing entities in the video caption."""

    caption_entities: list[MessageEntity] | None = None
    """*Optional.* List of special entities that appear in the caption, which
    can be specified instead of parse_mode.
    """

    reply_markup: InlineKeyboardMarkup | None = None
    """*Optional.* Inline keyboard attached to the message."""

    input_message_content: InputMessageContent | None = None
    """*Optional.* Content of the message to be sent instead of the video."""

    type: Literal["video"] = field(default_factory=lambda: "video")
    """Type of the result, must be `video`."""


@final
class InlineQueryResultCachedSticker(TelegramType):
    """Represents a link to a sticker stored on the Telegram servers. By
    default, this sticker will be sent by the user. Alternatively, you can use
    ``input_message_content`` to send a message with the specified content
    instead of the sticker.

    See: https://core.telegram.org/bots/api#inlinequeryresultcachedsticker
    """

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    sticker_file_id: str
    """A valid file identifier of the sticker."""

    reply_markup: InlineKeyboardMarkup | None = None
    """*Optional.* Inline keyboard attached to the message."""

    input_message_content: InputMessageContent | None = None
    """*Optional.* Content of the message to be sent instead of the sticker."""

    type: Literal["sticker"] = field(default_factory=lambda: "sticker")
    """Type of the result, must be `sticker`."""


@final
class InlineQueryResultCachedDocument(TelegramType):
    """Represents a link to a file stored on the Telegram servers. By default,
    this file will be sent by the user with an optional caption. Alternatively,
    you can use ``input_message_content`` to send a message with the specified
    content instead of the file.

    See: https://core.telegram.org/bots/api#inlinequeryresultcacheddocument
    """

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    title: str
    """Title for the result."""

    document_file_id: str
    """A valid file identifier for the file."""

    description: NoneStr = None
    """*Optional.* Short description of the result."""

    caption: str | None = None
    """*Optional.* Caption of the document to be sent, 0-1024 characters after
    entities parsing.
    """

    parse_mode: ParseMode | None = None
    """*Optional.* Mode for parsing entities in the document caption."""

    caption_entities: list[MessageEntity] | None = None
    """*Optional.* List of special entities that appear in the caption, which
    can be specified instead of ``parse_mode``.
    """

    reply_markup: InlineKeyboardMarkup | None = None
    """*Optional.* Inline keyboard attached to the message."""

    input_message_content: InputMessageContent | None = None
    """*Optional.* Content of the message to be sent instead of the file."""

    type: Literal["document"] = field(default_factory=lambda: "document")
    """Type of the result, must be `document`."""


@final
class InlineQueryResultCachedMpeg4Gif(TelegramType):
    """Represents a link to a video animation (H.264/MPEG-4 AVC video without
    sound) stored on the Telegram servers. By default, this animated MPEG-4 file
    will be sent by the user with an optional caption. Alternatively, you can
    use ``input_message_content`` to send a message with the specified content
    instead of the animation.

    See: https://core.telegram.org/bots/api#inlinequeryresultcachedmpeg4gif
    """

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    mpeg4_file_id: str
    """A valid file identifier for the MPEG4 file."""

    title: NoneStr = None
    """Optional. Title for the result."""

    caption: str | None = None
    """*Optional.* Caption of the MPEG-4 file to be sent, 0-1024 characters
    after entities parsing.
    """

    parse_mode: ParseMode | None = None
    """*Optional.* Mode for parsing entities in the caption."""

    caption_entities: list[MessageEntity] | None = None
    """*Optional.* List of special entities that appear in the caption, which
    can be specified instead of ``parse_mode``.
    """

    reply_markup: InlineKeyboardMarkup | None = None
    """*Optional.* Inline keyboard attached to the message."""

    input_message_content: InputMessageContent | None = None
    """*Optional.* Content of the message to be sent instead of the video
    animation.
    """

    type: Literal["mpeg4_gif"] = field(default_factory=lambda: "mpeg4_gif")
    """Type of the result, must be `mpeg4_gif`."""


@final
class InlineQueryResultGif(TelegramType):
    """Represents a link to an animated GIF file. By default, this animated GIF
    file will be sent by the user with optional caption. Alternatively, you can
    use ``input_message_content`` to send a message with the specified content
    instead of the animation.

    See: https://core.telegram.org/bots/api#inlinequeryresultgif
    """

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    gif_url: str
    """A valid URL for the GIF file. File size must not exceed 1MB."""

    thumbnail_url: str
    """URL of the static (JPEG or GIF) or animated (MPEG4) thumbnail for the
    result.
    """

    gif_width: NoneInt = None
    """Optional. Width of the GIF."""

    gif_height: NoneInt = None
    """Optional. Height of the GIF."""

    gif_duration: NoneInt = None
    """Optional. Duration of the GIF in seconds."""

    thumbnail_mime_type: ThumbnailMimeType | None = None
    """*Optional.* MIME type of the thumbnail."""

    title: NoneStr = None
    """*Optional.* Title for the result."""

    caption: str | None = None
    """*Optional.* Caption of the GIF file to be sent, 0-1024 characters after
    entities parsing.
    """

    parse_mode: ParseMode | None = None
    """*Optional.* Mode for parsing entities in the caption."""

    caption_entities: list[MessageEntity] | None = None
    """*Optional.* List of special entities that appear in the caption, which
    can be specified instead of ``parse_mode``.
    """

    reply_markup: InlineKeyboardMarkup | None = None
    """*Optional.* Inline keyboard attached to the message."""

    input_message_content: InputMessageContent | None = None
    """*Optional.* Content of the message to be sent instead of the GIF
    animation.
    """

    type: Literal["gif"] = field(default_factory=lambda: "gif")
    """Type of the result, must be `gif`."""


@final
class InlineQueryResultsButton(TelegramType):
    """This object represents a button to be shown above inline query results.
    You *must* use exactly one of the optional fields.

    See: https://core.telegram.org/bots/api#inlinequeryresultsbutton
    """

    text: str
    """Label text on the button."""

    web_app: WebAppInfo | None = None
    """*Optional.* Description of the Web App that will be launched when the
    user presses the button. The Web App will be able to switch back to the
    inline mode using the method switchInlineQuery inside the Web App.
    """

    start_parameter: NoneStr = None
    """*Optional.* Deep-linking parameter for the /start message sent to the
    bot when a user presses the button. 1-64 characters, only A-Z, a-z, 0-9, _
    and - are allowed.
    """


# https://core.telegram.org/bots/api#inlinequeryresult
InlineQueryResult: TypeAlias = (
    "InlineQueryResultArticle "
    "| InlineQueryResultAudio "
    "| InlineQueryResultCachedAudio "
    "| InlineQueryResultCachedDocument "
    "| InlineQueryResultCachedGif "
    "| InlineQueryResultCachedMpeg4Gif "
    "| InlineQueryResultCachedPhoto "
    "| InlineQueryResultCachedSticker "
    "| InlineQueryResultCachedVideo "
    "| InlineQueryResultCachedVoice "
    "| InlineQueryResultContact "
    "| InlineQueryResultDocument "
    "| InlineQueryResultGame "
    "| InlineQueryResultGif "
    "| InlineQueryResultLocation "
    "| InlineQueryResultMpeg4Gif "
    "| InlineQueryResultPhoto "
    "| InlineQueryResultVenue "
    "| InlineQueryResultVideo "
    "| InlineQueryResultVoice"
)
