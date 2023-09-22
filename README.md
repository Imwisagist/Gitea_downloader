# Gitea_downloader
[![Actions Status](https://github.com/Imwisagist/Radium/actions/workflows/radium_ci.yml/badge.svg)](https://github.com/Imwisagist/Radium/actions/workflows/radium_ci.yml)

Asynchronous script that downloads the HEAD contents of the repository
https://gitea.radium.group/radium/project-configuration in a temporary folder
of 3 streams. After performing all asynchronous tasks, the script counts sha256
hashes from each downloaded file.

The code passes the wemake-python-style guide linter check without any comments.
Nitpick configuration - https://gitea.radium.group/radium/project-configuration

Tests are written for the script on Pytest

### Clone the repository and enter:
```
git clone https://github.com/Imwisagist/Radium.git && cd Radium/
```
### Install poetry:
```
pip install poetry
```
##### Installing dependencies:
```
poetry install
```
##### Running the script:
```
poetry run python main.py
```
##### Checking by linter:
```
poetry run flake8 main.py
```
##### Running tests:
```
poetry run pytest -vv
```
##### Show test coverage:
```
poetry run pytest --cov-report term-missing --cov=gitea_downloader --cov-report xml
```
