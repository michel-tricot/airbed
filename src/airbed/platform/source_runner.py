import logging
import os.path
import shutil
import subprocess
import tempfile

from abc import ABC, abstractmethod
from distutils import file_util
from pathlib import Path
from typing import Generator, Iterable

from airbyte_cdk.models import AirbyteMessage, Type

from airbed.tools.processes import run_and_stream_lines
from airbed.tools.tools import parse_json


class SourceRunner(ABC):
    @abstractmethod
    def spec(self) -> Iterable[AirbyteMessage]:
        pass

    @abstractmethod
    def check(self) -> Iterable[AirbyteMessage]:
        pass

    @abstractmethod
    def discover(self) -> Iterable[AirbyteMessage]:
        pass

    @abstractmethod
    def read(self) -> Iterable[AirbyteMessage]:
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


class ContainerSourceRunner(SourceRunner):

    INPUT_FILES_PATH = "/input_files"

    def __init__(self, image_name: str, image_tag: str, container_launcher: str = "docker"):
        self.image_name = image_name
        self.image_tag = image_tag
        self.container_launcher = container_launcher

        subprocess.check_output(
            [
                self.container_launcher,
                "pull",
                self._image_id(),
            ]
        )

    def spec(self) -> Iterable[AirbyteMessage]:
        g = run_and_stream_lines([self.container_launcher, "run", "--rm", self._image_id(), "spec"])
        return self._parse_lines(g)

    def check(self, config_file) -> Iterable[AirbyteMessage]:
        tmp_dir = tempfile.mkdtemp()
        try:
            self._copy_file(config_file, tmp_dir, "config.json")

            g = run_and_stream_lines(
                [
                    self.container_launcher,
                    "run",
                    "--rm",
                    "-v",
                    f"{tmp_dir}:{self.INPUT_FILES_PATH}",
                    self._image_id(),
                    "check",
                    "--config",
                    os.path.join(self.INPUT_FILES_PATH, "config.json"),
                ]
            )
            for message in self._parse_lines(g):
                yield message
        finally:
            shutil.rmtree(tmp_dir)

    def discover(self, config_file) -> Iterable[AirbyteMessage]:
        tmp_dir = tempfile.mkdtemp()
        try:
            self._copy_file(config_file, tmp_dir, "config.json")

            g = run_and_stream_lines(
                [
                    self.container_launcher,
                    "run",
                    "--rm",
                    "-v",
                    f"{tmp_dir}:{self.INPUT_FILES_PATH}",
                    self._image_id(),
                    "discover",
                    "--config",
                    os.path.join(self.INPUT_FILES_PATH, "config.json"),
                ]
            )
            for message in self._parse_lines(g):
                yield message
        finally:
            shutil.rmtree(tmp_dir)

    def read(self, config_file, catalog_file, state_file=None) -> Iterable[AirbyteMessage]:
        tmp_dir = tempfile.mkdtemp()
        try:
            self._copy_file(config_file, tmp_dir, "config.json")
            self._copy_file(catalog_file, tmp_dir, "catalog.json")

            cmd = [
                self.container_launcher,
                "run",
                "--rm",
                "-v",
                f"{tmp_dir}:{self.INPUT_FILES_PATH}",
                self._image_id(),
                "read",
                "--config",
                os.path.join(self.INPUT_FILES_PATH, "config.json"),
                "--catalog",
                os.path.join(self.INPUT_FILES_PATH, "catalog.json"),
            ]

            if state_file:
                self._copy_file(state_file, tmp_dir, "state.json")
                state_args = ["--state", os.path.join(self.INPUT_FILES_PATH, "state.json")]
                cmd.extend(state_args)

            g = run_and_stream_lines(cmd)

            for message in self._parse_lines(g):
                yield message
        finally:
            shutil.rmtree(tmp_dir)

    def _image_id(self):
        return f"{self.image_name}:{self.image_tag}"

    def _copy_file(self, file, dst_dir, name):
        copied_file = os.path.join(dst_dir, name)
        shutil.copyfile(file, copied_file, follow_symlinks=True)


if __name__ == "__main__":
    source_runner = ContainerSourceRunner("airbyte/source-pokeapi", "0.1.5-dev.819dd97d48")
    source_runner.spec()
