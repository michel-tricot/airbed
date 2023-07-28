from typing import Generic, Iterable, List, TypeVar

from airbyte_cdk.models import AirbyteRecordMessage, Type
from pydantic.errors import ConfigError

from ..base import create_full_catalog

try:
    from langchain.document_loaders.base import BaseLoader
    from langchain.schema import Document
except (TypeError, ConfigError) as e:
    # can't use the real type because of pydantic versions mismatch
    from .hack_types import BaseLoader, Document

from airbyte_embed_cdk.source_runner import SourceRunner, ContainerSourceRunner


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
    def __init__(
            self,
            source: SourceRunner[TConfig, TState],
            config: TConfig,
            streams: List[str] = None,
            state: TState = None,
            document_transformer=default_transformer,
    ):
        self.source = source
        self.config = config
        self.streams = streams
        self.state = state
        self.document_transformer = document_transformer

    def load(self) -> List[Document]:
        return list(self._stream_load_data())

    def _stream_load_data(self) -> Iterable[Document]:
        configured_catalog = create_full_catalog(self.source, self.config, self.streams)

        for message in self.source.read(self.config, configured_catalog, self.state):
            if message.type == Type.RECORD:
                # TODO: do we want to have accumulation mechanism?
                yield self.document_transformer(message.record)
