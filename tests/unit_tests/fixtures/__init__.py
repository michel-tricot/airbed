from pathlib import Path

from airbyte_embed_cdk.tools import read_json

data_path = Path(__file__).parent / "data"


class Fixtures:
    CONFIG = read_json(data_path / "config.json")
    CATALOG = read_json(data_path / "catalog.json")
    CONFIGURED_CATALOG = read_json(data_path / "configured_catalog.json")
    STATE = read_json(data_path / "state.json")
    BAD_CONFIGURED_CATALOG = read_json(data_path / "bad_configured_catalog.json")
