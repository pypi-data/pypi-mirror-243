from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import UserProfilePhotos

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.typing import NoneInt


@final
class GetUserProfilePhotos(TelegramMethod[UserProfilePhotos]):
    """See :meth:`yatbaf.bot.Bot.get_user_profile_photos`"""

    user_id: int
    offset: NoneInt = None
    limit: NoneInt = None
