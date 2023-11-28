from __future__ import annotations

from typing import final

from yatbaf.types import WebhookInfo

from .abc import TelegramMethod


@final
class GetWebhookInfo(TelegramMethod[WebhookInfo]):
    """See :meth:`yatbaf.bot.Bot.get_webhook_info`"""
