from typing import List

from airbyte_embed_cdk.integrations.langchain.loader import (
    BaseLangchainLoader,
    default_transformer,
)
from airbyte_embed_cdk.source_runner import ContainerSourceRunner


class MetaConfig(type):
    def __init__(cls, name, bases, dct):
        cls.attr = 100


def airbyte_langchain_loader(name, version):
    def constructor(config, streams: List[str] = None, state=None, document_transformer=default_transformer):
        source = ContainerSourceRunner(name, version)
        return BaseLangchainLoader(source, config, streams, state, document_transformer)

    return constructor
