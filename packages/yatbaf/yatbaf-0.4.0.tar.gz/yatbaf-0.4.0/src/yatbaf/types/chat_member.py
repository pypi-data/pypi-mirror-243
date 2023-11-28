from __future__ import annotations

__all__ = [
    "ChatMember",
    "ChatMemberAdministrator",
    "ChatMemberBanned",
    "ChatMemberLeft",
    "ChatMemberMember",
    "ChatMemberOwner",
    "ChatMemberRestricted",
    "ChatMemberUpdated",
]

# from datetime import datetime
from typing import ClassVar
from typing import Literal
from typing import TypeAlias
from typing import final

from msgspec import field

from yatbaf.typing import NoneBool
from yatbaf.typing import NoneStr

from .abc import TelegramType
from .chat import Chat
from .chat_invite_link import ChatInviteLink
from .user import User


@final
class ChatMemberAdministrator(
    TelegramType, tag="administrator", tag_field="status"
):  # yapf: disable
    """Represents a chat member that has some additional privileges.

    See: https://core.telegram.org/bots/api#chatmemberadministrator
    """

    user: User
    """Information about the user."""

    can_be_edited: bool
    """``True``, if the bot is allowed to edit administrator privileges of that
    user.
    """

    is_anonymous: bool
    """``True``, if the user's presence in the chat is hidden."""

    can_manage_chat: bool
    """``True``, if the administrator can access the chat event log, chat
    statistics, message statistics in channels, see channel members, see
    anonymous administrators in supergroups and ignore slow mode. Implied by
    any other administrator privilege.
    """

    can_delete_messages: bool
    """``True``, if the administrator can delete messages of other users."""

    can_manage_video_chats: bool
    """``True``, if the administrator can manage video chats."""

    can_restrict_members: bool
    """``True``, if the administrator can restrict, ban or unban chat members."""  # noqa: E501

    can_promote_members: bool
    """``True``, if the administrator can add new administrators with a subset
    of their own privileges or demote administrators that they have promoted,
    directly or indirectly (promoted by administrators that were appointed by
    the user).
    """

    can_change_info: bool
    """``True``, if the user is allowed to change the chat title, photo and
    other settings.
    """

    can_invite_users: bool
    """``True``, if the user is allowed to invite new users to the chat."""

    can_post_messages: NoneBool = None
    """*Optional.* ``True``, if the administrator can post in the channel.

    .. note::

        Channels only.
    """

    can_edit_messages: NoneBool = None
    """*Optional.* ``True``, if the administrator can edit messages of other
    users and can pin messages.

    .. note::

        Channels only.
    """

    can_pin_messages: NoneBool = None
    """*Optional.* ``True``, if the user is allowed to pin messages.

    .. note::

        Groups and Supergroups only.
    """

    can_manage_topics: NoneBool = None
    """*Optional.* ``True``, if the user is allowed to create, rename, close,
    and reopen forum topics.

    .. note::

        Supergroups only.
    """

    can_post_stories: NoneBool = None
    """*Optional.* ``True``, if the administrator can post stories in the
    channel.

    .. note::

        Channels only.
    """

    can_edit_stories: NoneBool = None
    """Optional. ``True``, if the administrator can edit stories posted by other
    users.

    .. note::

        Channels only.
    """

    can_delete_stories: NoneBool = None
    """*Optional.* ``True``, if the administrator can delete stories posted by
    other users.

    .. note::

        Channels only.
    """

    custom_title: NoneStr = None
    """*Optional.* Custom title for this user."""

    status: ClassVar[Literal["administrator"]] = "administrator"
    """The member's status in the chat, always `administrator`."""


@final
class ChatMemberBanned(TelegramType, tag="kicked", tag_field="status"):
    """Represents a chat member that was banned in the chat and can't return to
    the chat or view chat messages.

    See: https://core.telegram.org/bots/api#chatmemberbanned
    """

    user: User
    """Information about the user."""

    until_date: int  # datetime
    """Date when restrictions will be lifted for this user; unix time. If 0,
    then the user is banned forever.
    """

    status: ClassVar[Literal["kicked"]] = "kicked"
    """The member's status in the chat, always `kicked`."""


