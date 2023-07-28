import os.path
import unittest

from airbyte_embed_cdk.platform.source_runner import ContainerSourceRunner
from airbyte_embed_cdk.platform.tools import get_first_message
from airbyte_embed_cdk.tools.tools import read_json
from airbyte_cdk.models import ConfiguredAirbyteCatalog, Type, AirbyteMessage


class PlatformToolsTestCase(unittest.TestCase):
    def test_first_message(self):
        log_message = AirbyteMessage.parse_obj({"type": Type.LOG})
        record_message = AirbyteMessage.parse_obj({"type": Type.RECORD})

        self.assertEqual(record_message, get_first_message([log_message, record_message], Type.RECORD))
        self.assertFalse(get_first_message([log_message, record_message], Type.CATALOG))


if __name__ == "__main__":
    unittest.main()
