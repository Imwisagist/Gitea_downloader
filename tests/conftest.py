"""Конфигуpационный файл для pytest."""

import asyncio
import platform
from typing import Generator

import pytest

pytest_plugins = [
    'tests.fixtures',
]


@pytest.fixture(scope='session')
def event_loop() -> Generator:
    """Создание петли событий."""
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
