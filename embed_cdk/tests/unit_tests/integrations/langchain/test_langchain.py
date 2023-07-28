import unittest

from airbyte_embed_cdk.integrations.langchain.loader import BaseLangchainLoader
from airbyte_embed_cdk.source_runner import ContainerSourceRunner
from airbyte_embed_cdk.tools import parse_json

CONFIG = parse_json('{"count": 10, "seed": 0, "parallelism": 1, "always_updated": false}')


class LangchainTestCase(unittest.TestCase):
    def test_main(self):
        source_runner = ContainerSourceRunner("airbyte/source-faker", "4.0.0")

        reader = BaseLangchainLoader(source_runner, config=CONFIG, streams=["users"])
        data = reader.load()

        self.assertEqual(10, len(data))


if __name__ == "__main__":
    unittest.main()
