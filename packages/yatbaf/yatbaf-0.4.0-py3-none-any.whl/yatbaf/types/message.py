from __future__ import annotations

__all__ = ("Message",)

# from datetime import datetime

from typing import TYPE_CHECKING
from typing import final

from msgspec import field

from yatbaf.types import chat as _chat
from yatbaf.typing import NoneBool
from yatbaf.typing import NoneInt
from yatbaf.typing import NoneStr

from .abc import TelegramType
from .animation import Animation
from .audio import Audio
from .chat_shared import ChatShared
from .contact import Contact
from .dice import Dice
from .document import Document
from .forum_topic_closed import ForumTopicClosed
from .forum_topic_created import ForumTopicCreated
from .forum_topic_edited import ForumTopicEdited
from .forum_topic_reopened import ForumTopicReopened
from .game import Game
from .general_forum_topic_hidden import GeneralForumTopicHidden
from .general_forum_topic_unhidden import GeneralForumTopicUnhidden
from .inline_keyboard_markup import InlineKeyboardMarkup
from .invoice import Invoice
from .location import Location
from .message_auto_delete_timer_changed import MessageAutoDeleteTimerChanged
from .message_entity import MessageEntity
from .passport import PassportData
from .photo_size import PhotoSize
from .poll import Poll
from .proximity_alert_triggered import ProximityAlertTriggered
from .sticker import Sticker
from .story import Story
from .successful_payment import SuccessfulPayment
from .user import User
from .user_shared import UserShared
from .venue import Venue
from .video import Video
from .video_chat_ended import VideoChatEnded
from .video_chat_participants_invited import VideoChatParticipantsInvited
from .video_chat_scheduled import VideoChatScheduled
from .video_chat_started import VideoChatStarted
from .video_note import VideoNote
from .voice import Voice
from .web_app_data import WebAppData
from .write_access_allowed import WriteAccessAllowed

if TYPE_CHECKING:
    from yatbaf.enums import ParseMode
    from yatbaf.enums import PollType
    from yatbaf.types import InputMedia
    from yatbaf.types import InputMediaAudio
    from yatbaf.types import InputMediaDocument
    from yatbaf.types import InputMediaPhoto
    from yatbaf.types import InputMediaVideo
    from yatbaf.types import MessageId
    from yatbaf.typing import InputFile
    from yatbaf.typing import ReplyMarkup


