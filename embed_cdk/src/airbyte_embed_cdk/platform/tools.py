from typing import Iterable, Optional

from airbyte_cdk.models import AirbyteMessage, Type

from airbyte_embed_cdk.tools.tools import get_first


def get_first_message(messages: Iterable[AirbyteMessage], message_type: Type) -> Optional[AirbyteMessage]:
    return get_first(messages, lambda m: m.type == message_type)
