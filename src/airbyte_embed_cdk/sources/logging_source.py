import logging
from typing import Iterable, List, Optional

from airbyte_cdk.models import Level, Type
from airbyte_protocol.models import AirbyteLogMessage, AirbyteMessage

from airbyte_embed_cdk.models.source import SourceRunner
from airbyte_embed_cdk.sources.decorator_source import DecoratorSourceRunner


class LoggingSourceRunner(DecoratorSourceRunner):
    def __init__(self, decorated: SourceRunner, logged_types: Optional[List[Type]] = None) -> None:
        super().__init__(decorated)
        self.logged_types = logged_types or [Type.LOG]

    def _process(self, messages: Iterable[AirbyteMessage]) -> Iterable[AirbyteMessage]:
        for message in messages:
            if message.type in self.logged_types:
                if message.type == Type.LOG:
                    level = LoggingSourceRunner._convert_level(message.log.level)
                    msg = LoggingSourceRunner._convert_message(message.log)
                    logging.log(level, msg)
                else:
                    logging.info(message.json())
            yield message

    LEVEL_MAPPING = {
        Level.FATAL: logging.FATAL,
        Level.ERROR: logging.ERROR,
        Level.WARN: logging.WARNING,
        Level.INFO: logging.INFO,
        Level.DEBUG: logging.DEBUG,
        Level.TRACE: logging.DEBUG,
    }

    @staticmethod
    def _convert_level(level: Level) -> int:
        return LoggingSourceRunner.LEVEL_MAPPING.get(level, logging.NOTSET)

    @staticmethod
    def _convert_message(log_message: AirbyteLogMessage) -> str:
        stacktrace = ""
        if log_message.stack_trace:
            stacktrace = f"\n\n{log_message.stack_trace}"
        return f"{log_message.message}{stacktrace}"
