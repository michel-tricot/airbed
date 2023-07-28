import logging
import os.path
import shutil
import subprocess
import tempfile

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generic, Iterable, TypeVar

from airbyte_cdk.models import AirbyteMessage, ConfiguredAirbyteCatalog, Type
from pydantic.typing import PathLike

from airbyte_embed_cdk.processes import run_and_stream_lines
from airbyte_embed_cdk.tools import parse_json, write_json


TConfig = TypeVar("TConfig")
TState = TypeVar("TState")


class SourceRunner(ABC, Generic[TConfig, TState]):
    @abstractmethod
    def spec(self) -> Iterable[AirbyteMessage]:
        # Maybe we should return the spec directly?
        pass

    @abstractmethod
    def check(self, config: TConfig) -> Iterable[AirbyteMessage]:
        pass

    @abstractmethod
    def discover(self, config: TConfig) -> Iterable[AirbyteMessage]:
        # Maybe we should return the catalog directly?
        pass

    @abstractmethod
    def read(self, config: TConfig, catalog: ConfiguredAirbyteCatalog, state: TState) -> Iterable[AirbyteMessage]:
        pass

    @staticmethod
    def _parse_lines(line_generator: Iterable[str]) -> Iterable[AirbyteMessage]:
        for line in line_generator:
            parsed_line = parse_json(line)
            if parsed_line:
                obj = AirbyteMessage.parse_obj(parsed_line)
                if obj.type != Type.LOG:
                    yield obj
                else:
                    logging.info(obj)
            else:
                logging.info(line)


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
        g = run_and_stream_lines([self.container_runner, "run", "--rm", self._image_id(), "spec"])
        return self._parse_lines(g)

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
            g = run_and_stream_lines(cmd)
            for message in self._parse_lines(g):
                yield message
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
            g = run_and_stream_lines(cmd)
            for message in self._parse_lines(g):
                yield message
        finally:
            shutil.rmtree(tmp_dir)

    def read(self, config: TConfig, catalog: ConfiguredAirbyteCatalog, state: TState = None) -> Iterable[AirbyteMessage]:
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

            g = run_and_stream_lines(cmd)

            for message in self._parse_lines(g):
                yield message
        finally:
            shutil.rmtree(tmp_dir)

    def _image_id(self):
        return f"{self.image_name}:{self.image_tag}"

    @staticmethod
    def _write_file(obj, dst: PathLike[str]):
        write_json(dst, obj)
