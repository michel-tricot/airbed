from typing import Callable, Generic, Iterable, List, Optional

from airbyte_cdk.models import AirbyteRecordMessage, Type
from airbyte_protocol.models import AirbyteStateMessage
from pydantic.errors import ConfigError

from airbyte_embed_cdk.catalog import create_full_refresh_catalog

try:
    from langchain.document_loaders.base import BaseLoader
    from langchain.schema import Document
except ImportError:
    import warnings

    warnings.warn("dependency not found, please install to enable langchain")
    raise
except (TypeError, ConfigError):
    # can't use the real type because of pydantic versions mismatch
    from .hack_types import BaseLoader, Document  # type: ignore[assignment]

from airbyte_embed_cdk.models.source import SourceRunner, TConfig, TState

Transformer = Callable[[AirbyteRecordMessage], Document]


def default_transformer(record: AirbyteRecordMessage) -> Document:
    document = Document(
        # TODO(michel): terrible transformation
        page_content=str(record.data),
        metadata={"stream_name": record.stream, "emitted_at": record.emitted_at},
    )

    return document


class BaseLangchainLoader(BaseLoader, Generic[TConfig, TState]):
    def __init__(
        self,
        source: SourceRunner[TConfig, TState],
        config: TConfig,
        stream: str,
        state: Optional[TState] = None,
        document_transformer: Transformer = default_transformer,
    ):
        self.source = source
        self.config = config
        self.stream = stream
        self.state = state
        self.document_transformer = document_transformer

        self.last_state: Optional[AirbyteStateMessage] = None

    def load(self) -> List[Document]:
        return list(self._stream_load_data())

    def _stream_load_data(self) -> Iterable[Document]:
        configured_catalog = create_full_refresh_catalog(self.source, self.config, [self.stream])

        for message in self.source.read(self.config, configured_catalog, self.state):
            if message.type == Type.RECORD:
                # TODO(michel): do we want to have accumulation mechanism?
                yield self.document_transformer(message.record)
            elif message.type is Type.STATE and message.state:
                self.last_state = message.state
