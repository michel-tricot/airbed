[![build](https://github.com/michel-tricot/airbed/actions/workflows/build.yaml/badge.svg)](https://github.com/michel-tricot/airbed/actions/workflows/build.yaml)

# How to use
## Langchain

```python
# Container based
from airbyte_embed_cdk.integrations.langchain import container_airbyte_langchain_loader


FakerLoader = container_airbyte_langchain_loader("airbyte/source-faker", "4.0.0")

config = ...
reader = FakerLoader(config=config, stream="users")
data = reader.load()

# Python package based
from airbyte_embed_cdk.integrations.langchain import cdk_airbyte_container_langchain_reader
from source_pokeapi import SourcePokeapi

CdkPokeapiReader = cdk_airbyte_container_langchain_reader(SourcePokeapi)

config = ...
reader = CdkPokeapiReader(config=config, stream="pokemon")
data = reader.load()
```

## LLamaIndex

```python
from airbyte_embed_cdk.integrations.llama_index import container_airbyte_llamaindex_reader

FakerReader = container_airbyte_llamaindex_reader("airbyte/source-faker", "4.0.0")

config = ...
reader = FakerReader(config=config)
data = reader.load_data("users")

# Python package based
from airbyte_embed_cdk.integrations.llama_index import cdk_airbyte_container_llamaindex_reader
from source_pokeapi import SourcePokeapi

CdkPokeapiLoader = cdk_airbyte_container_llamaindex_reader(SourcePokeapi)

config = ...
reader = CdkPokeapiLoader(config=config, stream="pokemon")
data = reader.load()
```

# Current issues
1. `pydantic` version not compatible with langchain had to go through a hack (see `hack_types.py`)
2. doesn't work with python > 3.9 because the cdk/model lib is not compatible

# Ideas
1. Generate:
   1. Automatically generate docs and push it on both hubs (with a fake config generated from spec?)
   2. Could we also generate a config object from spec for each connector?
2. Can we make snowflake work that library? The building blocks are probably the same

# Development
```shell
# Get started
poetry install --all-extras

# Tests
make test
```