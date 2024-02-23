from os import environ
from os.path import join, dirname

from dotenv import load_dotenv
from loguru import logger

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)
logger.info('loading .env')


def get_env(key: str) -> str:
    value = environ.get(key)
    if value is None:
        raise KeyError(f'{key} is not found in .env')
    return value


HOST = get_env('HOST')
TOKEN = get_env('TOKEN')


logger.info(f'use: {HOST}')
