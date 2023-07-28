import os.path
import unittest

from airbyte_embed_cdk.platform.catalog import get_stream
from airbyte_embed_cdk.platform.source_runner import ContainerSourceRunner
from airbyte_embed_cdk.platform.tools import get_first_message
from airbyte_embed_cdk.tools.tools import read_json
from airbyte_cdk.models import ConfiguredAirbyteCatalog, Type, AirbyteMessage, AirbyteCatalog


class CatalogTestCase(unittest.TestCase):
    def test_get_stream(self):
        catalog = AirbyteCatalog.parse_obj(read_json(os.path.join(os.path.dirname(__file__), "../fixtures/catalog.json")))

        self.assertTrue(get_stream(catalog, "users"))
        self.assertFalse(get_stream(catalog, "users2"))


if __name__ == "__main__":
    unittest.main()
