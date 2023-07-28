import os.path
import unittest

from airbyte_embed_cdk.platform.catalog import get_stream
from airbyte_embed_cdk.platform.source_runner import ContainerSourceRunner
from airbyte_embed_cdk.platform.tools import get_first_message
from airbyte_embed_cdk.tools.tools import read_json, get_first
from airbyte_cdk.models import ConfiguredAirbyteCatalog, Type, AirbyteMessage, AirbyteCatalog


class ToolsTestCase(unittest.TestCase):
    def test_get_first(self):
        self.assertEqual(1, get_first([1], lambda e: e == 1))
        self.assertEqual(1, get_first([2, 1], lambda e: e == 1))
        self.assertFalse(get_first([2, 3], lambda e: e == 1))


if __name__ == "__main__":
    unittest.main()
