"""Тестовая задача для Radium."""
import asyncio
import hashlib
import os
import shutil
import sys
import tempfile

import aiohttp

ENDPOINT: str = 'https://gitea.radium.group/radium/project-configuration'
API_ENDPOINT: str = ('https://gitea.radium.group/api/v1/'
                     'repos/radium/project-configuration/contents/')
CHUNK_SIZE, STREAMS_COUNT, HTTP_OK = 4096, 3, 200
SEMAPHORE: asyncio.Semaphore = asyncio.Semaphore(STREAMS_COUNT)


async def get_response(
    session: aiohttp.ClientSession, url: str,
) -> aiohttp.ClientResponse:
    """Запрашивает данные с заданного адреса методом GET."""
    response: aiohttp.ClientResponse = await session.get(url)
    if response.status != HTTP_OK:
        raise ConnectionError(
            'Не успешный код ответа: {0}'.format(response.status),
        )
    return response


async def download_file(
    file_data: dict, session: aiohttp.ClientSession, path: str = '',
) -> None:
    """Скачивает файл по заданному пути."""
    async with SEMAPHORE:
        file_url: str = '{0}/raw/branch/master/{1}'.format(
            ENDPOINT, file_data.get('path'),
        )
        response_raw_file = await get_response(session, file_url)
        try:
            with open(
                '{0}{1}'.format(path, file_data.get('name')),
                'wb',
            ) as binary_write_file:
                binary_write_file.write(await response_raw_file.content.read())
        except Exception as error:
            raise OSError('Не удалось записать файл, ошибка:{0}'.format(error))


async def download_files(
    catalog: dict, session: aiohttp.ClientSession, tasks, path: str = '',
) -> None:
    """Pекуpсивно ищет в ответе файлы и пеpедаёт на скачивание."""
    for file_or_dir in catalog:
        if not file_or_dir.get('type'):
            raise KeyError('Не валидный ответ, отсутствует ключ type')
        if file_or_dir.get('type') == 'file':
            task = asyncio.ensure_future(
                download_file(file_or_dir, session, path),
            )
            tasks.append(task)
        else:
            path: str = '{0}/'.format(file_or_dir.get('path'))
            tmp_dir: str = ''.join((os.getcwd(), '/', path))
            if not os.path.exists(tmp_dir):
                os.mkdir(tmp_dir)
            response = await get_response(session, API_ENDPOINT + path)
            await download_files(
                await response.json(), session, tasks, path=path,
            )


def get_hash(filename: str) -> str:
    """Вычисление хэша одного файла."""
    hsh = hashlib.sha256()
    try:
        with open(filename, 'rb') as binary_read_file:
            while True:
                chunk: bytes = binary_read_file.read(CHUNK_SIZE)
                if not chunk:
                    break
                hsh.update(chunk)
    except FileNotFoundError as error:
        raise FileNotFoundError('Файл не найден', error)
    return hsh.hexdigest()


def get_sha256_from_files() -> list[str]:
    """Вычисления хэша всех файлов в директории."""
    sha256: list[str] = []
    for dirpath, _, filenames in os.walk('.'):
        for filename in filenames:
            filepath: str = os.path.join(dirpath, filename)
            filehash: str = get_hash(filepath)
            sha256.append('{0}: {1}\n'.format(filename, filehash))
    return sha256


async def main(tmp_dir: str) -> None:
    """Главная функция."""
    async with aiohttp.ClientSession() as session:
        response = await get_response(session, API_ENDPOINT)
        response_json: dict = await response.json()
        os.chdir(tmp_dir)
        tasks: list = []
        await download_files(response_json, session, tasks)
        await asyncio.gather(*tasks)
    sha256_array: list[str] = get_sha256_from_files()
    for sha256 in sha256_array:
        sys.stdout.write(sha256)


if __name__ == '__main__':
    temp_dir: str = tempfile.mkdtemp()
    asyncio.run(main(temp_dir))
    shutil.rmtree(temp_dir, ignore_errors=True)
