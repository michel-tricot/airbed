from typing import Generic, Iterable, List, TypeVar

from airbyte_cdk.models import AirbyteRecordMessage, Type
from pydantic.errors import ConfigError

from ..base import create_full_catalog

try:
    from llama_index.readers.base import BaseReader
    from llama_index.readers.schema.base import Document
except (TypeError, ConfigError) as e:
    # can't use the real type because of pydantic versions mismatch
    from .hack_types import BaseReader, Document

from airbyte_embed_cdk.source_runner import SourceRunner


def default_transformer(record: AirbyteRecordMessage) -> Document:
    document = Document(
        # TODO: terrible transformation
        text=str(record.data),
        metadata={"stream_name": record.stream, "emitted_at": record.emitted_at},
    )

    return document


TConfig = TypeVar("TConfig")
TState = TypeVar("TState")


class BaseLLamaIndexReader(BaseReader, Generic[TConfig, TState]):
    def __init__(self, source: SourceRunner[TConfig, TState], config: TConfig, document_transformer=default_transformer):
        self.source = source
        self.config = config
        self.document_transformer = document_transformer

    def load_data(self, streams: List[str], state: TState = None) -> List[Document]:
        return list(self._stream_load_data(streams, state))

    def _stream_load_data(self, streams: List[str], state: TState) -> Iterable[Document]:
        configured_catalog = create_full_catalog(self.source, self.config, streams)

        for message in self.source.read(self.config, configured_catalog, state):
            if message.type == Type.RECORD:
                # TODO: do we want to have accumulation mechanism?
                yield self.document_transformer(message.record)