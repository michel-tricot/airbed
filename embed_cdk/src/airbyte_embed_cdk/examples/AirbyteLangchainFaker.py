from airbyte_embed_cdk.integrations.langchain.loader import BaseLangchainLoader


class AirbyteLangchainFaker(BaseLangchainLoader):
    def __init__(self, **kwargs):
        super().__init__(kwargs)
