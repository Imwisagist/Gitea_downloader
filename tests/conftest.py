"""Configuration file for pytest."""
from pathlib import Path

from aiohttp import ClientSession
import pytest_asyncio

from tests.mocks import FakeSession


@pytest_asyncio.fixture()
async def fake_session() -> FakeSession:
    """Creating a fake session."""
    return FakeSession()


@pytest_asyncio.fixture()
async def temp_file(tmp_path: callable) -> Path:
    """Creating a temporary file."""
    test_file: Path = tmp_path / 'test1.txt'
    test_file.write_text('test_content1')
    return test_file


@pytest_asyncio.fixture()
async def real_session() -> ClientSession:
    """Creating a real session."""
    async with ClientSession() as session:
        yield session
