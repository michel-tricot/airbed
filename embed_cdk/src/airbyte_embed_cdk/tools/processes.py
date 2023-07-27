import logging
import subprocess

from typing import Iterable, List


def run_and_stream_lines(cmd: List[str]) -> Iterable[str]:
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    line = True
    try:
        while line:
            line = process.stdout.readline()
            yield line
        logging.debug("Execution finished")
    except GeneratorExit:
        logging.debug("Execution stopped")
        process.kill()
    finally:
        process.wait()

    if process.returncode:
        raise subprocess.CalledProcessError(process.returncode, cmd)
