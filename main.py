import hashlib
import os

import requests
from requests import Response

"""1)Напишите скрипт, асинхронно, в 3 одновременных задачи, скачивающий содержимое
HEAD репозитория https://gitea.radium.group/radium/project-configuration во временную папку."""

"""2)После выполнения всех асинхронных задач скрипт должен посчитать sha256 хэши от каждого файла."""

"""3)Код должен проходить без замечаний проверку линтером wemake-python-styleguide. 
Конфигурация nitpick - https://gitea.radium.group/radium/project-configuration"""

"""4)Обязательно 100% покрытие тестами"""


ENDPOINT: str = 'https://gitea.radium.group/radium/project-configuration'
API_ENDPOIND = 'https://gitea.radium.group/api/v1/repos/radium/project-configuration/contents/'


def download_file(item: dict, path: str = '') -> None:
    """Скачивает файл по заданному пути"""
    file_url: str = f"{ENDPOINT}/raw/branch/master/{item.get('path')}"
    file: Response = requests.get(file_url)
    with open(f"{path}{item.get('name')}", 'wb') as f:
        f.write(file.content)


def get_all_files(data: dict, path: str = '') -> None:
    """Pекуpсивно ищет в ответе файлы и пеpедаёт на скачивание"""
    for item in data:
        if item.get('type') == 'file':
            download_file(item, path)
        else:
            path: str = item.get('path') + '/'
            temp_dir: str = ''.join((os.getcwd(), '/', path))
            if not os.path.exists(temp_dir):
                os.mkdir(temp_dir)
            response: Response = requests.get(API_ENDPOIND + path)
            get_all_files(response.json(), path=path)


def get_hash(filename: str) -> str:
    """Вычисление хэша одного файла"""
    hsh = hashlib.sha256()
    with open(filename, 'rb') as file:
        while True:
            chunk: bytes = file.read(4096)
            if not chunk:
                break
            hsh.update(chunk)
    return hsh.hexdigest()


def get_sha256_from_all_files() -> list[str]:
    """Вычисления хэша всех файлов в директории"""
    result: list = []
    for dirpath, _, filenames in os.walk('.'):
        for filename in filenames:
            filepath: str = os.path.join(dirpath, filename)
            filehash: str = get_hash(filepath)
            result.append(f"{filename}: {filehash}")
    return result


def main() -> None:
    """Главная функция"""
    response: Response = requests.get(API_ENDPOIND)
    data: dict = response.json()

    temp_dir: str = ''.join((os.getcwd(), '/downloads/'))
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)

    os.chdir(temp_dir)
    get_all_files(data)

    print(*get_sha256_from_all_files(), sep='\n')


if __name__ == '__main__':
    main()
