from typing import Any, List, Iterable, Generic, TypeVar

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document

from airbed.platform.source_runner import SourceRunner

from airbyte_cdk.models import AirbyteRecordMessage, Type, ConfiguredAirbyteCatalog


def default_transformer(record: AirbyteRecordMessage) -> Document:
    document = Document(
        text=None,
        metadata={
            "stream_name": record.stream,
            "emitted_at": record.emitted_at
        },
    )

    return document


class DocumentTransformer:
    def __init__(self, source: SourceRunner):
        pass


TConfig = TypeVar("TConfig")
TState = TypeVar("TState")


class BaseLLamaIndexReader(BaseReader, Generic[TConfig, TState]):

    def __init__(self, source: SourceRunner[TConfig, TState], document_transformer=default_transformer):
        self.source = source
        self.document_transformer = document_transformer

    def load_data(self, config: TConfig, streams: List[str], state: TState = None) -> List[Document]:
        return list(self._stream_load_data(config, streams, state))

    def _stream_load_data(self, config: TConfig, streams: List[str], state: TState) -> Iterable[Document]:
        configured_catalog = self._to_configured_catalog(streams)

        for message in self.source.read(config, configured_catalog, state):
            if message.type == Type.RECORD:
                # TODO: do we want to have accumulation mechanism?
                yield self.document_transformer(message.record)

    def _to_configured_catalog(self, streams: List[str]) -> ConfiguredAirbyteCatalog:
        pass
