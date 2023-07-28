from abc import ABC, abstractmethod
from typing import Iterable, Optional

from airbyte_protocol.models import AirbyteMessage, ConfiguredAirbyteCatalog

from airbyte_embed_cdk.models.source import SourceRunner, TConfig, TState


class DecoratorSourceRunner(SourceRunner, ABC):
    def __init__(self, decorated: SourceRunner):
        self.decorated = decorated

    def spec(self) -> Iterable[AirbyteMessage]:
        yield from self._process(self.decorated.spec())

    def check(self, config: TConfig) -> Iterable[AirbyteMessage]:
        yield from self._process(self.decorated.check(config))

    def discover(self, config: TConfig) -> Iterable[AirbyteMessage]:
        yield from self._process(self.decorated.discover(config))

    def read(self, config: TConfig, catalog: ConfiguredAirbyteCatalog, state: Optional[TState]) -> Iterable[AirbyteMessage]:
        yield from self._process(self.decorated.read(config, catalog, state))

    @abstractmethod
    def _process(self, messages: Iterable[AirbyteMessage]) -> Iterable[AirbyteMessage]:
        pass
