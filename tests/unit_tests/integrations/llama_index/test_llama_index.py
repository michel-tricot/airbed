import unittest

from airbyte_embed_cdk.integrations.llama_index.reader import BaseLLamaIndexReader
from airbyte_embed_cdk.source_runner import ContainerSourceRunner

from unit_tests.fixtures import Fixtures


class LLamaIndexTestCase(unittest.TestCase):
    def test_main(self):
        source_runner = ContainerSourceRunner("airbyte/source-faker", "4.0.0")

        reader = BaseLLamaIndexReader(source_runner, config=Fixtures.CONFIG)
        data = reader.load_data(["users"])

        self.assertEqual(10, len(data))


if __name__ == "__main__":
    unittest.main()
