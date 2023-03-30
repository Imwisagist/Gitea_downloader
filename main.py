import asyncio
import hashlib
import os

import aiohttp
from aiohttp import ClientResponse

"""1)Напишите скрипт, асинхронно, в 3 одновременных задачи, скачивающий содержимое
HEAD репозитория https://gitea.radium.group/radium/project-configuration во временную папку."""

"""2)После выполнения всех асинхронных задач скрипт должен посчитать sha256 хэши от каждого файла."""

"""3)Код должен проходить без замечаний проверку линтером wemake-python-styleguide. 
Конфигурация nitpick - https://gitea.radium.group/radium/project-configuration"""

"""4)Обязательно 100% покрытие тестами"""


ENDPOINT: str = 'https://gitea.radium.group/radium/project-configuration'
API_ENDPOIND = 'https://gitea.radium.group/api/v1/repos/radium/project-configuration/contents/'


async def download_file(item: dict, session, path: str = '') -> None:
    """Скачивает файл по заданному пути"""
    file_url: str = f"{ENDPOINT}/raw/branch/master/{item.get('path')}"
    file: ClientResponse = await session.get(file_url)
    with open(f"{path}{item.get('name')}", 'wb') as f:
        f.write(await file.content.read())


async def get_all_files(data: dict, session, path: str = '') -> None:
    """Pекуpсивно ищет в ответе файлы и пеpедаёт на скачивание"""
    for item in data:
        if item.get('type') == 'file':
            await download_file(item, session, path)
        else:
            path: str = item.get('path') + '/'
            temp_dir: str = ''.join((os.getcwd(), '/', path))
            if not os.path.exists(temp_dir):
                os.mkdir(temp_dir)
            response: ClientResponse = await session.get(API_ENDPOIND + path)
            await get_all_files(await response.json(), session, path=path)


async def get_hash(filename: str) -> str:
    """Вычисление хэша одного файла"""
    hsh = hashlib.sha256()
    with open(filename, 'rb') as file:
        while True:
            chunk: bytes = file.read(4096)
            if not chunk:
                break
            hsh.update(chunk)
    return hsh.hexdigest()


async def get_sha256_from_all_files() -> list[str]:
    """Вычисления хэша всех файлов в директории"""
    result: list = []
    for dirpath, _, filenames in os.walk('.'):
        for filename in filenames:
            filepath: str = os.path.join(dirpath, filename)
            filehash: str = await get_hash(filepath)
            result.append(f"{filename}: {filehash}")
    return result


async def main() -> None:
    """Главная функция"""
    async with aiohttp.ClientSession() as session:
        response: ClientResponse = await session.get(API_ENDPOIND)
        data: dict = await response.json()

        temp_dir: str = ''.join((os.getcwd(), '/downloads/'))
        if not os.path.exists(temp_dir):
            os.mkdir(temp_dir)

        os.chdir(temp_dir)
        await get_all_files(data, session)
        result: list[str] = await get_sha256_from_all_files()
        print(*result, sep='\n')


if __name__ == '__main__':
    asyncio.run(main())
