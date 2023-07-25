from abc import ABC, abstractmethod
from typing import Iterable

from airbyte_cdk.models import AirbyteMessage


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


class ContainerSourceRunner(SourceRunner):
    def spec(self) -> Iterable[AirbyteMessage]:
        pass

    def check(self) -> Iterable[AirbyteMessage]:
        pass

    def discover(self) -> Iterable[AirbyteMessage]:
        pass

    def read(self) -> Iterable[AirbyteMessage]:
        pass

    def __init__(self, image_name: str, tag: str, ):
        pass
