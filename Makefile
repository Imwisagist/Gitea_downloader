install:
	poetry install

start:
	poetry run python main.py

linter:
	poetry run flake8 main.py

tests:
	poetry run pytest -vv

coverage:
	poetry run pytest --cov-report term-missing --cov=gitea_downloader --cov-report xml
