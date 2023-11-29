from __future__ import annotations

from typing import final

from yatbaf.typing import NoneBool

from .abc import TelegramType


@final
class ChatPermissions(TelegramType):
    """Describes actions that a non-administrator user is allowed to take in
    a chat.

    See: https://core.telegram.org/bots/api#chatpermissions
    """

    can_send_messages: NoneBool = None
    """*Optional.* ``True``, if the user is allowed to send text messages,
    contacts, invoices, locations and venues.
    """

    can_send_audios: NoneBool = None
    """*Optional.* ``True``, if the user is allowed to send audios."""

    can_send_documents: NoneBool = None
    """*Optional.* ``True``, if the user is allowed to send documents."""

    can_send_photos: NoneBool = None
    """*Optional.* ``True``, if the user is allowed to send photos."""

    can_send_videos: NoneBool = None
    """*Optional.* ``True``, if the user is allowed to send videos."""

    can_send_video_notes: NoneBool = None
    """*Optional.* ``True``, if the user is allowed to send video notes."""

    can_send_voice_notes: NoneBool = None
    """*Optional.* ``True``, if the user is allowed to send voice notes."""

    can_send_polls: NoneBool = None
    """*Optional.* ``True``, if the user is allowed to send polls."""

    can_send_other_messages: NoneBool = None
    """*Optional.* ``True``, if the user is allowed to send animations, games,
    stickers and use inline bots.
    """

    can_add_web_page_previews: NoneBool = None
    """*Optional.* ``True``, if the user is allowed to add web page previews to
    their messages.
    """

    can_change_info: NoneBool = None
    """*Optional.* ``True``, if the user is allowed to change the chat title,
    photo and other settings.

    .. note::

        Ignored in public supergroups.
    """

    can_invite_users: NoneBool = None
    """*Optional.* ``True``, if the user is allowed to invite new users to the chat."""  # noqa: E501

    can_pin_messages: NoneBool = None
    """*Optional.* ``True``, if the user is allowed to pin messages.

    .. note::

        Ignored in public supergroups.
    """

    can_manage_topics: NoneBool = None
    """*Optional.* ``True``, if the user is allowed to create forum topics.

    .. note::

        If omitted defaults to the value of ``can_pin_messages``.
    """