@final
class ChatMemberLeft(TelegramType, tag="left", tag_field="status"):
    """Represents a chat member that isn't currently a member of the chat, but
    may join it themselves.

    See: https://core.telegram.org/bots/api#chatmemberleft
    """

    user: User
    """Information about the user."""

    status: ClassVar[Literal["left"]] = "left"
    """The member's status in the chat, always `left`."""


@final
class ChatMemberMember(TelegramType, tag="member", tag_field="status"):
    """Represents a chat member that has no additional privileges or
    restrictions.

    See: https://core.telegram.org/bots/api#chatmembermember
    """

    user: User
    """Information about the user."""

    status: ClassVar[Literal["member"]] = "member"
    """The member's status in the chat, always `member`."""


@final
class ChatMemberOwner(TelegramType, tag="creator", tag_field="status"):
    """Represents a chat member that owns the chat and has all administrator
    privileges.

    See:  https://core.telegram.org/bots/api#chatmemberowner
    """

    user: User
    """Information about the user."""

    is_anonymous: bool
    """``True``, if the user's presence in the chat is hidden."""

    custom_title: NoneStr = None
    """*Optional.* Custom title for this user."""

    status: ClassVar[Literal["creator"]] = "creator"
    """The member's status in the chat, always `creator`."""


@final
class ChatMemberRestricted(TelegramType, tag="restricted", tag_field="status"):
    """Represents a chat member that is under certain restrictions in the chat.
    Supergroups only.

    See: https://core.telegram.org/bots/api#chatmemberrestricted
    """

    user: User
    """Information about the user."""

    is_member: bool
    """``True``, if the user is a member of the chat at the moment of the
    request.
    """

    can_send_messages: bool
    """``True``, if the user is allowed to send text messages, contacts,
    invoices, locations and venues.
    """

    can_send_audios: bool
    """``True``, if the user is allowed to send audios."""

    can_send_documents: bool
    """``True``, if the user is allowed to send documents."""

    can_send_photos: bool
    """``True``, if the user is allowed to send photos."""

    can_send_videos: bool
    """``True``, if the user is allowed to send videos."""

    can_send_video_notes: bool
    """``True``, if the user is allowed to send video notes."""

    can_send_voice_notes: bool
    """``True``, if the user is allowed to send voice notes."""

    can_send_polls: bool
    """``True``, if the user is allowed to send polls."""

    can_send_other_messages: bool
    """``True``, if the user is allowed to send animations, games, stickers
    and use inline bots.
    """

    can_add_web_page_previews: bool
    """``True``, if the user is allowed to add web page previews to their
    messages.
    """

    can_change_info: bool
    """``True``, if the user is allowed to change the chat title, photo and
    other settings.
    """

    can_invite_users: bool
    """``True``, if the user is allowed to invite new users to the chat."""

    can_pin_messages: bool
    """``True``, if the user is allowed to pin messages."""

    can_manage_topics: bool
    """``True``, if the user is allowed to create forum topics."""

    until_date: int  # TODO: datetime
    """Date when restrictions will be lifted for this user; unix time. If 0,
    then the user is restricted forever.
    """

    status: ClassVar[Literal["restricted"]] = "restricted"
    """The member's status in the chat, always `restricted`."""


ChatMember: TypeAlias = (
    "ChatMemberAdministrator "
    "| ChatMemberBanned "
    "| ChatMemberLeft "
    "| ChatMemberMember "
    "| ChatMemberOwner "
    "| ChatMemberRestricted"
)


@final
class ChatMemberUpdated(TelegramType):
    """This object represents changes in the status of a chat member.

    See: https://core.telegram.org/bots/api#chatmemberupdated
    """

    chat: Chat
    """Chat the user belongs to."""

    from_: User = field(name="from")
    """Performer of the action, which resulted in the change."""

    date: int  # TODO: datetime
    """Date the change was done in Unix time."""

    old_chat_member: ChatMember
    """Previous information about the chat member."""

    new_chat_member: ChatMember
    """New information about the chat member."""

    invite_link: ChatInviteLink | None = None
    """*Optional.* Chat invite link, which was used by the user to join the
    chat; for joining by invite link events only.
    """

    via_chat_folder_invite_link: NoneBool = None
    """*Optional.* ``True``, if the user joined the chat via a chat folder
    invite link.
    """
