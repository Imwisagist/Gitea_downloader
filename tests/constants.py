"""Test data."""

EXPECTED_HASH = '7de399840d99f97e59d2df18beacf81c1df68bef660cad1cf171a6100fb58fca'

REAL_FILE = {
    'name': 'LICENSE',
    'path': 'LICENSE',
    'type': 'file',
}

FAKE_DIR = {
    'type': 'dir',
    'path': 'nitpick',
}


FAKE_FILE_1 = {
    'content': 'fake_content_1',
    'encoding': 'base64',
    'url': 'fake_url_1.1',
    'sha': 'fake_sha_1',
    'size': 111,
}

FAKE_FILE_2 = {
    'content': 'fake_content_2',
    'encoding': 'base64',
    'url': 'fake_url_2.1',
    'sha': 'fake_sha_2',
    'size': 222,
}

FAKE_FILE_3 = {
    'content': 'fake_content_3',
    'encoding': 'base64',
    'url': 'fake_url_3.1',
    'sha': 'fake_sha_3',
    'size': 333,
}

FAKE_FILE_4 = {
    'content': 'fake_content_4',
    'encoding': 'base64',
    'url': 'fake_url_4.1',
    'sha': 'fake_sha_4',
    'size': 444,
}
