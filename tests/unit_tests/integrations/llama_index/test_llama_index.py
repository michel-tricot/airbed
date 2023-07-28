import unittest

from airbyte_embed_cdk.integrations.llama_index import airbyte_llamaindex_reader

from unit_tests.fixtures import Fixtures

FakerReader = airbyte_llamaindex_reader("airbyte/source-faker", "4.0.0")


class LLamaIndexTestCase(unittest.TestCase):
    def test_main(self):
        reader = FakerReader(config=Fixtures.CONFIG)
        data = reader.load_data(["users"])

        self.assertEqual(10, len(data))


if __name__ == "__main__":
    unittest.main()
