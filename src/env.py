# SPDX-FileCopyrightText: sousuke0422 and All Contributor
# SPDX-License-Identifier: MIT

from os import environ
from os.path import dirname, join

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


URL = get_env('URL')
TOKEN = get_env('TOKEN')


logger.info(f'use: {URL}')
