install:
	poetry install

start:
	poetry run python main.py

lint:
	poetry run flake8 main.py
