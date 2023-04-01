"""Тесты для функции хэшиpования."""
import pytest

from main import get_hash
from tests.constants import HASH1, HASH2


class TestHash:
    @pytest.mark.asyncio()
    async def test_correct_calculate_hashes(self, tmp_path: callable) -> None:
        test_file1: str = '{0}/test1.txt'.format(str(tmp_path))
        test_file2: str = '{0}/test2.txt'.format(str(tmp_path))
        with open(test_file1, 'w') as tf1:
            tf1.write('test_content1')
        with open(test_file2, 'w') as tf2:
            tf2.write('test_content2')
        assert HASH1 == await get_hash(test_file1), "Хэш не совпадает"
        assert HASH2 == await get_hash(test_file2), "Хэш не совпадает"

    @pytest.mark.asyncio()
    async def test_correct_return_datatype(self, tmp_path: callable) -> None:
        test_file1: str = '{0}/test2.txt'.format(str(tmp_path))
        with open(test_file1, 'w') as tf1:
            tf1.write('test_content1')
        assert isinstance(await get_hash(test_file1), str), "Не верный тип данных"
