import asyncio
import os
import sys

import cv2
import aiohttp
from loguru import logger
from qreader import QReader
from mipac.client import Client
from mipac.http import Route
from mipac.utils.pagination import Pagination
from mipac.models.drive import File
from mipac.models.note import Note
from mipac.types.note import INote


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.env import URL, TOKEN
from src.func import spam_action
from src.target import TARGETS


class QRCodeChecker:
    def __init__(self, file: File):
        self.__file: File = file

    async def download(self):
        os.makedirs("tmp", exist_ok=True)

        async with aiohttp.ClientSession() as session:
            async with session.get(self.__file.url) as response:
                with open(f"tmp/{self.__file.name}", "wb") as f:
                    f.write(await response.read())

    async def cleanup(self):
        os.remove(f"tmp/{self.__file.name}")

    async def check(self):
        await self.download()

        # 画像の前処理
        gray = cv2.cvtColor(cv2.imread(f"tmp/{self.__file.name}"), cv2.COLOR_BGR2RGB)
        resized = cv2.resize(gray, (0, 0), fx=0.5, fy=0.5)

        # QRコードの検出
        qreader = QReader()
        texts = qreader.detect_and_decode(resized)

        # クリーンアップ
        await self.cleanup()

        return texts

async def check_old_timeline():
    try:
        with open('tmp/last_id.txt', 'r') as f:
            last_id = f.read()
    except FileNotFoundError:
        last_id = None
    client = Client(URL, TOKEN)
    pagination = Pagination[INote](client.http, Route('POST', '/api/notes/local-timeline'), json={
        'untilId': last_id
    })
    
    
    while pagination.is_final is False:
        raw_notes = await pagination.next()
        for raw_note in raw_notes:
            note = Note(raw_note, client=client.api)
            
            if 0 < len(note.mentions):
                for file in note.files:
                    texts = await QRCodeChecker(file).check()
                    for target in TARGETS:
                        if any(target['key'] in text for text in texts if isinstance(text, str)):
                            logger.success(f'QRコードにパターン一致: {target['key']}')
                            await spam_action(note, client.api, target)
                            break
        
        with open('tmp/last_id.txt', 'w') as f:
            f.write(raw_notes[-1]['id'])



if __name__ == '__main__':
    asyncio.run(check_old_timeline())