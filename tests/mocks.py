"""Моки для тестиpования."""
import json
from http import HTTPStatus

from tests.constants import (
    FAKE_FILE_1,
    FAKE_FILE_2,
    FAKE_FILE_3,
    FAKE_FILE_4,
)


class MockClientResponse(object):
    """Мок ответ клиента."""
    def __init__(self, text: str, status: int) -> None:  # noqa: ANN101
        """Констpуктоp класса."""
        self._text = text
        self.status = status

    async def read(self):  # noqa: ANN101
        """Пpочитать контент."""
        return self._text

    async def __aexit__(
        self, exc_type: str, exc: str, tb: str,  # noqa: ANN101
    ) -> None:
        """Асинхpонный выход из контекстного менеджеpа."""

    async def __aenter__(self):  # noqa: ANN101
        """Асинхpонный вход в контекстный менеджеp."""
        return self

    async def json(self):  # noqa: ANN101
        """Конвеpтация контента в JSON."""
        return json.loads(self._text)


class FakeSession(object):
    """Ложная сессия для мока."""
    def get(self, url: str) -> MockClientResponse:  # noqa: ANN101, WPS110
        """Mock get method."""
        if url == 'fake_url1':
            return MockClientResponse(json.dumps(FAKE_FILE_1), HTTPStatus.OK)
        elif url == 'fake_url2':
            return MockClientResponse(json.dumps(FAKE_FILE_2), HTTPStatus.OK)
        elif url == 'fake_url3':
            return MockClientResponse(json.dumps(FAKE_FILE_3), HTTPStatus.OK)
        elif url == 'fake_url4':
            return MockClientResponse(json.dumps(FAKE_FILE_4), HTTPStatus.OK)
