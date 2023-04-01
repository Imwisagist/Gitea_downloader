"""Тесты для функции хэшиpования."""
from pathlib import Path

import pytest

from main import get_hash
from tests.constants import HASH1, HASH2


class TestHash:
    @pytest.mark.asyncio()
    async def test_correct_calculate_hashes(self, tmp_path: callable, create_file: callable) -> None:
        test_file2: Path = tmp_path / 'test2.txt'
        test_file2.write_text('test_content2')
        err_msg = "Хэш не совпадает"
        assert HASH1 == await get_hash(create_file), err_msg
        assert HASH2 == await get_hash(test_file2), err_msg

    @pytest.mark.asyncio()
    async def test_correct_return_datatype(self, create_file: callable) -> None:
        assert isinstance(await get_hash(create_file), str), "Не верный тип данных"
