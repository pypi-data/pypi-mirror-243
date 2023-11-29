from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.typing import NoneBool
from yatbaf.typing import NoneInt
from yatbaf.typing import NoneStr

from .abc import TelegramType

if TYPE_CHECKING:
    from yatbaf.types import UserProfilePhotos


@final
class User(TelegramType):
    """This object represents a Telegram user or bot.

    See: https://core.telegram.org/bots/api#user
    """

    id: int
    """Unique identifier for this user or bot."""

    is_bot: bool
    """``True``, if this user is a bot."""

    first_name: str
    """User's or bot's first name."""

    last_name: NoneStr = None
    """*Optional.* User's or bot's last name."""

    username: NoneStr = None
    """*Optional.* User's or bot's username."""

    language_code: NoneStr = None
    """*Optional.* IETF language tag of the user's language."""

    is_premium: NoneBool = None
    """*Optional.* ``True``, if this user is a Telegram Premium user."""

    added_to_attachment_menu: NoneBool = None
    """
    *Optional.* ``True``, if this user added the bot to the attachment menu.
    """

    can_join_groups: NoneBool = None
    """*Optional.* ``True``, if the bot can be invited to groups.

    .. note::

        Returned only in :meth:`get_me <yatbaf.bot.Bot.get_me>`.
    """

    can_read_all_group_messages: NoneBool = None
    """*Optional.* ``True``, if privacy mode is disabled for the bot.

    .. note::

        Returned only in :meth:`get_me <yatbaf.bot.Bot.get_me>`.
    """

    supports_inline_queries: NoneBool = None
    """*Optional.* ``True``, if the bot supports inline queries.

    .. note::

        Returned only in :meth:`get_me <yatbaf.bot.Bot.get_me>`.
    """

    async def get_photos(
        self,
        offset: NoneInt = None,
        limit: NoneInt = None,
    ) -> UserProfilePhotos:
        """Get profile photos.

        See: :meth:`get_user_profile_photos <yatbaf.bot.Bot.get_user_profile_photos>`
        """  # noqa: E501

        return await self.bot.get_user_profile_photos(
            user_id=self.id,
            offset=offset,
            limit=limit,
        )
