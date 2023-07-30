from logging import Logger
from typing import Iterable, Optional

from airbyte_cdk.connector import TConfig
from airbyte_cdk.sources.source import Source, TState
from airbyte_protocol.models import AirbyteMessage, ConfiguredAirbyteCatalog, Type
from pydantic import BaseModel

from airbyte_embed_cdk.models.source import SourceRunner


class CdkSourceRunner(SourceRunner):
    def __init__(self, source: Source, logger: Logger):
        self._source = source
        self._logger = logger

    def spec(self) -> Iterable[AirbyteMessage]:
        spec = self._source.spec(self._logger)
        yield AirbyteMessage(type=Type.SPEC, spec=spec)

    def check(self, config: TConfig) -> Iterable[AirbyteMessage]:
        if isinstance(config, BaseModel):
            config = config.dict()
        status = self._source.check(self._logger, config)
        yield AirbyteMessage(type=Type.CONNECTION_STATUS, connectionStatus=status)

    def discover(self, config: TConfig) -> Iterable[AirbyteMessage]:
        if isinstance(config, BaseModel):
            config = config.dict()
        catalog = self._source.discover(self._logger, config)
        yield AirbyteMessage(type=Type.CATALOG, catalog=catalog)

    def read(self, config: TConfig, catalog: ConfiguredAirbyteCatalog, state: Optional[TState]) -> Iterable[AirbyteMessage]:
        if isinstance(config, BaseModel):
            config = config.dict()
        yield from self._source.read(self._logger, config, catalog, state)  # type: ignore
