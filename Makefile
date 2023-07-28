format-black:
	poetry run black .

format-isort:
	poetry run isort .

lint-black:
	poetry run black . --check

lint-isort:
	poetry run isort . --check

lint-flake8:
	poetry run flake

format: format-black format-isort

lint: lint-black lint-isort lint-flake8
