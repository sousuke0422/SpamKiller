# SPDX-FileCopyrightText: sousuke0422 and All Contributor
# SPDX-License-Identifier: MIT

"""
手動実行
"""

import asyncio

from loguru import logger
from mipac.client import Client

from src.env import URL, TOKEN
from src.func import spam_action, text_helper
from src.qrcode import QRCodeChecker
from src.target import TARGETS


async def main():
    client = Client(URL, TOKEN)
    await client.http.login()
    api = client.api
    me = await api.get_me()
    logger.success(f'Logged in: {me.username}')
    # 適宜IDは変えること
    note_id = input('note_id: ')

    if len(note_id) == 0:
        raise ValueError('note_id is must be a least 1 character')

    note = await api.note.action.get(note_id)
    logger.info(f'User: @{note.user.username}@{note.user.host}')
    logger.info(f'Context: {note.text}')
    if note.user.host and len(note.mentions) >= 2:
        logger.info(f'スパムチェック開始: {URL}/notes/{note.id}')

        for target in TARGETS:
            if note.text is None:
                continue

            text = text_helper(note.text)
            if target['key'] in text:
                logger.success(f'パターン一致: {target['key']}')
                await spam_action(note, api, target)
            elif len(note.user.username) == 10:
                logger.warning(
                    f'spamの可能性があります: @{note.user.username}@{note.user.host} ⚠️'
                )

    if 0 < len(note.mentions):
        for file in note.files:
            texts = await QRCodeChecker(file).check()
            # TARGETSに含まれる文字列が含まれている場合
            for target in TARGETS:
                if any(target['key'] in text for text in texts if isinstance(text, str)):
                    logger.success(f'QRコードにパターン一致: {target['key']}')
                    await spam_action(note, api, target)
                    break

if __name__ == '__main__':
    asyncio.run(main())
