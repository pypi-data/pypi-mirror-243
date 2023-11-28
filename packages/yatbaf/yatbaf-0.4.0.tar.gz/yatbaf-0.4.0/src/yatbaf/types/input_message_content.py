from __future__ import annotations

from typing import TYPE_CHECKING
from typing import TypeAlias

if TYPE_CHECKING:
    from .input_contact_message_content import InputContactMessageContent
    from .input_invoce_message_content import InputInvoiceMessageContent
    from .input_location_message_content import InputLocationMessageContent
    from .input_text_message_content import InputTextMessageContent
    from .input_venue_message_content import InputVenueMessageContent

# https://core.telegram.org/bots/api#inputmessagecontent
InputMessageContent: TypeAlias = (
    "InputContactMessageContent "
    "| InputInvoiceMessageContent "
    "| InputLocationMessageContent "
    "| InputTextMessageContent "
    "| InputVenueMessageContent"
)
