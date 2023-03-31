"""
Конфигуpационный файл.
"""
import logging
import os
import sys
import asyncio

ENDPOINT: str = 'https://gitea.radium.group/radium/project-configuration'
API_ENDPOINT: str = ('https://gitea.radium.group/api/v1/'
                     'repos/radium/project-configuration/contents/')
CHUNK_SIZE, STREAMS_COUNT, HTTP_OK = 4096, 3, 200
SEMAPHORE: asyncio.Semaphore = asyncio.Semaphore(STREAMS_COUNT)


def get_logger(logger_name: str, logfile_name: str = '') -> logging.Logger:

    logger: logging.Logger = logging.getLogger(logger_name)

    logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_formatter = logging.Formatter('%(message)s')
    stream_handler.setFormatter(stream_formatter)
    stream_handler.addFilter(logging.Filter(logger_name))
    logger.addHandler(stream_handler)
    sys.stderr = ''

    if logfile_name:
        logs_dir_path: str = ''.join((os.path.dirname(os.getcwd()), '/logs'))
        if not os.path.exists(logs_dir_path):
            os.makedirs(logs_dir_path)

        file_handler = logging.FileHandler(
            f'{logs_dir_path}/{logfile_name}.txt', encoding='UTF-8')
        file_formatter = logging.Formatter(
                '%(asctime)s, %(levelname)s, Путь - %(pathname)s, '
                'Файл - %(filename)s, Функция - %(funcName)s, '
                'Номер строки - %(lineno)d, %(message)s.'
            )
        file_handler.setFormatter(file_formatter)
        file_handler.addFilter(logging.Filter(logger_name))
        logger.addHandler(file_handler)
    return logger

