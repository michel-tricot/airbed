from typing import Optional, List

from airbyte_cdk.models import ConfiguredAirbyteCatalog, AirbyteCatalog, AirbyteStream, ConfiguredAirbyteStream, SyncMode

from airbyte_embed_cdk.tools.tools import get_first


def get_stream(catalog: AirbyteCatalog, stream_name: str) -> Optional[AirbyteStream]:
    return get_first(catalog.streams, lambda s: s.name == stream_name)


def to_configured_stream(stream: AirbyteStream,
                         sync_mode: SyncMode = SyncMode.full_refresh,
                         cursor_field: Optional[List[str]] = None,
                         primary_key: Optional[List[List[str]]] = None) -> ConfiguredAirbyteStream:
    return ConfiguredAirbyteStream.parse_obj({
        stream,
        sync_mode,
        cursor_field,
        primary_key
    })


def to_configured_catalog(configured_streams: List[ConfiguredAirbyteStream]):
    return ConfiguredAirbyteCatalog.parse_obj({
        "streams": configured_streams
    })


def full_refresh_streams(catalog: AirbyteCatalog, stream_names: List[str]) -> ConfiguredAirbyteCatalog:
    configured_streams = []

    for stream_name in stream_names:
        stream = get_stream(catalog, stream_name)
        configured_streams.append(to_configured_stream(stream))

    return to_configured_catalog(configured_streams)
