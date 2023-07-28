from typing import Generic, Iterable, List, TypeVar

from airbyte_cdk.models import AirbyteRecordMessage, ConfiguredAirbyteCatalog, Type

from airbyte_embed_cdk.platform.catalog import full_refresh_streams
from airbyte_embed_cdk.platform.source_runner import SourceRunner
from airbyte_embed_cdk.tools import get_first_message

# can't use the real type because of pydantic versions mis-match
# from llama_index.readers.base import BaseReader
# from llama_index.readers.schema.base import Document
from .hack_types import BaseReader, Document


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
    def __init__(self, source: SourceRunner[TConfig, TState], document_transformer=default_transformer):
        self.source = source
        self.document_transformer = document_transformer

    def load_data(self, config: TConfig, streams: List[str], state: TState = None) -> List[Document]:
        return list(self._stream_load_data(config, streams, state))

    def _stream_load_data(self, config: TConfig, streams: List[str], state: TState) -> Iterable[Document]:
        configured_catalog = self._to_configured_catalog(config, streams)

        for message in self.source.read(config, configured_catalog, state):
            if message.type == Type.RECORD:
                # TODO: do we want to have accumulation mechanism?
                yield self.document_transformer(message.record)

    def _to_configured_catalog(self, config, streams) -> ConfiguredAirbyteCatalog:
        catalog_message = get_first_message(self.source.discover(config), Type.CATALOG)

        if not catalog_message:
            raise Exception("Can't retrieve catalog from source")

        return full_refresh_streams(catalog_message.catalog, streams)
