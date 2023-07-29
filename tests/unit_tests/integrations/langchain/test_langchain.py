import unittest

from airbyte_embed_cdk.integrations.langchain import container_airbyte_langchain_loader

from unit_tests.fixtures import Fixtures

FakerLoader = container_airbyte_langchain_loader("airbyte/source-faker", "4.0.0")


class LangchainTestCase(unittest.TestCase):
    def test_main(self):
        reader = FakerLoader(config=Fixtures.CONFIG, stream="users")
        data = reader.load()

        self.assertEqual(10, len(data))


if __name__ == "__main__":
    unittest.main()
