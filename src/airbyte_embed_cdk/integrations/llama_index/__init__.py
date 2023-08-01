import logging
from typing import Protocol

from airbyte_cdk.sources import Source

from airbyte_embed_cdk.integrations.llama_index.reader import (
    BaseLLamaIndexReader,
    Transformer,
    default_transformer,
)
from airbyte_embed_cdk.models.source import TConfig, TState
from airbyte_embed_cdk.sources.cdk_source import CdkSourceRunner
from airbyte_embed_cdk.sources.container_source import ContainerSourceRunner


class ReaderClass(Protocol):
    def __call__(
        self,
        config: TConfig,
        document_transformer: Transformer,
    ) -> BaseLLamaIndexReader[TConfig, TState]:
        pass


def cdk_airbyte_llamaindex_reader(source_class: type[Source]) -> ReaderClass:
    def constructor(
        config: TConfig,
        document_transformer: Transformer = default_transformer,
    ) -> BaseLLamaIndexReader[TConfig, TState]:
        source = CdkSourceRunner(source_class(), logging.getLogger(__name__))
        return BaseLLamaIndexReader(source, config, document_transformer)

    return constructor


def container_airbyte_llamaindex_reader(name: str, default_version: str) -> ReaderClass:
    def constructor(
        config: TConfig, document_transformer: Transformer = default_transformer, version: str = default_version
    ) -> BaseLLamaIndexReader[TConfig, TState]:
        # TODO(michel): How early should we check the config?
        source = ContainerSourceRunner(name, version)
        return BaseLLamaIndexReader(source, config, document_transformer)

    return constructor
