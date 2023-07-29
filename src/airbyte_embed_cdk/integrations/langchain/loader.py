from typing import Callable, Generic, List, Optional

from airbyte_cdk.models import AirbyteRecordMessage
from pydantic.errors import ConfigError

from ..base_integration import EmbeddedIntegration

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


class BaseLangchainLoader(BaseLoader, EmbeddedIntegration[TConfig, TState, Document], Generic[TConfig, TState]):
    def __init__(
        self,
        source: SourceRunner[TConfig, TState],
        config: TConfig,
        stream: str,
        state: Optional[TState] = None,
        document_transformer: Transformer = default_transformer,
    ):
        super().__init__(source, config)
        self.stream = stream
        self.state = state

        self.document_transformer = document_transformer

    def load(self) -> List[Document]:
        return list(self._load_data(self.stream, self.state))

    def _handle_record(self, record: AirbyteRecordMessage) -> Optional[Document]:
        return self.document_transformer(record)
