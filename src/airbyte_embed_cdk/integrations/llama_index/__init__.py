from typing import Protocol

from airbyte_embed_cdk.container_source import ContainerSourceRunner
from airbyte_embed_cdk.integrations.llama_index.reader import (
    BaseLLamaIndexReader,
    Transformer,
    default_transformer,
)
from airbyte_embed_cdk.models.source import TConfig, TState


class ReaderClass(Protocol):
    def __call__(
        self,
        config: TConfig,
        document_transformer: Transformer = default_transformer,
    ) -> BaseLLamaIndexReader[TConfig, TState]:
        pass


def airbyte_llamaindex_reader(name: str, version: str) -> ReaderClass:
    def constructor(
        config: TConfig,
        document_transformer: Transformer = default_transformer,
    ) -> BaseLLamaIndexReader[TConfig, TState]:
        # TODO(michel): How early should we check the config?
        source = ContainerSourceRunner(name, version)
        return BaseLLamaIndexReader(source, config, document_transformer)

    return constructor
