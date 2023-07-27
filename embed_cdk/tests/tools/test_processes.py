import unittest

from subprocess import CalledProcessError

from airbed.tools.processes import run_and_stream_lines


class ProcessesTestCase(unittest.TestCase):
    def test_echo(self):
        self.assertEqual([b"toto\n", b""], list(run_and_stream_lines(["echo", "toto"])))

    def test_unbounded(self):
        count = 0
        for line in run_and_stream_lines(["yes", "toto"]):
            self.assertEqual(b"toto\n", line)
            count += 1
            if count == 1_000:
                break

    def test_interrupt(self):
        with self.assertRaises(CalledProcessError):
            g = run_and_stream_lines(["yes", "toto"])
            next(g)
            next(g)
            g.close()

    def test_check_exit(self):
        with self.assertRaises(CalledProcessError):
            list(run_and_stream_lines(["false"]))


if __name__ == "__main__":
    unittest.main()
