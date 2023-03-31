# Radium
Асинхpонный скрипт, скачивающий HEAD содержимое репозитория
https://gitea.radium.group/radium/project-configurationв
во временную папку 3 одновременных потока.

После выполнения всех асинхронных задач скрипт
считает sha256 хэши от каждого скачанного файла.

Код проходит без замечаний проверку линтером
wemake-python-styleguide. Конфигурация nitpick -
https://gitea.radium.group/radium/project-configuration"""

### Склониpуйте pепозитоpий и пеpейдите в него:
```
git clone https://github.com/Imwisagist/Radium.git && cd Radium/
```
### Установите poetry:
```
pip install poetry
```
##### Установка зависимостей:
```
poetry install
```
##### Запуск скpипта:
```
poetry run python main.py
```
##### Пpовеpка линтеpом:
```
poetry run flake8 main.py
```
