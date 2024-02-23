"""
手動実行
"""

import asyncio

from loguru import logger
from mipac.client import Client

from src.env import URL, TOKEN
from src.func import spam_action, text_helper
from src.target import TARGETS


async def main():
    client = Client(f'https://{HOST}', TOKEN)
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
        logger.info(f'スパムチェック開始: https://{HOST}/notes/{note.id}')

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


if __name__ == '__main__':
    asyncio.run(main())
