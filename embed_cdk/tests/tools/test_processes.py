import logging
import unittest

from airbyte_embed_cdk.tools.processes import run_and_stream_lines, ProcessResult

logging.basicConfig(level=logging.DEBUG)


class ProcessesTestCase(unittest.TestCase):
    def test_echo(self):
        process_result = ProcessResult()
        self.assertEqual(
            ["toto", ""],
            list(run_and_stream_lines(["echo", "toto"], process_result)))

        self.assertEqual(process_result.returncode, 0)

    def test_echo_2(self):
        process_result = ProcessResult()
        self.assertEqual(
            ["toto", "toto", ""],
            list(run_and_stream_lines(["echo", "toto\ntoto"], process_result)))

        self.assertEqual(process_result.returncode, 0)

    def test_interrupt(self):
        process_result = ProcessResult()
        g = run_and_stream_lines(["yes", "toto"], process_result)
        next(g)
        next(g)
        g.close()

        self.assertEqual(process_result.returncode, -9)

    def test_exception(self):
        with self.assertRaises(Exception):
            process_result = ProcessResult()
            count = 0
            for line in run_and_stream_lines(["yes", "toto"], process_result):
                self.assertEqual("toto", line)
                count += 1
                if count == 1_000:
                    raise Exception("test")

        self.assertEqual(process_result.returncode, -9)

    def test_break(self):
        process_result = ProcessResult()
        count = 0
        for line in run_and_stream_lines(["yes", "toto"], process_result):
            self.assertEqual("toto", line)
            count += 1
            if count == 1_000:
                break

        self.assertEqual(process_result.returncode, -9)

    def test_check_exit(self):
        process_result = ProcessResult()
        list(run_and_stream_lines(["false"], process_result))
        self.assertEqual(process_result.returncode, 1)


if __name__ == "__main__":
    unittest.main()
