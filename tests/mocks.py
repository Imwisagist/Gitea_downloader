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
    def __init__(self, text: str, status: int) -> None:
        self._text = text
        self.status = status

    async def read(self):
        return self._text

    async def __aexit__(
        self, exc_type: str, exc: str, tb: str,
    ) -> None:
        pass

    async def __aenter__(self):
        return self

    async def json(self):
        return json.loads(self._text)


class FakeSession(object):
    def get(self, url: str) -> MockClientResponse:
        if url == 'fake_url1':
            return MockClientResponse(json.dumps(FAKE_FILE_1), HTTPStatus.OK)
        elif url == 'fake_url2':
            return MockClientResponse(json.dumps(FAKE_FILE_2), HTTPStatus.OK)
        elif url == 'fake_url3':
            return MockClientResponse(json.dumps(FAKE_FILE_3), HTTPStatus.OK)
        elif url == 'fake_url4':
            return MockClientResponse(json.dumps(FAKE_FILE_4), HTTPStatus.OK)
