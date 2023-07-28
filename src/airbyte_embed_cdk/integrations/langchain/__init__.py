from typing import Callable, List, Optional

from airbyte_embed_cdk.integrations.langchain.loader import (
    BaseLangchainLoader,
    Transformer,
    default_transformer,
)
from airbyte_embed_cdk.models.source import TConfig, TState
from airbyte_embed_cdk.source_runner import ContainerSourceRunner

LoaderGenerator = Callable[[TConfig, Optional[List[str]], Optional[TState], Transformer], BaseLangchainLoader[TConfig, TState]]


def airbyte_langchain_loader(name: str, version: str) -> LoaderGenerator:
    def constructor(
        config: TConfig,
        streams: Optional[List[str]] = None,
        state: Optional[TState] = None,
        document_transformer: Transformer = default_transformer,
    ) -> BaseLangchainLoader[TConfig, TState]:
        source = ContainerSourceRunner(name, version)
        return BaseLangchainLoader(source, config, streams, state, document_transformer)

    return constructor
