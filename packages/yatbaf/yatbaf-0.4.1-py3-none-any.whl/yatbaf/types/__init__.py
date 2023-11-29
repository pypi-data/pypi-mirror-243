"""Telegram Bot API Types.

See: https://core.telegram.org/bots/api#available-types
"""

__all__ = [
    "Animation",
    "Audio",
    "BotCommand",
    "BotCommandScope",
    "BotCommandScopeAllChatAdministrators",
    "BotCommandScopeAllGroupChats",
    "BotCommandScopeAllPrivateChats",
    "BotCommandScopeChat",
    "BotCommandScopeChatAdministrators",
    "BotCommandScopeChatMember",
    "BotCommandScopeDefault",
    "BotDescription",
    "BotName",
    "BotShortDescription",
    "CallbackGame",
    "CallbackQuery",
    "Chat",
    "ChatAdministratorRights",
    "ChatInviteLink",
    "ChatJoinRequest",
    "ChatLocation",
    "ChatMember",
    "ChatMemberAdministrator",
    "ChatMemberBanned",
    "ChatMemberLeft",
    "ChatMemberMember",
    "ChatMemberOwner",
    "ChatMemberRestricted",
    "ChatMemberUpdated",
    "ChatPermissions",
    "ChatPhoto",
    "ChatShared",
    "ChosenInlineResult",
    "Contact",
    "Dice",
    "Document",
    "EncryptedCredentials",
    "EncryptedPassportElement",
    "File",
    "ForceReply",
    "ForumTopic",
    "ForumTopicClosed",
    "ForumTopicCreated",
    "ForumTopicEdited",
    "ForumTopicReopened",
    "Game",
    "GameHighScore",
    "GeneralForumTopicHidden",
    "GeneralForumTopicUnhidden",
    "InlineKeyboardButton",
    "InlineKeyboardMarkup",
    "InlineQuery",
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
    "InputContactMessageContent",
    "InputInvoiceMessageContent",
    "InputLocationMessageContent",
    "InputMedia",
    "InputMediaAnimation",
    "InputMediaAudio",
    "InputMediaDocument",
    "InputMediaPhoto",
    "InputMediaVideo",
    "InputMessageContent",
    "InputSticker",
    "InputTextMessageContent",
    "InputVenueMessageContent",
    "Invoice",
    "KeyboardButton",
    "KeyboardButtonPollType",
    "KeyboardButtonRequestChat",
    "KeyboardButtonRequestUser",
    "LabeledPrice",
    "Location",
    "LoginUrl",
    "MaskPosition",
    "MenuButton",
    "MenuButtonCommands",
    "MenuButtonDefault",
    "MenuButtonWebApp",
    "Message",
    "MessageAutoDeleteTimerChanged",
    "MessageEntity",
    "MessageId",
    "OrderInfo",
    "PassportData",
    "PassportElementError",
    "PassportElementErrorDataField",
    "PassportElementErrorFile",
    "PassportElementErrorFiles",
    "PassportElementErrorFrontSide",
    "PassportElementErrorReverseSide",
    "PassportElementErrorSelfie",
    "PassportElementErrorTranslationFile",
    "PassportElementErrorTranslationFiles",
    "PassportElementErrorUnspecified",
    "PassportFile",
    "PhotoSize",
    "Poll",
    "PollAnswer",
    "PollOption",
    "PreCheckoutQuery",
    "ProximityAlertTriggered",
    "ReplyKeyboardMarkup",
    "ReplyKeyboardRemove",
    "ResponseParameters",
    "SentWebAppMessage",
    "ShippingAddress",
    "ShippingOption",
    "ShippingQuery",
    "Sticker",
    "StickerSet",
    "Story",
    "SuccessfulPayment",
    "SwitchInlineQueryChosenChat",
    "Update",
    "User",
    "UserProfilePhotos",
    "UserShared",
    "Venue",
    "Video",
    "VideoChatEnded",
    "VideoChatParticipantsInvited",
    "VideoChatScheduled",
    "VideoChatStarted",
    "VideoNote",
    "Voice",
    "WebAppData",
    "WebAppInfo",
    "WebhookInfo",
    "WriteAccessAllowed",
]

