"""Конфигуpационный файл для pytest."""
from pathlib import Path

import aiohttp
import pytest_asyncio

from tests.mocks import FakeSession


@pytest_asyncio.fixture()
async def fake_session() -> FakeSession:
    """Создание поддельной сессии."""
    return FakeSession()


@pytest_asyncio.fixture()
async def temp_file(tmp_path: callable) -> Path:
    """Создание временного файла."""
    test_file: Path = tmp_path / 'test1.txt'
    test_file.write_text('test_content1')
    return test_file


@pytest_asyncio.fixture()
async def real_session() -> aiohttp.ClientSession:
    """Настоящая сессия."""
    async with aiohttp.ClientSession() as session:
        yield session
