import logging

from abc import ABC, abstractmethod

from airbyte_embed_cdk.platform.source_runner import SourceRunner
from airbyte_cdk.models import (
    AirbyteCatalog,
    AirbyteConnectionStatus,
    AirbyteControlMessage,
    AirbyteLogMessage,
    AirbyteMessage,
    AirbyteRecordMessage,
    AirbyteStateMessage,
    AirbyteTraceMessage,
    ConnectorSpecification,
    Type,
)


class MessageCollector(ABC):
    @abstractmethod
    def onMessage(self, message: AirbyteMessage):
        pass


class CompositeMessageCollector(MessageCollector):
    def __init__(self, *collectors: MessageCollector):
        self.collectors = list(collectors)

    def onMessage(self, message: AirbyteMessage):
        for collector in self.collectors:
            collector.onMessage(message)


class LoggingMessageCollector(MessageCollector):
    def __init__(self, logger: logging.Logger, level: int):
        self.logger = logger
        self.level = level

    def onMessage(self, message: AirbyteMessage):
        self.logger.log(self.level, message)


class DispatchMessageCollector(MessageCollector):
    def onMessage(self, message: AirbyteMessage):
        if message.type == Type.RECORD:
            self.onRecord(message.record)
        elif message.type == Type.STATE:
            self.onState(message.state)
        elif message.type == Type.LOG:
            self.onLog(message.log)
        elif message.type == Type.SPEC:
            self.onSpec(message.spec)
        elif message.type == Type.CONNECTION_STATUS:
            self.onConnectionStatus(message.connectionStatus)
        elif message.type == Type.CATALOG:
            self.onCatalog(message.catalog)
        elif message.type == Type.TRACE:
            self.onTrace(message.trace)
        elif message.type == Type.CONTROL:
            self.onControl(message.control)
        else:
            self.onUnknown(message)

    def onRecord(self, record: AirbyteRecordMessage):
        pass

    def onState(self, state: AirbyteStateMessage):
        pass

    def onLog(self, log: AirbyteLogMessage):
        pass

    def onSpec(self, spec: ConnectorSpecification):
        pass

    def onConnectionStatus(self, connection_status: AirbyteConnectionStatus):
        pass

    def onCatalog(self, catalog: AirbyteCatalog):
        pass

    def onTrace(self, trace: AirbyteTraceMessage):
        pass

    def onControl(self, control: AirbyteControlMessage):
        pass

    def onUnknown(self, message: AirbyteMessage):
        pass


class Worker(ABC):
    def __init__(self, source_runner: Runner):
        self.source_runner = source_runner

    def start(self, collector: MessageCollector):
        for message in self.source_runner.read():
            collector.onMessage(message)
