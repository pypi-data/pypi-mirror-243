from __future__ import annotations

__all__ = ["Chat"]

from typing import TYPE_CHECKING
from typing import final

import yatbaf.types.message as message
from yatbaf.enums import ChatType
from yatbaf.typing import NoneBool
from yatbaf.typing import NoneInt
from yatbaf.typing import NoneStr

from .abc import TelegramType
from .bot_command_scope import BotCommandScopeChat
from .bot_command_scope import BotCommandScopeChatAdministrators
from .bot_command_scope import BotCommandScopeChatMember
from .chat_location import ChatLocation
from .chat_permissions import ChatPermissions
from .chat_photo import ChatPhoto

if TYPE_CHECKING:
    from yatbaf.types import BotCommand
    from yatbaf.types import ChatInviteLink
    from yatbaf.types import ChatMember
    from yatbaf.typing import InputFile


@final
class Chat(TelegramType):
    """This object represents a chat.

    See: https://core.telegram.org/bots/api#chat
    """

    id: int
    """Unique identifier for this chat."""

    type: ChatType
    """Type of chat (see :class:`yatbaf.enums.ChatType`)."""

    title: NoneStr = None
    """*Optional.* Title, for supergroups, channels and group chats."""

    username: NoneStr = None
    """*Optional.* Username, for private chats, supergroups and channels if available."""  # noqa: E501

    first_name: NoneStr = None
    """*Optional.* First name of the other party in a private chat."""

    last_name: NoneStr = None
    """*Optional.* Last name of the other party in a private chat."""

    is_forum: NoneBool = None
    """*Optional.* ``True``, if the supergroup chat is a forum (has topics enabled)."""  # noqa: E501

    photo: ChatPhoto | None = None
    """*Optional.* Chat photo. Returned only in :meth:`~yatbaf.bot.Bot.get_chat`."""  # noqa: E501

    active_usernames: list[str] | None = None
    """*Optional.* If non-empty, the list of all active chat usernames;
    for private chats, supergroups and channels. Returned only in
    :meth:`~yatbaf.bot.Bot.get_chat`.
    """

    emoji_status_custom_emoji_id: NoneStr = None
    """*Optional.* Custom emoji identifier of emoji status of the other party
    in a private chat. Returned only in :meth:`~yatbaf.bot.Bot.get_chat`.
    """  # noqa: E501

    emoji_status_expiration_date: NoneInt = None
    """*Optional.* Expiration date of the emoji status of the other party in a
    private chat, if any. Returned only in :meth:`~yatbaf.bot.Bot.get_chat`.
    """

    bio: NoneStr = None
    """*Optional.* Bio of the other party in a private chat. Returned only in
    :meth:`~yatbaf.bot.Bot.get_chat`.
    """

    has_private_forwards: NoneBool = None
    """*Optional.* ``True``, if privacy settings of the other party in the
    private chat allows to use tg://user?id=<user_id> links only in chats with
    the user. Returned only in :meth:`~yatbaf.bot.Bot.get_chat`.
    """

    has_restricted_voice_and_video_messages: NoneBool = None
    """*Optional.* ``True``, if the privacy settings of the other party restrict
    sending voice and video note messages in the private chat. Returned only in
    :meth:`~yatbaf.bot.Bot.get_chat`.
    """

    join_to_send_messages: NoneBool = None
    """*Optional.* True, if users need to join the supergroup before they can
    send messages. Returned only in :meth:`~yatbaf.bot.Bot.get_chat`.
    """  # noqa: E501

    join_by_request: NoneBool = None
    """*Optional.* True, if all users directly joining the supergroup need to
    be approved by supergroup administrators. Returned only in
    :meth:`~yatbaf.bot.Bot.get_chat`.
    """

    description: NoneStr = None
    """*Optional.* Description, for groups, supergroups and channel chats.
    Returned only in :meth:`~yatbaf.bot.Bot.get_chat`.
    """

    invite_link: NoneStr = None
    """*Optional.* Primary invite link, for groups, supergroups and channel
    chats. Returned only in :meth:`~yatbaf.bot.Bot.get_chat`.
    """

    pinned_message: message.Message | None = None
    """*Optional.* The most recent pinned message (by sending date).
    Returned only in :meth:`~yatbaf.bot.Bot.get_chat`.
    """

    permissions: ChatPermissions | None = None
    """*Optional.* Default chat member permissions, for groups and supergroups.
    Returned only in :meth:`~yatbaf.bot.Bot.get_chat`.
    """

    slow_mode_delay: NoneInt = None
    """*Optional.* For supergroups, the minimum allowed delay between
    consecutive messages sent by each unpriviledged user; in seconds. Returned
    only in :meth:`~yatbaf.bot.Bot.get_chat`.
    """

    message_auto_delete_time: NoneInt = None
    """*Optional.* The time after which all messages sent to the chat will be
    automatically deleted; in seconds. Returned only in
    :meth:`~yatbaf.bot.Bot.get_chat`.
    """

    has_aggressive_anti_spam_enabled: NoneBool = None
    """*Optional.* ``True``, if aggressive anti-spam checks are enabled in the
    supergroup. The field is only available to chat administrators. Returned
    only in :meth:`~yatbaf.bot.Bot.get_chat`.
    """

    has_hidden_members: NoneBool = None
    """*Optional.* ``True``, if non-administrators can only get the list of bots
    and administrators in the chat. Returned only in
    :meth:`~yatbaf.bot.Bot.get_chat`.
    """

    has_protected_content: NoneBool = None
    """*Optional.* ``True``, if messages from the chat can't be forwarded to
    other chats. Returned only in :meth:`~yatbaf.bot.Bot.get_chat`.
    """

    sticker_set_name: NoneStr = None
    """*Optional.* For supergroups, name of group sticker set. Returned only in
    :meth:`~yatbaf.bot.Bot.get_chat`.
    """

    can_set_sticker_set: NoneBool = None
    """*Optional.* ``True``, if the bot can change the group sticker set.
    Returned only in :meth:`~yatbaf.bot.Bot.get_chat`.
    """

    linked_chat_id: NoneInt = None
    """*Optional.* Unique identifier for the linked chat, i.e. the discussion
    group identifier for a channel and vice versa; for supergroups and channel
    chats. Returned only in :meth:`~yatbaf.bot.Bot.get_chat`.
    """

    location: ChatLocation | None = None
    """*Optional.* For supergroups, the location to which the supergroup is
    connected. Returned only in :meth:`~yatbaf.bot.Bot.get_chat`.
    """

    async def ban_member(
        self,
        user_id: int,
        until_date: NoneInt = None,
        revorke_messages: NoneBool = None,
    ) -> bool:
        """Ban member.

        See: :meth:`~yatbaf.bot.Bot.unban_chat_member`
        """
        return await self.bot.ban_chat_member(
            chat_id=self.id,
            user_id=user_id,
            until_date=until_date,
            revorke_messages=revorke_messages,
        )

    async def unban_member(
        self,
        user_id: int,
        only_if_banned: NoneBool = None,
    ) -> bool:
        """Unban member.

        See: :meth:`~yatbaf.bot.Bot.unban_chat_member`
        """
        return await self.bot.unban_chat_member(
            chat_id=self.id,
            user_id=user_id,
            only_if_banned=only_if_banned,
        )

    async def restrict_member(
        self,
        user_id: int,
        permissions: ChatPermissions,
        *,
        use_independent_chat_permissions: NoneBool = None,
        unitl_date: NoneInt = None,
    ) -> bool:
        """Restrict member.

        See: :meth:`~yatbaf.bot.Bot.restrict_chat_member`
        """
        return await self.bot.restrict_chat_member(
            chat_id=self.id,
            user_id=user_id,
            permissions=permissions,
            use_independent_chat_permissions=use_independent_chat_permissions,
            until_date=unitl_date,
        )

    async def promote_member(
        self,
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
        """Promote member.

        See: :meth:`~yatbaf.bot.Bot.promote_chat_member`
        """
        return await self.bot.promote_chat_member(
            chat_id=self.id,
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

    async def set_andministrator_custom_title(
        self,
        user_id: int,
        custom_title: str,
    ) -> bool:
        """See: :meth:`~yatbaf.bot.Bot.set_chat_administrator_custom_title`"""
        return await self.bot.set_chat_administrator_custom_title(
            chat_id=self.id,
            user_id=user_id,
            custom_title=custom_title,
        )

    async def ban_sender_chat(self, sender_chat_id: int) -> bool:
        """See: :meth:`~yatbaf.bot.Bot.ban_chat_sender_chat`"""
        return await self.bot.ban_chat_sender_chat(
            chat_id=self.id,
            sender_chat_id=sender_chat_id,
        )

    async def unban_sender_chat(self, sender_chat_id: int) -> bool:
        """See: :meth:`~yatbaf.bot.Bot.unban_chat_sender_chat`"""
        return await self.bot.unban_chat_sender_chat(
            chat_id=self.id,
            sender_chat_id=sender_chat_id,
        )

    async def set_permissions(
        self,
        permissions: ChatPermissions,
        *,
        use_independent_chat_permissions: NoneBool = None,
    ) -> bool:
        """See: :meth:`~yatbaf.bot.Bot.set_chat_permissions`"""
        return await self.bot.set_chat_permissions(
            chat_id=self.id,
            permissions=permissions,
            use_independent_chat_permissions=use_independent_chat_permissions,
        )

    async def export_invite_link(self) -> str:
        """See: :meth:`~yatbaf.bot.Bot.export_chat_invite_link`"""
        return await self.bot.export_chat_invite_link(chat_id=self.id)

    async def create_invite_link(
        self,
        *,
        name: NoneStr = None,
        expite_date: NoneInt = None,
        member_limit: NoneInt = None,
        create_join_request: NoneBool = None,
    ) -> ChatInviteLink:
        """See: :meth:`~yatbaf.bot.Bot.create_chat_invite_link`"""
        return await self.bot.create_chat_invite_link(
            chat_id=self.id,
            name=name,
            expire_date=expite_date,
            member_limit=member_limit,
            creates_join_request=create_join_request,
        )

    async def edit_invite_link(
        self,
        invite_link: str,
        *,
        name: NoneStr = None,
        expite_date: NoneInt = None,
        member_limit: NoneInt = None,
        create_join_request: NoneBool = None,
    ) -> ChatInviteLink:
        """See: :meth:`~yatbaf.bot.Bot.edit_chat_invite_link`"""
        return await self.bot.edit_chat_invite_link(
            chat_id=self.id,
            invite_link=invite_link,
            name=name,
            expire_date=expite_date,
            member_limit=member_limit,
            creates_join_request=create_join_request,
        )

    async def revoke_invite_link(self, invite_link: str) -> ChatInviteLink:
        """See: :meth:`~yatbaf.bot.Bot.revoke_chat_invite_link`"""
        return await self.bot.revoke_chat_invite_link(
            chat_id=self.id,
            invite_link=invite_link,
        )

    async def approve_join_request(self, user_id: int) -> bool:
        """See: :meth:`~yatbaf.bot.Bot.approve_chat_join_request`"""
        return await self.bot.approve_chat_join_request(
            chat_id=self.id,
            user_id=user_id,
        )

    async def decline_join_request(self, user_id: int) -> bool:
        """See: :meth:`~yatbaf.bot.Bot.decline_chat_join_request`"""
        return await self.bot.decline_chat_join_request(
            chat_id=self.id,
            user_id=user_id,
        )

    async def set_photo(self, photo: InputFile) -> bool:
        """See: :meth:`~yatbaf.bot.Bot.set_chat_photo`"""
        return await self.bot.set_chat_photo(
            chat_id=self.id,
            photo=photo,
        )

    async def delete_photo(self) -> bool:
        """See: :meth:`~yatbaf.bot.Bot.delete_chat_photo`"""  # noqa: E501
        return await self.bot.delete_chat_photo(chat_id=self.id)

    async def set_title(self, title: str) -> bool:
        """See: :meth:`~yatbaf.bot.Bot.set_chat_title`"""
        return await self.bot.set_chat_title(
            chat_id=self.id,
            title=title,
        )

    async def set_description(self, *, description: NoneStr = None) -> bool:
        """See: :meth:`~yatbaf.bot.Bot.set_chat_description`"""
        return await self.bot.set_chat_description(
            chat_id=self.id,
            description=description,
        )

    async def pin_message(
        self,
        message_id: int,
        disable_notification: NoneBool = None,
    ) -> bool:
        """See: :meth:`~yatbaf.bot.Bot.pin_chat_message`"""
        return await self.bot.pin_chat_message(
            chat_id=self.id,
            message_id=message_id,
            disable_notification=disable_notification,
        )

    async def unpin_message(self, message_id: int) -> bool:
        """See: :meth:`~yatbaf.bot.Bot.unpin_chat_message`"""
        return await self.bot.unpin_chat_message(
            chat_id=self.id,
            message_id=message_id,
        )

    async def unpin_all_messages(self) -> bool:
        """See: :meth:`~yatbaf.bot.Bot.unpin_all_chat_messages`"""
        return await self.bot.unpin_all_chat_messages(chat_id=self.id)

    async def leave(self) -> bool:
        """See: :meth:`~yatbaf.bot.Bot.leave_chat`"""
        return await self.bot.leave_chat(chat_id=self.id)

    async def get_administrators(self) -> list[ChatMember]:
        """See: :meth:`~yatbaf.bot.Bot.get_chat_administrators`"""
        return await self.bot.get_chat_administrators(chat_id=self.id)

    async def get_member_count(self) -> int:
        """See: :meth:`~yatbaf.bot.Bot.get_chat_member_count`"""
        return await self.bot.get_chat_member_count(chat_id=self.id)

    async def get_member(self, user_id: int) -> ChatMember:
        """See: :meth:`~yatbaf.bot.Bot.get_chat_member`"""
        return await self.bot.get_chat_member(
            chat_id=self.id,
            user_id=user_id,
        )

    async def set_commands(
        self,
        commands: list[BotCommand],
        language_code: NoneStr = None,
    ) -> bool:
        """See :meth:`~yatbaf.bot.Bot.set_my_commands`,
        :class:`~yatbaf.types.bot_command_scope.BotCommandScopeChat`
        """
        return await self.bot.set_my_commands(
            commands=commands,
            scope=BotCommandScopeChat(self.id),
            language_code=language_code,
        )

    async def delete_commands(self, language_code: NoneStr = None) -> bool:
        """See :meth:`~yatbaf.bot.Bot.delete_my_commands`,
        :class:`~yatbaf.types.bot_command_scope.BotCommandScopeChat`
        """
        return await self.bot.delete_my_commands(
            scope=BotCommandScopeChat(self.id),
            language_code=language_code,
        )

    async def set_member_commands(
        self,
        user_id: int,
        commands: list[BotCommand],
        language_code: NoneStr = None,
    ) -> bool:
        """See :meth:`~yatbaf.bot.Bot.set_my_commands`,
        :class:`~yatbaf.types.bot_command_scope.BotCommandScopeChatMember`
        """
        return await self.bot.set_my_commands(
            commands=commands,
            scope=BotCommandScopeChatMember(
                chat_id=self.id,
                user_id=user_id,
            ),
            language_code=language_code,
        )

    async def delete_member_commands(
        self, user_id: int, language_code: NoneStr = None
    ) -> bool:
        """See :meth:`~yatbaf.bot.Bot.delete_my_commands`,
        :class:`~yatbaf.types.bot_command_scope.BotCommandScopeChatMember`
        """  # noqa: E501
        return await self.bot.delete_my_commands(
            scope=BotCommandScopeChatMember(
                chat_id=self.id,
                user_id=user_id,
            ),
            language_code=language_code,
        )

    async def set_administrators_commands(
        self,
        commands: list[BotCommand],
        language_code: NoneStr = None,
    ) -> bool:
        """See :meth:`~yatbaf.bot.Bot.set_my_commands`,
        :class:`~yatbaf.types.bot_command_scope.BotCommandScopeChatAdministrators`
        """  # noqa: E501
        return await self.bot.set_my_commands(
            commands=commands,
            scope=BotCommandScopeChatAdministrators(chat_id=self.id),
            language_code=language_code,
        )

    async def delete_administrators_commands(
        self, language_code: NoneStr = None
    ) -> bool:
        """See :meth:`~yatbaf.bot.Bot.delete_my_commands`,
        :class:`~yatbaf.types.bot_command_scope.BotCommandScopeChatAdministrators`
        """  # noqa: E501
        return await self.bot.delete_my_commands(
            scope=BotCommandScopeChatAdministrators(chat_id=self.id),
            language_code=language_code,
        )