@final
class Message(TelegramType, kw_only=True):
    """This object represents a message.

    See: https://core.telegram.org/bots/api#message
    """

    message_id: int
    """Unique message identifier inside this chat."""

    message_thread_id: NoneInt = None
    """*Optional.* Unique identifier of a message thread to which the message
    belongs.

    .. note::

        For supergroups only.
    """

    from_: User | None = field(name="from")
    """*Optional.* Sender of the message; empty for messages sent to channels.

    .. note::

        For backward compatibility, the field contains a fake sender user
        in non-channel chats, if the message was sent on behalf of a chat.
    """

    sender_chat: _chat.Chat | None = None
    """*Optional.* Sender of the message, sent on behalf of a chat. For example,
    the channel itself for channel posts, the supergroup itself for messages
    from anonymous group administrators, the linked channel for messages
    automatically forwarded to the discussion group.

    .. note::

        For backward compatibility, the field from contains a fake sender user
        in non-channel chats, if the message was sent on behalf of a chat.
    """

    date: int  # TODO: datetime
    """Date the message was sent in Unix time."""

    chat: _chat.Chat
    """Conversation the message belongs to."""

    forward_from: User | None = None
    """*Optional.* For forwarded messages, sender of the original message."""

    forward_from_chat: _chat.Chat | None = None
    """*Optional.* For messages forwarded from channels or from anonymous
    administrators, information about the original sender chat.
    """

    forward_from_message_id: NoneInt = None
    """*Optional.* For messages forwarded from channels, identifier of the
    original message in the channel.
    """

    forward_signature: NoneStr = None
    """*Optional.* For forwarded messages that were originally sent in channels
    or by an anonymous chat administrator, signature of the message sender if
    present.
    """

    forward_sender_name: NoneStr = None
    """*Optional.* Sender's name for messages forwarded from users who disallow
    adding a link to their account in forwarded messages.
    """

    forward_date: NoneInt = None  # TODO: datetime
    """*Optional.* For forwarded messages, date the original message was sent
    in Unix time.
    """

    is_topic_message: NoneBool = None
    """*Optional.* True, if the message is sent to a forum topic."""

    is_automatic_forward: NoneBool = None
    """*Optional.* True, if the message is a channel post that was automatically
    forwarded to the connected discussion group.
    """

    reply_to_message: Message | None = None
    """*Optional.* For replies, the original message.

    .. note::

        :class:`Message` object in this field will not contain further
        ``reply_to_message`` fields even if it itself is a reply.
    """

    via_bot: User | None = None
    """*Optional.* Bot through which the message was sent."""

    edit_date: NoneInt = None  # TODO: datetime
    """*Optional.* Date the message was last edited in Unix time."""

    has_protected_content: NoneBool = None
    """*Optional.* ``True``, if the message can't be forwarded."""

    media_group_id: NoneStr = None
    """*Optional.* The unique identifier of a media message group this message
    belongs to.
    """

    author_signature: NoneStr = None
    """*Optional.* Signature of the post author for messages in channels, or
    the custom title of an anonymous group administrator.
    """

    text: NoneStr = None
    """*Optional.* For text messages, the actual UTF-8 text of the message."""

    entities: list[MessageEntity] | None = None
    """*Optional.* For text messages, special entities like usernames, URLs,
    bot commands, etc. that appear in the text.
    """

    animation: Animation | None = None
    """*Optional.* Message is an animation, information about the animation.

    .. note::

        For backward compatibility, when this field is set, the ``document``
        field will also be set.
    """

    audio: Audio | None = None
    """*Optional.* Message is an audio file, information about the file."""

    document: Document | None = None
    """*Optional.* Message is a general file, information about the file."""

    photo: list[PhotoSize] | None = None
    """*Optional.* Message is a photo, available sizes of the photo."""

    sticker: Sticker | None = None
    """*Optional.* Message is a sticker, information about the sticker."""

    story: Story | None = None
    """*Optional.* Message is a forwarded story"""

    video: Video | None = None
    """*Optional.* Message is a video, information about the video."""

    video_note: VideoNote | None = None
    """
    *Optional.* Message is a video note, information about the video message.
    """

    voice: Voice | None = None
    """*Optional.* Message is a voice message, information about the file."""

    caption: NoneStr = None
    """*Optional.* Caption for the animation, audio, document, photo, video or
    voice.
    """

    caption_entities: list[MessageEntity] | None = None
    """*Optional.* For messages with a caption, special entities like usernames,
    URLs, bot commands, etc. that appear in the caption.
    """

    has_media_spoiler: NoneBool = None
    """*Optional.* True, if the message media is covered by a spoiler animation."""  # noqa: E501

    contact: Contact | None = None
    """*Optional.* Message is a shared contact, information about the contact."""  # noqa: E501

    dice: Dice | None = None
    """*Optional.* Message is a dice with random value."""

    game: Game | None = None
    """*Optional.* Message is a game, information about the game."""

    poll: Poll | None = None
    """*Optional.* Message is a native poll, information about the poll."""

    venue: Venue | None = None
    """*Optional.* Message is a venue, information about the venue.

    .. note::

        For backward compatibility, when this field is set, the ``location``
        field will also be set.
    """

    location: Location | None = None
    """*Optional.* Message is a shared location, information about the location."""  # noqa: E501

    new_chat_members: list[User] | None = None
    """*Optional.* New members that were added to the group or supergroup and
    information about them (the bot itself may be one of these members).
    """

    left_chat_member: User | None = None
    """*Optional.* A member was removed from the group, information about them
    (this member may be the bot itself).
    """

    new_chat_title: NoneStr = None
    """*Optional.* A chat title was changed to this value."""

    new_chat_photo: list[PhotoSize] | None = None
    """*Optional.* A chat photo was change to this value."""

    delete_chat_photo: NoneBool = None
    """*Optional.* Service message: the chat photo was deleted."""

    group_chat_created: NoneBool = None
    """*Optional.* Service message: the group has been created."""

    supergroup_chat_created: NoneBool = None
    """*Optional.* Service message: the supergroup has been created.

    .. note::

        This field can't be received in a message coming through updates,
        because bot can't be a member of a supergroup when it is created.
        It can only be found in ``reply_to_message`` if someone replies to a
        very first message in a directly created supergroup.
    """

    channel_chat_created: NoneBool = None
    """*Optional.* Service message: the channel has been created.

    .. note::

        This field can't be received in a message coming through updates,
        because bot can't be a member of a channel when it is created. It
        can only be found in ``reply_to_message`` if someone replies to a very
        first message in a channel.
    """

    message_auto_delete_timer_changed: MessageAutoDeleteTimerChanged | None = None  # noqa: E501, yapf: disable
    """*Optional.* Service message: auto-delete timer settings changed in the chat."""  # noqa: E501

    migrate_to_chat_id: NoneInt = None
    """*Optional.* The group has been migrated to a supergroup with the
    specified identifier.
    """

    migrate_from_chat_id: NoneInt = None
    """*Optional.* The supergroup has been migrated from a group with the
    specified identifier.
    """

    pinned_message: Message | None = None
    """*Optional.* Specified message was pinned.

    .. note::

        :class:`Message` object in this field will not contain further
        ``reply_to_message`` fields even if it is itself a reply.
    """

    invoice: Invoice | None = None
    """*Optional.* Message is an invoice for a payment, information about
    the invoice.
    """

    successful_payment: SuccessfulPayment | None = None
    """*Optional.* Message is a service message about a successful payment,
    information about the payment.
    """

    user_shared: UserShared | None = None
    """*Optional.* Service message: a user was shared with the bot."""

    chat_shared: ChatShared | None = None
    """*Optional.* Service message: a chat was shared with the bot."""

    connected_website: NoneStr = None
    """*Optional.* The domain name of the website on which the user has logged in."""  # noqa: E501

    write_access_allowed: WriteAccessAllowed | None = None
    """*Optional.* Service message: the user allowed the bot added to the
    attachment menu to write messages."""

    passport_data: PassportData | None = None
    """*Optional.* Telegram Passport data."""

    proximity_alert_triggered: ProximityAlertTriggered | None = None
    """*Optional.* Service message. A user in the chat triggered another user's
    proximity alert while sharing Live Location.
    """

    forum_topic_created: ForumTopicCreated | None = None
    """*Optional.* Service message: forum topic created."""

    forum_topic_edited: ForumTopicEdited | None = None
    """*Optional.* Service message: forum topic edited."""

    forum_topic_closed: ForumTopicClosed | None = None
    """*Optional.* Service message: forum topic closed."""

    forum_topic_reopened: ForumTopicReopened | None = None
    """*Optional.* Service message: forum topic reopened."""

    general_forum_topic_hidden: GeneralForumTopicHidden | None = None
    """*Optional.* Service message: the 'General' forum topic hidden."""

    general_forum_topic_unhidden: GeneralForumTopicUnhidden | None = None
    """*Optional.* Service message: the 'General' forum topic unhidden."""

    video_chat_scheduled: VideoChatScheduled | None = None
    """*Optional.* Service message: video chat scheduled."""

    video_chat_started: VideoChatStarted | None = None
    """*Optional.* Service message: video chat started."""

    video_chat_ended: VideoChatEnded | None = None
    """*Optional.* Service message: video chat ended."""

    video_chat_participants_invited: VideoChatParticipantsInvited | None = None
    """*Optional.* Service message: new participants invited to a video chat."""

    web_app_data: WebAppData | None = None
    """*Optional.* Service message: data sent by a Web App."""

    reply_markup: InlineKeyboardMarkup | None = None
    """*Optional.* Inline keyboard attached to the message. ``login_url``
    buttons are represented as ordinary ``url`` buttons.
    """

    async def answer(
        self,
        text: str,
        parse_mode: ParseMode | None = None,
        entities: list[MessageEntity] | None = None,
        disable_web_page_preview: NoneBool = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Send message.

        See: :meth:`~yatbaf.bot.Bot.send_message`
        """
        return await self.bot.send_message(
            chat_id=self.chat.id,
            text=text,
            message_thread_id=self.message_thread_id,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )

    async def reply(
        self,
        text: str,
        parse_mode: ParseMode | None = None,
        entities: list[MessageEntity] | None = None,
        disable_web_page_preview: NoneBool = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Reply to message.

        See: :meth:`~yatbaf.bot.Bot.send_message`
        """
        return await self.bot.send_message(
            chat_id=self.chat.id,
            text=text,
            message_thread_id=self.message_thread_id,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=self.message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )

    async def edit(
        self,
        text: str,
        parse_mode: ParseMode | None = None,
        entities: list[MessageEntity] | None = None,
        disable_web_page_preview: NoneBool = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message | bool:
        """Edit message text.

        See: :meth:`~yatbaf.bot.Bot.edit_message_text`
        """
        return await self.bot.edit_message_text(
            text=text,
            chat_id=self.chat.id,
            message_id=self.message_id,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            reply_markup=reply_markup,
        )

    async def delete(self) -> bool:
        """Delete message.

        See: :meth:`~yatbaf.bot.Bot.delete_message`
        """
        return await self.bot.delete_message(
            chat_id=self.chat.id,
            message_id=self.message_id,
        )

    async def forward(
        self,
        chat_id: str | int,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
    ) -> Message:
        """Forward message.

        See: :meth:`~yatbaf.bot.Bot.forward_message`
        """
        return await self.bot.forward_message(
            chat_id=chat_id,
            from_chat_id=self.chat.id,
            message_id=self.message_id,
            message_thread_id=self.message_thread_id,
            disable_notification=disable_notification,
            protect_content=protect_content,
        )

    async def copy(
        self,
        chat_id: str | int,
        *,
        caption: NoneStr = None,
        parse_mode: ParseMode | None = None,
        caption_entities: list[MessageEntity] | None = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        reply_to_message_id: NoneInt = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> MessageId:
        """Copy message.

        See: :meth:`~yatbaf.bot.Bot.copy_message`
        """
        return await self.bot.copy_message(
            chat_id=chat_id,
            from_chat_id=self.chat.id,
            message_id=self.message_id,
            message_thread_id=self.message_thread_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )

    async def answer_photo(
        self,
        photo: InputFile | str,
        *,
        caption: NoneStr = None,
        parse_mode: ParseMode | None = None,
        caption_entities: list[MessageEntity] | None = None,
        has_spoiler: NoneBool = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Send photo.

        See: :meth:`~yatbaf.bot.Bot.send_photo`
        """
        return await self.bot.send_photo(
            chat_id=self.chat.id,
            photo=photo,
            message_thread_id=self.message_thread_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            has_spoiler=has_spoiler,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )

    async def reply_photo(
        self,
        photo: InputFile | str,
        *,
        caption: NoneStr = None,
        parse_mode: ParseMode | None = None,
        caption_entities: list[MessageEntity] | None = None,
        has_spoiler: NoneBool = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Send photo as reply.

        See: :meth:`~yatbaf.bot.Bot.send_photo`
        """
        return await self.bot.send_photo(
            chat_id=self.chat.id,
            photo=photo,
            message_thread_id=self.message_thread_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            has_spoiler=has_spoiler,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=self.message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )

    async def answer_audio(
        self,
        audio: InputFile | str,
        *,
        caption: NoneStr = None,
        parse_mode: ParseMode | None = None,
        caption_entities: list[MessageEntity] | None = None,
        duration: NoneInt = None,
        performer: NoneStr = None,
        title: NoneStr = None,
        thumbnail: InputFile | str | None = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Send audio.

        See: :meth:`~yatbaf.bot.Bot.send_audio`
        """
        return await self.bot.send_audio(
            chat_id=self.chat.id,
            audio=audio,
            message_thread_id=self.message_thread_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            performer=performer,
            title=title,
            thumbnail=thumbnail,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )

    async def reply_with_audio(
        self,
        audio: InputFile | str,
        *,
        caption: NoneStr = None,
        parse_mode: ParseMode | None = None,
        caption_entities: list[MessageEntity] | None = None,
        duration: NoneInt = None,
        performer: NoneStr = None,
        title: NoneStr = None,
        thumbnail: InputFile | str | None = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Send audio as reply.

        See: :meth:`~yatbaf.bot.Bot.send_audio`
        """
        return await self.bot.send_audio(
            chat_id=self.chat.id,
            audio=audio,
            message_thread_id=self.message_thread_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            performer=performer,
            title=title,
            thumbnail=thumbnail,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=self.message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )

    async def answer_document(
        self,
        document: InputFile | str,
        *,
        thumbnail: InputFile | str | None = None,
        caption: NoneStr = None,
        parse_mode: ParseMode | None = None,
        caption_entities: list[MessageEntity] | None = None,
        disable_content_type_detection: NoneBool = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        reply_to_message_id: NoneInt = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Send document.

        See: :meth:`~yatbaf.bot.Bot.send_document`
        """
        return await self.bot.send_document(
            chat_id=self.chat.id,
            document=document,
            message_thread_id=self.message_thread_id,
            thumbnail=thumbnail,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_content_type_detection=disable_content_type_detection,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )

    async def reply_document(
        self,
        document: InputFile | str,
        *,
        thumbnail: InputFile | str | None = None,
        caption: NoneStr = None,
        parse_mode: ParseMode | None = None,
        caption_entities: list[MessageEntity] | None = None,
        disable_content_type_detection: NoneBool = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Send document as reply.

        See: :meth:`~yatbaf.bot.Bot.send_document`
        """
        return await self.bot.send_document(
            chat_id=self.chat.id,
            document=document,
            message_thread_id=self.message_thread_id,
            thumbnail=thumbnail,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_content_type_detection=disable_content_type_detection,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=self.message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )

    async def answer_video(
        self,
        video: InputFile | str,
        *,
        duration: NoneInt = None,
        width: NoneInt = None,
        height: NoneInt = None,
        thumbnail: InputFile | str | None = None,
        caption: NoneStr = None,
        parse_mode: ParseMode | None = None,
        caption_entities: list[MessageEntity] | None = None,
        has_spoiler: NoneBool = None,
        supports_streaming: NoneBool = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Send video.

        See: :meth:`~yatbaf.bot.Bot.send_video`
        """
        return await self.bot.send_video(
            chat_id=self.chat.id,
            video=video,
            message_thread_id=self.message_thread_id,
            duration=duration,
            width=width,
            height=height,
            thumbnail=thumbnail,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            has_spoiler=has_spoiler,
            supports_streaming=supports_streaming,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )

    async def reply_video(
        self,
        video: InputFile | str,
        *,
        duration: NoneInt = None,
        width: NoneInt = None,
        height: NoneInt = None,
        thumbnail: InputFile | str | None = None,
        caption: NoneStr = None,
        parse_mode: ParseMode | None = None,
        caption_entities: list[MessageEntity] | None = None,
        has_spoiler: NoneBool = None,
        supports_streaming: NoneBool = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Send video as reply.

        See: :meth:`~yatbaf.bot.Bot.send_video`
        """
        return await self.bot.send_video(
            chat_id=self.chat.id,
            video=video,
            message_thread_id=self.message_thread_id,
            duration=duration,
            width=width,
            height=height,
            thumbnail=thumbnail,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            has_spoiler=has_spoiler,
            supports_streaming=supports_streaming,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=self.message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )

    async def answer_animation(
        self,
        animation: InputFile | str,
        *,
        duration: NoneInt = None,
        width: NoneInt = None,
        height: NoneInt = None,
        thumbnail: InputFile | str | None = None,
        caption: NoneStr = None,
        parse_mode: ParseMode | None = None,
        caption_entities: list[MessageEntity] | None = None,
        has_spoiler: NoneBool = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Send animation.

        See: :meth:`~yatbaf.bot.Bot.send_animation`
        """
        return await self.bot.send_animation(
            chat_id=self.chat.id,
            animation=animation,
            message_thread_id=self.message_thread_id,
            duration=duration,
            width=width,
            height=height,
            thumbnail=thumbnail,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            has_spoiler=has_spoiler,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )

    async def reply_animation(
        self,
        animation: InputFile | str,
        *,
        duration: NoneInt = None,
        width: NoneInt = None,
        height: NoneInt = None,
        thumbnail: InputFile | str | None = None,
        caption: NoneStr = None,
        parse_mode: ParseMode | None = None,
        caption_entities: list[MessageEntity] | None = None,
        has_spoiler: NoneBool = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Send annotation as reply.

        See: :meth:`yatbaf.bot.Bot.send_animation`
        """
        return await self.bot.send_animation(
            chat_id=self.chat.id,
            animation=animation,
            message_thread_id=self.message_thread_id,
            duration=duration,
            width=width,
            height=height,
            thumbnail=thumbnail,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            has_spoiler=has_spoiler,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=self.message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )

    async def answer_voice(
        self,
        voice: InputFile | str,
        *,
        caption: NoneStr = None,
        parse_mode: ParseMode | None = None,
        caption_entities: list[MessageEntity] | None = None,
        duration: NoneInt = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Send voice.

        See: :meth:`yatbaf.bot.Bot.send_voice`
        """
        return await self.bot.send_voice(
            chat_id=self.chat.id,
            voice=voice,
            message_thread_id=self.message_thread_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )

    async def reply_voice(
        self,
        voice: InputFile | str,
        *,
        caption: NoneStr = None,
        parse_mode: ParseMode | None = None,
        caption_entities: list[MessageEntity] | None = None,
        duration: NoneInt = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Send voice as reply.

        See: :meth:`yatbaf.bot.Bot.send_voice`
        """
        return await self.bot.send_voice(
            chat_id=self.chat.id,
            voice=voice,
            message_thread_id=self.message_thread_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=self.message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )

    async def answer_video_note(
        self,
        video_note: InputFile | str,
        *,
        duration: NoneInt = None,
        length: NoneInt = None,
        thumbnail: InputFile | str | None = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Send video note.

        See: :meth:`~yatbaf.bot.Bot.send_video_note`
        """
        return await self.bot.send_video_note(
            chat_id=self.chat.id,
            video_note=video_note,
            message_thread_id=self.message_thread_id,
            duration=duration,
            length=length,
            thumbnail=thumbnail,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )

    async def reply_video_note(
        self,
        video_note: InputFile | str,
        *,
        duration: NoneInt = None,
        length: NoneInt = None,
        thumbnail: InputFile | str | None = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Send video note as reply.

        See: :meth:`~yatbaf.bot.Bot.send_video_note`
        """
        return await self.bot.send_video_note(
            chat_id=self.chat.id,
            video_note=video_note,
            message_thread_id=self.message_thread_id,
            duration=duration,
            length=length,
            thumbnail=thumbnail,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=self.message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )

    # yapf: disable
    async def answer_media_group(
        self,
        media: list[InputMediaAudio | InputMediaDocument | InputMediaPhoto | InputMediaVideo],  # noqa: E501
        *,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        allow_sending_without_reply: NoneBool = None,
    ) -> list[Message]:
        """Send media group.

        See: :meth:`~yatbaf.bot.Bot.send_media_group`
        """
        # yapf: enable
        return await self.bot.send_media_group(
            chat_id=self.chat.id,
            media=media,
            message_thread_id=self.message_thread_id,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_sending_without_reply=allow_sending_without_reply,
        )

    # yapf: disable
    async def reply_media_group(
        self,
        media: list[InputMediaAudio | InputMediaDocument | InputMediaPhoto | InputMediaVideo],  # noqa: E501
        *,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        allow_sending_without_reply: NoneBool = None,
    ) -> list[Message]:
        """Send media group as reply.

        See: :meth:`~yatbaf.bot.Bot.send_media_group`
        """
        # yapf: enable
        return await self.bot.send_media_group(
            chat_id=self.chat.id,
            media=media,
            message_thread_id=self.message_thread_id,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=self.message_id,
            allow_sending_without_reply=allow_sending_without_reply,
        )

    async def answer_location(
        self,
        latitude: float,
        longtitude: float,
        *,
        horizontal_accuracy: float | None = None,
        live_period: NoneInt = None,
        heading: NoneInt = None,
        proximity_alert_radius: NoneInt = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Send location.

        See: :meth:`~yatbaf.bot.Bot.send_location`
        """
        return await self.bot.send_location(
            chat_id=self.chat.id,
            latitude=latitude,
            longtitude=longtitude,
            message_thread_id=self.message_thread_id,
            horizontal_accuracy=horizontal_accuracy,
            live_period=live_period,
            heading=heading,
            proximity_alert_radius=proximity_alert_radius,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )

    async def reply_location(
        self,
        latitude: float,
        longtitude: float,
        *,
        horizontal_accuracy: float | None = None,
        live_period: NoneInt = None,
        heading: NoneInt = None,
        proximity_alert_radius: NoneInt = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Send location as reply.

        See: :meth:`~yatbaf.bot.Bot.send_location`
        """
        return await self.bot.send_location(
            chat_id=self.chat.id,
            latitude=latitude,
            longtitude=longtitude,
            message_thread_id=self.message_thread_id,
            horizontal_accuracy=horizontal_accuracy,
            live_period=live_period,
            heading=heading,
            proximity_alert_radius=proximity_alert_radius,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=self.message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )

    async def answer_venue(
        self,
        latitude: float,
        longtitude: float,
        title: str,
        address: str,
        *,
        foursquare_id: NoneStr = None,
        foursquare_type: NoneStr = None,
        google_place_id: NoneStr = None,
        google_place_type: NoneStr = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Send venue.

        See: :meth:`~yatbaf.bot.Bot.send_venue`
        """
        return await self.bot.send_venue(
            chat_id=self.chat.id,
            latitude=latitude,
            longtitude=longtitude,
            title=title,
            address=address,
            message_thread_id=self.message_thread_id,
            foursquare_id=foursquare_id,
            foursquare_type=foursquare_type,
            google_place_id=google_place_id,
            google_place_type=google_place_type,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )

    async def reply_venue(
        self,
        latitude: float,
        longtitude: float,
        title: str,
        address: str,
        *,
        foursquare_id: NoneStr = None,
        foursquare_type: NoneStr = None,
        google_place_id: NoneStr = None,
        google_place_type: NoneStr = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Send venue as reply.

        See: :meth:`~yatbaf.bot.Bot.send_venue`
        """
        return await self.bot.send_venue(
            chat_id=self.chat.id,
            latitude=latitude,
            longtitude=longtitude,
            title=title,
            address=address,
            message_thread_id=self.message_thread_id,
            foursquare_id=foursquare_id,
            foursquare_type=foursquare_type,
            google_place_id=google_place_id,
            google_place_type=google_place_type,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=self.message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )

    async def answer_contact(
        self,
        phone_number: str,
        first_name: str,
        *,
        last_name: NoneStr = None,
        vcard: NoneStr = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Send contact.

        See: :meth:`~yatbaf.bot.Bot.send_contact`
        """
        return await self.bot.send_contact(
            chat_id=self.chat.id,
            phone_number=phone_number,
            first_name=first_name,
            message_thread_id=self.message_thread_id,
            last_name=last_name,
            vcard=vcard,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )

    async def reply_contact(
        self,
        phone_number: str,
        first_name: str,
        *,
        last_name: NoneStr = None,
        vcard: NoneStr = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Send contact as reply.

        See: :meth:`~yatbaf.bot.Bot.send_contact`
        """
        return await self.bot.send_contact(
            chat_id=self.chat.id,
            phone_number=phone_number,
            first_name=first_name,
            message_thread_id=self.message_thread_id,
            last_name=last_name,
            vcard=vcard,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=self.message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )

    async def answer_poll(
        self,
        question: str,
        options: list[str],
        *,
        is_anonymous: NoneBool = None,
        type: PollType | None = None,
        allows_multiple_answers: NoneBool = None,
        correct_option_id: NoneInt = None,
        explanation: NoneStr = None,
        explanation_parse_mode: ParseMode | None = None,
        explanation_entities: list[MessageEntity] | None = None,
        open_period: NoneInt = None,
        close_date: NoneInt = None,
        is_closed: NoneBool = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Send poll.

        See: :meth:`~yatbaf.bot.Bot.send_poll`
        """
        return await self.bot.send_poll(
            chat_id=self.chat.id,
            question=question,
            options=options,
            message_thread_id=self.message_thread_id,
            is_anonymous=is_anonymous,
            type=type,
            allows_multiple_answers=allows_multiple_answers,
            correct_option_id=correct_option_id,
            explanation=explanation,
            explanation_parse_mode=explanation_parse_mode,
            explanation_entities=explanation_entities,
            open_period=open_period,
            close_date=close_date,
            is_closed=is_closed,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )

    async def reply_poll(
        self,
        question: str,
        options: list[str],
        *,
        is_anonymous: NoneBool = None,
        type: PollType | None = None,
        allows_multiple_answers: NoneBool = None,
        correct_option_id: NoneInt = None,
        explanation: NoneStr = None,
        explanation_parse_mode: ParseMode | None = None,
        explanation_entities: list[MessageEntity] | None = None,
        open_period: NoneInt = None,
        close_date: NoneInt = None,
        is_closed: NoneBool = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Send poll as reply.

        See: :meth:`~yatbaf.bot.Bot.send_poll`
        """
        return await self.bot.send_poll(
            chat_id=self.chat.id,
            question=question,
            options=options,
            message_thread_id=self.message_thread_id,
            is_anonymous=is_anonymous,
            type=type,
            allows_multiple_answers=allows_multiple_answers,
            correct_option_id=correct_option_id,
            explanation=explanation,
            explanation_parse_mode=explanation_parse_mode,
            explanation_entities=explanation_entities,
            open_period=open_period,
            close_date=close_date,
            is_closed=is_closed,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=self.message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )

    async def stop_poll(
        self, *, reply_markup: InlineKeyboardMarkup | None = None
    ) -> Poll:
        """Stop poll.

        See: :meth:`~yatbaf.bot.Bot.stop_poll`
        """
        return await self.bot.stop_poll(
            chat_id=self.chat.id,
            message_id=self.message_id,
            reply_markup=reply_markup,
        )

    async def answer_dice(
        self,
        *,
        emoji: NoneStr = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Send dice.

        See: :meth:`~yatbaf.bot.Bot.send_dice`
        """
        return await self.bot.send_dice(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id,
            emoji=emoji,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )

    async def reply_dice(
        self,
        *,
        emoji: NoneStr = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Send dice as reply.

        See: :meth:`~yatbaf.bot.Bot.send_dice`
        """

        return await self.bot.send_dice(
            chat_id=self.chat.id,
            message_thread_id=self.message_thread_id,
            emoji=emoji,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=self.message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )

    async def anwser_game(
        self,
        game_short_name: str,
        *,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message:
        """Send game.

        See: :meth:`~yatbaf.bot.Bot.send_game`
        """
        return await self.bot.send_game(
            chat_id=self.chat.id,
            game_short_name=game_short_name,
            message_thread_id=self.message_thread_id,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )

    async def reply_game(
        self,
        game_short_name: str,
        *,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message:
        """Send game as reply.

        See: :meth:`~yatbaf.bot.Bot.send_game`
        """
        return await self.bot.send_game(
            chat_id=self.chat.id,
            game_short_name=game_short_name,
            message_thread_id=self.message_thread_id,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=self.message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )

    async def edit_caption(
        self,
        *,
        caption: NoneStr = None,
        parse_mode: ParseMode | None = None,
        caption_entities: list[MessageEntity] | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message | bool:
        """Edit message caption.

        See: :meth:`~yatbaf.bot.Bot.edit_message_caption`
        """
        return await self.bot.edit_message_caption(
            chat_id=self.chat.id,
            message_id=self.message_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            reply_markup=reply_markup,
        )

    async def edit_media(
        self,
        media: InputMedia,
        *,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message | bool:
        """Edit message media.

        See: :meth:`~yatbaf.bot.Bot.edit_message_media`
        """
        return await self.bot.edit_message_media(
            media=media,
            chat_id=self.chat.id,
            message_id=self.message_id,
            reply_markup=reply_markup,
        )

    async def edit_reply_markup(
        self,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message | bool:
        """Edit message reply markup.

        See: :meth:`~yatbaf.bot.Bot.edit_message_reply_markup`
        """
        return await self.bot.edit_message_reply_markup(
            chat_id=self.chat.id,
            message_id=self.message_id,
            reply_markup=reply_markup,
        )

    async def pin(self, disable_notification: NoneBool = None) -> bool:
        """Pin message.

        See: :meth:`~yatbaf.bot.Bot.pin_chat_message`
        """
        return await self.bot.pin_chat_message(
            chat_id=self.chat.id,
            message_id=self.message_id,
            disable_notification=disable_notification,
        )

    async def unpin(self) -> bool:
        """Unpin message.

        See: :meth:`~yatbaf.bot.Bot.unpin_chat_message`
        """
        return await self.bot.unpin_chat_message(
            chat_id=self.chat.id,
            message_id=self.message_id,
        )
