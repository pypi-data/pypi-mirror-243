from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramType

if TYPE_CHECKING:
    from yatbaf.enums import Currency
    from yatbaf.typing import NoneBool
    from yatbaf.typing import NoneInt
    from yatbaf.typing import NoneStr

    from .labeled_price import LabeledPrice


@final
class InputInvoiceMessageContent(TelegramType):
    """Represents the content of an invoice message to be sent as the result
    of an inline query.

    See: https://core.telegram.org/bots/api#inputinvoicemessagecontent
    """

    title: str
    """Product name, 1-32 characters."""

    description: str
    """Product description, 1-255 characters."""

    payload: str
    """Bot-defined invoice payload, 1-128 bytes. This will not be displayed to
    the user, use for your internal processes.
    """

    provider_token: str
    """Payment provider token, obtained via @BotFather."""

    currency: Currency
    """Three-letter ISO 4217 currency code."""

    price: list[LabeledPrice]
    """Price breakdown, a list of components."""

    max_tip_amount: NoneInt = None
    """*Optional.* The maximum accepted amount for tips in the smallest units of
    the currency (integer, not float/double).
    """

    suggested_tip_amounts: list[int] | None = None
    """*Optional.* A list of suggested amounts of tip in the smallest units of
    the currency (integer, not float/double).
    """

    provider_data: NoneStr = None
    """*Optional.* A JSON-serialized object for data about the invoice, which
    will be shared with the payment provider. A detailed description of the
    required fields should be provided by the payment provider.
    """

    photo_url: NoneStr = None
    """*Optional.* URL of the product photo for the invoice. Can be a photo of
    the goods or a marketing image for a service.
    """

    photo_size: NoneInt = None
    """*Optional.* Photo size in bytes."""

    photo_width: NoneInt = None
    """*Optional.* Photo width."""

    photo_height: NoneInt = None
    """*Optional.* Photo height."""

    need_name: NoneBool = None
    """*Optional.* Pass ``True`` if you require the user's full name to
    complete the order.
    """

    need_phone_number: NoneBool = None
    """*Optional.* Pass ``True`` if you require the user's phone number to
    complete the order.
    """

    need_email: NoneBool = None
    """*Optional.* Pass ``True`` if you require the user's email address to
    complete the order.
    """

    need_shipping_address: NoneBool = None
    """*Optional.* Pass ``True`` if you require the user's shipping address to
    complete the order.
    """

    send_phone_number_to_provider: NoneBool = None
    """*Optional.* Pass ``True`` if the user's phone number should be sent to
    provider.
    """

    send_email_to_provider: NoneBool = None
    """*Optional.* Pass ``True`` if the user's email address should be sent to
    provider.
    """

    is_flexible: NoneBool = None
    """*Optional.* Pass ``True`` if the final price depends on the shipping
    method.
    """
