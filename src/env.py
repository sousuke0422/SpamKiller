from os import environ
from os.path import join, dirname

from dotenv import load_dotenv
from loguru import logger

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)
logger.info('loading .env')

HOST = environ.get('HOST')
TOKEN = environ.get('TOKEN')
logger.info(f'use: {HOST}')
