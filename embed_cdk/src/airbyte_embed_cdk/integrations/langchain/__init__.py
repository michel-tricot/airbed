from typing import List

from airbyte_embed_cdk.integrations.langchain.loader import default_transformer, BaseLangchainLoader
from airbyte_embed_cdk.source_runner import ContainerSourceRunner


def airbyte_langchain_loader(name, version):
    def constructor(config,
                    streams: List[str] = None,
                    state=None,
                    document_transformer=default_transformer):
        source = ContainerSourceRunner(name, version)
        return BaseLangchainLoader(source, config, streams, state, document_transformer)

    return constructor
