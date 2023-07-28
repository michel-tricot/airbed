import unittest

from airbyte_embed_cdk.integrations.llama_index.reader import BaseLLamaIndexReader
from airbyte_embed_cdk.platform.source_runner import ContainerSourceRunner
from airbyte_embed_cdk.tools import read_json

CONFIG = read_json('fixtures/config.json')


class MainTestCase(unittest.TestCase):
    def test_main(self):
        source_runner = ContainerSourceRunner("airbyte/source-faker", "4.0.0")

        reader = BaseLLamaIndexReader(source_runner)
        data = reader.load_data(CONFIG, ["users"])
        print(data)
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