from .animation import Animation
from .audio import Audio
from .bot_command import BotCommand
from .bot_command_scope import BotCommandScope
from .bot_command_scope import BotCommandScopeAllChatAdministrators
from .bot_command_scope import BotCommandScopeAllGroupChats
from .bot_command_scope import BotCommandScopeAllPrivateChats
from .bot_command_scope import BotCommandScopeChat
from .bot_command_scope import BotCommandScopeChatAdministrators
from .bot_command_scope import BotCommandScopeChatMember
from .bot_command_scope import BotCommandScopeDefault
from .bot_description import BotDescription
from .bot_name import BotName
from .bot_short_description import BotShortDescription
from .callback_game import CallbackGame
from .callback_query import CallbackQuery
from .chat import Chat
from .chat_administrator_rights import ChatAdministratorRights
from .chat_invite_link import ChatInviteLink
from .chat_join_request import ChatJoinRequest
from .chat_location import ChatLocation
from .chat_member import ChatMember
from .chat_member import ChatMemberAdministrator
from .chat_member import ChatMemberBanned
from .chat_member import ChatMemberLeft
from .chat_member import ChatMemberMember
from .chat_member import ChatMemberOwner
from .chat_member import ChatMemberRestricted
from .chat_member import ChatMemberUpdated
from .chat_permissions import ChatPermissions
from .chat_photo import ChatPhoto
from .chat_shared import ChatShared
from .chosen_inline_result import ChosenInlineResult
from .contact import Contact
from .dice import Dice
from .document import Document
from .file import File
from .force_reply import ForceReply
from .forum_topic import ForumTopic
from .forum_topic_closed import ForumTopicClosed
from .forum_topic_created import ForumTopicCreated
from .forum_topic_edited import ForumTopicEdited
from .forum_topic_reopened import ForumTopicReopened
from .game import Game
from .game_high_score import GameHighScore
from .general_forum_topic_hidden import GeneralForumTopicHidden
from .general_forum_topic_unhidden import GeneralForumTopicUnhidden
from .inline_keyboard_button import InlineKeyboardButton
from .inline_keyboard_markup import InlineKeyboardMarkup
from .inline_query import InlineQuery
from .inline_query_result import InlineQueryResult
from .inline_query_result import InlineQueryResultArticle
from .inline_query_result import InlineQueryResultAudio
from .inline_query_result import InlineQueryResultCachedAudio
from .inline_query_result import InlineQueryResultCachedDocument
from .inline_query_result import InlineQueryResultCachedGif
from .inline_query_result import InlineQueryResultCachedMpeg4Gif
from .inline_query_result import InlineQueryResultCachedPhoto
from .inline_query_result import InlineQueryResultCachedSticker
from .inline_query_result import InlineQueryResultCachedVideo
from .inline_query_result import InlineQueryResultCachedVoice
from .inline_query_result import InlineQueryResultContact
from .inline_query_result import InlineQueryResultDocument
from .inline_query_result import InlineQueryResultGame
from .inline_query_result import InlineQueryResultGif
from .inline_query_result import InlineQueryResultLocation
from .inline_query_result import InlineQueryResultMpeg4Gif
from .inline_query_result import InlineQueryResultPhoto
from .inline_query_result import InlineQueryResultsButton
from .inline_query_result import InlineQueryResultVenue
from .inline_query_result import InlineQueryResultVideo
from .inline_query_result import InlineQueryResultVoice
from .input_contact_message_content import InputContactMessageContent
from .input_invoce_message_content import InputInvoiceMessageContent
from .input_location_message_content import InputLocationMessageContent
from .input_media import InputMedia
from .input_media import InputMediaAnimation
from .input_media import InputMediaAudio
from .input_media import InputMediaDocument
from .input_media import InputMediaPhoto
from .input_media import InputMediaVideo
from .input_message_content import InputMessageContent
from .input_sticker import InputSticker
from .input_text_message_content import InputTextMessageContent
from .input_venue_message_content import InputVenueMessageContent
from .invoice import Invoice
from .keyboard_button import KeyboardButton
from .keyboard_button import KeyboardButtonPollType
from .keyboard_button import KeyboardButtonRequestChat
from .keyboard_button import KeyboardButtonRequestUser
from .labeled_price import LabeledPrice
from .location import Location
from .login_url import LoginUrl
from .mask_position import MaskPosition
from .menu_button import MenuButton
from .menu_button import MenuButtonCommands
from .menu_button import MenuButtonDefault
from .menu_button import MenuButtonWebApp
from .message import Message
from .message_auto_delete_timer_changed import MessageAutoDeleteTimerChanged
from .message_entity import MessageEntity
from .message_id import MessageId
from .order_info import OrderInfo
from .passport import EncryptedCredentials
from .passport import EncryptedPassportElement
from .passport import PassportData
from .passport import PassportFile
from .passport_element_error import PassportElementError
from .passport_element_error import PassportElementErrorDataField
from .passport_element_error import PassportElementErrorFile
from .passport_element_error import PassportElementErrorFiles
from .passport_element_error import PassportElementErrorFrontSide
from .passport_element_error import PassportElementErrorReverseSide
from .passport_element_error import PassportElementErrorSelfie
from .passport_element_error import PassportElementErrorTranslationFile
from .passport_element_error import PassportElementErrorTranslationFiles
from .passport_element_error import PassportElementErrorUnspecified
from .photo_size import PhotoSize
from .poll import Poll
from .poll_answer import PollAnswer
from .poll_option import PollOption
from .pre_checkout_query import PreCheckoutQuery
from .proximity_alert_triggered import ProximityAlertTriggered
from .reply_keyboard_markup import ReplyKeyboardMarkup
from .reply_keyboard_remove import ReplyKeyboardRemove
from .response_parameters import ResponseParameters
from .sent_web_app_message import SentWebAppMessage
from .shipping_address import ShippingAddress
from .shipping_option import ShippingOption
from .shipping_query import ShippingQuery
from .sticker import Sticker
from .sticker_set import StickerSet
from .story import Story
from .successful_payment import SuccessfulPayment
from .switch_inline_query_chosen_chat import SwitchInlineQueryChosenChat
from .update import Update
from .user import User
from .user_profile_photos import UserProfilePhotos
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
from .web_app_info import WebAppInfo
from .webhook_info import WebhookInfo
from .write_access_allowed import WriteAccessAllowed
