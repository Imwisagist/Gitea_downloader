import asyncio
import hashlib
import os
import tempfile
from asyncio import Task

import aiohttp
from aiohttp import ClientResponse

"""1)Напишите скрипт, асинхронно, в 3 одновременных задачи, скачивающий 
содержимое HEAD репозитория 
https://gitea.radium.group/radium/project-configuration во временную папку."""

"""2)После выполнения всех асинхронных задач скрипт должен 
посчитать sha256 хэши от каждого файла."""

"""3)Код должен проходить без замечаний проверку линтером 
wemake-python-styleguide. Конфигурация nitpick - 
https://gitea.radium.group/radium/project-configuration"""

"""4)Обязательно 100% покрытие тестами"""

ENDPOINT: str = 'https://gitea.radium.group/radium/project-configuration'

API_ENDPOINT: str = """
https://gitea.radium.group/api/v1/repos/radium/project-configuration/contents/
"""


async def download_file(
        item: dict, session, sema, path: str = '') -> None:
    """Скачивает файл по заданному пути"""
    async with sema:
        file_url: str = f"{ENDPOINT}/raw/branch/master/{item.get('path')}"
        file: ClientResponse = await session.get(file_url)
        with open(f"{path}{item.get('name')}", 'wb') as f:
            f.write(await file.content.read())


async def download_files(data: dict, session, path: str = '') -> None:
    """Pекуpсивно ищет в ответе файлы и пеpедаёт на скачивание"""
    tasks: list[Task] = []
    for item in data:
        if item.get('type') == 'file':
            task: Task = asyncio.ensure_future(
                download_file(item, session, semaphore, path)
            )
            tasks.append(task)
        else:
            path: str = item.get('path') + '/'
            temp_dir: str = ''.join((os.getcwd(), '/', path))
            if not os.path.exists(temp_dir):
                os.mkdir(temp_dir)
            response: ClientResponse = await session.get(API_ENDPOINT + path)
            await download_files(await response.json(), session, path=path)
    await asyncio.gather(*tasks)


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


async def get_sha256_from_files() -> list[str]:
    """Вычисления хэша всех файлов в директории"""
    result: list[str] = []
    for dirpath, _, filenames in os.walk('.'):
        for filename in filenames:
            filepath: str = os.path.join(dirpath, filename)
            filehash: str = await get_hash(filepath)
            result.append(f"{filename}: {filehash}")
    return result


async def main() -> None:
    """Главная функция"""
    temp_dir: str = tempfile.mkdtemp()
    async with aiohttp.ClientSession() as session:
        response: ClientResponse = await session.get(API_ENDPOINT)
        data: dict = await response.json()
        os.chdir(temp_dir)
        await download_files(data, session)

    result: list[str] = await get_sha256_from_files()
    print(*result, sep='\n')


if __name__ == '__main__':
    semaphore = asyncio.Semaphore(3)
    asyncio.run(main())
