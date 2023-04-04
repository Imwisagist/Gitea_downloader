"""Test task for Radium.

The script in 3 streams downloads the contents of the remote git repository,
saves it to a temporary folder and counts the hash of each file.
"""
import sys
from asyncio import Semaphore, create_task, gather, run
from hashlib import sha256
from http import HTTPStatus
from pathlib import Path
from tempfile import TemporaryDirectory

from aiofiles import open as aio_open
from aiohttp import ClientResponse, ClientSession

from custom_exceptions import DirectoryNotFound

REPO_ENDPOINT: str = 'https://gitea.radium.group/radium/project-configuration'
API_ENDPOINT: str = (
    'https://gitea.radium.group/api/v1/repos/radium/' +
    'project-configuration/contents/'
)


async def get_response(session: ClientSession, url: str) -> ClientResponse:
    """Request data from the specified address using the GET method."""
    response: ClientResponse = await session.get(url)
    if response.status != HTTPStatus.OK:
        raise ConnectionError(
            'Unsuccessful response code: {0}'.format(response.status),
        )
    return response


async def download_file(
    file_data: dict, session: ClientSession, path: Path,
) -> None:
    """Download file for by the specified path."""
    async with Semaphore(3):
        file_url: str = '{0}/raw/branch/master/{1}'.format(
            REPO_ENDPOINT, file_data.get('path'),
        )
        raw_file: ClientResponse = await get_response(session, file_url)
        async with aio_open(path / file_data.get('name'), 'wb') as b_file:
            await b_file.write(await raw_file.content.read())


async def parse_catalog(
    catalog: list | dict, session: ClientSession, tasks: list, path: Path,
) -> None:
    """Parse directories for files, transfers files for download."""
    for file_or_dir in catalog:
        if not file_or_dir.get('type'):
            raise KeyError('Not valid response, key "type" not found')

        if file_or_dir.get('type') == 'file':
            task = create_task(download_file(file_or_dir, session, path))
            tasks.append(task)

        elif file_or_dir.get('type') == 'dir':
            path: Path = path / file_or_dir.get('path')
            Path.mkdir(path)
            new_response: ClientResponse = await get_response(
                session, API_ENDPOINT + path.name,
            )
            await parse_catalog(
                await new_response.json(), session, tasks, path,
            )


async def download_files(path: Path) -> None:
    """Create a session and downloads all files."""
    if not path.exists():
        raise DirectoryNotFound('Temp directory not found!')

    async with ClientSession() as session:
        response: ClientResponse = await get_response(session, API_ENDPOINT)
        response_json: dict = await response.json()
        tasks: list = []
        await parse_catalog(response_json, session, tasks, path)
        await gather(*tasks)


async def print_hash(file_path: Path) -> None:
    """Print calculated hash for one file."""
    if not file_path.exists():
        raise FileNotFoundError('File not Found')

    hsh = sha256()
    chunk_size: int = 4096
    async with aio_open(file_path, 'rb') as binary_read_file:
        while True:
            chunk: bytes = await binary_read_file.read(chunk_size)
            if not chunk:
                break
            hsh.update(chunk)
        sys.stdout.write(
            '{0} hash: {1}\n'.format(file_path.name, hsh.hexdigest()),
        )


async def print_downloaded_files_hash(path: Path) -> None:
    """Create hash sum calculation tasks and runs them for execution."""
    if not path.exists():
        raise DirectoryNotFound('Temp directory not found!')

    file_paths = (el for el in path.rglob('*') if el.is_file())
    tasks = (create_task(print_hash(file_path)) for file_path in file_paths)
    await gather(*tasks)


async def main() -> None:
    """Start main function."""
    with TemporaryDirectory() as temp_dir:
        path: Path = Path(temp_dir)
        sys.stdout.write('Downloading files...\n')
        await download_files(path)
        sys.stdout.write('Calculation hash...\n')
        await print_downloaded_files_hash(path)


if __name__ == '__main__':
    run(main())   # pragma: no cover
