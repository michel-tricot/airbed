from typing import Optional, TypeVar

from airbyte_cdk.models import ConfiguredAirbyteCatalog, Type

from airbyte_embed_cdk.catalog import full_refresh_streams, get_all_stream_names
from airbyte_embed_cdk.source_runner import SourceRunner
from airbyte_embed_cdk.tools import get_first_message


TConfig = TypeVar("TConfig")


def create_full_catalog(source: SourceRunner, config: TConfig, streams: Optional[str] = None) -> ConfiguredAirbyteCatalog:
    catalog_message = get_first_message(source.discover(config), Type.CATALOG)

    if not catalog_message:
        raise Exception("Can't retrieve catalog from source")

    catalog = catalog_message.catalog
    if not streams:
        streams = get_all_stream_names(catalog)

    return full_refresh_streams(catalog, streams)
