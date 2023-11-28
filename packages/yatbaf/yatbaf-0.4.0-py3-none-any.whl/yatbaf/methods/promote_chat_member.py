from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.typing import NoneBool


@final
class PromoteChatMember(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.promote_chat_member`"""

    chat_id: str | int
    user_id: int
    is_anonymous: NoneBool = None
    can_manage_chat: NoneBool = None
    can_post_messages: NoneBool = None
    can_edit_messages: NoneBool = None
    can_delete_messages: NoneBool = None
    can_manage_video_chats: NoneBool = None
    can_restrict_members: NoneBool = None
    can_promote_members: NoneBool = None
    can_change_info: NoneBool = None
    can_invite_users: NoneBool = None
    can_pin_messages: NoneBool = None
    can_post_stories: NoneBool = None
    can_edit_stories: NoneBool = None
    can_delete_stories: NoneBool = None
    can_manage_topics: NoneBool = None
