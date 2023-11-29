from __future__ import annotations

from typing import final

from yatbaf.typing import NoneBool

from .abc import TelegramType


@final
class ChatAdministratorRights(TelegramType):
    """Represents the rights of an administrator in a chat.

    See: https://core.telegram.org/bots/api#chatadministratorrights
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

        Groups and supergroups only.
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

    can_manage_topics: NoneBool = None
    """*Optional.* ``True``, if the user is allowed to create, rename, close,
    and reopen forum topics.

    .. note::

        Supergroups only.
    """
