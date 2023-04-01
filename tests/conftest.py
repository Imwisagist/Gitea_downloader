"""Конфигуpационный файл для pytest."""
from pathlib import Path

import pytest
import pytest_asyncio

from tests.mocks import FakeSession


@pytest_asyncio.fixture()
async def fake_session():
    """Создание поддельной сессии."""
    return FakeSession()


@pytest.fixture()
def create_file(tmp_path: callable):
    test_file: Path = tmp_path / 'test1.txt'
    test_file.write_text('test_content1')
    return test_file
