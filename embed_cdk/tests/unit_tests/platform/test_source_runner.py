import os.path
import unittest

from airbyte_cdk.models import ConfiguredAirbyteCatalog, Type

from airbyte_embed_cdk.source_runner import ContainerSourceRunner
from airbyte_embed_cdk.tools import read_json


class SourceRunnerTestCase(unittest.TestCase):
    def test_spec(self):
        source_runner = ContainerSourceRunner("airbyte/source-faker", "4.0.0")
        cmd_output = source_runner.spec()
        cmd_output = list(filter(lambda m: m.type == Type.SPEC, cmd_output))
        self.assertEqual(1, len(cmd_output))

    def test_check(self):
        config = read_json(os.path.join(os.path.dirname(__file__), "../fixtures/config.json"))

        source_runner = ContainerSourceRunner("airbyte/source-faker", "4.0.0")
        cmd_output = source_runner.check(config=config)
        cmd_output = list(filter(lambda m: m.type == Type.CONNECTION_STATUS, cmd_output))

        self.assertEqual(1, len(cmd_output))

    def test_discover(self):
        config = read_json(os.path.join(os.path.dirname(__file__), "../fixtures/config.json"))

        source_runner = ContainerSourceRunner("airbyte/source-faker", "4.0.0")
        cmd_output = source_runner.discover(config=config)
        cmd_output = list(filter(lambda m: m.type == Type.CATALOG, cmd_output))

        self.assertEqual(1, len(cmd_output))

    def test_read_no_state(self):
        config = read_json(os.path.join(os.path.dirname(__file__), "../fixtures/config.json"))
        catalog = read_json(os.path.join(os.path.dirname(__file__), "../fixtures/configured_catalog.json"))

        source_runner = ContainerSourceRunner("airbyte/source-faker", "4.0.0")
        cmd_output = source_runner.read(config=config, catalog=ConfiguredAirbyteCatalog.parse_obj(catalog))
        cmd_output = list(filter(lambda m: m.type == Type.RECORD, cmd_output))

        self.assertEqual(30, len(cmd_output))

    def test_read_state(self):
        config = read_json(os.path.join(os.path.dirname(__file__), "../fixtures/config.json"))
        catalog = read_json(os.path.join(os.path.dirname(__file__), "../fixtures/configured_catalog.json"))
        state = read_json(os.path.join(os.path.dirname(__file__), "../fixtures/state.json"))

        source_runner = ContainerSourceRunner("airbyte/source-faker", "4.0.0")
        cmd_output = source_runner.read(config=config, catalog=ConfiguredAirbyteCatalog.parse_obj(catalog), state=state)
        cmd_output = list(filter(lambda m: m.type == Type.RECORD, cmd_output))

        self.assertEqual(20, len(cmd_output))


if __name__ == "__main__":
    unittest.main()
