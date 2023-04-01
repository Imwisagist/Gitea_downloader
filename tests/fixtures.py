"""Фикстуpы для pytest."""
import pytest_asyncio

from tests.mocks import FakeSession


@pytest_asyncio.fixture()
async def fake_session():
    """Создание поддельной сессии."""
    return FakeSession()
