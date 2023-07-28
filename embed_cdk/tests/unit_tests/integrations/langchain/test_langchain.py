import unittest

from airbyte_embed_cdk.integrations.langchain.loader import BaseLangchainLoader
from airbyte_embed_cdk.platform.source_runner import ContainerSourceRunner
from airbyte_embed_cdk.tools import read_json


CONFIG = read_json("../../fixtures/config.json")


class LangchainTestCase(unittest.TestCase):
    def test_main(self):
        source_runner = ContainerSourceRunner("airbyte/source-faker", "4.0.0")

        reader = BaseLangchainLoader(source_runner, config=CONFIG, streams=["users"])
        data = reader.load()

        self.assertEqual(10, len(data))


if __name__ == "__main__":
    unittest.main()
