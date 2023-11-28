from __future__ import annotations

__all__ = ("Bot",)

import logging
from typing import TYPE_CHECKING

from .dispatcher import Dispatcher
from .methods import AddStickerToSet
from .methods import AnswerCallbackQuery
from .methods import AnswerInlineQuery
from .methods import AnswerPreCheckoutQuery
from .methods import AnswerShippingQuery
from .methods import AnswerWebAppQuery
from .methods import ApproveChatJoinRequest
from .methods import BanChatMember
from .methods import BanChatSenderChat
from .methods import Close
from .methods import CloseForumTopic
from .methods import CloseGeneralForumTopic
from .methods import CopyMessage
from .methods import CreateChatInviteLink
from .methods import CreateForumTopic
from .methods import CreateInvoiceLink
from .methods import CreateNewStickerSet
from .methods import DeclineChatJoinRequest
from .methods import DeleteChatPhoto
from .methods import DeleteChatStickerSet
from .methods import DeleteForumTopic
from .methods import DeleteMessage
from .methods import DeleteMyCommands
from .methods import DeleteStickerFromSet
from .methods import DeleteStickerSet
from .methods import DeleteWebhook
from .methods import EditChatInviteLink
from .methods import EditForumTopic
from .methods import EditGeneralForumTopic
from .methods import EditMessageCaption
from .methods import EditMessageLiveLocation
from .methods import EditMessageMedia
from .methods import EditMessageReplyMarkup
from .methods import EditMessageText
from .methods import ExportChatInviteLink
from .methods import ForwardMessage
from .methods import GetChat
from .methods import GetChatAdministrators
from .methods import GetChatMember
from .methods import GetChatMemberCount
from .methods import GetChatMenuButton
from .methods import GetCustomEmojiStickers
from .methods import GetFile
from .methods import GetForumTopicIconStickers
from .methods import GetGameHighScores
from .methods import GetMe
from .methods import GetMyCommands
from .methods import GetMyDefaultAdministratorRights
from .methods import GetMyDescription
from .methods import GetMyName
from .methods import GetMyShortDescription
from .methods import GetStickerSet
from .methods import GetUpdates
from .methods import GetUserProfilePhotos
from .methods import GetWebhookInfo
from .methods import HideGeneralForumTopic
from .methods import LeaveChat
from .methods import LogOut
from .methods import PinChatMessage
from .methods import PromoteChatMember
from .methods import ReopenForumTopic
from .methods import ReopenGeneralForumTopic
from .methods import RestrictChatMember
from .methods import RevokeChatInviteLink
from .methods import SendAnimation
from .methods import SendAudio
from .methods import SendChatAction
from .methods import SendContact
from .methods import SendDice
from .methods import SendDocument
from .methods import SendGame
from .methods import SendInvoice
from .methods import SendLocation
from .methods import SendMediaGroup
from .methods import SendMessage
from .methods import SendPhoto
from .methods import SendPoll
from .methods import SendSticker
from .methods import SendVenue
from .methods import SendVideo
from .methods import SendVideoNote
from .methods import SendVoice
from .methods import SetChatAdministratorCustomTitle
from .methods import SetChatDescription
from .methods import SetChatMenuButton
from .methods import SetChatPermissions
from .methods import SetChatPhoto
from .methods import SetChatStickerSet
from .methods import SetChatTitle
from .methods import SetCustomEmojiStickerSetThumbnail
from .methods import SetGameScore
from .methods import SetMyCommands
from .methods import SetMyDefaultAdministratorRights
from .methods import SetMyDescription
from .methods import SetMyName
from .methods import SetMyShortDescription
from .methods import SetPassportDataErrors
from .methods import SetStickerEmojiList
from .methods import SetStickerKeywords
from .methods import SetStickerMaskPosition
from .methods import SetStickerPositionInSet
from .methods import SetStickerSetThumbnail
from .methods import SetStickerSetTitle
from .methods import SetWebhook
from .methods import StopMessageLiveLocation
from .methods import StopPoll
from .methods import UnbanChatMember
from .methods import UnbanChatSenderChat
from .methods import UnhideGeneralForumTopic
from .methods import UnpinAllChatMessages
from .methods import UnpinAllForumTopicMessages
from .methods import UnpinAllGeneralForumTopicMessages
from .methods import UnpinChatMessage
from .methods import UploadStickerFile
from .types.abc import TelegramType

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from .enums import ChatAction
    from .enums import IconColor
    from .enums import ParseMode
    from .enums import PollType
    from .enums import StickerFormat
    from .enums import StickerType
    from .enums import UpdateType
    from .types import BotCommand
    from .types import BotCommandScope
    from .types import BotDescription
    from .types import BotName
    from .types import BotShortDescription
    from .types import Chat
    from .types import ChatAdministratorRights
    from .types import ChatInviteLink
    from .types import ChatMember
    from .types import ChatPermissions
    from .types import File
    from .types import ForumTopic
    from .types import GameHighScore
    from .types import InlineKeyboardMarkup
    from .types import InlineQueryResult
    from .types import InlineQueryResultsButton
    from .types import InputMedia
    from .types import InputMediaAudio
    from .types import InputMediaDocument
    from .types import InputMediaPhoto
    from .types import InputMediaVideo
    from .types import InputSticker
    from .types import LabeledPrice
    from .types import MaskPosition
    from .types import MenuButton
    from .types import Message
    from .types import MessageEntity
    from .types import MessageId
    from .types import PassportElementError
    from .types import Poll
    from .types import SentWebAppMessage
    from .types import ShippingOption
    from .types import Sticker
    from .types import StickerSet
    from .types import Update
    from .types import User
    from .types import UserProfilePhotos
    from .types import WebhookInfo
    from .typing import InputFile
    from .typing import NoneBool
    from .typing import NoneInt
    from .typing import NoneStr
    from .typing import ReplyMarkup
    from .typing import ResultModelT

log = logging.getLogger(__name__)

CHUNK_SIZE = 64 * 1024


