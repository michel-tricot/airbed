format-ruff:
	poetry run ruff --fix .

format-black:
	poetry run black .

lint-black:
	poetry run black . --check

lint-ruff:
	poetry run ruff .

format: format-ruff format-black

lint: lint-ruff lint-black

test:
	poetry run pytest
