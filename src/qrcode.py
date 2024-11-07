import os

import aiohttp
from mipac.models.drive import File
import cv2
from qreader import QReader


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
