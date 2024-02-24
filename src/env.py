# SPDX-FileCopyrightText: sousuke0422 and All Contributor
# SPDX-License-Identifier: MIT

from os import environ
from os.path import dirname, join

from mipac.utils.util import MISSING
from dotenv import load_dotenv
from loguru import logger

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)
logger.info('loading .env')


def get_env(key: str, default=MISSING) -> str:
    value = environ.get(key)

    if value:
        return value

    if default is not MISSING:
        return default

    raise ValueError(f'{key} is not found in .env')


URL = get_env('URL')
TOKEN = get_env('TOKEN')
USER_ACTION = get_env('USER_ACTION', 'suspend')

logger.info(f'use: {URL}')