class Bot(Dispatcher):
    """Bot object."""

    __slots__ = ()

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Bot[id={self._id}]>"

    def run(self) -> None:
        """Run long polling."""
        from yatbaf.long_polling import LongPolling
        LongPolling(self).start()

    def _bind_self(self, update: ResultModelT, /) -> ResultModelT:
        if isinstance(update, TelegramType):
            update._bind_bot_obj(self)

        # Return type of several methods is `list[TelegramType]`:
        elif isinstance(update, list):
            for obj in update:
                obj._bind_bot_obj(self)

        return update

    def get_file_content(self, file: File) -> AsyncIterator[bytes]:
        """Download file.

        :param file: :class:`~yatbaf.types.file.File` object.
            See :meth:`get_file`.
        """
        return self._api_client.download_file(file, chunk_size=CHUNK_SIZE)

    async def get_me(self) -> User:
        """Returns basic information about the bot.

        See: https://core.telegram.org/bots/api#getme
        """
        return await self._call_api(GetMe())

    async def get_my_name(self, language_code: NoneStr = None) -> BotName:
        """
        Use this method to get the current bot name for the given user language.

        See: https://core.telegram.org/bots/api#getmyname

        :param language_code: *Optional.* A two-letter ISO 639-1 language code
            or an empty string.
        """
        return await self._call_api(GetMyName(language_code=language_code))

    async def set_my_name(
        self,
        name: NoneStr = None,
        language_code: NoneStr = None,
    ) -> bool:
        """Use this method to change the bot's name.

        See: https://core.telegram.org/bots/api#setmyname

        :param name: *Optional.* New bot name; 0-64 characters. Pass an empty
            string to remove the dedicated name for the given language.
        :param language_code: *Optional.* A two-letter ISO 639-1 language code.
            If empty, the name will be shown to all users for whose language
            there is no dedicated name.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            SetMyName(
                name=name,
                language_code=language_code,
            )
        )

    async def log_out(self) -> bool:
        """Use this method to log out from the cloud Bot API server before
        launching the bot locally. You **must** log out the bot before running
        it locally, otherwise there is no guarantee that the bot will receive
        updates. After a successful call, you can immediately log in on a local
        server, but will not be able to log in back to the cloud Bot API server
        for 10 minutes.

        See: https://core.telegram.org/bots/api#logout

        :returns: ``True`` on success.
        """
        return await self._call_api(LogOut())

    async def close(self) -> bool:
        """Use this method to close the bot instance before moving it from one
        local server to another.

        .. important::

            You need to delete the webhook before calling this method to ensure
            that the bot isn't launched again after server restart.

        .. warning::

            The method will raise :exc:`~yatbaf.exceptions.FloodError` in the
            first 10 minutes after the bot is launched.

        See: https://core.telegram.org/bots/api#close

        :returns: ``True`` on success.
        """  # noqa: E501
        return await self._call_api(Close())

    async def get_updates(
        self,
        *,
        offset: NoneInt = None,
        limit: NoneInt = None,
        timeout: NoneInt = None,
        allowed_updates: list[UpdateType] | None = None,
    ) -> list[Update]:
        """Use this method to receive incoming updates using long polling

        See: https://core.telegram.org/bots/api#getupdates

        :param offset: *Optional.* Identifier of the first update to be returned.
            Must be greater by one than the highest among the identifiers of
            previously received updates. By default, updates starting with the
            earliest unconfirmed update are returned. An update is considered
            confirmed as soon as getUpdates is called with an ``offset`` higher
            than its ``update_id``. The negative offset can be specified to
            retrieve updates starting from -offset update from the end of the
            updates queue. All previous updates will be forgotten.
        :param limit: *Optional.* Limits the number of updates to be retrieved.
            Values between 1-100 are accepted. Defaults to 100.
        :param timeout: *Optional.* Timeout in seconds for long polling.
            Defaults to 0, i.e. usual short polling. Should be positive, short
            polling should be used for testing purposes only.
        :param allowed_updates: A list of the update types you want your bot to
            receive. See :class:`~yatbaf.enums.UpdateType` for a complete list
            of available update types. Specify an empty list to receive all
            update types except ``chat_member`` (default). If not specified, the
            previous setting will be used.

        .. note::

            #. ``allowed_updates`` doesn't affect updates created before the
               call to the :meth:`get_updates`, so unwanted updates may be
               received for a short period of time.

        .. hint::

            In order to avoid getting duplicate updates, recalculate ``offset``
            after each server response.

        .. warning::

            This method will not work if an outgoing webhook is set up.
        """  # noqa: E501
        return await self._call_api(
            GetUpdates(
                offset=offset,
                limit=limit,
                timeout=timeout,
                allowed_updates=allowed_updates,
            )
        )

    async def set_webhook(
        self,
        url: str,
        *,
        certificate: InputFile | None = None,
        ip_address: NoneStr = None,
        max_connections: NoneInt = None,
        allowed_updates: list[UpdateType] | None = None,
        drop_pending_updates: NoneBool = None,
        secret_token: NoneStr = None,
    ) -> bool:
        """Use this method to specify a URL and receive incoming updates via an
        outgoing webhook.

        See: https://core.telegram.org/bots/api#setwebhook

        :param url: HTTPS URL to send updates to. Use an empty string to remove
            webhook integration.
        :param certificate: *Optional.* Upload your public key certificate so
            that the root certificate in use can be checked. See
            `self-signed guide`_ for details.
        :param ip_address: *Optional.* The fixed IP address which will be used
            to send webhook requests instead of the IP address resolved through
            DNS.
        :param max_connections: *Optional.* The maximum allowed number of
            simultaneous HTTPS connections to the webhook for update delivery,
            1-100. Defaults to 40. Use lower values to limit the load on your
            bot's server, and higher values to increase your bot's throughput.
        :param allowed_updates: *Optional.* List of the update types you want
            your bot to receive. See :class:`UpdateType <yatbaf.enums.UpdateType>`
            for a complete list of available update types.
        :param drop_pending_updates: Pass ``True`` to drop all pending updates.
        :param secret_token: *Optional.* A secret token to be sent in a header
            'X-Telegram-Bot-Api-Secret-Token' in every webhook request, 1-256
            characters. Only characters A-Z, a-z, 0-9, _ and - are allowed.
            The header is useful to ensure that the request comes from a webhook
            set by you.
        :returns: ``True`` on success.

        .. note::

            ``allowed_updates`` doesn't affect updates created before the call
            to the :meth:`set_webhook`, so unwanted updates may be received for
            a short period of time.

        .. _self-signed guide: https://core.telegram.org/bots/self-signed
        """  # noqa: E501
        return await self._call_api(
            SetWebhook(
                url=url,
                certificate=certificate,
                ip_address=ip_address,
                max_connections=max_connections,
                allowed_updates=allowed_updates,
                drop_pending_updates=drop_pending_updates,
                secret_token=secret_token,
            )
        )

    async def delete_webhook(
        self, drop_pending_updates: NoneBool = None
    ) -> bool:
        """Use this method to remove webhook integration if you decide to switch
        back to :meth:`get_updates`.

        See: https://core.telegram.org/bots/api#deletewebhook

        :param drop_pending_updates: *Optional.* Pass ``True`` to drop all
            pending updates.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            DeleteWebhook(drop_pending_updates=drop_pending_updates)
        )

    async def get_webhook_info(self) -> WebhookInfo:
        """Use this method to get current webhook status.

        .. note::

            If the bot is using :meth:`get_updates`, will return an object with
            the ``url`` field empty.

        See: https://core.telegram.org/bots/api#getwebhookinfo
        """
        return await self._call_api(GetWebhookInfo())

    async def send_message(
        self,
        chat_id: str | int,
        text: str,
        *,
        message_thread_id: NoneInt = None,
        parse_mode: ParseMode | None = None,
        entities: list[MessageEntity] | None = None,
        disable_web_page_preview: NoneBool = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        reply_to_message_id: NoneInt = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Use this method to send text messages.

        See: https://core.telegram.org/bots/api#sendmessage

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param text: Text of the message to be sent, 1-4096 characters after
            entities parsing.
        :param message_thread_id: *Optional.* Unique identifier for the target
            message thread (topic) of the forum; for forum supergroups only.
        :param parse_mode: *Optional.* Mode for parsing entities in the message
            text.
        :param entities: *Optional.* list of special entities that appear in
            message text, which can be specified instead of ``parse_mode``.
        :param disable_web_page_preview: *Optional.* Disables link previews for
            links in this message.
        :param disable_notification: *Optional.* Sends the message silently.
            Users will receive a notification with no sound.
        :param protect_content: *Optional.* Protects the contents of the sent
            message from forwarding and saving.
        :param reply_to_message_id: *Optional.* If the message is a reply, ID
            of the original message.
        :param allow_sending_without_reply: *Optional.* Pass ``True`` if the
            message should be sent even if the specified replied-to message
            is not found.
        :param reply_markup: *Optional.* Additional interface options.
        :returns: The sent :class:`~yatbaf.types.message.Message`
            on success.
        """
        return await self._call_api(
            SendMessage(
                chat_id=chat_id,
                text=text,
                message_thread_id=message_thread_id,
                parse_mode=parse_mode,
                entities=entities,
                disable_web_page_preview=disable_web_page_preview,
                disable_notification=disable_notification,
                protect_content=protect_content,
                reply_to_message_id=reply_to_message_id,
                allow_sending_without_reply=allow_sending_without_reply,
                reply_markup=reply_markup,
            )
        )

    async def forward_message(
        self,
        chat_id: str | int,
        from_chat_id: int | str,
        message_id: int,
        *,
        message_thread_id: NoneInt = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
    ) -> Message:
        """Use this method to forward messages of any kind.

        See: https://core.telegram.org/bots/api#forwardmessage

        .. note::

            Service messages can't be forwarded.

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param from_chat_id: Unique identifier for the chat where the original
            message was sent (or channel username in the format
            @channelusername).
        :param message_id: Message identifier in the chat specified in
            ``from_chat_id``.
        :param message_thread_id: *Optional.* Unique identifier for the target
            message thread (topic) of the forum; for forum supergroups only.
        :param disable_notification: *Optional.* Sends the message silently.
            Users will receive a notification with no sound.
        :param protect_content: *Optional.* Protects the contents of the
            forwarded message from forwarding and saving.
        :returns: On success, the sent :class:`~yatbaf.types.message.Message`
            is returned.
        """
        return await self._call_api(
            ForwardMessage(
                chat_id=chat_id,
                from_chat_id=from_chat_id,
                message_id=message_id,
                message_thread_id=message_thread_id,
                disable_notification=disable_notification,
                protect_content=protect_content,
            )
        )

    async def copy_message(
        self,
        chat_id: str | int,
        from_chat_id: str | int,
        message_id: int,
        *,
        message_thread_id: NoneInt = None,
        caption: NoneStr = None,
        parse_mode: ParseMode | None = None,
        caption_entities: list[MessageEntity] | None = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        reply_to_message_id: NoneInt = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> MessageId:
        """Use this method to copy messages of any kind. The method is analogous
        to the method :meth:`forward_message`, but the copied message doesn't
        have a link to the original message.

        .. note::

            Service messages and invoice messages can't be copied. A quiz poll
            can be copied only if the value of the field ``correct_option_id``
            is known to the bot.

        See: https://core.telegram.org/bots/api#copymessage

        :param chat_id: Unique identifier for the target chat or username of the
            target channel (in the format @channelusername).
        :param from_chat_id: Unique identifier for the chat where the original
            message was sent (or channel username in the format
            @channelusername).
        :param message_id: Message identifier in the chat specified in
            ``from_chat_id``.
        :param message_thread_id: *Optional.* Unique identifier for the target
            message thread (topic) of the forum; for forum supergroups only.
        :param caption: *Optional.* New caption for media, 0-1024 characters
            after entities parsing. If not specified, the original caption
            is kept.
        :param parse_mode: *Optional.* Mode for parsing entities in the new
            caption.
        :param caption_entities: *Optional.* List of
            :class:`~yatbaf.types.message_entity.MessageEntity`
            that appear in the new caption, which can be specified instead of
            ``parse_mode``.
        :param disable_notification: *Optional.* Sends the message silently.
            Users will receive a notification with no sound.
        :param protect_content: *Optional.* Protects the contents of the sent
            message from forwarding and saving.
        :param reply_to_message_id: *Optional.* If the message is a reply, ID
            of the original message.
        :param allow_sending_without_reply: *Optional.* Pass ``True`` if the
            message should be sent even if the specified replied-to message
            is not found.
        :param reply_markup: Additional interface options.
        :returns: :class:`~yatbaf.types.message_id.MessageId` of the sent
            message on success.
        """
        return await self._call_api(
            CopyMessage(
                chat_id=chat_id,
                from_chat_id=from_chat_id,
                message_id=message_id,
                message_thread_id=message_thread_id,
                caption=caption,
                parse_mode=parse_mode,
                caption_entities=caption_entities,
                disable_notification=disable_notification,
                protect_content=protect_content,
                reply_to_message_id=reply_to_message_id,
                allow_sending_without_reply=allow_sending_without_reply,
                reply_markup=reply_markup,
            )
        )

    async def send_photo(
        self,
        chat_id: str | int,
        photo: InputFile | str,
        *,
        message_thread_id: NoneInt = None,
        caption: NoneStr = None,
        parse_mode: ParseMode | None = None,
        caption_entities: list[MessageEntity] | None = None,
        has_spoiler: NoneBool = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        reply_to_message_id: NoneInt = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Use this method to send photos.

        See: https://core.telegram.org/bots/api#sendphoto

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param photo: Photo to send. The photo must be at most 10 MB in size.
            The photo's width and height must not exceed 10000 in total. Width
            and height ratio must be at most 20.
        :param message_thread_id: *Optional.* Unique identifier for the target
            message thread (topic) of the forum; for forum supergroups only.
        :param caption: *Optional.* Photo caption (may also be used when
            resending photos by ``file_id``), 0-1024 characters after entities
            parsing.
        :param parse_mode: *Optional.* Mode for parsing entities in the photo
            caption.
        :param caption_entities: *Optional.* List of
            :class:`~yatbaf.types.message_entity.MessageEntity`
            that appear in the caption, which can be specified instead of
            ``parse_mode``.
        :param has_spoiler: *Optional.* Pass ``True`` if the photo needs to be
            covered with a spoiler animation.
        :param disable_notification: *Optional.* Sends the message silently.
            Users will receive a notification with no sound.
        :param protect_content: *Optional.* Protects the contents of the sent
            message from forwarding and saving.
        :param reply_to_message_id: *Optional.* If the message is a reply, ID
            of the original message.
        :param allow_sending_without_reply: *Optional.* Pass ``True`` if the
            message should be sent even if the specified replied-to message is
            not found.
        :param reply_markup: *Optional.* Additional interface options.
        """
        return await self._call_api(
            SendPhoto(
                chat_id=chat_id,
                photo=photo,
                message_thread_id=message_thread_id,
                caption=caption,
                parse_mode=parse_mode,
                caption_entities=caption_entities,
                has_spoiler=has_spoiler,
                disable_notification=disable_notification,
                protect_content=protect_content,
                reply_to_message_id=reply_to_message_id,
                allow_sending_without_reply=allow_sending_without_reply,
                reply_markup=reply_markup,
            )
        )

    async def send_audio(
        self,
        chat_id: str | int,
        audio: InputFile | str,
        *,
        message_thread_id: NoneInt = None,
        caption: NoneStr = None,
        parse_mode: ParseMode | None = None,
        caption_entities: list[MessageEntity] | None = None,
        duration: NoneInt = None,
        performer: NoneStr = None,
        title: NoneStr = None,
        thumbnail: InputFile | str | None = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        reply_to_message_id: NoneInt = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Use this method to send audio files, if you want Telegram clients to
        display them in the music player. Your audio must be in the .MP3 or
        .M4A format.

        .. note::

            Bots can currently send audio files of up to 50 MB in size, this
            limit may be changed in the future.

        See: https://core.telegram.org/bots/api#sendaudio

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param audio: Audio file to send.
        :param message_thread_id: *Optional.* Unique identifier for the target
            message thread (topic) of the forum; for forum supergroups only.
        :param caption: *Optional.* Audio caption, 0-1024 characters after
            entities parsing.
        :param parse_mode: *Optional.* Mode for parsing entities in the audio
            caption.
        :param caption_entities: *Optional.* List of
            :class:`~yatbaf.types.message_entity.MessageEntity`
            that appear in the caption, which can be specified instead of
            ``parse_mode``.
        :param duration: *Optional.* Duration of the audio in seconds.
        :param performer: *Optional.* Performer.
        :param title: *Optional.* Track name.
        :param thumbnail: *Optional.* Thumbnail of the file sent; can be ignored
            if thumbnail generation for the file is supported server-side. The
            thumbnail should be in JPEG format and less than 200 kB in size. A
            thumbnail's width and height should not exceed 320.
        :param disable_notification: *Optional.* Sends the message silently.
            Users will receive a notification with no sound.
        :param protect_content: *Optional.* Protects the contents of the sent
            message from forwarding and saving.
        :param reply_to_message_id: *Optional.* If the message is a reply, ID
            of the original message.
        :param allow_sending_without_reply: *Optional.* Pass ``True`` if the
            message should be sent even if the specified replied-to message is
            not found.
        :param reply_markup: *Optional.* Additional interface options.
        """
        return await self._call_api(
            SendAudio(
                chat_id=chat_id,
                audio=audio,
                message_thread_id=message_thread_id,
                caption=caption,
                parse_mode=parse_mode,
                caption_entities=caption_entities,
                duration=duration,
                performer=performer,
                title=title,
                thumbnail=thumbnail,
                disable_notification=disable_notification,
                protect_content=protect_content,
                reply_to_message_id=reply_to_message_id,
                allow_sending_without_reply=allow_sending_without_reply,
                reply_markup=reply_markup,
            )
        )

    async def send_document(
        self,
        chat_id: str | int,
        document: InputFile | str,
        *,
        message_thread_id: NoneInt = None,
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
        """Use this method to send general files.

        .. important::

            Bots can currently send files of any type of up to 50 MB in size,
            this limit may be changed in the future.

        See: https://core.telegram.org/bots/api#senddocument

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param document: File to send.
        :param message_thread_id: *Optional.* Unique identifier for the target
            message thread (topic) of the forum; for forum supergroups only.
        :param thumbnail: *Optional.* Thumbnail of the file sent; can be ignored
            if thumbnail generation for the file is supported server-side. The
            thumbnail should be in JPEG format and less than 200 kB in size. A
            thumbnail's width and height should not exceed 320.
        :param caption: *Optional.* Document caption (may also be used when
            resending documents by ``file_id``), 0-1024 characters after
            entities parsing.
        :param parse_mode: *Optional.* Mode for parsing entities in the document
            caption.
        :param caption_entities: *Optional.* List of
            :class:`~yatbaf.types.message_entity.MessageEntity`
            that appear in the caption, which can be specified instead of
            ``parse_mode``.
        :param disable_content_type_detection: *Optional.* Disables automatic
            server-side content type detection for files uploaded using
            multipart/form-data.
        :param disable_notification: *Optional.* Sends the message silently.
            Users will receive a notification with no sound.
        :param protect_content: *Optional.* Protects the contents of the sent
            message from forwarding and saving.
        :param reply_to_message_id: *Optional.* If the message is a reply, ID
            of the original message.
        :param allow_sending_without_reply: *Optional.* Pass ``True`` if the
            message should be sent even if the specified replied-to message is
            not found.
        :param reply_markup: *Optional.* Additional interface options.
        """
        return await self._call_api(
            SendDocument(
                chat_id=chat_id,
                document=document,
                message_thread_id=message_thread_id,
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
        )

    async def send_video(
        self,
        chat_id: str | int,
        video: InputFile | str,
        *,
        message_thread_id: NoneInt = None,
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
        reply_to_message_id: NoneInt = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Use this method to send video files, Telegram clients support MPEG4
        videos (other formats may be sent as Document).

        .. important::

            Bots can currently send video files of up to 50 MB in size, this
            limit may be changed in the future.

        See: https://core.telegram.org/bots/api#sendvideo

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param video: Video to send.
        :param message_thread_id: *Optional.* Unique identifier for the target
            message thread (topic) of the forum; for forum supergroups only.
        :param duration: *Optional.* Duration of sent video in seconds.
        :param width: *Optional.* Video width.
        :param height: *Optional.* Video height.
        :param thumbnail: *Optional.* Thumbnail of the file sent; can be ignored
            if thumbnail generation for the file is supported server-side. The
            thumbnail should be in JPEG format and less than 200 kB in size. A
            thumbnail's width and height should not exceed 320.
        :param caption: *Optional.* Video caption (may also be used when
            resending videos by ``file_id``), 0-1024 characters after entities
            parsing.
        :param parse_mode: *Optional.* Mode for parsing entities in the video
            caption.
        :param caption_entities: *Optional.* List of
            :class:`~yatbaf.types.message_entity.MessageEntity`
            that appear in the caption, which can be specified instead of
            ``parse_mode``.
        :param has_spoiler: *Optional.* Pass ``True`` if the video needs to be
            covered with a spoiler animation.
        :param supports_streaming: *Optional.* Pass ``True`` if the uploaded
            video is suitable for streaming.
        :param disable_notification: *Optional.* Sends the message silently.
            Users will receive a notification with no sound.
        :param protect_content: *Optional.* Protects the contents of the sent
            message from forwarding and saving.
        :param reply_to_message_id: *Optional.* If the message is a reply, ID
            of the original message.
        :param allow_sending_without_reply: *Optional.* Pass ``True`` if the
            message should be sent even if the specified replied-to message is
            not found.
        :param reply_markup: *Optional.* Additional interface options.
        """
        return await self._call_api(
            SendVideo(
                chat_id=chat_id,
                video=video,
                message_thread_id=message_thread_id,
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
                reply_to_message_id=reply_to_message_id,
                allow_sending_without_reply=allow_sending_without_reply,
                reply_markup=reply_markup,
            )
        )

    async def send_animation(
        self,
        chat_id: str | int,
        animation: InputFile | str,
        *,
        message_thread_id: NoneInt = None,
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
        reply_to_message_id: NoneInt = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Use this method to send animation files (GIF or H.264/MPEG-4 AVC
        video without sound).

        .. important::

            Bots can currently send animation files of up to 50 MB in size,
            this limit may be changed in the future.

        See: https://core.telegram.org/bots/api#sendanimation

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param animation: Animation to send.
        :param message_thread_id: *Optional.* Unique identifier for the target
            message thread (topic) of the forum; for forum supergroups only.
        :param duration: *Optional.* Duration of sent animation in seconds.
        :param width: *Otpional.* Animation width.
        :param height: *Optional.* Animation height.
        :param thumbnail: *Optional.* Thumbnail of the file sent; can be ignored
            if thumbnail generation for the file is supported server-side. The
            thumbnail should be in JPEG format and less than 200 kB in size. A
            thumbnail's width and height should not exceed 320.
        :param caption: *Optional.* Animation caption (may also be used when
            resending animation by ``file_id``), 0-1024 characters after
            entities parsing.
        :param parse_mode: *Optional.* Mode for parsing entities in the
            animation caption.
        :param caption_entities: *Optional.* list of
            :class:`~yatbaf.types.message_entity.MessageEntity`
            that appear in the caption, which can be specified instead of
            ``parse_mode``.
        :param has_spoiler: *Optional.* Pass ``True`` if the animation needs
            to be covered with a spoiler animation.
        :param disable_notification: *Optional.* Sends the message silently.
            Users will receive a notification with no sound.
        :param protect_content: *Optional.* Protects the contents of the sent
            message from forwarding and saving.
        :param reply_to_message_id: *Optional.* If the message is a reply, ID
            of the original message.
        :param allow_sending_without_reply: *Optional.* Pass ``True`` if the
            message should be sent even if the specified replied-to message is
            not found.
        :param reply_markup: *Optional.* Additional interface options.
        """
        return await self._call_api(
            SendAnimation(
                chat_id=chat_id,
                animation=animation,
                message_thread_id=message_thread_id,
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
                reply_to_message_id=reply_to_message_id,
                allow_sending_without_reply=allow_sending_without_reply,
                reply_markup=reply_markup,
            )
        )

    async def send_voice(
        self,
        chat_id: str | int,
        voice: InputFile | str,
        *,
        message_thread_id: NoneInt = None,
        caption: NoneStr = None,
        parse_mode: ParseMode | None = None,
        caption_entities: list[MessageEntity] | None = None,
        duration: NoneInt = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        reply_to_message_id: NoneInt = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Use this method to send audio files, if you want Telegram clients to
        display the file as a playable voice message. For this to work, your
        audio must be in an .OGG file encoded with OPUS (other formats may be
        sent as Audio or Document).

        .. important::

            Bots can currently send voice messages of up to 50 MB in size, this
            limit may be changed in the future.

        See: https://core.telegram.org/bots/api#sendvoice

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param voice: Audio file to send.
        :param message_thread_id: *Optional.* Unique identifier for the target
            message thread (topic) of the forum; for forum supergroups only.
        :param caption: *Optional.* Voice message caption, 0-1024 characters
            after entities parsing.
        :param parse_mode: *Optional.* Mode for parsing entities in the voice
            message caption.
        :param caption_entities: *Optional.* List of
            :class:`~yatbaf.types.message_entity.MessageEntity`
            that appear in the caption, which can be specified instead of
            ``parse_mode``.
        :param duration: *Optional.* Duration of the voice message in seconds.
        :param disable_notification: *Optional.* Sends the message silently.
            Users will receive a notification with no sound.
        :param protect_content: *Optional.* Protects the contents of the sent
            message from forwarding and saving.
        :param reply_to_message_id: *Optional.* If the message is a reply, ID
            of the original message.
        :param allow_sending_without_reply: *Optional.* Pass ``True`` if the
            message should be sent even if the specified replied-to message is
            not found.
        :param reply_markup: *Optional.* Additional interface options.
        """
        return await self._call_api(
            SendVoice(
                chat_id=chat_id,
                voice=voice,
                message_thread_id=message_thread_id,
                caption=caption,
                parse_mode=parse_mode,
                caption_entities=caption_entities,
                duration=duration,
                disable_notification=disable_notification,
                protect_content=protect_content,
                reply_to_message_id=reply_to_message_id,
                allow_sending_without_reply=allow_sending_without_reply,
                reply_markup=reply_markup,
            )
        )

    async def send_video_note(
        self,
        chat_id: str | int,
        video_note: InputFile | str,
        *,
        message_thread_id: NoneInt = None,
        duration: NoneInt = None,
        length: NoneInt = None,
        thumbnail: InputFile | str | None = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        reply_to_message_id: NoneInt = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Use this method to send video messages.

        See: https://core.telegram.org/bots/api#sendvidenote

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param video_note: Video note to send.
        :param message_thread_id: *Optional.* Unique identifier for the target
            message thread (topic) of the forum; for forum supergroups only.
        :param duration: *Optional.* Duration of sent video in seconds.
        :param length: *Optional.* Video width and height, i.e. diameter of
            the video message.
        :param thumbnail: *Optional.* Thumbnail of the file sent; can be ignored
            if thumbnail generation for the file is supported server-side. The
            thumbnail should be in JPEG format and less than 200 kB in size. A
            thumbnail's width and height should not exceed 320.
        :param disable_notification: *Optional.* Sends the message silently.
            Users will receive a notification with no sound.
        :param protect_content: *Optional.* Protects the contents of the sent
            message from forwarding and saving.
        :param reply_to_message_id: *Optional.* If the message is a reply, ID
            of the original message.
        :param allow_sending_without_reply: *Optional.* Pass ``True`` if the
            message should be sent even if the specified replied-to message is
            not found.
        :param reply_markup: *Optional.* Additional interface options.
        """
        return await self._call_api(
            SendVideoNote(
                chat_id=chat_id,
                video_note=video_note,
                message_thread_id=message_thread_id,
                duration=duration,
                length=length,
                thumbnail=thumbnail,
                disable_notification=disable_notification,
                protect_content=protect_content,
                reply_to_message_id=reply_to_message_id,
                allow_sending_without_reply=allow_sending_without_reply,
                reply_markup=reply_markup,
            )
        )

    # yapf: disable
    async def send_media_group(
        self,
        chat_id: str | int,
        media: list[InputMediaAudio | InputMediaDocument | InputMediaPhoto | InputMediaVideo],  # noqa: E501
        *,
        message_thread_id: NoneInt = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        reply_to_message_id: NoneInt = None,
        allow_sending_without_reply: NoneBool = None,
    ) -> list[Message]:
        """Use this method to send a group of photos, videos, documents or
        audios as an album.

        .. note::

            Documents and audio files can be only grouped in an album with
            messages of the same type.

        See: https://core.telegram.org/bots/api#sendmediagroup

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param media: A list of
            :class:`~yatbaf.types.input_media.InputMediaAudio`,
            :class:`~yatbaf.types.input_media.InputMediaDocument`,
            :class:`~yatbaf.types.input_media.InputMediaPhoto` and
            :class:`~yatbaf.types.input_media.InputMediaVideo`
            to be sent, must include 2-10 items.
        :param message_thread_id: *Optional.* Unique identifier for the target
            message thread (topic) of the forum; for forum supergroups only.
        :param disable_notification: *Optional.* Sends messages silently. Users
            will receive a notification with no sound.
        :param protect_content: *Optional.* Protects the contents of the sent
            messages from forwarding and saving.
        :param reply_to_message_id: *Optional.* If the messages are a reply, ID
            of the original message.
        :param allow_sending_without_reply: *Optional.* Pass ``True`` if the
            message should be sent even if the specified replied-to message
            is not found.
        """
        # yapf: enable
        return await self._call_api(
            SendMediaGroup(
                chat_id=chat_id,
                media=media,
                message_thread_id=message_thread_id,
                disable_notification=disable_notification,
                protect_content=protect_content,
                reply_to_message_id=reply_to_message_id,
                allow_sending_without_reply=allow_sending_without_reply,
            )
        )

    async def send_location(
        self,
        chat_id: str | int,
        latitude: float,
        longtitude: float,
        *,
        message_thread_id: NoneInt = None,
        horizontal_accuracy: float | None = None,
        live_period: NoneInt = None,
        heading: NoneInt = None,
        proximity_alert_radius: NoneInt = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        reply_to_message_id: NoneInt = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Use this method to send point on the map.

        See: https://core.telegram.org/bots/api#sendlocation

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param latitude: Latitude of the location.
        :param longtitude: Longitude of the location.
        :param message_thread_id: *Optional.* Unique identifier for the target
            message thread (topic) of the forum; for forum supergroups only.
        :param horizontal_accuracy: *Optional.* The radius of uncertainty for
            the location, measured in meters; 0-1500.
        :param live_period: *Optional.* Period in seconds for which the
            location will be updated (see `Live Locations`_), should be
            between 60 and 86400.
        :param heading: *Optional.* For live locations, a direction in which
            the user is moving, in degrees. Must be between 1 and 360 if
            specified.
        :param proximity_alert_radius: *Optional.* For live locations, a
            maximum distance for proximity alerts about approaching another
            chat member, in meters. Must be between 1 and 100000 if specified.
        :param disable_notification: *Optional.* Sends the message silently.
            Users will receive a notification with no sound.
        :param protect_content: *Optional.* Protects the contents of the sent
            message from forwarding and saving.
        :param reply_to_message_id: *Optional.* If the message is a reply, ID
            of the original message.
        :param allow_sending_without_reply: *Optional.* Pass ``True`` if the
            message should be sent even if the specified replied-to message
            is not found.
        :param reply_markup: *Optional.* Additional interface options.

        .. _Live Locations: https://telegram.org/blog/live-locations
        """
        return await self._call_api(
            SendLocation(
                chat_id=chat_id,
                latitude=latitude,
                longtitude=longtitude,
                message_thread_id=message_thread_id,
                horizontal_accuracy=horizontal_accuracy,
                live_period=live_period,
                heading=heading,
                proximity_alert_radius=proximity_alert_radius,
                disable_notification=disable_notification,
                protect_content=protect_content,
                reply_to_message_id=reply_to_message_id,
                allow_sending_without_reply=allow_sending_without_reply,
                reply_markup=reply_markup,
            )
        )

    async def send_venue(
        self,
        chat_id: str | int,
        latitude: float,
        longtitude: float,
        title: str,
        address: str,
        *,
        message_thread_id: NoneInt = None,
        foursquare_id: NoneStr = None,
        foursquare_type: NoneStr = None,
        google_place_id: NoneStr = None,
        google_place_type: NoneStr = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        reply_to_message_id: NoneInt = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Use this method to send information about a venue.

        See: https://core.telegram.org/bots/api#sendvenue

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param latitude: Latitude of the venue.
        :param longtitude: Longitude of the venue.
        :param title: Name of the venue.
        :param address: Address of the venue.
        :param message_thread_id: *Optional.* Unique identifier for the target
            message thread (topic) of the forum; for forum supergroups only.
        :param foursquare_id: *Optional.* Foursquare identifier of the venue.
        :param foursquare_type: *Optional.* Foursquare type of the venue, if
            known.
        :param google_place_id: *Optional.* Google Places identifier of the
            venue.
        :param google_place_type: *Optional.* Google Places type of the venue.
            See `supported types`_.
        :param disable_notification: *Optional.* Sends the message silently.
            Users will receive a notification with no sound.
        :param protect_content: *Optional.* Protects the contents of the sent
            message from forwarding and saving.
        :param reply_to_message_id: *Optional.* If the message is a reply,
            ID of the original message.
        :param allow_sending_without_reply: *Optional.* Pass ``True`` if the
            message should be sent even if the specified replied-to message
            is not found.
        :param reply_markup: *Optional.* Additional interface options.

        .. _supported types: https://developers.google.com/places/web-service/supported_types
        """  # noqa: E501
        return await self._call_api(
            SendVenue(
                chat_id=chat_id,
                latitude=latitude,
                longtitude=longtitude,
                title=title,
                address=address,
                message_thread_id=message_thread_id,
                foursquare_id=foursquare_id,
                foursquare_type=foursquare_type,
                google_place_id=google_place_id,
                google_place_type=google_place_type,
                disable_notification=disable_notification,
                protect_content=protect_content,
                reply_to_message_id=reply_to_message_id,
                allow_sending_without_reply=allow_sending_without_reply,
                reply_markup=reply_markup,
            )
        )

    async def send_contact(
        self,
        chat_id: str | int,
        phone_number: str,
        first_name: str,
        *,
        message_thread_id: NoneInt = None,
        last_name: NoneStr = None,
        vcard: NoneStr = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        reply_to_message_id: NoneInt = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Use this method to send phone contacts.

        See: https://core.telegram.org/bots/api#sendcontact

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param phone_number: Contact's phone number.
        :param first_name: Contact's first name.
        :param message_thread_id: *Optional.* Unique identifier for the target
            message thread (topic) of the forum; for forum supergroups only.
        :param last_name: *Optional.* Contact's last name.
        :param vcard: *Optional.* Additional data about the contact in the
            form of a vCard, 0-2048 bytes.
        :param disable_notification: *Optional.* Sends the message silently.
            Users will receive a notification with no sound.
        :param protect_content: *Optional.* Protects the contents of the sent
            message from forwarding and saving.
        :param reply_to_message_id: *Optional.* If the message is a reply, ID
            of the original message.
        :param allow_sending_without_reply: *Optional.* Pass ``True`` if the
            message should be sent even if the specified replied-to message is
            not found.
        :param reply_markup: *Optional.* Additional interface options.
        """
        return await self._call_api(
            SendContact(
                chat_id=chat_id,
                phone_number=phone_number,
                first_name=first_name,
                message_thread_id=message_thread_id,
                last_name=last_name,
                vcard=vcard,
                disable_notification=disable_notification,
                protect_content=protect_content,
                reply_to_message_id=reply_to_message_id,
                allow_sending_without_reply=allow_sending_without_reply,
                reply_markup=reply_markup,
            )
        )

    async def send_poll(
        self,
        chat_id: str | int,
        question: str,
        options: list[str],
        *,
        message_thread_id: NoneInt = None,
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
        reply_to_message_id: NoneInt = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Use this method to send a native poll.

        See: https://core.telegram.org/bots/api#sendpoll

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param question: Poll question, 1-300 characters.
        :param options: List of answer options, 2-10 strings 1-100 characters
            each.
        :param message_thread_id: *Optional.* Unique identifier for the target
            message thread (topic) of the forum; for forum supergroups only.
        :param is_anonymous: *Optional.* ``True``, if the poll needs to be
            anonymous, defaults to ``True``.
        :param type: *Optional.* Poll type.
        :param allows_multiple_answers: *Optional.* ``True``, if the poll
            allows multiple answers, ignored for polls in quiz mode, defaults
            to ``False``.
        :param correct_option_id: *Optional.* 0-based identifier of the correct
            answer option, required for polls in quiz mode.
        :param explanation: *Optional.* Text that is shown when a user chooses
            an incorrect answer or taps on the lamp icon in a quiz-style poll,
            0-200 characters with at most 2 line feeds after entities parsing.
        :param explanation_parse_mode: *Optional.* Mode for parsing entities
            in the explanation.
        :param explanation_entities: *Optional.* list of
            :class:`MessageEntity <yatbaf.types.MessageEntity>` that appear
            in the poll explanation, which can be specified instead of
            ``explanation_parse_mode``.
        :param open_period: *Optional.* Amount of time in seconds the poll will
            be active after creation, 5-600. Can't be used together with
            ``close_date``.
        :param close_date: *Optional.* Point in time (Unix timestamp) when the
            poll will be automatically closed. Must be at least 5 and no more
            than 600 seconds in the future. Can't be used together with
            ``open_period``.
        :param is_closed: *Optional.* Pass ``True`` if the poll needs to be
            immediately closed. This can be useful for poll preview.
        :param disable_notification: *Optional.* Sends the message silently.
            Users will receive a notification with no sound.
        :param protect_content: *Optional.* Protects the contents of the sent
            message from forwarding and saving.
        :param reply_to_message_id: *Optional.* If the message is a reply, ID
            of the original message.
        :param allow_sending_without_reply: *Optional.* Pass ``True`` if the
            message should be sent even if the specified replied-to message is
            not found.
        :param reply_markup: *Optional.* Additional interface options.
        """
        return await self._call_api(
            SendPoll(
                chat_id=chat_id,
                question=question,
                options=options,
                message_thread_id=message_thread_id,
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
                reply_to_message_id=reply_to_message_id,
                allow_sending_without_reply=allow_sending_without_reply,
                reply_markup=reply_markup,
            )
        )

    async def send_dice(
        self,
        chat_id: str | int,
        *,
        message_thread_id: NoneInt = None,
        emoji: NoneStr = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        reply_to_message_id: NoneInt = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Use this method to send an animated emoji that will display a random
        value.

        See: https://core.telegram.org/bots/api#senddice

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param message_thread_id: *Optional.* Unique identifier for the target
            message thread (topic) of the forum; for forum supergroups only.
        :param emoji: *Optional.* Emoji on which the dice throw animation is
            based.
        :param disable_notification: *Optional.* Sends the message silently.
            Users will receive a notification with no sound.
        :param protect_content: *Optional.* Protects the contents of the sent
            message from forwarding.
        :param reply_to_message_id: *Optional.* If the message is a reply, ID
            of the original message.
        :param allow_sending_without_reply: *Optional.* Pass ``True`` if the
            message should be sent even if the specified replied-to message
            is not found.
        :param reply_markup: *Optional.* Additional interface options.
        """
        return await self._call_api(
            SendDice(
                chat_id=chat_id,
                message_thread_id=message_thread_id,
                emoji=emoji,
                disable_notification=disable_notification,
                protect_content=protect_content,
                reply_to_message_id=reply_to_message_id,
                allow_sending_without_reply=allow_sending_without_reply,
                reply_markup=reply_markup,
            )
        )

    async def send_chat_action(
        self,
        chat_id: str | int,
        action: ChatAction,
        *,
        message_thread_id: NoneInt = None,
    ) -> bool:
        """Use this method when you need to tell the user that something is
        happening on the bot's side. The status is set for 5 seconds or less
        (when a message arrives from your bot, Telegram clients clear its
        typing status).

        See: https://core.telegram.org/bots/api#sendchataction

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param action: :class:`~yatbaf.enums.ChatAction` to broadcast.
        :param action: *Optional.* Unique identifier for the target message
            thread; supergroups only.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            SendChatAction(
                chat_id=chat_id,
                action=action,
                message_thread_id=message_thread_id,
            )
        )

    async def get_user_profile_photos(
        self,
        user_id: int,
        *,
        offset: NoneInt = None,
        limit: NoneInt = None,
    ) -> UserProfilePhotos:
        """Use this method to get a list of profile pictures for a user.

        See: https://core.telegram.org/bots/api#getuserprofilephotos

        :param user_id: Unique identifier of the target user.
        :param offset: *Optional.* Sequential number of the first photo to be
            returned. By default, all photos are returned.
        :param limit: *Optional.* Limits the number of photos to be retrieved.
            Values between 1-100 are accepted. Defaults to 100.
        """
        return await self._call_api(
            GetUserProfilePhotos(
                user_id=user_id,
                offset=offset,
                limit=limit,
            )
        )

    async def get_file(self, file_id: str) -> File:
        """Use this method to get basic information about a file and prepare
        it for downloading.

        See: https://core.telegram.org/bots/api#getfile

        :param file_id: File identifier to get information about.
        :returns: :class:`~yatbaf.types.file.File` object on success.
        """
        return await self._call_api(GetFile(file_id=file_id))

    async def ban_chat_member(
        self,
        chat_id: str | int,
        user_id: int,
        *,
        until_date: NoneInt = None,
        revorke_messages: NoneBool = None,
    ) -> bool:
        """Use this method to ban a user in a group, a supergroup or a channel.

        .. important::

            The bot must be an administrator in the chat for this to work and
            must have the appropriate administrator rights.

        See: https://core.telegram.org/bots/api#banchatmember

        :param chat_id: Unique identifier for the target group or username of
            the target supergroup or channel (in the format @channelusername).
        :param user_id: Unique identifier of the target user.
        :param until_date: *Optional.* Date when the user will be unbanned,
            unix time. If user is banned for more than 366 days or less than
            30 seconds from the current time they are considered to be banned
            forever. Applied for supergroups and channels only.
        :param revorke_messages: *Optional.* Pass ``True`` to delete all
            messages from the chat for the user that is being removed. If
            ``False``, the user will be able to see messages in the group that
            were sent before the user was removed. Always ``True`` for
            supergroups and channels.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            BanChatMember(
                chat_id=chat_id,
                user_id=user_id,
                until_date=until_date,
                revorke_messages=revorke_messages,
            )
        )

    async def unban_chat_member(
        self,
        chat_id: str | int,
        user_id: int,
        *,
        only_if_banned: NoneBool = None,
    ) -> bool:
        """Use this method to unban a previously banned user in a supergroup
        or channel.

        .. important::

            The bot must be an administrator for this to work.

        See: https://core.telegram.org/bots/api#unbanchatmember

        :param chat_id: Unique identifier for the target group or username of
            the target supergroup or channel (in the format @channelusername).
        :param user_id: Unique identifier of the target user.
        :param only_if_banned: *Optional.* Do nothing if the user is not banned.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            UnbanChatMember(
                chat_id=chat_id,
                user_id=user_id,
                only_if_banned=only_if_banned,
            )
        )

    async def restrict_chat_member(
        self,
        chat_id: str | int,
        user_id: int,
        permissions: ChatPermissions,
        *,
        use_independent_chat_permissions: NoneBool = None,
        until_date: NoneInt = None,
    ) -> bool:
        """Use this method to restrict a user in a supergroup. Pass ``True`` for
        all permissions to lift restrictions from a user.

        .. important::

            The bot must be an administrator in the supergroup for this to work
            and must have the appropriate administrator rights.

        See: https://core.telegram.org/bots/api#restrictchatmember

        :param chat_id: Unique identifier for the target chat or username of
            the target supergroup (in the format @supergroupusername).
        :param user_id: Unique identifier of the target user.
        :param permissions: New user permissions.
        :param use_independent_chat_permissions: *Optional.* Pass ``True`` if
            chat permissions are set independently. Otherwise, the
            ``can_send_other_messages`` and ``can_add_web_page_previews``
            permissions will imply the ``can_send_messages``,
            ``can_send_audios``, ``can_send_documents``, ``can_send_photos``,
            ``can_send_videos``, ``can_send_video_notes``, and
            ``can_send_voice_notes`` permissions; the ``can_send_polls``
            permission will imply the ``can_send_messages`` permission.
        :param until_date: *Optional.* Date when restrictions will be lifted
            for the user, unix time. If user is restricted for more than 366
            days or less than 30 seconds from the current time, they are
            considered to be restricted forever.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            RestrictChatMember(
                chat_id=chat_id,
                user_id=user_id,
                permissions=permissions,
                use_independent_chat_permissions=use_independent_chat_permissions,  # noqa: E501
                until_date=until_date,
            )
        )  # yapf: disable

    async def promote_chat_member(
        self,
        chat_id: str | int,
        user_id: int,
        *,
        is_anonymous: NoneBool = None,
        can_manage_chat: NoneBool = None,
        can_post_messages: NoneBool = None,
        can_edit_messages: NoneBool = None,
        can_delete_messages: NoneBool = None,
        can_manage_video_chats: NoneBool = None,
        can_restrict_members: NoneBool = None,
        can_promote_members: NoneBool = None,
        can_change_info: NoneBool = None,
        can_invite_users: NoneBool = None,
        can_pin_messages: NoneBool = None,
        can_post_stories: NoneBool = None,
        can_edit_stories: NoneBool = None,
        can_delete_stories: NoneBool = None,
        can_manage_topics: NoneBool = None,
    ) -> bool:
        """Use this method to promote or demote a user in a supergroup or a
        channel. Pass ``False`` for all boolean parameters to demote a user.

        .. important::

            The bot must be an administrator in the chat for this to work and
            must have the appropriate administrator rights.

        See: https://core.telegram.org/bots/api#promotechatmember

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param user_id: Unique identifier of the target user.
        :param is_anonymous: *Optional.* Pass ``True`` if the administrator's
            presence in the chat is hidden.
        :param can_manage_chat: *Optional.* Pass ``True`` if the administrator
            can access the chat event log, chat statistics, message statistics
            in channels, see channel members, see anonymous administrators in
            supergroups and ignore slow mode. Implied by any other
            administrator privilege.
        :param can_post_messages: *Optional.* Pass ``True`` if the administrator
            can create channel posts, channels only.
        :param can_edit_messages: *Optional.* Pass ``True`` if the administrator
            can edit messages of other users and can pin messages, channels only.
        :param can_delete_messages: *Optional.* Pass ``True`` if the
            administrator can delete messages of other users.
        :param can_manage_video_chats: *Optional.* Pass ``True`` if the
            administrator can manage video chats.
        :param can_restrict_members: *Optional.* Pass ``True`` if the
            administrator can restrict, ban or unban chat members.
        :param can_promote_members: *Optional.* Pass ``True`` if the
            administrator can add new administrators with a subset of their own
            privileges or demote administrators that they have promoted,
            directly or indirectly (promoted by administrators that were
            appointed by him).
        :param can_change_info: *Optional.* Pass ``True`` if the administrator
            can change chat title, photo and other settings.
        :param can_invite_users: *Optional.* Pass ``True`` if the administrator
            can invite new users to the chat.
        :param can_pin_messages: *Optional.* Pass ``True`` if the administrator
            can pin messages, supergroups only.
        :param can_post_stories: *Optional.* Pass ``True`` if the administrator
            can post stories in the channel; channels only.
        :param can_edit_stories: *Optional.* Pass ``True`` if the administrator
            can edit stories posted by other users; channels only.
        :param can_delete_stories: *Optional.* Pass ``True`` if the administrator
            can delete stories posted by other users; channels only.
        :param can_manage_topics: *Optional.* Pass ``True`` if the user is
            allowed to create, rename, close, and reopen forum topics,
            supergroups only.
        :returns: ``True`` on success.
        """  # noqa: E501
        return await self._call_api(
            PromoteChatMember(
                chat_id=chat_id,
                user_id=user_id,
                is_anonymous=is_anonymous,
                can_manage_chat=can_manage_chat,
                can_post_messages=can_post_messages,
                can_edit_messages=can_edit_messages,
                can_delete_messages=can_delete_messages,
                can_manage_video_chats=can_manage_video_chats,
                can_restrict_members=can_restrict_members,
                can_promote_members=can_promote_members,
                can_change_info=can_change_info,
                can_invite_users=can_invite_users,
                can_pin_messages=can_pin_messages,
                can_post_stories=can_post_stories,
                can_edit_stories=can_edit_stories,
                can_delete_stories=can_delete_stories,
                can_manage_topics=can_manage_topics,
            )
        )

    async def set_chat_administrator_custom_title(
        self,
        chat_id: str | int,
        user_id: int,
        custom_title: str,
    ) -> bool:
        """Use this method to set a custom title for an administrator in a
        supergroup promoted by the bot.

        See: https://core.telegram.org/bots/api#setchatadministratorcustomtitle

        :param chat_id: Unique identifier for the target chat or username of
            the target supergroup (in the format @supergroupusername).
        :param user_id: Unique identifier of the target user.
        :param custom_title: New custom title for the administrator;
            0-16 characters, emoji are not allowed.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            SetChatAdministratorCustomTitle(
                chat_id=chat_id,
                user_id=user_id,
                custom_title=custom_title,
            )
        )

    async def ban_chat_sender_chat(
        self,
        chat_id: str | int,
        sender_chat_id: int,
    ) -> bool:
        """Use this method to ban a channel chat in a supergroup or a channel.
        Until the chat is unbanned, the owner of the banned chat won't be able
        to send messages on behalf of **any of their channels**.

        .. important::

            The bot must be an administrator in the supergroup or channel for
            this to work and must have the appropriate administrator rights.

        See: https://core.telegram.org/bots/api#banchatsenderchat

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param sender_chat_id: Unique identifier of the target sender chat.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            BanChatSenderChat(
                chat_id=chat_id,
                sender_chat_id=sender_chat_id,
            )
        )

    async def unban_chat_sender_chat(
        self,
        chat_id: str | int,
        sender_chat_id: int,
    ) -> bool:
        """Use this method to unban a previously banned channel chat in a
        supergroup or channel.

        .. important::

            The bot must be an administrator for this to work and must have
            the appropriate administrator rights.

        See: https://core.telegram.org/bots/api#unbanchatsenderchat

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param sender_chat_id: Unique identifier of the target sender chat.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            UnbanChatSenderChat(
                chat_id=chat_id,
                sender_chat_id=sender_chat_id,
            )
        )

    async def set_chat_permissions(
        self,
        chat_id: str | int,
        permissions: ChatPermissions,
        *,
        use_independent_chat_permissions: NoneBool = None,
    ) -> bool:
        """Use this method to set default chat permissions for all members.

        .. important::

            The bot must be an administrator in the group or a supergroup for
            this to work and must have the ``can_restrict_members``
            administrator rights.

        See: https://core.telegram.org/bots/api#setchatpermissions

        :param chat_id: Unique identifier for the target chat or username of
            the target supergroup (in the format @supergroupusername).
        :param permissions: New default chat permissions.
        :param use_independent_chat_permissions: *Optional.* Pass ``True`` if chat
            permissions are set independently. Otherwise, the ``can_send_other_messages``
            and ``can_add_web_page_previews`` permissions will imply the
            ``can_send_messages``, ``can_send_audios``, ``can_send_documents``,
            ``can_send_photos``, ``can_send_videos``, ``can_send_video_notes``,
            and ``can_send_voice_notes`` permissions; the ``can_send_polls``
            permission will imply the ``can_send_messages`` permission.
        :returns: ``True`` on success.
        """  # noqa: E501
        return await self._call_api(
            SetChatPermissions(
                chat_id=chat_id,
                permissions=permissions,
                use_independent_chat_permissions=use_independent_chat_permissions,  # noqa: E501
            )
        )  # yapf: disable

    async def export_chat_invite_link(
        self,
        chat_id: str | int,
    ) -> str:
        """Use this method to generate a new primary invite link for a chat;
        any previously generated primary link is revoked.

        .. important::

            The bot must be an administrator in the chat for this to work and
            must have the appropriate administrator rights.

        See: https://core.telegram.org/bots/api#exportchatinvitelink

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :returns: New invite link as :class:`str` on success.
        """
        return await self._call_api(ExportChatInviteLink(chat_id=chat_id))

    async def create_chat_invite_link(
        self,
        chat_id: str | int,
        *,
        name: NoneStr = None,
        expire_date: NoneInt = None,
        member_limit: NoneInt = None,
        creates_join_request: NoneBool = None,
    ) -> ChatInviteLink:
        """Use this method to create an additional invite link for a chat.

        .. important::

            The bot must be an administrator in the chat for this to work and
            must have the appropriate administrator rights.

        See: https://core.telegram.org/bots/api#createchatinvitelink

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param name: *Optional.* Invite link name; 0-32 characters.
        :param expire_date: *Optional.* Point in time (Unix timestamp) when the
            link will expire.
        :param member_limit: *Optional.* The maximum number of users that can
            be members of the chat simultaneously after joining the chat via
            this invite link; 1-99999.
        :param creates_join_request: *Optional.* ``True``, if users joining the
            chat via the link need to be approved by chat administrators.
            If ``True``, ``member_limit`` can't be specified.
        """
        return await self._call_api(
            CreateChatInviteLink(
                chat_id=chat_id,
                name=name,
                expire_date=expire_date,
                member_limit=member_limit,
                creates_join_request=creates_join_request,
            )
        )

    async def edit_chat_invite_link(
        self,
        chat_id: str | int,
        invite_link: str,
        *,
        name: NoneStr = None,
        expire_date: NoneInt = None,
        member_limit: NoneInt = None,
        creates_join_request: NoneBool = None,
    ) -> ChatInviteLink:
        """Use this method to edit a non-primary invite link created by the bot.

        .. important::

            The bot must be an administrator in the chat for this to work and
            must have the appropriate administrator rights.

        See: https://core.telegram.org/bots/api#editchatinvitelink

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param invite_link: The invite link to edit.
        :param name: *Optional.* Invite link name; 0-32 characters.
        :param expire_date: *Optional.* Point in time (Unix timestamp) when the
            link will expire.
        :param member_limit: *Optional.* The maximum number of users that can
            be members of the chat simultaneously after joining the chat via
            this invite link; 1-99999.
        :param creates_join_request: *Optional.* ``True``, if users joining the
            chat via the link need to be approved by chat administrators.
            If ``True``, ``member_limit`` can't be specified.
        """
        return await self._call_api(
            EditChatInviteLink(
                chat_id=chat_id,
                invite_link=invite_link,
                name=name,
                expire_date=expire_date,
                member_limit=member_limit,
                creates_join_request=creates_join_request,
            )
        )

    async def revoke_chat_invite_link(
        self,
        chat_id: str | int,
        invite_link: str,
    ) -> ChatInviteLink:
        """Use this method to revoke an invite link created by the bot.

        .. important::

            If the primary link is revoked, a new link is automatically
            generated. The bot must be an administrator in the chat for this to
            work and must have the appropriate administrator rights.

        See: https://core.telegram.org/bots/api#revokechatinvitelink

        :param chat_id: Unique identifier of the target chat or username of the
            target channel (in the format @channelusername).
        :param invite_link: The invite link to revoke.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            RevokeChatInviteLink(
                chat_id=chat_id,
                invite_link=invite_link,
            )
        )

    async def approve_chat_join_request(
        self,
        chat_id: str | int,
        user_id: int,
    ) -> bool:
        """Use this method to approve a chat join request.

        .. important::

            The bot must be an administrator in the chat for this to work and
            must have the ``can_invite_users`` administrator right.

        See: https://core.telegram.org/bots/api#approvechatjoinrequest

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param user_id: Unique identifier of the target user.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            ApproveChatJoinRequest(
                chat_id=chat_id,
                user_id=user_id,
            )
        )

    async def decline_chat_join_request(
        self,
        chat_id: str | int,
        user_id: int,
    ) -> bool:
        """Use this method to decline a chat join request.

        .. important::

            The bot must be an administrator in the chat for this to work and
            must have the ``can_invite_users`` administrator right.

        See: https://core.telegram.org/bots/api#declinechatjoinrequest

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param user_id: Unique identifier of the target user.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            DeclineChatJoinRequest(
                chat_id=chat_id,
                user_id=user_id,
            )
        )

    async def set_chat_photo(
        self,
        chat_id: str | int,
        photo: InputFile,
    ) -> bool:
        """Use this method to set a new profile photo for the chat.

        .. important::

            Photos can't be changed for private chats. The bot must be an
            administrator in the chat for this to work and must have the
            appropriate administrator rights.

        See: https://core.telegram.org/bots/api#setchatphoto

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param photo: New chat photo.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            SetChatPhoto(
                chat_id=chat_id,
                photo=photo,
            )
        )

    async def delete_chat_photo(self, chat_id: str | int) -> bool:
        """Use this method to delete a chat photo.

        .. important::

            Photos can't be changed for private chats. The bot must be an
            administrator in the chat for this to work and must have the
            appropriate administrator rights.

        See: https://core.telegram.org/bots/api#deletechatphoto

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :returns: ``True`` on success.
        """
        return await self._call_api(DeleteChatPhoto(chat_id=chat_id))

    async def set_chat_title(
        self,
        chat_id: str | int,
        title: str,
    ) -> bool:
        """Use this method to change the title of a chat.

        .. important::

            Titles can't be changed for private chats. The bot must be an
            administrator in the chat for this to work and must have the
            appropriate administrator rights.

        See: https://core.telegram.org/bots/api#setchattitle

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param title: New chat title, 1-128 characters.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            SetChatTitle(
                chat_id=chat_id,
                title=title,
            )
        )

    async def set_chat_description(
        self,
        chat_id: str | int,
        *,
        description: NoneStr = None,
    ) -> bool:
        """Use this method to change the description of a group, a supergroup
        or a channel.

        .. important::

            The bot must be an administrator in the chat for this to work and
            must have the appropriate administrator rights.

        See: https://core.telegram.org/bots/api#setchatdescription

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param description: *Optional.* New chat description, 0-255 characters.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            SetChatDescription(
                chat_id=chat_id,
                description=description,
            )
        )

    async def pin_chat_message(
        self,
        chat_id: str | int,
        message_id: int,
        disable_notification: NoneBool = None,
    ) -> bool:
        """Use this method to add a message to the list of pinned messages in
        a chat.

        .. important::

            If the chat is not a private chat, the bot must be an administrator
            in the chat for this to work and must have the ``can_pin_messages``
            administrator right in a supergroup or ``can_edit_messages``
            administrator right in a channel.

        See: https://core.telegram.org/bots/api#pinchatmessage

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param message_id: Identifier of a message to pin.
        :param disable_notification: *Optional.* Pass ``True`` if it is not
            necessary to send a notification to all chat members about the new
            pinned message. Notifications are always disabled in channels and
            private chats.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            PinChatMessage(
                chat_id=chat_id,
                message_id=message_id,
                disable_notification=disable_notification,
            )
        )

    async def unpin_chat_message(
        self,
        chat_id: str | int,
        message_id: NoneInt = None,
    ) -> bool:
        """Use this method to remove a message from the list of pinned messages
        in a chat.

        .. important::

            If the chat is not a private chat, the bot must be an administrator
            in the chat for this to work and must have the ``can_pin_messages``
            administrator right in a supergroup or ``can_edit_messages``
            administrator right in a channel.

        See: https://core.telegram.org/bots/api#unpinchatmessage

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param message_id: *Optional.* Identifier of a message to unpin. If not
            specified, the most recent pinned message (by sending date) will be
            unpinned.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            UnpinChatMessage(
                chat_id=chat_id,
                message_id=message_id,
            )
        )

    async def unpin_all_chat_messages(
        self,
        chat_id: str | int,
    ) -> bool:
        """Use this method to clear the list of pinned messages in a chat.

        .. important::

            If the chat is not a private chat, the bot must be an administrator
            in the chat for this to work and must have the ``can_pin_messages``
            administrator right in a supergroup or ``can_edit_messages``
            administrator right in a channel.

        See: https://core.telegram.org/bots/api#unpinallchatmessages

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :returns: ``True`` on success.
        """
        return await self._call_api(UnpinAllChatMessages(chat_id=chat_id))

    async def leave_chat(
        self,
        chat_id: str | int,
    ) -> bool:
        """Use this method for your bot to leave a group, supergroup or channel.

        See: https://core.telegram.org/bots/api#leavechat

        :param chat_id: Unique identifier for the target chat or username of
            the target supergroup or channel (in the format @channelusername).
        :returns: ``True`` on success.
        """
        return await self._call_api(LeaveChat(chat_id=chat_id))

    async def get_chat(
        self,
        chat_id: str | int,
    ) -> Chat:
        """Use this method to get up to date information about the chat (current
        name of the user for one-on-one conversations, current username of a
        user, group or channel, etc.).

        See: https://core.telegram.org/bots/api#getchat

        :param chat_id: Unique identifier for the target chat or username of
            the target supergroup or channel (in the format @channelusername).
        """
        return await self._call_api(GetChat(chat_id=chat_id))

    async def get_chat_administrators(
        self,
        chat_id: str | int,
    ) -> list[ChatMember]:
        """Use this method to get a list of administrators in a chat, which
        aren't bots.

        See: https://core.telegram.org/bots/api#getchatadministrators

        :param chat_id: Unique identifier for the target chat or username of
            the target supergroup or channel (in the format @channelusername).
        """
        return await self._call_api(GetChatAdministrators(chat_id=chat_id))

    async def get_chat_member_count(
        self,
        chat_id: str | int,
    ) -> int:
        """Use this method to get the number of members in a chat.

        See: https://core.telegram.org/bots/api#getchatmembercount

        :param chat_id: Unique identifier for the target chat or username of
            the target supergroup or channel (in the format @channelusername).
        """
        return await self._call_api(GetChatMemberCount(chat_id=chat_id))

    async def get_chat_member(
        self,
        chat_id: str | int,
        user_id: int,
    ) -> ChatMember:
        """Use this method to get information about a member of a chat.

        .. important::

            The method is only guaranteed to work for other users if the bot is
            an administrator in the chat.

        See: https://core.telegram.org/bots/api#getchatmember

        :param chat_id: Unique identifier for the target chat or username of
            the target supergroup or channel (in the format @channelusername).
        :param user_id: Unique identifier of the target user.
        """
        return await self._call_api(
            GetChatMember(
                chat_id=chat_id,
                user_id=user_id,
            )
        )

    async def set_chat_sticker_set(
        self,
        chat_id: str | int,
        sticker_set_name: str,
    ) -> bool:
        """Use this method to set a new group sticker set for a supergroup.

        .. important::

            The bot must be an administrator in the chat for this to work and
            must have the appropriate administrator rights. Use the field
            ``can_set_sticker_set`` optionally returned in :meth:`get_chat`
            requests to check if the bot can use this method.

        See: https://core.telegram.org/bots/api#setchatstickerset

        :param chat_id: Unique identifier for the target chat or username of
            the target supergroup (in the format @supergroupusername).
        :param sticker_set_name: Name of the sticker set to be set as the group
            sticker set.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            SetChatStickerSet(
                chat_id=chat_id,
                sticker_set_name=sticker_set_name,
            )
        )

    async def delete_chat_sticker_set(
        self,
        chat_id: str | int,
    ) -> bool:
        """Use this method to delete a group sticker set from a supergroup.

        .. important::

            The bot must be an administrator in the chat for this to work and
            must have the appropriate administrator rights. Use the field
            ``can_set_sticker_set`` optionally returned in :meth:`get_chat`
            requests to check if the bot can use this method.

        See: https://core.telegram.org/bots/api#deletechatstickerset

        :param chat_id: Unique identifier for the target chat or username of
            the target supergroup (in the format @supergroupusername).
        :returns: ``True`` on success.
        """
        return await self._call_api(DeleteChatStickerSet(chat_id=chat_id))

    async def get_forum_topic_icon_stickers(self) -> list[Sticker]:
        """Use this method to get custom emoji stickers, which can be used as
        a forum topic icon by any user.

        See: https://core.telegram.org/bots/api#getforumtopiciconstickers
        """
        return await self._call_api(GetForumTopicIconStickers())

    async def create_forum_topic(
        self,
        chat_id: str | int,
        name: str,
        *,
        icon_color: IconColor | None = None,
        icon_custom_emoji_id: NoneStr = None,
    ) -> ForumTopic:
        """Use this method to create a topic in a forum supergroup chat.

        .. important::

            The bot must be an administrator in the chat for this to work and
            must have the ``can_manage_topics`` administrator rights.

        See: https://core.telegram.org/bots/api#createforumtopic

        :param chat_id: Unique identifier for the target chat or username of
            the target supergroup (in the format @supergroupusername).
        :param name: Topic name, 1-128 characters.
        :param icon_color: *Optional.* Color of the topic icon.
        :param icon_custom_emoji_id: *Optional.* Unique identifier of the
            custom emoji shown as the topic icon. Use
            :meth:`get_forum_topic_icon_stickers` to get all allowed custom
            emoji identifiers.
        """
        return await self._call_api(
            CreateForumTopic(
                chat_id=chat_id,
                name=name,
                icon_color=icon_color,
                icon_custom_emoji_id=icon_custom_emoji_id,
            )
        )

    async def edit_forum_topic(
        self,
        chat_id: str | int,
        message_thread_id: int,
        *,
        name: NoneStr = None,
        icon_custom_emoji_id: NoneStr = None,
    ) -> bool:
        """Use this method to edit name and icon of a topic in a forum
        supergroup chat.

        .. important::

            The bot must be an administrator in the chat for this to work and
            must have ``can_manage_topics`` administrator rights, unless it is
            the creator of the topic.

        See: https://core.telegram.org/bots/api#editforumtopic

        :param chat_id: Unique identifier for the target chat or username of
            the target supergroup (in the format @supergroupusername).
        :param message_thread_id: Unique identifier for the target message
            thread of the forum topic.
        :param name: *Optional.* New topic name, 0-128 characters. If not
            specified or empty, the current name of the topic will be kept.
        :param icon_custom_emoji_id: *Optional.* New unique identifier of the
            custom emoji shown as the topic icon. Use
            :meth:`get_forum_topic_icon_stickers` to get all allowed custom
            emoji identifiers. Pass an empty string to remove the icon. If not
            specified, the current icon will be kept.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            EditForumTopic(
                chat_id=chat_id,
                message_thread_id=message_thread_id,
                name=name,
                icon_custom_emoji_id=icon_custom_emoji_id,
            )
        )

    async def close_forum_topic(
        self,
        chat_id: str | int,
        message_thread_id: int,
    ) -> bool:
        """Use this method to close an open topic in a forum supergroup chat.

        .. important::

            The bot must be an administrator in the chat for this to work and
            must have the ``can_manage_topics`` administrator rights, unless
            it is the creator of the topic.

        See: https://core.telegram.org/bots/api#closeforumtopic

        :param chat_id: Unique identifier for the target chat or username of
            the target supergroup (in the format @supergroupusername).
        :param message_thread_id: Unique identifier for the target message
            thread of the forum topic.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            CloseForumTopic(
                chat_id=chat_id,
                message_thread_id=message_thread_id,
            )
        )

    async def reopen_forum_topic(
        self,
        chat_id: str | int,
        message_thread_id: int,
    ) -> bool:
        """Use this method to reopen a closed topic in a forum supergroup chat.

        .. important::

            The bot must be an administrator in the chat for this to work and
            must have the ``can_manage_topics`` administrator rights, unless
            it is the creator of the topic.

        See: https://core.telegram.org/bots/api#reopenforumtopic

        :param chat_id: Unique identifier for the target chat or username of
            the target supergroup (in the format @supergroupusername).
        :param message_thread_id: Unique identifier for the target message
            thread of the forum topic.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            ReopenForumTopic(
                chat_id=chat_id,
                message_thread_id=message_thread_id,
            )
        )

    async def delete_forum_topic(
        self,
        chat_id: str | int,
        message_thread_id: int,
    ) -> bool:
        """Use this method to delete a forum topic along with all its messages
        in a forum supergroup chat.

        .. important::

            The bot must be an administrator in the chat for this to work and
            must have the ``can_delete_messages`` administrator rights.

        See: https://core.telegram.org/bots/api#deleteforumtopic

        :param chat_id: Unique identifier for the target chat or username of
            the target supergroup (in the format @supergroupusername).
        :param message_thread_id: Unique identifier for the target message
            thread of the forum topic.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            DeleteForumTopic(
                chat_id=chat_id,
                message_thread_id=message_thread_id,
            )
        )

    async def unpin_all_forum_topic_messages(
        self,
        chat_id: str | int,
        message_thread_id: int,
    ) -> bool:
        """Use this method to clear the list of pinned messages in a forum
        topic.

        .. important::

            The bot must be an administrator in the chat for this to work and
            must have the ``can_pin_messages`` administrator right in the
            supergroup.

        See: https://core.telegram.org/bots/api#unpinallforumtopicmessages

        :param chat_id: Unique identifier for the target chat or username of
            the target supergroup (in the format @supergroupusername).
        :param message_thread_id: Unique identifier for the target message
            thread of the forum topic.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            UnpinAllForumTopicMessages(
                chat_id=chat_id,
                message_thread_id=message_thread_id,
            )
        )

    async def edit_general_forum_topic(
        self,
        chat_id: str | int,
        name: str,
    ) -> bool:
        """Use this method to edit the name of the 'General' topic in a forum
        supergroup chat.

        .. important::

            The bot must be an administrator in the chat for this to work and
            must have ``can_manage_topics`` administrator rights.

        See: https://core.telegram.org/bots/api#editgeneralforumtopic

        :param chat_id: Unique identifier for the target chat or username of
            the target supergroup (in the format @supergroupusername).
        :param name: New topic name, 1-128 characters.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            EditGeneralForumTopic(
                chat_id=chat_id,
                name=name,
            )
        )

    async def close_general_forum_topic(
        self,
        chat_id: str | int,
    ) -> bool:
        """Use this method to close an open 'General' topic in a forum
        supergroup chat.

        .. important::

            The bot must be an administrator in the chat for this to work and
            must have the ``can_manage_topics`` administrator rights.

        See: https://core.telegram.org/bots/api#closegeneralforumtopic

        :param chat_id: Unique identifier for the target chat or username of
            the target supergroup (in the format @supergroupusername).
        :returns: ``True`` on success.
        """
        return await self._call_api(CloseGeneralForumTopic(chat_id=chat_id))

    async def reopen_general_forum_topic(
        self,
        chat_id: str | int,
    ) -> bool:
        """Use this method to reopen a closed 'General' topic in a forum
        supergroup chat.

        .. important::

            The bot must be an administrator in the chat for this to work and
            must have the ``can_manage_topics`` administrator rights.

        See: https://core.telegram.org/bots/api#reopengeneralforumtopic

        :param chat_id: Unique identifier for the target chat or username of
            the target supergroup (in the format @supergroupusername).
        :returns: ``True`` on success.
        """
        return await self._call_api(ReopenGeneralForumTopic(chat_id=chat_id))

    async def hide_general_forum_topic(
        self,
        chat_id: str | int,
    ) -> bool:
        """Use this method to hide the 'General' topic in a forum supergroup
        chat.

        .. important::

            The bot must be an administrator in the chat for this to work and
            must have the ``can_manage_topics`` administrator rights.

        See: https://core.telegram.org/bots/api#hidegeneralforumtopic

        :param chat_id: Unique identifier for the target chat or username of
            the target supergroup (in the format @supergroupusername).
        :returns: ``True`` on success.
        """
        return await self._call_api(HideGeneralForumTopic(chat_id=chat_id))

    async def unhide_general_forum_topic(
        self,
        chat_id: str | int,
    ) -> bool:
        """Use this method to unhide the 'General' topic in a forum supergroup
        chat.

        .. important::

            The bot must be an administrator in the chat for this to work and
            must have the ``can_manage_topics`` administrator rights.

        See: https://core.telegram.org/bots/api#unhidegeneralforumtopic

        :param chat_id: Unique identifier for the target chat or username of
            the target supergroup (in the format @supergroupusername).
        :returns: ``True`` on success.
        """
        return await self._call_api(UnhideGeneralForumTopic(chat_id=chat_id))

    async def unpin_all_general_forum_topic_messages(
        self, chat_id: str | int
    ) -> bool:
        """Use this method to clear the list of pinned messages in a General
        forum topic. The bot must be an administrator in the chat for this to
        work and must have the ``can_pin_messages`` administrator right in the
        supergroup.

        See: https://core.telegram.org/bots/api#unpinallgeneralforumtopicmessages

        :param chat_id: Unique identifier for the target chat or username of
            the target supergroup (in the format @supergroupusername).
        :returns: ``True`` on success.
        """  # noqa: E501
        return await self._call_api(
            UnpinAllGeneralForumTopicMessages(chat_id=chat_id)
        )

    async def answer_callback_query(
        self,
        callback_query_id: str,
        *,
        text: NoneStr = None,
        show_alert: NoneBool = None,
        url: NoneStr = None,
        cache_time: NoneInt = None,
    ) -> bool:
        """Use this method to send answers to callback queries sent from inline
        keyboards. The answer will be displayed to the user as a notification at
        the top of the chat screen or as an alert.

        See: https://core.telegram.org/bots/api#answercallbackquery

        :param callback_query_id: Unique identifier for the query to be
            answered.
        :param text: *Optional.* Text of the notification. If not specified,
            nothing will be shown to the user, 0-200 characters.
        :param show_alert: *Optional.* If ``True``, an alert will be shown by
            the client instead of a notification at the top of the chat screen.
        :param url: *Optional.* URL that will be opened by the user's client.
        :param cache_time: *Optional.* The maximum amount of time in seconds
            that the result of the callback query may be cached client-side.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            AnswerCallbackQuery(
                callback_query_id=callback_query_id,
                text=text,
                show_alert=show_alert,
                url=url,
                cache_time=cache_time,
            )
        )

    async def set_my_commands(
        self,
        commands: list[BotCommand],
        *,
        scope: BotCommandScope | None = None,
        language_code: NoneStr = None,
    ) -> bool:
        """Use this method to change the list of the bot's commands.

        See: https://core.telegram.org/bots/api#setmycommands

        :param commands: List of :class:`~yatbaf.types.BotCommand`
            to be set as the list of the bot's commands. At most 100 commands
            can be specified.
        :param scope: *Optional.* Describing scope of users for which the
            commands are relevant. Defaults to
            :class:`~yatbaf.types.bot_command_scope.BotCommandScopeDefault`.
        :param language_code: *Optional.* A two-letter ISO 639-1 language code.
            If empty, commands will be applied to all users from the given
            scope, for whose language there are no dedicated commands.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            SetMyCommands(
                commands=commands,
                scope=scope,
                language_code=language_code,
            )
        )

    async def delete_my_commands(
        self,
        *,
        scope: BotCommandScope | None = None,
        language_code: NoneStr = None,
    ) -> bool:
        """Use this method to delete the list of the bot's commands for the
        given scope and user language. After deletion, `higher level commands`_
        will be shown to affected users.

        See: https://core.telegram.org/bots/api#deletemycommands

        :param scope: *Optional.* Describing scope of users for which the
            commands are relevant. Defaults to
            :class:`~yatbaf.types.bot_command_scope.BotCommandScopeDefault`.
        :param language_code: *Optional.* A two-letter ISO 639-1 language code.
            If empty, commands will be applied to all users from the given
            scope, for whose language there are no dedicated commands.
        :returns: ``True`` on success.

        .. _higher level commands: https://core.telegram.org/bots/api#determining-list-of-commands
        """  # noqa: E501
        return await self._call_api(
            DeleteMyCommands(
                scope=scope,
                language_code=language_code,
            )
        )

    async def get_my_commands(
        self,
        *,
        scope: BotCommandScope | None = None,
        language_code: NoneStr = None,
    ) -> list[BotCommand]:
        """
        See: https://core.telegram.org/bots/api#getmycommands

        :param scope: *Optional.* Describing scope of users for which the
            commands are relevant. Defaults to
            :class:`~yatbaf.types.bot_command_scope.BotCommandScopeDefault`.
        :param language_code: *Optional.* A two-letter ISO 639-1 language code
            or an empty string.
        :returns: List of :class:`~yatbaf.types.bot_command.BotCommand`.
            If commands aren't set, an empty list is returned.
        """  # noqa: E501
        return await self._call_api(
            GetMyCommands(
                scope=scope,
                language_code=language_code,
            )
        )

    async def set_my_description(
        self,
        *,
        description: NoneStr = None,
        language_code: NoneStr = None,
    ) -> bool:
        """Use this method to change the bot's description, which is shown in
        the chat with the bot if the chat is empty.

        See: https://core.telegram.org/bots/api#setmydescription

        :param description: *Optional.* New bot description; 0-512 characters.
            Pass an empty string to remove the dedicated description for the
            given language.
        :param language_code: *Optional.* A two-letter ISO 639-1 language code.
            If empty, the description will be applied to all users for whose
            language there is no dedicated description.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            SetMyDescription(
                description=description,
                language_code=language_code,
            )
        )

    async def get_my_description(
        self,
        *,
        language_code: NoneStr = None,
    ) -> BotDescription:
        """Use this method to get the current bot description for the given
        user language.

        See: https://core.telegram.org/bots/api#getmydescription

        :param language_code: *Optional.* A two-letter ISO 639-1 language code
            or an empty string
        """
        return await self._call_api(
            GetMyDescription(language_code=language_code)
        )

    async def set_my_short_description(
        self,
        *,
        short_description: NoneStr = None,
        language_code: NoneStr = None,
    ) -> bool:
        """Use this method to change the bot's short description, which is shown
        on the bot's profile page and is sent together with the link when users
        share the bot.

        See: https://core.telegram.org/bots/api#setmyshortdescription

        :param short_description: *Optional.* New short description for the bot;
            0-120 characters. Pass an empty string to remove the dedicated short
            description for the given language.
        :param language_code: *Optional.* A two-letter ISO 639-1 language code.
            If empty, the short description will be applied to all users for
            whose language there is no dedicated short description.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            SetMyShortDescription(
                short_description=short_description,
                language_code=language_code,
            )
        )

    async def get_my_short_description(
        self,
        *,
        language_code: NoneStr = None,
    ) -> BotShortDescription:
        """Use this method to get the current bot short description for the
        given user language.

        See: https://core.telegram.org/bots/api#getmyshortdescription

        :param language_code: *Optional.* A two-letter ISO 639-1 language code
            or an empty string.
        """
        return await self._call_api(
            GetMyShortDescription(language_code=language_code)
        )

    async def set_chat_menu_button(
        self,
        *,
        chat_id: str | int | None = None,
        menu_button: MenuButton | None = None,
    ) -> bool:
        """Use this method to change the bot's menu button in a private chat,
        or the default menu button.

        See: https://core.telegram.org/bots/api#setchatmenubutton

        :param chat_id: *Optional.* Unique identifier for the target private
            chat. If not specified, default bot's menu button will be changed.
        :param menu_button: *Optional.* Bot's new menu button. Defaults to
            :class:`~yatbaf.types.menu_button.MenuButtonDefault`.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            SetChatMenuButton(
                chat_id=chat_id,
                menu_button=menu_button,
            )
        )

    async def get_chat_menu_button(
        self,
        chat_id: str | int,
    ) -> MenuButton:
        """Use this method to get the current value of the bot's menu button in
        a private chat, or the default menu button.

        See: https://core.telegram.org/bots/api#getchatmenubutton

        :param chat_id: *Optional.* Unique identifier for the target private
            chat. If not specified, default bot's menu button will be returned.
        """
        return await self._call_api(GetChatMenuButton(chat_id=chat_id))

    async def set_my_default_administrator_rights(
        self,
        *,
        rights: ChatAdministratorRights | None = None,
        for_channels: NoneBool = None,
    ) -> bool:
        """Use this method to change the default administrator rights requested
        by the bot when it's added as an administrator to groups or channels.
        These rights will be suggested to users, but they are free to modify
        the list before adding the bot.

        See: https://core.telegram.org/bots/api#setmydefaultadministratorrights

        :param rights: *Optional.* New default administrator rights. If not
            specified, the default administrator rights will be cleared.
        :param for_channels: *Optional.* Pass ``True`` to change the default
            administrator rights of the bot in channels. Otherwise, the
            default administrator rights of the bot for groups and supergroups
            will be changed.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            SetMyDefaultAdministratorRights(
                rights=rights,
                for_channels=for_channels,
            )
        )

    async def get_my_default_administrator_rights(
        self,
        *,
        for_channels: NoneBool = None,
    ) -> ChatAdministratorRights:
        """Use this method to get the current default administrator rights of
        the bot.

        See: https://core.telegram.org/bots/api#getmydefaultadministratorrights

        :param for_channels: *Optional.* Pass ``True`` to get default
            administrator rights of the bot in channels. Otherwise, default
            administrator rights of the bot for groups and supergroups will
            be returned.
        """
        return await self._call_api(
            GetMyDefaultAdministratorRights(for_channels=for_channels)
        )

    async def edit_message_text(
        self,
        text: str,
        *,
        chat_id: str | int | None = None,
        message_id: NoneInt = None,
        inline_message_id: NoneInt = None,
        parse_mode: ParseMode | None = None,
        entities: list[MessageEntity] | None = None,
        disable_web_page_preview: NoneBool = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message | bool:
        """Use this method to edit text and game messages.

        See: https://core.telegram.org/bots/api#editmessagetext

        :param text: New text of the message, 1-4096 characters after entities
            parsing.
        :param chat_id: *Optional.* Unique identifier for the target chat or
            username of the target channel (in the format @channelusername).
            Required if ``inline_message_id`` is not specified.
        :param message_id: *Optional.* Identifier of the message to edit.
            Required if ``inline_message_id`` is not specified.
        :param inline_message_id: *Optional.* Identifier of the inline message.
            Required if ``chat_id`` and ``message_id`` are not specified.
        :param parse_mode: *Optional.* Mode for parsing entities in the
            message text.
        :param entities: *Optional.* List of special entities that appear in
            message text, which can be specified instead of ``parse_mode``.
        :param disable_web_page_preview: *Optional.* Disables link previews for
            links in this message.
        :param reply_markup: Inline keyboard.
        :returns: On success, if the edited message is not an inline message,
            the edited :class:`~yatbaf.types.message.Message` is
            returned, otherwise ``True`` is returned.
        """
        return await self._call_api(
            EditMessageText(
                text=text,
                chat_id=chat_id,
                message_id=message_id,
                inline_message_id=inline_message_id,
                parse_mode=parse_mode,
                entities=entities,
                disable_web_page_preview=disable_web_page_preview,
                reply_markup=reply_markup,
            )
        )

    async def edit_message_caption(
        self,
        *,
        chat_id: str | int | None = None,
        message_id: NoneInt = None,
        inline_message_id: NoneInt = None,
        caption: NoneStr = None,
        parse_mode: ParseMode | None = None,
        caption_entities: list[MessageEntity] | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message | bool:
        """Use this method to edit captions of messages.

        See: https://core.telegram.org/bots/api#editmessagecaption

        :param chat_id: *Optional.* Required if ``inline_message_id`` is not
            specified. Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param message_id: *Optional.* Required if ``inline_message_id`` is not
            specified. Identifier of the message to edit.
        :param inline_message_id: *Optional.* Required if ``chat_id`` and
            ``message_id`` are not specified. Identifier of the inline message.
        :param caption: *Optional.* New caption of the message, 0-1024
            characters after entities parsing.
        :param parse_mode: *Optional.* Mode for parsing entities in the
            message caption.
        :param caption_entities: *Optional.* List of
            :class:`~yatbaf.types.message_entity.MessageEntity`
            that appear in the caption, which can be specified instead of
            ``parse_mode``.
        :param reply_markup: *Optional.* A JSON-serialized object for an
            inline keyboard.
        :returns: On success, if the edited message is not an inline message,
            the edited :class:`~yatbaf.types.message.Message` is
            returned, otherwise ``True`` is returned.
        """
        return await self._call_api(
            EditMessageCaption(
                chat_id=chat_id,
                message_id=message_id,
                inline_message_id=inline_message_id,
                caption=caption,
                parse_mode=parse_mode,
                caption_entities=caption_entities,
                reply_markup=reply_markup,
            )
        )

    async def edit_message_media(
        self,
        media: InputMedia,
        *,
        chat_id: str | int | None = None,
        message_id: NoneInt = None,
        inline_message_id: NoneInt = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message | bool:
        """Use this method to edit animation, audio, document, photo, or video
        messages.

        .. note::

            If a message is part of a message album, then it can be edited
            only to an audio for audio albums, only to a document for document
            albums and to a photo or a video otherwise. When an inline message
            is edited, a new file can't be uploaded; use a previously uploaded
            file via its file_id or specify a URL.

        See: https://core.telegram.org/bots/api#editmessagemedia

        :param media: A JSON-serialized object for a new media content of the
            message.
        :param chat_id: *Optional.* Required if ``inline_message_id`` is not
            specified. Unique identifier for the target chat or username of the
            target channel (in the format @channelusername).
        :param message_id: *Optional.* Required if ``inline_message_id`` is not
            specified. Identifier of the message to edit.
        :param inline_message_id: *Optional.* Required if ``chat_id`` and
            ``message_id`` are not specified. Identifier of the inline message.
        :param reply_markup: *Optional.* A JSON-serialized object for a new
            inline keyboard.
        :returns: On success, if the edited message is not an inline message,
            the edited :class:`Message <yatbaf.types.message.Message>` is
            returned, otherwise ``True`` is returned.
        """
        return await self._call_api(
            EditMessageMedia(
                media=media,
                chat_id=chat_id,
                message_id=message_id,
                inline_message_id=inline_message_id,
                reply_markup=reply_markup,
            )
        )

    async def edit_message_live_location(
        self,
        latitude: float,
        longtitude: float,
        *,
        chat_id: str | int | None = None,
        message_id: NoneInt = None,
        inline_message_id: NoneStr = None,
        horizontal_accuracy: float | None = None,
        heading: NoneInt = None,
        proximity_alert_radius: NoneInt = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message | bool:
        """Use this method to edit live location messages. A location can be
        edited until its ``live_period`` expires or editing is explicitly
        disabled by a call to :meth:`stop_message_live_location`.

        See: https://core.telegram.org/bots/api#editmessagelivelocation

        :param latitude: Latitude of new location.
        :param longtitude: Longitude of new location.
        :param chat_id: *Optional.* Required if ``inline_message_id`` is not
            specified. Unique identifier for the target chat or username of the
            target channel (in the format @channelusername).
        :param message_id: *Optional.* Required if ``inline_message_id`` is not
            specified. Identifier of the message to edit.
        :param inline_message_id: *Optional.* Required if ``chat_id`` and
            ``message_id`` are not specified. Identifier of the inline message.
        :param horizontal_accuracy: *Optional.* The radius of uncertainty for
            the location, measured in meters; 0-1500.
        :param heading: *Optional.* Direction in which the user is moving, in
            degrees. Must be between 1 and 360 if specified.
        :param proximity_alert_radius: *Optional.* The maximum distance for
            proximity alerts about approaching another chat member, in meters.
            Must be between 1 and 100000 if specified.
        :param reply_markup: *Optional.* A new inline keyboard.
        :returns: On success, if the edited message is not an inline message,
            the edited :class:`~yatbaf.types.message.Message` is
            returned, otherwise ``True`` is returned.
        """
        return await self._call_api(
            EditMessageLiveLocation(
                latitude=latitude,
                longtitude=longtitude,
                chat_id=chat_id,
                message_id=message_id,
                inline_message_id=inline_message_id,
                horizontal_accuracy=horizontal_accuracy,
                heading=heading,
                proximity_alert_radius=proximity_alert_radius,
                reply_markup=reply_markup,
            )
        )

    async def stop_message_live_location(
        self,
        *,
        chat_id: str | int | None = None,
        message_id: NoneInt = None,
        inline_message_id: NoneStr = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message | bool:
        """Use this method to stop updating a live location message before
        ``live_period`` expires.

        See: https://core.telegram.org/bots/api#stopmessagelivelocation

        :param chat_id: *Optional.* Required if ``inline_message_id`` is not
            specified. Unique identifier for the target chat or username of the
            target channel (in the format @channelusername).
        :param message_id: *Optional.* Required if ``inline_message_id`` is not
            specified. Identifier of the message with live location to stop.
        :param inline_message_id: *Optional.* Required if ``chat_id`` and
            ``message_id`` are not specified. Identifier of the inline message.
        :param reply_markup: *Optional.* Inline keyboard.
        :returns: On success, if the message is not an inline message, the
            edited :class:`~yatbaf.types.message.Message` is
            returned, otherwise ``True`` is returned.
        """
        return await self._call_api(
            StopMessageLiveLocation(
                chat_id=chat_id,
                message_id=message_id,
                inline_message_id=inline_message_id,
                reply_markup=reply_markup,
            )
        )

    async def edit_message_reply_markup(
        self,
        *,
        chat_id: str | int | None = None,
        message_id: NoneInt = None,
        inline_message_id: NoneStr = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message | bool:
        """Use this method to edit only the reply markup of messages.

        See: https://core.telegram.org/bots/api#editmessagereplymarkup

        :param chat_id: *Optional.* Required if ``inline_message_id`` is not
            specified. Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param message_id: *Optional.* Required if ``inline_message_id`` is not
            specified. Identifier of the message to edit.
        :param inline_message_id: *Optional.* Required if ``chat_id`` and
            ``message_id`` are not specified. Identifier of the inline message.
        :param reply_markup: *Optional.* Inline keyboard.
        :returns: On success, if the edited message is not an inline message,
            the edited :class:`~yatbaf.types.message.Message` is
            returned, otherwise ``True`` is returned.
        """
        return await self._call_api(
            EditMessageReplyMarkup(
                chat_id=chat_id,
                message_id=message_id,
                inline_message_id=inline_message_id,
                reply_markup=reply_markup,
            )
        )

    async def stop_poll(
        self,
        chat_id: str | int,
        message_id: int,
        *,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Poll:
        """Use this method to stop a poll which was sent by the bot.

        See: https://core.telegram.org/bots/api#stoppoll

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param message_id: Identifier of the original message with the poll.
        :param reply_markup: *Optional.* A :class:`~yatbaf.types.inline_keyboard_markup.InlineKeyboardMarkup`
            object for a new message inline keyboard.
        """  # noqa: E501
        return await self._call_api(
            StopPoll(
                chat_id=chat_id,
                message_id=message_id,
                reply_markup=reply_markup,
            )
        )

    async def delete_message(
        self,
        chat_id: str | int,
        message_id: int,
    ) -> bool:
        """Use this method to delete a message, including service messages.

        See: https://core.telegram.org/bots/api#deletemessage

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param message_id: Identifier of the message to delete.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            DeleteMessage(
                chat_id=chat_id,
                message_id=message_id,
            )
        )

    async def send_sticker(
        self,
        chat_id: str | int,
        sticker: InputFile | str,
        *,
        message_thread_id: NoneInt = None,
        emoji: NoneStr = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """Use this method to send static .WEBP, animated .TGS, or video .WEBM
        stickers.

        See: https://core.telegram.org/bots/api#sendsticker

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param sticker: Sticker to send.
        :param message_thread_id: *Optional.* Unique identifier for the target
            message thread (topic) of the forum; for forum supergroups only.
        :param emoji: *Optional.* Emoji associated with the sticker; only for
            just uploaded stickers.
        :param disable_notification: *Optional.* Sends the message silently.
            Users will receive a notification with no sound.
        :param protect_content: *Optional.* Protects the contents of the sent
            message from forwarding and saving.
        :param reply_to_message_id: *Optional.* If the message is a reply, ID
            of the original message.
        :param allow_sending_without_reply: *Optional.* Pass ``True`` if the
            message should be sent even if the specified replied-to message
            is not found.
        :param reply_markup: *Optional.* Additional interface options.
        """
        return await self._call_api(
            SendSticker(
                chat_id=chat_id,
                sticker=sticker,
                message_thread_id=message_thread_id,
                emoji=emoji,
                disable_notification=disable_notification,
                protect_content=protect_content,
                allow_sending_without_reply=allow_sending_without_reply,
                reply_markup=reply_markup,
            )
        )

    async def get_sticker_set(self, name: str) -> StickerSet:
        """Use this method to get a sticker set.

        See: https://core.telegram.org/bots/api#getstickerset

        :param name: Name of the sticker set.
        """

        return await self._call_api(GetStickerSet(name=name))

    async def get_custom_emoji_stickers(
        self,
        custom_emoji_ids: list[str],
    ) -> list[Sticker]:
        """Use this method to get information about custom emoji stickers by
        their identifiers.

        See: https://core.telegram.org/bots/api#getcustomemojistickers

        :param custom_emoji_ids: List of custom emoji identifiers. At most 200
            custom emoji identifiers can be specified.
        """
        return await self._call_api(
            GetCustomEmojiStickers(custom_emoji_ids=custom_emoji_ids)
        )

    async def upload_sticker_file(
        self,
        user_id: int,
        sticker: InputFile,
        sticker_format: StickerFormat,
    ) -> File:
        """Use this method to upload a file with a sticker for later use in the
        :meth:`create_new_sticker_set` and :meth:`add_sticker_to_set`
        methods (the file can be used multiple times).

        See: https://core.telegram.org/bots/api#uploadstickerfile

        :param user_id: User identifier of sticker file owner.
        :param sticker: A file with the sticker in .WEBP, .PNG, .TGS, or .WEBM
            format.
        :param sticker_format: Format of the sticker.
        """
        return await self._call_api(
            UploadStickerFile(
                user_id=user_id,
                sticker=sticker,
                sticker_format=sticker_format,
            )
        )

    async def create_new_sticker_set(
        self,
        user_id: int,
        name: str,
        title: str,
        stickers: list[InputSticker],
        sticker_format: StickerFormat,
        *,
        sticker_type: StickerType | None = None,
        needs_repainting: NoneBool = None,
    ) -> bool:
        """Use this method to create a new sticker set owned by a user. The bot
        will be able to edit the sticker set thus created.

        See: https://core.telegram.org/bots/api#createnewstickerset

        :param user_id: User identifier of created sticker set owner.
        :param name: Short name of sticker set, to be used in t.me/addstickers/
            URLs (e.g., animals). Can contain only English letters, digits and
            underscores. Must begin with a letter, can't contain consecutive
            underscores and must end in "_by_<bot_username>". <bot_username> is
            case insensitive. 1-64 characters.
        :param title: Sticker set title, 1-64 characters.
        :param stickers: A list of 1-50 initial stickers to be added to the
            sticker set.
        :param sticker_format: Format of stickers in the set.
        :param sticker_type: *Optional.* Type of stickers in the set.
            By default, a regular (:attr:`StickerType.REGULAR`) sticker set is
            created.
        :param needs_repainting: *Optional.* Pass ``True`` if stickers in the
            sticker set must be repainted to the color of text when used in
            messages, the accent color if used as emoji status, white on chat
            photos, or another appropriate color based on context; for custom
            emoji sticker sets only.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            CreateNewStickerSet(
                user_id=user_id,
                name=name,
                title=title,
                stickers=stickers,
                sticker_format=sticker_format,
                sticker_type=sticker_type,
                needs_repainting=needs_repainting,
            )
        )

    async def add_sticker_to_set(
        self,
        user_id: int,
        name: str,
        sticker: InputSticker,
    ) -> bool:
        """Use this method to add a new sticker to a set created by the bot.

        See: https://core.telegram.org/bots/api#addstickertoset

        :param user_id: User identifier of sticker set owner.
        :param name: Sticker set name.
        :param sticker: Information about the added sticker.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            AddStickerToSet(
                user_id=user_id,
                name=name,
                sticker=sticker,
            )
        )

    async def set_sticker_position_in_set(
        self,
        sticker: str,
        position: int,
    ) -> bool:
        """Use this method to move a sticker in a set created by the bot to a
        specific position.

        See: https://core.telegram.org/bots/api#setstickerpositioninset

        :param sticker: File identifier of the sticker.
        :param position: New sticker position in the set, zero-based.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            SetStickerPositionInSet(
                sticker=sticker,
                position=position,
            )
        )

    async def delete_sticker_from_set(self, sticker: str) -> bool:
        """Use this method to delete a sticker from a set created by the bot.

        See: https://core.telegram.org/bots/api#deletestickerfromset

        :param sticker: File identifier of the sticker.
        :returns: ``True`` on success.
        """
        return await self._call_api(DeleteStickerFromSet(sticker=sticker))

    async def set_sticker_emoji_list(
        self,
        sticker: str,
        emoji_list: list[str],
    ) -> bool:
        """Use this method to change the list of emoji assigned to a regular or
        custom emoji sticker.

        .. note::

            The sticker must belong to a sticker set created by the bot.

        See: https://core.telegram.org/bots/api#setstickeremojilist

        :param sticker: File identifier of the sticker.
        :param emoji_list: List of 1-20 emoji associated with the sticker.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            SetStickerEmojiList(
                sticker=sticker,
                emoji_list=emoji_list,
            )
        )

    async def set_sticker_keywords(
        self,
        sticker: str,
        *,
        keywords: list[str] | None = None,
    ) -> bool:
        """Use this method to change search keywords assigned to a regular or
        custom emoji sticker.

        .. note::

            The sticker must belong to a sticker set created by the bot.

        See: https://core.telegram.org/bots/api#setstickerkeywords

        :param sticker: File identifier of the sticker.
        :param keywords: *Optional.* A list of 0-20 search keywords for the
            sticker with total length of up to 64 characters.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            SetStickerKeywords(
                sticker=sticker,
                keywords=keywords,
            )
        )

    async def set_sticker_mask_position(
        self,
        sticker: str,
        *,
        mask_position: MaskPosition | None = None,
    ) -> bool:
        """Use this method to change the mask position of a mask sticker.

        .. note::

            The sticker must belong to a sticker set created by the bot.

        See: https://core.telegram.org/bots/api#setstickermaskposition

        :param sticker: File identifier of the sticker.
        :param mask_position: *Optional.* the position where the mask should be
            placed on faces. Omit the parameter to remove the mask position.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            SetStickerMaskPosition(
                sticker=sticker,
                mask_position=mask_position,
            )
        )

    async def set_sticker_set_title(self, name: str, title: str) -> bool:
        """Use this method to set the title of a created sticker set.

        See: https://core.telegram.org/bots/api#setstickersettitle

        :param name: Sticker set name.
        :param title: Sticker set title, 1-64 characters.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            SetStickerSetTitle(
                name=name,
                title=title,
            )
        )

    async def set_sticker_set_thumbnail(
        self,
        name: str,
        user_id: int,
        *,
        thumbnail: InputFile | str | None = None,
    ) -> bool:
        """
        Use this method to set the thumbnail of a regular or mask sticker set.

        .. note::

            The format of the thumbnail file must match the format of the
            stickers in the set.

        See: https://core.telegram.org/bots/api#setstickersetthumbnail

        :param name: Sticker set name.
        :param user_id: User identifier of the sticker set owner.
        :param thumbnail: *Optional.* A .WEBP or .PNG image with the thumbnail,
            must be up to 128 kilobytes in size and have a width and height of
            exactly 100px, or a .TGS animation with a thumbnail up to 32
            kilobytes in size, or a WEBM video with the thumbnail up to 32
            kilobytes in size.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            SetStickerSetThumbnail(
                name=name,
                user_id=user_id,
                thumbnail=thumbnail,
            )
        )

    async def set_custom_emoji_sticker_set_thumbnail(
        self,
        name: str,
        custom_emoji_id: str,
    ) -> bool:
        """Use this method to set the thumbnail of a custom emoji sticker set.

        See: https://core.telegram.org/bots/api#setcustomemojistickersetthumbnail

        :param name: Sticker set name.
        :param custom_emoji_id: *Optional.* Custom emoji identifier of a sticker
            from the sticker set; pass an empty string to drop the thumbnail and
            use the first sticker as the thumbnail.
        :returns: ``True`` on success.
        """  # noqa: E501
        return await self._call_api(
            SetCustomEmojiStickerSetThumbnail(
                name=name,
                custom_emoji_id=custom_emoji_id,
            )
        )

    async def delete_sticker_set(self, name: str) -> bool:
        """Use this method to delete a sticker set that was created by the bot.

        See: https://core.telegram.org/bots/api#deletestickerset

        :param name: Sticker set name.
        :returns: ``True`` on success.
        """
        return await self._call_api(DeleteStickerSet(name=name))

    async def answer_inline_query(
        self,
        inline_query_id: str,
        results: list[InlineQueryResult],
        *,
        cache_time: NoneInt = None,
        is_personal: NoneBool = None,
        next_offset: NoneStr = None,
        button: InlineQueryResultsButton | None = None,
    ) -> bool:
        """Use this method to send answers to an inline query.

        .. warning::

            No more than 50 results per query are allowed.

        See: https://core.telegram.org/bots/api#answerinlinequery

        :param inline_query_id: Unique identifier for the answered query.
        :param result: A list of results for the inline query.
        :param cache_time: *Optional.* The maximum amount of time in seconds
            that the result of the inline query may be cached on the server.
            Defaults to 300.
        :param is_personal: *Optional.* Pass ``True`` if results may be cached on
            the server side only for the user that sent the query. By default,
            results may be returned to any user who sends the same query.
        :param next_offset: *Optional.* Pass the offset that a client should
            send in the next query with the same text to receive more results.
            Pass an empty string if there are no more results or if you don't
            support pagination. Offset length can't exceed 64 bytes.
        :param button: *Optional.* A :class:`~yatbaf.types.inline_query_result.InlineQueryResultsButton`
            to be shown above inline query results.
        :returns: ``True`` on success.
        """  # noqa: E501
        return await self._call_api(
            AnswerInlineQuery(
                inline_query_id=inline_query_id,
                results=results,
                cache_time=cache_time,
                is_personal=is_personal,
                next_offset=next_offset,
                button=button,
            )
        )

    async def answer_web_app_query(
        self,
        web_app_query_id: str,
        result: InlineQueryResult,
    ) -> SentWebAppMessage:
        """Use this method to set the result of an interaction with a Web App
        and send a corresponding message on behalf of the user to the chat from
        which the query originated.

        See: https://core.telegram.org/bots/api#answerwebappquery

        :param web_app_query_id: Unique identifier for the query to be answered.
        :param result: :class:`~yatbaf.type.inline_query_result.InlineQueryResult` to be sent.
        """  # noqa: E501
        return await self._call_api(
            AnswerWebAppQuery(
                web_app_query_id=web_app_query_id,
                result=result,
            )
        )

    async def send_invoice(
        self,
        chat_id: str | int,
        *,
        title: str,
        description: str,
        payload: str,
        provider_token: str,
        currency: str,
        prices: list[LabeledPrice],
        message_thread_id: NoneInt = None,
        max_tip_amount: NoneInt = None,
        suggested_tip_amounts: list[int] | None = None,
        start_parameter: NoneStr = None,
        provider_data: NoneStr = None,
        photo_url: NoneStr = None,
        photo_size: NoneInt = None,
        photo_width: NoneInt = None,
        photo_height: NoneInt = None,
        need_name: NoneBool = None,
        need_phone_number: NoneBool = None,
        need_email: NoneBool = None,
        need_shipping_address: NoneBool = None,
        send_phone_number_to_provider: NoneBool = None,
        send_email_to_provider: NoneBool = None,
        is_flexible: NoneBool = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        reply_to_message_id: NoneInt = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message:
        """Use this method to send invoices.

        See: https://core.telegram.org/bots/api#sendinvoice

        :param chat_id: Unique identifier for the target chat or username of
            the target channel (in the format @channelusername).
        :param title: Product name, 1-32 characters.
        :param description: Product description, 1-255 characters.
        :param payload: Bot-defined invoice payload, 1-128 bytes. This will not
            be displayed to the user, use for your internal processes.
        :param provider_token: Payment provider token, obtained via BotFather.
        :param currency: Three-letter ISO 4217 currency code.
        :param prices: Price breakdown, a list of components (e.g. product
            price, tax, discount, delivery cost, delivery tax, bonus, etc.).
        :param message_thread_id: *Optional.* Unique identifier for the target
            message thread (topic) of the forum; for forum supergroups only.
        :param max_tip_amount: *Optional.* The maximum accepted amount for tips
            in the smallest units of the currency.

            .. important::

                Integer, **not** float/double. For example, for a maximum tip of
                US$ 1.45 pass ``max_tip_amount`` = 145. See the exp parameter
                in `currencies.json <https://core.telegram.org/bots/payments/currencies.json>`_,
                it shows the number of digits past the decimal point for each
                currency (2 for the majority of currencies).
        :param suggested_tip_amounts: *Optional.* A list of suggested amounts
            of tips in the smallest units of the currency. At most 4 suggested
            tip amounts can be specified. The suggested tip amounts must be
            positive, passed in a strictly increased order and must not exceed
            ``max_tip_amount``.

            .. important::

                Integer, **not** float/double.
        :param start_parameter: *Optional.* Unique deep-linking parameter. If
            left empty, forwarded copies of the sent message will have a Pay
            button, allowing multiple users to pay directly from the forwarded
            message, using the same invoice. If non-empty, forwarded copies of
            the sent message will have a URL button with a deep link to the bot
            (instead of a Pay button), with the value used as the start
            parameter.
        :param provider_data: *Optional.* JSON-serialized data about the
            invoice, which will be shared with the payment provider. A detailed
            description of required fields should be provided by the payment
            provider.
        :param photo_url: *Optional.* URL of the product photo for the invoice.
            Can be a photo of the goods or a marketing image for a service.
            People like it better when they see what they are paying for.
        :param photo_size: *Optional.* Photo size in bytes.
        :param photo_width: *Optional.* Photo width.
        :param photo_height: *Optional.* Photo height.
        :param need_name: *Optional.* Pass ``True`` if you require the user's
            full name to complete the order.
        :param need_phone_number: *Optional.* Pass ``True`` if you require the
            user's phone number to complete the order.
        :param need_email: *Optional.* Pass ``True`` if you require the user's
            email address to complete the order.
        :param need_shipping_address: *Optional.* Pass ``True`` if you require
            the user's shipping address to complete the order.
        :param send_phone_number_to_provider: *Optional.* Pass ``True`` if the
            user's phone number should be sent to the provider.
        :param send_email_to_provider: *Optional.* Pass ``True`` if the user's
            email address should be sent to the provider.
        :param is_flexible: *Optional.* Pass ``True`` if the final price depends
            on the shipping method.
        :param disable_notification: *Optional.* Sends the message silently.
            Users will receive a notification with no sound.
        :param protect_content: *Optional.* Protects the contents of the sent
            message from forwarding and saving.
        :param reply_to_message_id: *Optional.* If the message is a reply, ID
            of the original message.
        :param allow_sending_without_reply: *Optional.* Pass ``True`` if the
            message should be sent even if the specified replied-to message is
            not found.
        :param reply_markup: *Optional.* If empty, one 'Pay total price' button
            will be shown. If not empty, the first button must be a Pay button.
        """  # noqa: E501
        return await self._call_api(
            SendInvoice(
                chat_id=chat_id,
                title=title,
                description=description,
                payload=payload,
                provider_token=provider_token,
                currency=currency,
                prices=prices,
                message_thread_id=message_thread_id,
                max_tip_amount=max_tip_amount,
                suggested_tip_amounts=suggested_tip_amounts,
                start_parameter=start_parameter,
                provider_data=provider_data,
                photo_url=photo_url,
                photo_size=photo_size,
                photo_width=photo_width,
                photo_height=photo_height,
                need_name=need_name,
                need_phone_number=need_phone_number,
                need_email=need_email,
                need_shipping_address=need_shipping_address,
                send_phone_number_to_provider=send_phone_number_to_provider,
                send_email_to_provider=send_email_to_provider,
                is_flexible=is_flexible,
                disable_notification=disable_notification,
                protect_content=protect_content,
                reply_to_message_id=reply_to_message_id,
                allow_sending_without_reply=allow_sending_without_reply,
                reply_markup=reply_markup,
            )
        )

    async def create_invoice_link(
        self,
        *,
        title: str,
        description: str,
        payload: str,
        provider_token: str,
        currency: str,
        prices: list[LabeledPrice],
        max_tip_amount: NoneInt = None,
        suggested_tip_amounts: list[int] | None = None,
        provider_data: NoneStr = None,
        photo_url: NoneStr = None,
        photo_size: NoneInt = None,
        photo_width: NoneInt = None,
        photo_height: NoneInt = None,
        need_name: NoneBool = None,
        need_phone_number: NoneBool = None,
        need_email: NoneBool = None,
        need_shipping_address: NoneBool = None,
        send_phone_number_to_provider: NoneBool = None,
        send_email_to_provider: NoneBool = None,
        is_flexible: NoneBool = None,
    ) -> str:
        """Use this method to create a link for an invoice.

        See: https://core.telegram.org/bots/api#createinvoicelink

        :param title: Product name, 1-32 characters.
        :param description: Product description, 1-255 characters.
        :param payload: Bot-defined invoice payload, 1-128 bytes. This will not
            be displayed to the user, use for your internal processes.
        :param provider_token: Payment provider token, obtained via BotFather.
        :param currency: Three-letter ISO 4217 currency code.
        :param prices: Price breakdown, a list of components (e.g. product
            price, tax, discount, delivery cost, delivery tax, bonus, etc.)
        :param max_tip_amount: *Optional.* The maximum accepted amount for tips
            in the smallest units of the currency.

            .. important::

                Integer, **not** float/double.
        :param suggested_tip_amounts: *Optional.* A list of suggested amounts of
            tips in the smallest units of the currency. At most 4 suggested tip
            amounts can be specified. The suggested tip amounts must be
            positive, passed in a strictly increased order and must not exceed
            ``max_tip_amount``.

            .. important::

                Integer, **not** float/double.
        :param provider_data: *Optional.* Data about the invoice, which will be
            shared with the payment provider. A detailed description of required
            fields should be provided by the payment provider.
        :param photo_url: *Optional.* URL of the product photo for the invoice.
            Can be a photo of the goods or a marketing image for a service.
        :param photo_size: *Optional.* Photo size in bytes.
        :param photo_width: *Optional.* Photo width.
        :param photo_height: *Optional.* Photo height.
        :param need_name: *Optional.* Pass ``True`` if you require the user's
            full name to complete the order.
        :param need_phone_number: *Optional.* Pass ``True`` if you require the
            user's phone number to complete the order.
        :param need_email: *Optional.* Pass ``True`` if you require the user's
            email address to complete the order.
        :param need_shipping_address: *Optional.* Pass ``True`` if you require
            the user's shipping address to complete the order.
        :param send_phone_number_to_provider: *Optional.* Pass ``True`` if the
            user's phone number should be sent to the provider.
        :param send_email_to_provider: *Optional.* Pass ``True`` if the user's
            email address should be sent to the provider.
        :param is_flexible: *Optional.* Pass ``True`` if the final price depends
            on the shipping method.
        :returns: Created invoice link as :class:`str` on success.
        """
        return await self._call_api(
            CreateInvoiceLink(
                title=title,
                description=description,
                payload=payload,
                provider_token=provider_token,
                currency=currency,
                prices=prices,
                max_tip_amount=max_tip_amount,
                suggested_tip_amounts=suggested_tip_amounts,
                provider_data=provider_data,
                photo_url=photo_url,
                photo_size=photo_size,
                photo_width=photo_width,
                photo_height=photo_height,
                need_name=need_name,
                need_phone_number=need_phone_number,
                need_email=need_email,
                need_shipping_address=need_shipping_address,
                send_phone_number_to_provider=send_phone_number_to_provider,
                send_email_to_provider=send_email_to_provider,
                is_flexible=is_flexible,
            )
        )

    async def answer_shipping_query(
        self,
        shipping_query_id: str,
        ok: bool,
        *,
        shipping_options: list[ShippingOption] | None = None,
        error_message: NoneStr = None,
    ) -> bool:
        """If you sent an invoice requesting a shipping address and the
        parameter ``is_flexible`` was specified, the Bot API will send an
        :class:`yatbaf.types.update.Update` with a ``shipping_query`` field
        to the bot. Use this method to reply to shipping queries.

        See: https://core.telegram.org/bots/api#answershippingquery

        :param shipping_query_id: Unique identifier for the query to be
            answered.
        :param ok: Pass ``True`` if delivery to the specified address is
            possible and ``False`` if there are any problems (for example, if
            delivery to the specified address is not possible).
        :param shipping_options: *Optional.* Required if ``ok`` is ``True``.
            A list of available :class:`~yatbaf.types.shipping_options.ShippingOption`.
        :param error_message: *Optional.* Required if ``ok`` is ``False``. Error
            message in human readable form that explains why it is impossible
            to complete the order (e.g. 'Sorry, delivery to your desired
            address is unavailable'). Telegram will display this message to
            the user.
        :returns: ``True`` on success.
        """  # noqa: E501
        return await self._call_api(
            AnswerShippingQuery(
                shipping_query_id=shipping_query_id,
                ok=ok,
                shipping_options=shipping_options,
                error_message=error_message,
            )
        )

    async def answer_pre_checkout_query(
        self,
        pre_checkout_query_id: str,
        ok: bool,
        *,
        error_message: NoneStr = None,
    ) -> bool:
        """Use this method to respond to such pre-checkout queries.

        .. important::

            The Bot API must receive an answer within 10 seconds after the
            pre-checkout query was sent.

        See: https://core.telegram.org/bots/api#answerprecheckoutquery

        :param pre_check_query_id: Unique identifier for the query to be
            answered.
        :param ok: Specify ``True`` if everything is alright (goods are
            available, etc.) and the bot is ready to proceed with the order.
            Use ``False`` if there are any problems.
        :param error_message: Required if ``ok`` is ``False``. Error message in
            human readable form that explains the reason for failure to proceed
            with the checkout.
        :returns: ``True`` on success.
        """
        return await self._call_api(
            AnswerPreCheckoutQuery(
                pre_checkout_query_id=pre_checkout_query_id,
                ok=ok,
                error_message=error_message,
            )
        )

    async def set_passport_data_errors(
        self,
        user_id: int,
        errors: list[PassportElementError],
    ) -> bool:
        """Informs a user that some of the Telegram Passport elements they
        provided contains errors. The user will not be able to re-submit their
        Passport to you until the errors are fixed (the contents of the field
        for which you returned the error must change).

        See: https://core.telegram.org/bots/api#setpassportdataerrors

        :param user_id: User identifier.
        :param errors: List of :class:`~yatbaf.types.passport_element_error.PassportElementError`.
        :returns: ``True`` on success.
        """  # noqa: E501
        return await self._call_api(
            SetPassportDataErrors(
                user_id=user_id,
                errors=errors,
            )
        )

    async def send_game(
        self,
        chat_id: str | int,
        game_short_name: str,
        *,
        message_thread_id: NoneInt = None,
        disable_notification: NoneBool = None,
        protect_content: NoneBool = None,
        reply_to_message_id: NoneInt = None,
        allow_sending_without_reply: NoneBool = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message:
        """Use this method to send a game.

        See: https://core.telegram.org/bots/api#sendgame

        :param chat_id: Unique identifier for the target chat.
        :param game_short_name: Short name of the game, serves as the unique
            identifier for the game. Set up your games via @BotFather.
        :param message_thread_id: *Optional.* Unique identifier for the target
            message thread (topic) of the forum; for forum supergroups only.
        :param disable_notification: *Optional.* Sends the message silently.
            Users will receive a notification with no sound.
        :param protect_content: *Optional.* Protects the contents of the sent
            message from forwarding and saving.
        :param reply_to_message_id: *Optional.* If the message is a reply, ID
            of the original message.
        :param allow_sending_without_reply: *Optional.* Pass ``True`` if the
            message should be sent even if the specified replied-to message
            is not found.
        :param reply_markup: *Optional.* If empty, one 'Play game_title' button
            will be shown. If not empty, the first button must launch the game.
        """
        return await self._call_api(
            SendGame(
                chat_id=chat_id,
                game_short_name=game_short_name,
                message_thread_id=message_thread_id,
                disable_notification=disable_notification,
                protect_content=protect_content,
                reply_to_message_id=reply_to_message_id,
                allow_sending_without_reply=allow_sending_without_reply,
                reply_markup=reply_markup,
            )
        )

    async def set_game_score(
        self,
        user_id: int,
        score: int,
        *,
        force: NoneBool = None,
        disable_edit_message: NoneBool = None,
        chat_id: NoneInt = None,
        message_id: NoneInt = None,
        inline_message_id: NoneInt = None,
    ) -> Message | bool:
        """Use this method to set the score of the specified user in a game
            message.

        .. note::

            Returns an error, if the new score is not greater than the user's
            current score in the chat and force is ``False``.

        See: https://core.telegram.org/bots/api#setgamescore

        :param user_id: User identifier.
        :param score: New score, must be non-negative.
        :param force: Pass ``True`` if the high score is allowed to decrease.
            This can be useful when fixing mistakes or banning cheaters.
        :param disable_notification: *Optional.* Pass ``True`` if the game
            message should not be automatically edited to include the current
            scoreboard.
        :param chat_id: *Optional.* Required if ``inline_message_id`` is not
            specified. Unique identifier for the target chat.
        :param message_id: *Optional.* Required if ``inline_message_id`` is
            not specified. Identifier of the sent message.
        :param inline_message_id: *Optional.* Required if ``chat_id`` and
            ``message_id`` are not specified. Identifier of the inline message.
        :returns: On success, if the message is not an inline message,
            the :class:`~yatbaf.types.message.Message` is returned,
            otherwise ``True`` is returned.
        """
        return await self._call_api(
            SetGameScore(
                user_id=user_id,
                score=score,
                force=force,
                disable_edit_message=disable_edit_message,
                chat_id=chat_id,
                message_id=message_id,
                inline_message_id=inline_message_id,
            )
        )

    async def get_game_high_scores(
        self,
        user_id: int,
        *,
        chat_id: NoneInt = None,
        message_id: NoneInt = None,
        inline_message_id: NoneStr = None,
    ) -> list[GameHighScore]:
        """Use this method to get data for high score tables. Will return the
        score of the specified user and several of their neighbors in a game.

        See: https://core.telegram.org/bots/api#getgamehighscores

        :param user_id: *Optional.* Target user id.
        :param chat_id: *Optional.* Required if ``inline_message_id`` is not
            specified. Unique identifier for the target chat.
        :param message_id: *Optional.* Required if ``inline_message_id`` is not
            specified. Identifier of the sent message.
        :param inline_message_id: *Optional.* Required if ``chat_id`` and
            ``message_id`` are not specified. Identifier of the inline message.
        """
        return await self._call_api(
            GetGameHighScores(
                user_id=user_id,
                chat_id=chat_id,
                message_id=message_id,
                inline_message_id=inline_message_id,
            )
        )
