```

# Get started
poetry install

# Get started with integrations
poetry install -E llama-index
poetry install -E langchain
poetry install --all-extras

# Lint
poetry run black --check . &&
poetry run isort --check . &&
poetry run flake8

# Format
poetry run black . &&
poetry run isort .

# Tests
poetry run pytest

```