import os.path
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Iterable, Optional, List

from airbyte_cdk.models import AirbyteMessage, ConfiguredAirbyteCatalog

from airbyte_embed_cdk.models.source import SourceRunner, TConfig, TState
from airbyte_embed_cdk.processes import run_and_stream_lines, ProcessResult
from airbyte_embed_cdk.tools import write_json

CONTAINER_RUNNER = os.getenv("AIRBYTE_CONTAINER_RUNNER", "docker")


class ContainerSourceRunner(SourceRunner):
    INPUT_FILES_PATH = Path("/input_files")

    def __init__(self, image_name: str, image_tag: str):
        self.image_name = image_name
        self.image_tag = image_tag
        self.container_runner = CONTAINER_RUNNER

        subprocess.check_output(
            [
                self.container_runner,
                "pull",
                self._image_id(),
            ]
        )

    def spec(self) -> Iterable[AirbyteMessage]:
        cmd = [self.container_runner, "run", "--rm", self._image_id(), "spec"]
        yield from self._run(cmd)

    def check(self, config: TConfig) -> Iterable[AirbyteMessage]:
        tmp_dir = Path(tempfile.mkdtemp())
        try:
            self._write_file(config, tmp_dir / "config.json")

            cmd = [
                self.container_runner,
                "run",
                "--rm",
                "-v",
                f"{tmp_dir}:{self.INPUT_FILES_PATH}",
                self._image_id(),
                "check",
                "--config",
                self.INPUT_FILES_PATH / "config.json",
            ]

            yield from self._run(cmd)
        finally:
            shutil.rmtree(tmp_dir)

    def discover(self, config: TConfig) -> Iterable[AirbyteMessage]:
        tmp_dir = Path(tempfile.mkdtemp())
        try:
            self._write_file(config, tmp_dir / "config.json")

            cmd = [
                self.container_runner,
                "run",
                "--rm",
                "-v",
                f"{tmp_dir}:{self.INPUT_FILES_PATH}",
                self._image_id(),
                "discover",
                "--config",
                self.INPUT_FILES_PATH / "config.json",
            ]

            yield from self._run(cmd)
        finally:
            shutil.rmtree(tmp_dir)

    def read(self, config: TConfig, catalog: ConfiguredAirbyteCatalog, state: Optional[TState] = None) -> Iterable[AirbyteMessage]:
        tmp_dir = Path(tempfile.mkdtemp())
        try:
            self._write_file(config, tmp_dir / "config.json")
            self._write_file(catalog, tmp_dir / "catalog.json")

            cmd = [
                self.container_runner,
                "run",
                "--rm",
                "-v",
                f"{tmp_dir}:{self.INPUT_FILES_PATH}",
                self._image_id(),
                "read",
                "--config",
                self.INPUT_FILES_PATH / "config.json",
                "--catalog",
                self.INPUT_FILES_PATH / "catalog.json",
            ]

            if state:
                self._write_file(state, tmp_dir / "state.json")
                state_args = ["--state", self.INPUT_FILES_PATH / "state.json"]
                cmd.extend(state_args)

            yield from self._run(cmd)
        finally:
            shutil.rmtree(tmp_dir)

    def _run(self, cmd: List[Any]) -> Iterable[AirbyteMessage]:
        result = ProcessResult()
        g = run_and_stream_lines(cmd, result)
        for message in self._parse_lines(g):
            yield message

    def _image_id(self) -> str:
        return f"{self.image_name}:{self.image_tag}"

    @staticmethod
    def _write_file(obj: Any, dst: Path) -> None:
        write_json(dst, obj)
