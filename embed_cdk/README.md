```
# Get started
poetry install

# Get started with integrations
poetry install -E llama-index
poetry install -E langchain
poetry install --all-extras

# Style
poetry run black . &&
poetry run isort . &&
poetry run flake8


```