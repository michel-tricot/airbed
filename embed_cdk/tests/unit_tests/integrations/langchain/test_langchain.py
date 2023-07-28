import unittest

from airbyte_embed_cdk.integrations.langchain import airbyte_langchain_loader
from airbyte_embed_cdk.tools import parse_json

CONFIG = parse_json('{"count": 10, "seed": 0, "parallelism": 1, "always_updated": false}')

FakerLoader = airbyte_langchain_loader("airbyte/source-faker", "4.0.0")


class LangchainTestCase(unittest.TestCase):
    def test_main(self):
        reader = FakerLoader(config=CONFIG, streams=["users"])
        data = reader.load()

        self.assertEqual(10, len(data))


if __name__ == "__main__":
    unittest.main()
