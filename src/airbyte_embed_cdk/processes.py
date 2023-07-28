import logging
import subprocess
from typing import Any, Iterable, List, Optional


class ProcessResult:
    returncode: int


def run_and_stream_lines(cmd: List[Any], result: Optional[ProcessResult] = None) -> Iterable[str]:
    logging.debug(f"Running {' '.join([str(p) for p in cmd])}")
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True) as process:
        try:
            line = "initial"
            while line and process.stdout:
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
