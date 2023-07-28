import os.path
import unittest

from airbyte_cdk.models import AirbyteCatalog
from airbyte_embed_cdk.catalog import get_stream
from airbyte_embed_cdk.tools import read_json


class CatalogTestCase(unittest.TestCase):
    def test_get_stream(self):
        catalog = AirbyteCatalog.parse_obj(read_json(os.path.join(os.path.dirname(__file__), "fixtures/data/catalog.json")))

        self.assertTrue(get_stream(catalog, "users"))
        self.assertFalse(get_stream(catalog, "users2"))


if __name__ == "__main__":
    unittest.main()
