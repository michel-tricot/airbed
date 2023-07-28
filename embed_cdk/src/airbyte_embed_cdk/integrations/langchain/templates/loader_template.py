from typing import TypeVar, List

from airbyte_embed_cdk.integrations.langchain.loader import BaseLangchainLoader, default_transformer
from airbyte_embed_cdk.integrations.langchain.templates.config_template import ConfigTemplate
from airbyte_embed_cdk.source_runner import ContainerSourceRunner

IMAGE_NAME = "airbyte/faker"
IMAGE_TAG = "4.0.0"

TState = TypeVar("TState")


class AirbyteLangchainFaker(BaseLangchainLoader[ConfigTemplate, TState]):
    def __init__(self,
                 config: ConfigTemplate,
                 streams: List[str] = None,
                 state: TState = None,
                 document_transformer=default_transformer):
        super().__init__(
            ContainerSourceRunner(IMAGE_NAME, IMAGE_TAG),
            config,
            streams,
            state,
            document_transformer)
