# How to use
## Langchain

```python
from airbyte_embed_cdk.integrations.langchain import airbyte_langchain_loader

FakerLoader = airbyte_langchain_loader("airbyte/source-faker", "4.0.0")

config = ...
reader = FakerLoader(config=config, streams=["users"])
data = reader.load()
```

## LLamaIndex

```python
from airbyte_embed_cdk.integrations.llama_index import airbyte_llamaindex_reader

FakerReader = airbyte_llamaindex_reader("airbyte/source-faker", "4.0.0")

config = ...
reader = FakerReader(config=config)
data = reader.load_data(["users"])
```

# Current issues
1. `pydantic` version not compatible with langchain had to go through a hack (see `hack_types.py`)
2. doesn't work with python > 3.9 because the cdk/model lib is not compatible

# Ideas
1. Right now it launches docker. What if we have a published version of each python connector? `ModuleSource`
2. Generate:
   1. Automatically generate docs and push it on both hubs (with a fake config generated from spec?)
   2. Could we also generate a config object from spec for each connector?
3. Can we make snowflake work that library? The building blocks are probably the same

# Development
```
# Get started
poetry install --all-extras

# Tests
make test
```