format-ruff:
	poetry run ruff --fix .

format-black:
	poetry run black .

lint-black:
	poetry run black . --check

lint-ruff:
	poetry run ruff .

lint-mypy:
	poetry run mypy src tests

format: format-ruff format-black

lint: lint-mypy lint-ruff lint-black

test:
	poetry run pytest
