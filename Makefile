format-ruff:
	poetry run ruff --fix .

format-black:
	poetry run black .

lint-black:
	poetry run black . --check

lint-isort:
	poetry run isort . --check

lint-flake8:
	poetry run flake8

format: format-ruff format-black

lint: lint-black lint-isort lint-flake8

test:
	poetry run pytest
