from typing import Generic, Iterable, List, TypeVar

from airbyte_cdk.models import AirbyteRecordMessage, ConfiguredAirbyteCatalog, Type
from pydantic.errors import ConfigError

try:
    from langchain.document_loaders.base import BaseLoader
    from langchain.schema import Document
except (TypeError, ConfigError) as e:
    # can't use the real type because of pydantic versions mismatch
    from .hack_types import BaseLoader, Document

from airbyte_embed_cdk.platform.catalog import full_refresh_streams
from airbyte_embed_cdk.platform.source_runner import SourceRunner
from airbyte_embed_cdk.tools import get_first_message


def default_transformer(record: AirbyteRecordMessage) -> Document:
    document = Document(
        # TODO: terrible transformation
        page_content=str(record.data),
        metadata={"stream_name": record.stream, "emitted_at": record.emitted_at},
    )

    return document


TConfig = TypeVar("TConfig")
TState = TypeVar("TState")


class BaseLangchainLoader(BaseLoader, Generic[TConfig, TState]):
    def __init__(self,
                 source: SourceRunner[TConfig, TState],
                 config: TConfig,
                 streams: List[str] = None,
                 state: TState = None,
                 document_transformer=default_transformer):
        self.source = source
        self.config = config
        self.streams = streams
        self.state = state
        self.document_transformer = document_transformer

    def load(self) -> List[Document]:
        return list(self._stream_load_data())

    def _stream_load_data(self) -> Iterable[Document]:
        configured_catalog = self._to_configured_catalog()

        for message in self.source.read(self.config, configured_catalog, self.state):
            if message.type == Type.RECORD:
                # TODO: do we want to have accumulation mechanism?
                yield self.document_transformer(message.record)

    def _to_configured_catalog(self) -> ConfiguredAirbyteCatalog:
        catalog_message = get_first_message(self.source.discover(self.config), Type.CATALOG)

        if not catalog_message:
            raise Exception("Can't retrieve catalog from source")

        catalog = catalog_message.catalog
        streams = self.streams
        if not streams:
            streams = [stream.name for stream in catalog.streams]

        return full_refresh_streams(catalog, streams)
