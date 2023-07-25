import logging
from abc import ABC, abstractmethod

from airbed.platform.source_runner import Runner
from airbyte_cdk.models import AirbyteMessage, Type, AirbyteStateMessage, ConnectorSpecification, AirbyteRecordMessage, AirbyteCatalog, AirbyteLogMessage, AirbyteTraceMessage, AirbyteControlMessage, AirbyteConnectionStatus


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
        match message.type:
            case Type.RECORD:
                self.onRecord(message.record)
            case Type.STATE:
                self.onState(message.state)
            case Type.LOG:
                self.onLog(message.log)
            case Type.SPEC:
                self.onSpec(message.spec)
            case Type.CONNECTION_STATUS:
                self.onConnectionStatus(message.connectionStatus)
            case Type.CATALOG:
                self.onCatalog(message.catalog)
            case Type.TRACE:
                self.onTrace(message.trace)
            case Type.CONTROL:
                self.onControl(message.control)
            case _:
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
