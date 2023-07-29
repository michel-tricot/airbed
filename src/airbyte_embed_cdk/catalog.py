from typing import List, Optional

from airbyte_cdk.models import (
    AirbyteCatalog,
    AirbyteStream,
    ConfiguredAirbyteCatalog,
    ConfiguredAirbyteStream,
    DestinationSyncMode,
    SyncMode,
    Type,
)

from airbyte_embed_cdk.models.source import SourceRunner, TConfig
from airbyte_embed_cdk.tools import get_first, get_first_message


def get_stream(catalog: AirbyteCatalog, stream_name: str) -> Optional[AirbyteStream]:
    return get_first(catalog.streams, lambda s: s.name == stream_name)


def get_stream_names(catalog: AirbyteCatalog) -> List[str]:
    return [stream.name for stream in catalog.streams]


def to_configured_stream(
    stream: AirbyteStream,
    sync_mode: SyncMode = SyncMode.full_refresh,
    destination_sync_mode: DestinationSyncMode = DestinationSyncMode.append,
    cursor_field: Optional[List[str]] = None,
    primary_key: Optional[List[List[str]]] = None,
) -> ConfiguredAirbyteStream:
    return ConfiguredAirbyteStream(
        stream=stream, sync_mode=sync_mode, destination_sync_mode=destination_sync_mode, cursor_field=cursor_field, primary_key=primary_key
    )


def to_configured_catalog(configured_streams: List[ConfiguredAirbyteStream]) -> ConfiguredAirbyteCatalog:
    return ConfiguredAirbyteCatalog(streams=configured_streams)


def create_full_refresh_catalog(stream_names: List[str], catalog: AirbyteCatalog) -> ConfiguredAirbyteCatalog:
    configured_streams = []

    for stream_name in stream_names:
        stream = get_stream(catalog, stream_name)
        configured_streams.append(to_configured_stream(stream))

    return to_configured_catalog(configured_streams)


def retrieve_catalog(source: SourceRunner, config: TConfig) -> AirbyteCatalog:
    catalog_message = get_first_message(source.discover(config), Type.CATALOG)

    if not catalog_message or not catalog_message.catalog:
        raise Exception("Can't retrieve catalog from source")

    return catalog_message.catalog
