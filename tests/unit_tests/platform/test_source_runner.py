import unittest

from airbyte_cdk.models import ConfiguredAirbyteCatalog, Type

from airbyte_embed_cdk.source_runner import ContainerSourceRunner
from ..fixtures import Fixtures


class ContainerSourceRunnerTestCase(unittest.TestCase):
    def test_spec(self):
        source_runner = ContainerSourceRunner("airbyte/source-faker", "4.0.0")
        cmd_output = source_runner.spec()
        cmd_output = list(filter(lambda m: m.type == Type.SPEC, cmd_output))
        self.assertEqual(1, len(cmd_output))

    def test_check(self):
        source_runner = ContainerSourceRunner("airbyte/source-faker", "4.0.0")
        cmd_output = source_runner.check(config=Fixtures.CONFIG)
        cmd_output = list(filter(lambda m: m.type == Type.CONNECTION_STATUS, cmd_output))

        self.assertEqual(1, len(cmd_output))

    def test_discover(self):
        source_runner = ContainerSourceRunner("airbyte/source-faker", "4.0.0")
        cmd_output = source_runner.discover(config=Fixtures.CONFIG)
        cmd_output = list(filter(lambda m: m.type == Type.CATALOG, cmd_output))

        self.assertEqual(1, len(cmd_output))

    def test_read_no_state(self):
        source_runner = ContainerSourceRunner("airbyte/source-faker", "4.0.0")
        cmd_output = source_runner.read(config=Fixtures.CONFIG,
                                        catalog=ConfiguredAirbyteCatalog.parse_obj(Fixtures.CONFIGURED_CATALOG))
        cmd_output = list(filter(lambda m: m.type == Type.RECORD, cmd_output))

        self.assertEqual(30, len(cmd_output))

    def test_read_state(self):
        source_runner = ContainerSourceRunner("airbyte/source-faker", "4.0.0")
        cmd_output = source_runner.read(config=Fixtures.CONFIG,
                                        catalog=ConfiguredAirbyteCatalog.parse_obj(Fixtures.CONFIGURED_CATALOG),
                                        state=Fixtures.STATE)
        cmd_output = list(filter(lambda m: m.type == Type.RECORD, cmd_output))

        self.assertEqual(20, len(cmd_output))


if __name__ == "__main__":
    unittest.main()
