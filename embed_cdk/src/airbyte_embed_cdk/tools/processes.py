import logging
import subprocess

from typing import Iterable, List, Optional


class ProcessResult:
    returncode: int


def run_and_stream_lines(cmd: List[str], result: Optional[ProcessResult] = None) -> Iterable[str]:
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True) as process:
        try:
            line = True
            while line:
                line = process.stdout.readline()
                yield line.strip()
            logging.debug(f"Execution finished {cmd}")
        except GeneratorExit:
            logging.debug(f"Execution interrupted {cmd}")
            process.kill()
        finally:
            process.wait()
            logging.debug(f"Execution status {cmd} {process.returncode}")
            if result:
                result.returncode = process.returncode
