"""Тесты для функции хэшиpования."""
from pathlib import Path

import pytest

from tests.constants import HASH1, HASH2
from main import get_hash


@pytest.mark.asyncio()
async def test_correct_calculate_hashes(tmp_path: callable) -> None:
    test_file1: Path = tmp_path / Path('test1.txt')
    test_file2: Path = tmp_path / Path('test2.txt')
    with open(test_file1, 'w') as tf1:
        tf1.write('test_content1')
    with open(test_file2, 'w') as tf2:
        tf2.write('test_content2')
    assert HASH1 == await get_hash(str(tmp_path / Path('test1.txt')))
    assert HASH2 == await get_hash(str(tmp_path / Path('test2.txt')))
