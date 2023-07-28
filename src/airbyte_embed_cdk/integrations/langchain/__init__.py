from typing import List, Optional, Protocol

from airbyte_embed_cdk.container_source import ContainerSourceRunner
from airbyte_embed_cdk.integrations.langchain.loader import (
    BaseLangchainLoader,
    Transformer,
    default_transformer,
)
from airbyte_embed_cdk.models.source import TConfig, TState


class LoaderClass(Protocol):
    def __call__(
        self,
        config: TConfig,
        streams: Optional[List[str]] = None,
        state: Optional[TState] = None,
        document_transformer: Transformer = default_transformer,
    ) -> BaseLangchainLoader[TConfig, TState]:
        pass


def airbyte_langchain_loader(name: str, version: str) -> LoaderClass:
    def constructor(
        config: TConfig,
        streams: Optional[List[str]] = None,
        state: Optional[TState] = None,
        document_transformer: Transformer = default_transformer,
    ) -> BaseLangchainLoader[TConfig, TState]:
        # TODO(michel): How early should we check the config?
        source = ContainerSourceRunner(name, version)
        return BaseLangchainLoader(source, config, streams, state, document_transformer)

    return constructor
