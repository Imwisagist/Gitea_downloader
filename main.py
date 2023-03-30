"""Тестовая задача для Radium."""
import asyncio
import hashlib
import os
import sys
import tempfile

import aiohttp

ENDPOINT: str = 'https://gitea.radium.group/radium/project-configuration'

API_ENDPOINT: str = """
https://gitea.radium.group/api/v1/repos/radium/project-configuration/contents/
"""

CHUNK_SIZE, STREAMS_COUNT = 4096, 3


async def download_file(
    file_data: dict, session, sema: asyncio.Semaphore, path: str = '',
):
    """Скачивает файл по заданному пути."""
    async with sema:
        file_url: str = '{0}/raw/branch/master/{1}'.format(
            ENDPOINT, file_data.get('path'),
        )
        response_raw_file = await session.get(file_url)
        with open(
            '{0}{1}'.format(path, file_data.get('name')),
            'wb',
        ) as binary_write_file:
            binary_write_file.write(await response_raw_file.content.read())


async def download_files(
    catalog: dict, session, tasks, path: str = '',
) -> None:
    """Pекуpсивно ищет в ответе файлы и пеpедаёт на скачивание."""
    for file_or_dir in catalog:
        if file_or_dir.get('type') == 'file':
            task = asyncio.ensure_future(
                download_file(
                    file_or_dir, session, semaphore, path,
                ),
            )
            tasks.append(task)
        else:
            path: str = '{0}/'.format(file_or_dir.get('path'))
            temp_dir: str = ''.join((os.getcwd(), '/', path))
            if not os.path.exists(temp_dir):
                os.mkdir(temp_dir)
            response = await session.get(API_ENDPOINT + path)
            await download_files(
                await response.json(), session, tasks, path=path,
            )


async def get_hash(filename: str) -> str:
    """Вычисление хэша одного файла."""
    hsh = hashlib.sha256()
    with open(filename, 'rb') as binary_read_file:
        while True:
            chunk: bytes = binary_read_file.read(CHUNK_SIZE)
            if not chunk:
                break
            hsh.update(chunk)
    return hsh.hexdigest()


async def print_sha256_from_files() -> None:
    """Вычисления хэша всех файлов в директории."""
    for dirpath, _, filenames in os.walk('.'):
        for filename in filenames:
            filepath: str = os.path.join(dirpath, filename)
            filehash: str = await get_hash(filepath)
            sys.stdout.write('{0}: {1}\n'.format(filename, filehash))


async def main() -> None:
    """Главная функция."""
    temp_dir: str = tempfile.mkdtemp()
    async with aiohttp.ClientSession() as session:
        response = await session.get(API_ENDPOINT)
        response_json: dict = await response.json()
        os.chdir(temp_dir)
        tasks: list = []
        await download_files(response_json, session, tasks)
        await asyncio.gather(*tasks)
    await print_sha256_from_files()


if __name__ == '__main__':
    semaphore: asyncio.Semaphore = asyncio.Semaphore(STREAMS_COUNT)
    asyncio.run(main())
