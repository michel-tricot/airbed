from abc import ABC, abstractmethod
from typing import Generic, Iterable, Optional, TypeVar

from airbyte_protocol.models import AirbyteRecordMessage, AirbyteStateMessage, Type

from airbyte_embed_cdk.catalog import create_full_refresh_catalog
from airbyte_embed_cdk.models.source import SourceRunner, TConfig, TState

TOutput = TypeVar("TOutput")


class EmbeddedIntegration(ABC, Generic[TConfig, TState, TOutput]):
    def __init__(self, source: SourceRunner[TConfig, TState], config: TConfig, state: Optional[TState] = None):
        self.source = source
        self.config = config
        self.state = state

        self.last_state: Optional[AirbyteStateMessage] = None

    @abstractmethod
    def _handle_record(self, record: AirbyteRecordMessage) -> Optional[TOutput]:
        pass

    def _load_data(self, stream: str) -> Iterable[TOutput]:
        configured_catalog = create_full_refresh_catalog(self.source, self.config, [stream])

        for message in self.source.read(self.config, configured_catalog, self.state):
            if message.type == Type.RECORD:
                # TODO(michel): do we want to have accumulation mechanism?
                output = self._handle_record(message.record)
                if output:
                    yield output
            elif message.type is Type.STATE and message.state:
                self.last_state = message.state