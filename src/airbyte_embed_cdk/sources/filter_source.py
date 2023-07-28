from typing import Callable, Iterable

from airbyte_cdk.models import Type
from airbyte_protocol.models import AirbyteMessage

from airbyte_embed_cdk.models.source import SourceRunner
from airbyte_embed_cdk.sources.decorator_source import DecoratorSourceRunner

Predicate = Callable[[AirbyteMessage], bool]


class FilterSourceRunner(DecoratorSourceRunner):
    def __init__(self, decorated: SourceRunner, predicate: Predicate = lambda m: m == Type.LOG) -> None:
        super().__init__(decorated)
        self.predicate = predicate

    def _process(self, messages: Iterable[AirbyteMessage]) -> Iterable[AirbyteMessage]:
        for message in messages:
            if not self.predicate(message):
                yield message
