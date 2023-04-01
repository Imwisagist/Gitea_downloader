"""Тестовая задача для Radium.

Скpипт в 3 потока скачивает содеpжимое удалённого gitea pепозитоpия,
сохpаняет во вpеменную папку и считает хэш каждого файла.
"""
import asyncio
import hashlib
import os
import tempfile
from pathlib import Path

import aiohttp

import config as cfg


async def get_response(
    session: aiohttp.ClientSession, url: str,
) -> aiohttp.ClientResponse:
    """Запрашивает данные с заданного адреса методом GET."""
    response: aiohttp.ClientResponse = await session.get(url)
    if response.status != cfg.HTTP_OK:
        raise ConnectionError(
            'Не успешный код ответа: {0}'.format(response.status),
        )
    return response


async def download_file(
    file_data: dict, session: aiohttp.ClientSession, path: str = '',
) -> None:
    """Скачивает файл по заданному пути."""
    async with cfg.SEMAPHORE:
        file_url: str = '{0}/raw/branch/master/{1}'.format(
            cfg.ENDPOINT, file_data.get('path'),
        )
        response_raw_file = await get_response(session, file_url)
        try:
            with open(
                '{0}{1}'.format(path, file_data.get('name')), 'wb',
            ) as binary_write_file:
                binary_write_file.write(await response_raw_file.content.read())
        except Exception as error:
            raise OSError('Не удалось записать файл, ошибка:{0}'.format(error))


async def parse_catalog(
    catalog: dict, session: aiohttp.ClientSession, tasks: list, path: str = '',
) -> None:
    """Паpсит каталоги на наличие файлов, файлы пеpедаёт на скачивание."""
    for file_or_dir in catalog:
        if not file_or_dir.get('type'):
            raise KeyError('Не валидный ответ, отсутствует ключ type')
        if file_or_dir.get('type') == 'file':
            task = asyncio.ensure_future(
                download_file(file_or_dir, session, path),
            )
            tasks.append(task)
        elif file_or_dir.get('type') == 'dir':
            path: str = '{0}/'.format(file_or_dir.get('path'))
            os.mkdir(''.join((os.getcwd(), '/', path)))
            new_response = await get_response(
                session, cfg.API_ENDPOINT + path,
            )
            await parse_catalog(
                await new_response.json(), session, tasks, path,
            )


async def download_files() -> None:
    """Cоздаёт сессию и скачивает все файлы."""
    async with aiohttp.ClientSession() as session:
        response = await get_response(session, cfg.API_ENDPOINT)
        response_json: dict = await response.json()
        tasks: list = []
        await parse_catalog(response_json, session, tasks)
        await asyncio.gather(*tasks)


async def get_hash(filename: str | Path) -> str:
    """Вычисляет хэш для одного файла и пишет в логер."""
    hsh = hashlib.sha256()
    try:
        with open(filename, 'rb') as binary_read_file:
            while True:
                chunk: bytes = binary_read_file.read(cfg.CHUNK_SIZE)
                if not chunk:
                    break
                hsh.update(chunk)
            return hsh.hexdigest()
    except FileNotFoundError as error:
        raise FileNotFoundError('Файл не найден', error)


async def print_sha256_from_files() -> None:
    """Передаёт все файлы на вычисление хэша."""
    for dirpath, _, filenames in os.walk('.'):
        for filename in filenames:
            filepath: str = os.path.join(dirpath, filename)
            logger.info('Хэш файла {0}: {1}'.format(
                filepath[2:], await get_hash(filepath),
            ))


async def main() -> None:
    """Главная функция."""
    logger.info('Скачивание файлов..')
    with tempfile.TemporaryDirectory() as temp_dir:
        old_cwd: str = os.getcwd()
        os.chdir(temp_dir)
        await download_files()
        logger.info('Вычисление хэша...')
        await print_sha256_from_files()
        os.chdir(old_cwd)


if __name__ == '__main__':
    logger = cfg.get_logger('gitea_downloader')
    asyncio.run(main())
