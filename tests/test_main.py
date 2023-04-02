"""Тесты для главного модуля."""
import os
from pathlib import WindowsPath

import pytest
from aiohttp import ClientResponse

from main import (
    download_file, get_response, download_files, parse_catalog,
    print_downloaded_files_hash, get_hash, main,
)
from tests.constants import REAL_FILE, FAKE_FILE_1, FAKE_DIR, EXPECTED_HASH


class TestsDownload:
    @pytest.mark.asyncio()
    async def test_download_files_works(self, tmp_path: callable) -> None:
        await download_files(str(tmp_path))
        assert len(os.listdir(tmp_path)) == 3

    @pytest.mark.asyncio()
    async def test_get_not_successful_response_status_code(self, real_session: callable) -> None:
        with pytest.raises(ConnectionError):
            await get_response(real_session, 'https://ya.ru/404')

    @pytest.mark.asyncio()
    async def test_get_response_works(self, real_session: callable) -> None:
        response: ClientResponse = await get_response(real_session, 'https://ya.ru/')
        assert response.status == 200

    @pytest.mark.asyncio()
    async def test_download_file(self, real_session: callable, tmp_path: callable) -> None:
        await download_file(REAL_FILE, real_session, str(tmp_path) + '/')
        assert (tmp_path / REAL_FILE['path']).exists()

    @pytest.mark.asyncio()
    async def test_parse_catalog_create_task(self, fake_session: callable, tmp_path: callable) -> None:
        tasks: list = []
        await parse_catalog([REAL_FILE], fake_session, tasks, str(tmp_path))
        assert len(tasks) == 1

    @pytest.mark.asyncio()
    async def test_parse_catalog_fake_file_call_raise(self, fake_session: callable, tmp_path: callable) -> None:
        with pytest.raises(KeyError):
            await parse_catalog([FAKE_FILE_1], fake_session, [], str(tmp_path))

    @pytest.mark.asyncio()
    async def test_parse_catalog_create_dir(self, real_session: callable, tmp_path: callable) -> None:
        await parse_catalog([FAKE_DIR], real_session, [], str(tmp_path))
        assert len(os.listdir(tmp_path)) == 1

    @pytest.mark.asyncio()
    async def test_download_files_fake_path_call_raise(self) -> None:
        with pytest.raises(NotADirectoryError):
            await download_files('GO://gym')


class TestsHash:
    @pytest.mark.asyncio()
    async def test_correct_calculate_hashes(self, temp_file: callable) -> None:
        assert EXPECTED_HASH == await get_hash(temp_file), "Хэш не совпадает"

    @pytest.mark.asyncio()
    async def test_get_hash_fake_path_call_raise(self) -> None:
        with pytest.raises(FileNotFoundError):
            await get_hash('G://file.gym')

    @pytest.mark.asyncio()
    async def test_print_sha256_from_files(self, capsys: callable, temp_file: callable) -> None:
        file: WindowsPath = temp_file
        await print_downloaded_files_hash(str(file.parent))
        assert 'Хэш файла test1.txt' in capsys.readouterr().out

    @pytest.mark.asyncio()
    async def test_print_hash_fake_path_call_raise(self) -> None:
        with pytest.raises(NotADirectoryError):
            await print_downloaded_files_hash('GO://gym')


class TestsMain:
    @pytest.mark.asyncio()
    async def test_main_print_text(self, capsys: callable) -> None:
        await main()
        assert 'Скачивание файлов...\nВычисление хэша...\n' in capsys.readouterr().out
