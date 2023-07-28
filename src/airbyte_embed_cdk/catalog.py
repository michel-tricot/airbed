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


def get_all_stream_names(catalog: AirbyteCatalog) -> List[str]:
    return [stream.name for stream in catalog.streams]


def to_configured_stream(
    stream: AirbyteStream,
    sync_mode: SyncMode = SyncMode.full_refresh,
    destination_sync_mode: DestinationSyncMode = DestinationSyncMode.overwrite,
    cursor_field: Optional[List[str]] = None,
    primary_key: Optional[List[List[str]]] = None,
) -> ConfiguredAirbyteStream:
    return ConfiguredAirbyteStream.parse_obj(
        {
            "stream": stream,
            "sync_mode": sync_mode,
            "destination_sync_mode": destination_sync_mode,
            "cursor_field": cursor_field,
            "primary_key": primary_key,
        }
    )


def to_configured_catalog(configured_streams: List[ConfiguredAirbyteStream]):
    return ConfiguredAirbyteCatalog.parse_obj({"streams": configured_streams})


def full_refresh_streams(catalog: AirbyteCatalog, stream_names: List[str]) -> ConfiguredAirbyteCatalog:
    configured_streams = []

    for stream_name in stream_names:
        stream = get_stream(catalog, stream_name)
        configured_streams.append(to_configured_stream(stream))

    return to_configured_catalog(configured_streams)


def create_full_catalog(source: SourceRunner, config: TConfig, streams: Optional[str] = None) -> ConfiguredAirbyteCatalog:
    catalog_message = get_first_message(source.discover(config), Type.CATALOG)

    if not catalog_message:
        raise Exception("Can't retrieve catalog from source")

    catalog = catalog_message.catalog
    if not streams:
        streams = get_all_stream_names(catalog)

    return full_refresh_streams(catalog, streams)
