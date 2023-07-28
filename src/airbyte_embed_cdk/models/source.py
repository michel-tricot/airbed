from abc import ABC, abstractmethod
from typing import Generic, Iterable, Optional, TypeVar

from airbyte_protocol.models import AirbyteLogMessage, AirbyteMessage, ConfiguredAirbyteCatalog, Level, Type

from airbyte_embed_cdk.tools import parse_json

TConfig = TypeVar("TConfig")
TState = TypeVar("TState")


class SourceRunner(ABC, Generic[TConfig, TState]):
    @abstractmethod
    def spec(self) -> Iterable[AirbyteMessage]:
        # Maybe we should return the spec directly?
        pass

    @abstractmethod
    def check(self, config: TConfig) -> Iterable[AirbyteMessage]:
        pass

    @abstractmethod
    def discover(self, config: TConfig) -> Iterable[AirbyteMessage]:
        # Maybe we should return the catalog directly?
        pass

    @abstractmethod
    def read(self, config: TConfig, catalog: ConfiguredAirbyteCatalog, state: Optional[TState]) -> Iterable[AirbyteMessage]:
        pass

    @staticmethod
    def _parse_lines(line_generator: Iterable[str]) -> Iterable[AirbyteMessage]:
        for line in line_generator:
            parsed_line = parse_json(line)
            if parsed_line:
                obj = AirbyteMessage.parse_obj(parsed_line)
            else:
                obj = AirbyteMessage.parse_obj(
                    {"type": Type.LOG, "log": AirbyteLogMessage.parse_obj({"level": Level.DEBUG, "message": line})}
                )
            yield obj
