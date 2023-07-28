import unittest

from airbyte_cdk.models import AirbyteMessage, Type

from airbyte_embed_cdk.tools import get_first, get_first_message


class ToolsTestCase(unittest.TestCase):
    def test_first_message(self):
        log_message = AirbyteMessage.parse_obj({"type": Type.LOG})
        record_message = AirbyteMessage.parse_obj({"type": Type.RECORD})

        self.assertEqual(record_message, get_first_message([log_message, record_message], Type.RECORD))
        self.assertFalse(get_first_message([log_message, record_message], Type.CATALOG))

    def test_get_first(self):
        self.assertEqual(1, get_first([1], lambda e: e == 1))
        self.assertEqual(1, get_first([2, 1], lambda e: e == 1))
        self.assertFalse(get_first([2, 3], lambda e: e == 1))


if __name__ == "__main__":
    unittest.main()
