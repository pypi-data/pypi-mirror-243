from __future__ import annotations

__all__ = ("Content",)

from typing import TYPE_CHECKING
from typing import Final
from typing import final

from yatbaf.enums import ContentType

if TYPE_CHECKING:
    from yatbaf.types import Message


@final
class Content:
    """Content filter.

    Use it to filter message by content::

        @on_message(filters=[Content("photo")])
        async def process_photo(message: Message) -> None:
            ...

        @on_message(filters=[Content(ContentType.DOCUMENT)])
        async def process_document(message: Message) -> None:
            ...

    See :class:`~yatbaf.enums.ContentType`.
    """

    __slots__ = (
        "content",
        "priority",
    )

    def __init__(
        self,
        *content: ContentType | str,
        priority: int = 300,
    ) -> None:
        """
        :param content: Content type.
        :param priority: Filter priority. Default 300.
        :raise ValueError: If ``content`` is empty or wrong type was passed.
        """
        if not content:
            raise ValueError("You must pass at least one type.")
        self.content = frozenset([ContentType(c) for c in content])
        self.priority = priority

    def check(self, update: Message) -> bool:
        for c in self.content:
            if getattr(update, c) is not None:
                return True
        return False


media_content: Final[Content] = Content(
    ContentType.AUDIO,
    ContentType.VIDEO,
    ContentType.VIDEO_NOTE,
    ContentType.VOICE,
    ContentType.PHOTO,
    ContentType.ANIMATION,
    ContentType.STICKER,
    ContentType.DOCUMENT,
)
"""Media content filter.

Use it to filter message with: ``animation``, ``audio``, ``document``,
``photo``, ``sticker``, ``video``, ``video note`` or ``voice``.

Usage::

    @on_message(filters=[media_content])
    async def callback(message: Message) -> None:
        ...
"""
