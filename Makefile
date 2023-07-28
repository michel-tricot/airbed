format-autoflake:
	poetry run pautoflake .

format-black:
	poetry run black .

format-isort:
	poetry run isort .

lint-black:
	poetry run black . --check

lint-isort:
	poetry run isort . --check

lint-flake8:
	poetry run flake8

format: format-autoflake format-black format-isort

lint: lint-black lint-isort lint-flake8
